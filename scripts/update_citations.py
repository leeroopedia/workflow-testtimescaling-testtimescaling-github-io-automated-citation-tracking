#!/usr/bin/env python3
"""
Update arXiv citation counts and generate a Shields.io badge JSON.

Usage:
    python scripts/update_citations.py
    python scripts/update_citations.py --config config/papers.json
    python scripts/update_citations.py --output badges/arxiv_citations.json
    python scripts/update_citations.py --help
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path so src/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.citation_fetcher import fetch_total_citations
from src.badge_generator import build_badge_data, write_badge_json
from src.paper_config import load_papers, extract_arxiv_ids

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/papers.json"),
        help="Path to papers JSON config file (default: config/papers.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("arxiv_citations.json"),
        help="Path for output badge JSON file (default: arxiv_citations.json)",
    )
    parser.add_argument(
        "--label",
        default="arXiv Citations",
        help='Badge label text (default: "arXiv Citations")',
    )
    parser.add_argument(
        "--color",
        default="blue",
        help='Badge color (default: "blue")',
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP request timeout in seconds (default: 10)",
    )
    args = parser.parse_args()

    logger.info("Starting citation update...")

    # Load papers from config
    papers = load_papers(args.config)
    arxiv_ids = extract_arxiv_ids(papers)
    logger.info("Tracking %d paper(s): %s", len(arxiv_ids), arxiv_ids)

    # Fetch citation counts
    total = fetch_total_citations(arxiv_ids, timeout=args.timeout)

    # Generate and write badge JSON
    badge = build_badge_data(total, label=args.label, color=args.color)
    output_path = write_badge_json(badge, args.output)

    logger.info("Done — %d total citations written to %s", total, output_path)


if __name__ == "__main__":
    main()
