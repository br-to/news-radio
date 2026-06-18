"""Discord webhook for posting audio files."""

import os
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


async def post_to_discord(audio_path: Path, summary: str = "") -> None:
    """Post an audio file to Discord via webhook.

    Args:
        audio_path: Path to the MP3 file to post.
        summary: Optional text summary to include with the audio.
    """
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    content = "Today's News Radio"
    if summary:
        content = f"{content}\n\n{summary}"

    async with httpx.AsyncClient() as client:
        with open(audio_path, "rb") as f:
            response = await client.post(
                webhook_url,
                data={"content": content},
                files={"file": ("news_radio.mp3", f, "audio/mpeg")},
                timeout=60,
            )
            response.raise_for_status()

    logger.info("Posted audio to Discord webhook")
