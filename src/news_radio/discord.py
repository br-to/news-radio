"""Discord webhook notification for the news-radio pipeline."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

# Discord webhook attachments are capped around 25MB on non-boosted servers.
# Leave headroom below that so the request doesn't get rejected.
MAX_ATTACHMENT_BYTES = 24 * 1024 * 1024


async def notify_discord(content: str, audio_path: Path | None = None) -> None:
    """Post a message (and optionally an audio file) to the configured webhook."""
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        logger.warning("DISCORD_WEBHOOK_URL not set; skipping Discord notification")
        return

    async with httpx.AsyncClient(timeout=30.0) as client:
        if audio_path and audio_path.exists() and audio_path.stat().st_size <= MAX_ATTACHMENT_BYTES:
            files = {"file": (audio_path.name, audio_path.read_bytes(), "audio/mpeg")}
            resp = await client.post(webhook_url, data={"content": content}, files=files)
        else:
            if audio_path and audio_path.exists():
                content += "\n\n(音声ファイルが大きいため添付を省略しました。NotebookLMアプリで確認してください。)"
            resp = await client.post(webhook_url, json={"content": content})

    if resp.status_code >= 300:
        logger.error("Discord notification failed: %s %s", resp.status_code, resp.text)
    else:
        logger.info("Discord notification sent")


async def notify_discord_error(message: str) -> None:
    """Notify Discord that the pipeline failed."""
    await notify_discord(f"news-radio の実行に失敗しました:\n```\n{message}\n```")
