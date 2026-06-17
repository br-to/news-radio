"""Discord Webhook client for posting audio files."""

import os
import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)


async def post_to_discord(audio_path: Path) -> None:
    """Post an audio file to Discord via webhook.

    Args:
        audio_path: Path to the audio file to upload.
    """
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    async with httpx.AsyncClient() as client:
        with open(audio_path, "rb") as f:
            response = await client.post(
                webhook_url,
                data={"content": "Today's news radio is ready!"},
                files={"file": (audio_path.name, f, "audio/mpeg")},
            )
            response.raise_for_status()

    logger.info("Successfully posted audio to Discord")
