"""Entry point for the news radio pipeline."""

import asyncio
import logging
import sys

from news_radio.audio import generate_audio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run(news_text: str) -> None:
    """Run the audio generation pipeline.

    Args:
        news_text: News text to convert to audio.
    """
    if not news_text.strip():
        logger.info("No news text provided. Skipping.")
        return

    logger.info("Starting news radio pipeline (%d chars)", len(news_text))

    # Generate audio overview via notebooklm CLI
    audio_path = await generate_audio(news_text)
    logger.info("Generated audio: %s", audio_path)
    logger.info("Pipeline complete")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) > 1:
        text = open(sys.argv[1], encoding="utf-8").read()
    else:
        text = sys.stdin.read()

    asyncio.run(run(text))


if __name__ == "__main__":
    main()
