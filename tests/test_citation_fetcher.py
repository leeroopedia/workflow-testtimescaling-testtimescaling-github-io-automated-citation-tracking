"""Tests for the citation fetcher module."""

from unittest.mock import patch, Mock

from src.citation_fetcher import fetch_arxiv_citation_count, fetch_total_citations


def _mock_response(json_data, status_code=200):
    mock = Mock()
    mock.json.return_value = json_data
    mock.status_code = status_code
    mock.raise_for_status.return_value = None
    return mock


@patch("src.citation_fetcher.requests.get")
def test_fetch_arxiv_citation_count_success(mock_get):
    mock_get.return_value = _mock_response({"citationCount": 42})
    result = fetch_arxiv_citation_count("2503.24235")
    assert result == 42


@patch("src.citation_fetcher.requests.get")
def test_fetch_arxiv_citation_count_missing_field(mock_get):
    mock_get.return_value = _mock_response({})
    result = fetch_arxiv_citation_count("2503.24235")
    assert result == 0


@patch("src.citation_fetcher.requests.get")
def test_fetch_arxiv_citation_count_api_error(mock_get):
    mock_get.side_effect = Exception("Connection error")
    result = fetch_arxiv_citation_count("2503.24235")
    assert result == 0


@patch("src.citation_fetcher.requests.get")
def test_fetch_total_citations(mock_get):
    mock_get.side_effect = [
        _mock_response({"citationCount": 10}),
        _mock_response({"citationCount": 20}),
    ]
    result = fetch_total_citations(["1111.11111", "2222.22222"])
    assert result == 30
