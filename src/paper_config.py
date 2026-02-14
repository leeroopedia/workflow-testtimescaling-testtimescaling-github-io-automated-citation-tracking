"""
Load paper configuration from JSON files.

Reads the list of tracked papers (title + arXiv ID) from a JSON
configuration file used by the citation tracking pipeline.
"""

import json
import logging
from pathlib import Path
from typing import TypedDict

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path("config/papers.json")


class PaperEntry(TypedDict):
    title: str
    arxiv_id: str


def load_papers(config_path: str | Path = DEFAULT_CONFIG_PATH) -> list[PaperEntry]:
    """Load the list of tracked papers from a JSON file.

    The file should contain a JSON array of objects, each with
    "title" and "arxiv_id" keys.

    Args:
        config_path: Path to the papers JSON file.

    Returns:
        A list of paper entry dictionaries.

    Raises:
        FileNotFoundError: If the config file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Paper config not found: {config_path}")

    with open(config_path) as f:
        papers = json.load(f)

    logger.info("Loaded %d paper(s) from %s", len(papers), config_path)
    return papers


def extract_arxiv_ids(papers: list[PaperEntry]) -> list[str]:
    """Extract arXiv IDs from a list of paper entries.

    Args:
        papers: List of paper entry dictionaries.

    Returns:
        List of arXiv ID strings.
    """
    return [p["arxiv_id"] for p in papers]
