# Automated Citation Tracking

> Automatically track and display arXiv paper citation counts as a live Shields.io badge using GitHub Actions and the Semantic Scholar API.

## Overview

### What is this?

A fully automated pipeline that keeps your repository's citation count badge up to date. It runs daily via GitHub Actions, queries the Semantic Scholar API for citation counts of your tracked arXiv papers, and writes a JSON file that Shields.io reads to render a live badge in your README.

### Why use this?

Manually checking and updating citation counts is tedious and easy to forget. This workflow eliminates that burden entirely — once configured, it refreshes your citation data every day with zero human intervention. It is especially useful for academic project pages, survey repositories, and paper companion sites where showing current citation metrics adds credibility and keeps visitors informed.

### When to use this?

Use this workflow when you maintain a GitHub repository associated with one or more arXiv papers and want to display a live citation count badge. It works best for:

**Example use cases:**
- A survey paper repository that tracks aggregate citations across multiple related papers
- A research project page that showcases citation growth over time
- An academic group's landing page with live citation metrics for their publications

---

## Quick Start

### Prerequisites

- Python 3.10+
- A GitHub repository with Actions enabled
- arXiv paper IDs you want to track

### Installation

```bash
git clone https://github.com/leeroopedia/workflow-testtimescaling-testtimescaling-github-io-automated-citation-tracking.git
cd workflow-testtimescaling-testtimescaling-github-io-automated-citation-tracking
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run locally to test citation fetching
python scripts/update_citations.py

# Specify a custom papers config
python scripts/update_citations.py --config config/papers.json

# Write output to a custom location
python scripts/update_citations.py --output badges/arxiv_citations.json
```

Once pushed to GitHub, the included GitHub Actions workflow runs automatically every day at midnight UTC.

---

## Project Structure

```
workflow-testtimescaling-testtimescaling-github-io-automated-citation-tracking/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── arxiv_citations.json                # Output: Shields.io badge JSON (auto-updated)
├── .gitignore
├── config/
│   └── papers.json                     # Paper list configuration (title + arXiv IDs)
├── src/
│   ├── __init__.py
│   ├── citation_fetcher.py             # Semantic Scholar API client
│   ├── badge_generator.py              # Shields.io badge JSON builder
│   └── paper_config.py                 # Paper list loader and parser
├── scripts/
│   └── update_citations.py             # CLI entry point for the pipeline
├── tests/
│   ├── __init__.py
│   ├── test_citation_fetcher.py        # Unit tests for API fetching
│   ├── test_badge_generator.py         # Unit tests for badge generation
│   └── test_paper_config.py            # Unit tests for config loading
└── .github/
    └── workflows/
        └── update_citations.yml        # GitHub Actions workflow (daily cron)
```

**Why this structure?** This is a CI/CD automation pipeline with a clear data flow: config in → API fetch → badge output. The code is split by responsibility: `config/` holds the paper list that drives the pipeline, `src/` contains the three logical stages (load config, fetch citations, generate badge), `scripts/` provides the CLI entry point, and `.github/workflows/` defines the automation schedule. This separation makes it straightforward to add papers, swap the API source, or change the badge format independently.

---

## Configuration

### Adding Papers

Edit `config/papers.json` to add or remove papers:

```json
[
  {
    "title": "What, How, Where, and How Well? A Survey on Test-Time Scaling in Large Language Models",
    "arxiv_id": "2503.24235"
  },
  {
    "title": "Another Paper Title",
    "arxiv_id": "2401.12345"
  }
]
```

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--config` | Path to the papers JSON file | `config/papers.json` |
| `--output` | Path for the output badge JSON | `arxiv_citations.json` |
| `--label` | Text label on the badge | `arXiv Citations` |
| `--color` | Badge color (any Shields.io color name) | `blue` |
| `--timeout` | HTTP request timeout in seconds | `10` |

### GitHub Actions Schedule

The workflow in `.github/workflows/update_citations.yml` runs on a daily cron schedule (`0 0 * * *` — midnight UTC). You can also trigger it manually from the Actions tab using the `workflow_dispatch` event.

---

## Detailed Usage

### Step-by-Step Guide

1. **Add your papers** to `config/papers.json` with their arXiv IDs.
2. **Test locally** by running `python scripts/update_citations.py` — this writes `arxiv_citations.json`.
3. **Push to GitHub** — the Actions workflow will take over from here.
4. **Add the badge** to your README using the Shields.io endpoint format:

```markdown
![arXiv Citations](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/arxiv_citations.json)
```

### How the Pipeline Works

1. **Trigger**: GitHub Actions cron fires at midnight UTC (or manual dispatch).
2. **Checkout**: The workflow checks out the repository.
3. **Fetch**: The Python script reads `config/papers.json`, queries Semantic Scholar for each paper's citation count, and sums the totals.
4. **Generate**: A Shields.io-compatible JSON file is written to `arxiv_citations.json`.
5. **Commit**: The workflow commits and pushes the updated file (with `[skip ci]` to prevent recursive triggers).

### Manual Trigger

Go to the **Actions** tab in your GitHub repository, select the "Update Arxiv Citations" workflow, and click "Run workflow".

---

## Development

### Running Tests

```bash
pip install pytest
pytest tests/ -v
```

### Code Style

The codebase uses type hints throughout and follows standard Python conventions. All modules include docstrings.

---

## References

- [Semantic Scholar API Documentation](https://api.semanticscholar.org/)
- [Shields.io Endpoint Badges](https://shields.io/endpoint)
- [GitHub Actions Scheduled Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- Source workflow: [testtimescaling/testtimescaling.github.io](https://github.com/testtimescaling/testtimescaling.github.io)

---

## License

MIT
