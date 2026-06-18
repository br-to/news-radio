"""Entry point for the news radio pipeline."""

import asyncio
import logging
import os

from news_radio.audio import generate_audio
from news_radio.discord import post_to_discord

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run(news_text: str) -> None:
    """Run the audio generation and posting pipeline.

    Args:
        news_text: News text to convert to audio and post.
    """
    if not news_text.strip():
        logger.info("No news text provided. Skipping.")
        return

    logger.info("Starting news radio pipeline (%d chars)", len(news_text))

    # Generate audio overview
    storage_path = os.environ.get("NOTEBOOKLM_STORAGE_PATH")
    audio_path = await generate_audio(news_text, storage_path=storage_path)
    logger.info("Generated audio: %s", audio_path)

    # Post to Discord
    await post_to_discord(audio_path)
    logger.info("Posted to Discord")

    logger.info("Pipeline complete")


def main() -> None:
    """CLI entry point for standalone testing."""
    import sys

    if len(sys.argv) > 1:
        # Read news text from file
        text = open(sys.argv[1]).read()
    else:
        # Read from stdin
        text = sys.stdin.read()

    asyncio.run(run(text))


if __name__ == "__main__":
    main()
