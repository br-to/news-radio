"""Discord channel news fetcher."""

import os
import logging
from datetime import datetime, timezone, timedelta

import httpx

logger = logging.getLogger(__name__)

DISCORD_API_BASE = "https://discord.com/api/v10"


async def fetch_news(
    channel_id: str | None = None,
    bot_id: str | None = None,
    limit: int = 20,
) -> str:
    """Fetch recent news messages from a Discord channel.

    Retrieves messages posted by the specified bot within the last 24 hours
    and combines them into a single text block suitable for audio generation.

    Args:
        channel_id: Discord channel ID. Falls back to NEWS_CHANNEL_ID env var.
        bot_id: Filter messages by this author ID. Falls back to NEWS_BOT_ID env var.
        limit: Max messages to fetch from Discord API.

    Returns:
        Combined news text ready for NotebookLM input.
    """
    token = os.environ["DISCORD_BOT_TOKEN"]
    channel_id = channel_id or os.environ["NEWS_CHANNEL_ID"]
    bot_id = bot_id or os.environ.get("NEWS_BOT_ID")

    headers = {
        "Authorization": f"Bot {token}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
            headers=headers,
            params={"limit": limit},
        )
        response.raise_for_status()

    messages = response.json()

    # Filter by bot author if specified
    if bot_id:
        messages = [m for m in messages if m.get("author", {}).get("id") == bot_id]

    # Filter to last 24 hours
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    recent = []
    for msg in messages:
        ts = datetime.fromisoformat(msg["timestamp"].replace("+00:00", "+00:00"))
        if ts >= cutoff:
            recent.append(msg)

    if not recent:
        logger.warning("No recent news messages found in channel %s", channel_id)
        return ""

    # Messages come newest-first from Discord API, reverse for chronological order
    recent.reverse()

    # Combine message contents
    texts = [msg["content"] for msg in recent if msg.get("content")]
    combined = "\n\n".join(texts)

    logger.info("Fetched %d news messages from Discord", len(texts))
    return combined
