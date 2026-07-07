"""Entry point for the news radio pipeline."""

import argparse
import asyncio
import logging
import sys
from datetime import date

from news_radio.audio import generate_audio
from news_radio.discord import notify, post_audio
from news_radio.search import collect_news, format_news_text

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def run(
    news_text: str | None = None,
    *,
    auto_search: bool = False,
    wait: bool = True,
    discord: bool = True,
) -> None:
    """Run the news radio pipeline."""
    today = date.today().isoformat()

    try:
        if auto_search:
            if discord:
                await notify(f"📻 News Radio 開始 ({today}) — ニュース収集中...")
            logger.info("Collecting news via Brave Search")
            articles = await collect_news()
            if not articles:
                raise RuntimeError("No news articles found")
            news_text = format_news_text(articles)
            logger.info("Collected %d articles", len(articles))

        if not news_text or not news_text.strip():
            logger.info("No news text provided. Skipping.")
            return

        if discord and not auto_search:
            await notify(f"📻 News Radio 開始 ({today}) — 音声生成中...")

        logger.info("Starting audio pipeline (%d chars)", len(news_text))
        audio_path = await generate_audio(news_text, wait=wait)

        if audio_path:
            logger.info("Generated audio: %s", audio_path)
            if discord:
                await post_audio(audio_path, title=today)
                audio_path.unlink(missing_ok=True)
        elif discord:
            await notify(
                f"📻 News Radio ({today}) — 音声生成を開始しました。"
                "完了まで15〜20分かかります（NotebookLM通知も確認してください）。"
            )

        logger.info("Pipeline complete")
    except Exception as exc:
        logger.exception("Pipeline failed")
        if discord:
            await notify(f"❌ News Radio 失敗 ({today}): {exc}")
        raise


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate news radio audio via NotebookLM and post to Discord",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="News text file. Omit for full auto mode (Brave Search → audio → Discord).",
    )
    parser.add_argument(
        "--async",
        dest="async_mode",
        action="store_true",
        help="Start generation and exit immediately (no Discord audio upload).",
    )
    parser.add_argument(
        "--no-discord",
        action="store_true",
        help="Skip Discord notifications.",
    )
    args = parser.parse_args()

    if args.input_file:
        text = open(args.input_file, encoding="utf-8").read()
        auto_search = False
    else:
        text = None
        auto_search = True

    asyncio.run(
        run(
            text,
            auto_search=auto_search,
            wait=not args.async_mode,
            discord=not args.no_discord,
        )
    )


if __name__ == "__main__":
    main()
