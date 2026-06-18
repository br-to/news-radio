"""Brave Search API client for fetching news articles."""

import os
import logging

import httpx

logger = logging.getLogger(__name__)

BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/news/search"


async def fetch_news(query: str = "latest news today", count: int = 5) -> list[dict]:
    """Fetch news articles from Brave Search API.

    Args:
        query: Search query string.
        count: Number of articles to retrieve.

    Returns:
        List of article dicts with 'title', 'url', and 'description' keys.
    """
    api_key = os.environ["BRAVE_API_KEY"]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            BRAVE_SEARCH_URL,
            headers={"X-Subscription-Token": api_key},
            params={"q": query, "count": count},
        )
        response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    articles = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "description": r.get("description", ""),
        }
        for r in results
    ]

    return articles
