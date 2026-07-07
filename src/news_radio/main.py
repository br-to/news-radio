"""Entry point for the news radio pipeline."""

import argparse
import asyncio
import logging
import sys

from news_radio.audio import generate_audio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run(news_text: str, *, wait: bool = True) -> None:
    """Run the audio generation pipeline.

    Args:
        news_text: News text to convert to audio.
        wait: If True, wait for generation and download MP3.
    """
    if not news_text.strip():
        logger.info("No news text provided. Skipping.")
        return

    logger.info("Starting news radio pipeline (%d chars)", len(news_text))

    audio_path = await generate_audio(news_text, wait=wait)
    if audio_path:
        logger.info("Generated audio: %s", audio_path)
    logger.info("Pipeline complete")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate news radio audio via NotebookLM")
    parser.add_argument(
        "input_file",
        nargs="?",
        help="News text file. Reads stdin if omitted.",
    )
    parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Start generation and exit immediately (for Cowork/automation).",
    )
    args = parser.parse_args()

    if args.input_file:
        text = open(args.input_file, encoding="utf-8").read()
    else:
        text = sys.stdin.read()

    asyncio.run(run(text, wait=not args.async_mode))


if __name__ == "__main__":
    main()
