"""
Fetch citation counts from the Semantic Scholar API.

This module provides functions to query the Semantic Scholar Graph API
for citation counts of arXiv papers, identified by their arXiv IDs.
"""

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

SEMANTIC_SCHOLAR_API_URL = (
    "https://api.semanticscholar.org/graph/v1/paper/ARXIV:{arxiv_id}?fields=citationCount"
)
DEFAULT_TIMEOUT = 10


def fetch_arxiv_citation_count(
    arxiv_id: str, timeout: int = DEFAULT_TIMEOUT
) -> int:
    """Fetch the citation count for a single arXiv paper from Semantic Scholar.

    Args:
        arxiv_id: The arXiv identifier (e.g., "2503.24235").
        timeout: HTTP request timeout in seconds.

    Returns:
        The citation count as an integer. Returns 0 if the API call fails
        or the paper is not found.
    """
    url = SEMANTIC_SCHOLAR_API_URL.format(arxiv_id=arxiv_id)
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        count = data.get("citationCount", 0)
        logger.info("ArXiv:%s — %d citations", arxiv_id, count)
        return count
    except requests.RequestException as exc:
        logger.warning("Failed to fetch citations for ArXiv:%s — %s", arxiv_id, exc)
        return 0


def fetch_total_citations(
    arxiv_ids: list[str], timeout: int = DEFAULT_TIMEOUT
) -> int:
    """Fetch and sum citation counts for a list of arXiv papers.

    Args:
        arxiv_ids: List of arXiv identifiers.
        timeout: HTTP request timeout in seconds.

    Returns:
        The total citation count across all papers.
    """
    total = 0
    for arxiv_id in arxiv_ids:
        total += fetch_arxiv_citation_count(arxiv_id, timeout=timeout)
    logger.info(
        "Total citations for %d paper(s): %d", len(arxiv_ids), total
    )
    return total
