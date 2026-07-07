"""Automated daily pipeline: collect news -> generate audio -> notify Discord."""

import asyncio
import logging
from datetime import date

from news_radio.audio import generate_audio
from news_radio.discord import notify_discord, notify_discord_error
from news_radio.news import fetch_news, format_articles

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _summary_message(date_str: str, articles: list) -> str:
    lines = [f"🎙 News Radio - {date_str} の音声を生成しました", ""]
    for article in articles:
        lines.append(f"- [{article.title}]({article.url})")
    return "\n".join(lines)


async def run_daily() -> None:
    date_str = date.today().isoformat()
    logger.info("Starting daily news-radio pipeline for %s", date_str)

    articles = await fetch_news()
    if not articles:
        logger.warning("No articles collected; aborting")
        await notify_discord_error("収集できるニュースがありませんでした")
        return

    news_text = format_articles(articles, date_str)
    logger.info("Collected %d articles", len(articles))

    audio_path = await generate_audio(news_text)
    logger.info("Generated audio: %s", audio_path)

    await notify_discord(_summary_message(date_str, articles), audio_path)
    logger.info("Pipeline complete")


def main() -> None:
    try:
        asyncio.run(run_daily())
    except Exception as exc:  # noqa: BLE001 - top-level entry point must not crash silently
        logger.exception("Pipeline failed")
        asyncio.run(notify_discord_error(str(exc)))
        raise


if __name__ == "__main__":
    main()
