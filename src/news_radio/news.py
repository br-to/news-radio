"""News collection using the Brave Search API."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

BRAVE_NEWS_ENDPOINT = "https://api.search.brave.com/res/v1/news/search"

# 海外ソース多め・法律/規制系は除外する方針のクエリ
QUERIES = [
    "blockchain AI agents",
    "onchain finance DeFi",
    "prediction markets Polymarket Kalshi",
]

# タイトルにこれらの語を含む記事は除外（法律・規制・訴訟系）
EXCLUDE_KEYWORDS = [
    "lawsuit", "regulation", "regulator", "compliance", "sec charges",
    "sued", "legal", "court", "法律", "規制", "訴訟", "金融庁",
]

# 読めない/ペイウォールが強いことで知られるドメインは避ける
PAYWALL_DOMAINS = [
    "wsj.com", "ft.com", "bloomberg.com", "nikkei.com", "economist.com",
]

MAX_ARTICLES_PER_QUERY = 6
MAX_TOTAL_ARTICLES = 8
ACCESSIBILITY_TIMEOUT = 8.0


@dataclass
class Article:
    title: str
    description: str
    url: str
    source: str


def _is_excluded(title: str) -> bool:
    lowered = title.lower()
    return any(kw.lower() in lowered for kw in EXCLUDE_KEYWORDS)


def _is_paywalled(url: str) -> bool:
    return any(domain in url for domain in PAYWALL_DOMAINS)


async def _search_query(client: httpx.AsyncClient, api_key: str, query: str) -> list[Article]:
    resp = await client.get(
        BRAVE_NEWS_ENDPOINT,
        params={
            "q": query,
            "count": MAX_ARTICLES_PER_QUERY,
            "search_lang": "en",
            "country": "US",
            "freshness": "pd",  # past day
        },
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
        timeout=ACCESSIBILITY_TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()

    articles: list[Article] = []
    for item in data.get("results", []):
        title = item.get("title", "")
        url = item.get("url", "")
        if not title or not url:
            continue
        if _is_excluded(title) or _is_paywalled(url):
            continue
        articles.append(
            Article(
                title=title,
                description=item.get("description", ""),
                url=url,
                source=item.get("meta_url", {}).get("hostname", ""),
            )
        )
    return articles


async def _is_accessible(client: httpx.AsyncClient, url: str) -> bool:
    """Best-effort check that the article is actually readable (not dead/blocked)."""
    try:
        resp = await client.get(
            url,
            timeout=ACCESSIBILITY_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (news-radio bot)"},
        )
        return resp.status_code == 200 and len(resp.content) > 500
    except (httpx.HTTPError, httpx.TimeoutException):
        return False


async def fetch_news() -> list[Article]:
    """Fetch today's blockchain / AI / on-chain finance / prediction market news."""
    api_key = os.environ.get("BRAVE_API_KEY")
    if not api_key:
        raise RuntimeError("BRAVE_API_KEY environment variable is not set")

    async with httpx.AsyncClient() as client:
        collected: list[Article] = []
        seen_urls: set[str] = set()

        for query in QUERIES:
            try:
                results = await _search_query(client, api_key, query)
            except httpx.HTTPError as exc:
                logger.warning("Brave search failed for %r: %s", query, exc)
                continue
            for article in results:
                if article.url in seen_urls:
                    continue
                seen_urls.add(article.url)
                collected.append(article)

        # 実際に開ける記事だけ残す
        accessible: list[Article] = []
        for article in collected:
            if await _is_accessible(client, article.url):
                accessible.append(article)
            if len(accessible) >= MAX_TOTAL_ARTICLES:
                break

    logger.info("Collected %d accessible articles", len(accessible))
    return accessible


def format_articles(articles: list[Article], date_str: str) -> str:
    """Render articles into the text format NotebookLM ingests."""
    lines = [f"# Today's News - {date_str}", ""]
    for i, article in enumerate(articles, start=1):
        lines.append(f"## {i}. {article.title}")
        if article.description:
            lines.append(article.description)
        lines.append(f"URL: {article.url}")
        lines.append("")
    return "\n".join(lines)
