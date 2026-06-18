"""Audio generation using NotebookLM CLI."""

import asyncio
import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

NOTEBOOK_TITLE = "News Radio"


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

    Creates a temporary notebook, adds the news text as a source,
    generates an Audio Overview (SHORT length), downloads the MP3,
    then cleans up the notebook.

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

    # Create a notebook
    stdout, stderr, rc = await _run_cmd(["notebooklm", "create", NOTEBOOK_TITLE, "--json"])
    if rc != 0:
        raise RuntimeError(f"Failed to create notebook: {stderr}")

    import json
    notebook_data = json.loads(stdout)
    notebook_id = notebook_data["id"]
    logger.info("Created notebook: %s", notebook_id)

    try:
        # Set as current notebook
        await _run_cmd(["notebooklm", "use", notebook_id])

        # Write news text to a temp file and add as source
        text_file = Path(tempfile.gettempdir()) / "news_input.txt"
        text_file.write_text(news_text, encoding="utf-8")

        stdout, stderr, rc = await _run_cmd([
            "notebooklm", "source", "add", str(text_file),
            "--title", "Today's News",
        ])
        if rc != 0:
            raise RuntimeError(f"Failed to add source: {stderr}")
        logger.info("Added news text as source")

        # Generate audio overview (short, wait for completion)
        stdout, stderr, rc = await _run_cmd([
            "notebooklm", "generate", "audio",
            "--length", "short",
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

    finally:
        # Clean up the notebook
        stdout, stderr, rc = await _run_cmd(["notebooklm", "delete", notebook_id, "--confirm"])
        if rc == 0:
            logger.info("Cleaned up notebook: %s", notebook_id)
        else:
            logger.warning("Failed to delete notebook %s: %s", notebook_id, stderr)

    return output_path
