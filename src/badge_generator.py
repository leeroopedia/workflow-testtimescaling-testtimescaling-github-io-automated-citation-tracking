"""
Generate Shields.io endpoint badge JSON files.

Produces JSON conforming to the Shields.io endpoint badge schema
(https://shields.io/endpoint) so that citation counts can be rendered
as live badges in a repository README.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_LABEL = "arXiv Citations"
DEFAULT_COLOR = "blue"
SCHEMA_VERSION = 1


def build_badge_data(
    total_citations: int,
    label: str = DEFAULT_LABEL,
    color: str = DEFAULT_COLOR,
) -> dict[str, Any]:
    """Build a Shields.io endpoint badge payload.

    Args:
        total_citations: The number to display on the badge.
        label: The badge label text.
        color: The badge color name (e.g., "blue", "green").

    Returns:
        A dictionary conforming to the Shields.io endpoint schema.
    """
    return {
        "schemaVersion": SCHEMA_VERSION,
        "label": label,
        "message": str(total_citations),
        "color": color,
    }


def write_badge_json(
    badge_data: dict[str, Any],
    output_path: str | Path = "arxiv_citations.json",
) -> Path:
    """Write badge data to a JSON file.

    Args:
        badge_data: The Shields.io badge payload dictionary.
        output_path: Destination file path.

    Returns:
        The resolved Path that was written.
    """
    output_path = Path(output_path)
    with open(output_path, "w") as f:
        json.dump(badge_data, f)
    logger.info("Badge JSON written to %s", output_path)
    return output_path
