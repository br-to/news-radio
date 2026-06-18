"""Audio generation using NotebookLM CLI."""

import asyncio
import json
import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

AUDIO_PROMPT = (
    "落ち着いたトーンでニュースを解説してください。"
    "大袈裟なリアクションや過度な興奮は不要。"
    "淡々と事実を伝え、冷静に考察を話す形式で。"
)


async def _run_cmd(cmd: list[str]) -> tuple[str, str, int]:
    """Run a shell command and return stdout, stderr, returncode."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode(), proc.returncode


async def generate_audio(
    news_text: str,
    output_dir: str | None = None,
) -> Path:
    """Generate an audio overview from news text using notebooklm CLI.

    Uses a pre-configured persistent notebook (set via `notebooklm use <id>`).
    Replaces existing sources with the new news text, generates an Audio Overview,
    and downloads the MP3.

    Args:
        news_text: Combined news text to convert to audio.
        output_dir: Directory to save the audio file. Defaults to temp dir.

    Returns:
        Path to the generated MP3 file.
    """
    if not news_text.strip():
        raise ValueError("news_text is empty")

    output_dir = output_dir or tempfile.gettempdir()
    output_path = Path(output_dir) / "news_radio.mp3"

    # Delete existing sources to avoid mixing old news
    stdout, stderr, rc = await _run_cmd(["notebooklm", "source", "list", "--json"])
    if rc == 0 and stdout.strip():
        sources = json.loads(stdout)
        for source in sources:
            await _run_cmd(["notebooklm", "source", "delete", source["id"]])
        logger.info("Deleted %d existing sources", len(sources))

    # Write news text to temp file and add as source
    text_file = Path(tempfile.gettempdir()) / "news_radio_input.txt"
    text_file.write_text(news_text, encoding="utf-8")

    stdout, stderr, rc = await _run_cmd([
        "notebooklm", "source", "add", str(text_file),
        "--title", "Today's News",
    ])
    if rc != 0:
        raise RuntimeError(f"Failed to add source: {stderr}")
    logger.info("Added news text as source")

    # Generate audio overview (default length, brief format, calm tone)
    stdout, stderr, rc = await _run_cmd([
        "notebooklm", "generate", "audio",
        AUDIO_PROMPT,
        "--length", "default",
        "--format", "brief",
        "--language", "ja",
        "--wait",
        "--timeout", "900",
        "--retry", "2",
    ])
    if rc != 0:
        raise RuntimeError(f"Audio generation failed: {stderr}")
    logger.info("Audio generation complete")

    # Download the latest audio
    stdout, stderr, rc = await _run_cmd([
        "notebooklm", "download", "audio",
        str(output_path),
        "--latest",
        "--force",
    ])
    if rc != 0:
        raise RuntimeError(f"Failed to download audio: {stderr}")
    logger.info("Audio downloaded: %s", output_path)

    return output_path
