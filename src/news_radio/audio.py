"""Audio generation using NotebookLM Audio Overview."""

import logging
import tempfile
from pathlib import Path

from notebooklm import NotebookLMClient

logger = logging.getLogger(__name__)

NOTEBOOK_TITLE = "News Radio"


async def generate_audio(
    news_text: str,
    output_dir: str | None = None,
    storage_path: str | None = None,
) -> Path:
    """Generate an audio overview from news text using notebooklm-py.

    Creates a temporary notebook, adds the news text as a source,
    generates an Audio Overview (SHORT length), downloads the MP3,
    then cleans up the notebook.

    Args:
        news_text: Combined news text to convert to audio.
        output_dir: Directory to save the audio file. Defaults to temp dir.
        storage_path: Path to NotebookLM storage_state.json for auth.

    Returns:
        Path to the generated MP3 file.
    """
    if not news_text.strip():
        raise ValueError("news_text is empty")

    output_dir = output_dir or tempfile.gettempdir()
    output_path = Path(output_dir) / "news_radio.mp3"

    client_kwargs = {}
    if storage_path:
        client_kwargs["storage_path"] = storage_path

    async with NotebookLMClient.from_storage(**client_kwargs) as client:
        # Create a notebook for this session
        notebook = await client.notebooks.create(NOTEBOOK_TITLE)
        notebook_id = notebook.id
        logger.info("Created notebook: %s", notebook_id)

        try:
            # Add news text as a paste source
            await client.sources.add_text(notebook_id, news_text, title="Today's News")
            logger.info("Added news text as source")

            # Generate audio overview
            status = await client.artifacts.generate_audio(
                notebook_id,
                length="short",
            )
            logger.info("Audio generation started, waiting for completion...")

            await client.artifacts.wait_for_completion(
                notebook_id,
                status.task_id,
                timeout=1200,
            )

            # Download the audio file
            result_path = await client.artifacts.download_audio(
                notebook_id,
                str(output_path),
            )
            logger.info("Audio downloaded: %s", result_path)

        finally:
            # Clean up the notebook
            await client.notebooks.delete(notebook_id)
            logger.info("Cleaned up notebook: %s", notebook_id)

    return Path(result_path)
