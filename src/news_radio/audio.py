"""Audio generation using NotebookLM Audio Overview."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def generate_audio(articles: list[dict]) -> Path:
    """Generate an audio overview from news articles using notebooklm-py.

    Args:
        articles: List of article dicts with 'title', 'url', and 'description'.

    Returns:
        Path to the generated audio file.
    """
    # Format articles into source text
    source_text = _format_articles(articles)

    # TODO: Implement notebooklm-py integration
    # The notebooklm-py library will be used to:
    # 1. Create a notebook with the source text
    # 2. Generate an Audio Overview
    # 3. Download the resulting audio file
    raise NotImplementedError("NotebookLM audio generation not yet implemented")


def _format_articles(articles: list[dict]) -> str:
    """Format articles into a single text block for NotebookLM input.

    Args:
        articles: List of article dicts.

    Returns:
        Formatted string containing all articles.
    """
    parts = []
    for i, article in enumerate(articles, 1):
        parts.append(
            f"Article {i}: {article['title']}\n"
            f"URL: {article['url']}\n"
            f"{article['description']}\n"
        )
    return "\n---\n".join(parts)
