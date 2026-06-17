"""Entry point for the news radio pipeline."""

import asyncio
import logging

from news_radio.search import fetch_news
from news_radio.audio import generate_audio
from news_radio.discord import post_to_discord

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run() -> None:
    """Run the full news radio pipeline."""
    logger.info("Starting news radio pipeline")

    # Step 1: Fetch news articles
    articles = await fetch_news()
    logger.info("Fetched %d articles", len(articles))

    # Step 2: Generate audio overview
    audio_path = await generate_audio(articles)
    logger.info("Generated audio: %s", audio_path)

    # Step 3: Post to Discord
    await post_to_discord(audio_path)
    logger.info("Posted to Discord")

    logger.info("Pipeline complete")


def main() -> None:
    """Synchronous entry point."""
    asyncio.run(run())


if __name__ == "__main__":
    main()
