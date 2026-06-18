"""Discord webhook for posting audio files."""

import logging
import os
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


async def post_to_discord(audio_path: Path, title: str = "") -> None:
    """Post an audio file to Discord via webhook.

    Args:
        audio_path: Path to the audio file to post.
        title: Optional title to include with the audio.
    """
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    content = f"Today's News Radio: {title}" if title else "Today's News Radio"

    async with httpx.AsyncClient() as client:
        with open(audio_path, "rb") as f:
            response = await client.post(
                webhook_url,
                data={"content": content},
                files={"file": ("news_radio.mp3", f, "audio/mpeg")},
                timeout=120,
            )
            response.raise_for_status()

    logger.info("Posted audio to Discord webhook")
