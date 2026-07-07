"""Brave Search API client for fetching news articles."""

import logging
import os
from datetime import date

import httpx

logger = logging.getLogger(__name__)

BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"
DEFAULT_QUERIES = ("AI artificial intelligence", "blockchain crypto", "prediction market")


async def fetch_news(
    query: str,
    *,
    count: int = 3,
    freshness: str = "pd",
) -> list[dict]:
    """Fetch news articles from Brave Search API.

    Args:
        query: Search query string.
        count: Number of articles to retrieve per query.
        freshness: Time filter (pd=24h, pw=7d, pm=31d).

    Returns:
        List of article dicts with title, url, and description.
    """
    api_key = os.environ["BRAVE_API_KEY"]

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            BRAVE_NEWS_URL,
            headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
            params={
                "q": query,
                "count": count,
                "freshness": freshness,
                "search_lang": "en",
            },
        )
        response.raise_for_status()

    results = response.json().get("results", [])
    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "description": item.get("description", ""),
        }
        for item in results
        if item.get("title") and item.get("url")
    ]


async def collect_news(
    queries: tuple[str, ...] | None = None,
    *,
    count_per_query: int = 3,
) -> list[dict]:
    """Collect news from multiple queries, deduplicated by URL."""
    queries = queries or _queries_from_env()
    seen_urls: set[str] = set()
    articles: list[dict] = []

    for query in queries:
        batch = await fetch_news(query, count=count_per_query)
        for article in batch:
            url = article["url"]
            if url in seen_urls:
                continue
            seen_urls.add(url)
            articles.append(article)
        logger.info("Query %r: %d articles (total %d)", query, len(batch), len(articles))

    return articles


def format_news_text(articles: list[dict], *, title_date: date | None = None) -> str:
    """Format articles into text for NotebookLM."""
    title_date = title_date or date.today()
    lines = [f"# Today's News - {title_date.isoformat()}", ""]

    for index, article in enumerate(articles, start=1):
        lines.extend([
            f"## {index}. {article['title']}",
            article.get("description") or "(No description)",
            f"URL: {article['url']}",
            "",
        ])

    return "\n".join(lines).strip()


def _queries_from_env() -> tuple[str, ...]:
    raw = os.environ.get("NEWS_QUERIES", "")
    if not raw.strip():
        return DEFAULT_QUERIES
    return tuple(q.strip() for q in raw.split(",") if q.strip())
