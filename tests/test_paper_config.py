"""Tests for the paper configuration module."""

import json
import tempfile
from pathlib import Path

import pytest

from src.paper_config import load_papers, extract_arxiv_ids


def test_load_papers():
    papers_data = [
        {"title": "Paper A", "arxiv_id": "1234.56789"},
        {"title": "Paper B", "arxiv_id": "9876.54321"},
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "papers.json"
        with open(config_path, "w") as f:
            json.dump(papers_data, f)
        result = load_papers(config_path)
        assert len(result) == 2
        assert result[0]["arxiv_id"] == "1234.56789"


def test_load_papers_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_papers("/nonexistent/path/papers.json")


def test_extract_arxiv_ids():
    papers = [
        {"title": "Paper A", "arxiv_id": "1111.11111"},
        {"title": "Paper B", "arxiv_id": "2222.22222"},
    ]
    ids = extract_arxiv_ids(papers)
    assert ids == ["1111.11111", "2222.22222"]


def test_extract_arxiv_ids_empty():
    assert extract_arxiv_ids([]) == []
