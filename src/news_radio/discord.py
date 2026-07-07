"""Discord webhook notifications."""

import logging
import os
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


def webhook_url() -> str | None:
    """Return Discord webhook URL if configured."""
    return os.environ.get("DISCORD_WEBHOOK_URL")


async def notify(message: str) -> None:
    """Send a text message to Discord."""
    url = webhook_url()
    if not url:
        logger.debug("DISCORD_WEBHOOK_URL not set, skipping notification")
        return

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json={"content": message})
        response.raise_for_status()

    logger.info("Discord notification sent")


async def post_audio(audio_path: Path, *, title: str = "News Radio") -> None:
    """Post an audio file to Discord via webhook."""
    url = webhook_url()
    if not url:
        logger.warning("DISCORD_WEBHOOK_URL not set, skipping audio upload")
        return

    content = f"🎙️ Today's News Radio: {title}"

    async with httpx.AsyncClient(timeout=120) as client:
        with open(audio_path, "rb") as handle:
            response = await client.post(
                url,
                data={"content": content},
                files={"file": ("news_radio.mp3", handle, "audio/mpeg")},
            )
            response.raise_for_status()

    logger.info("Posted audio to Discord")
