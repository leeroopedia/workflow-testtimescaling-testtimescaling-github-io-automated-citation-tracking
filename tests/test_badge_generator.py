"""Tests for the badge generator module."""

import json
import tempfile
from pathlib import Path

from src.badge_generator import build_badge_data, write_badge_json


def test_build_badge_data_defaults():
    result = build_badge_data(42)
    assert result == {
        "schemaVersion": 1,
        "label": "arXiv Citations",
        "message": "42",
        "color": "blue",
    }


def test_build_badge_data_custom():
    result = build_badge_data(10, label="Citations", color="green")
    assert result["label"] == "Citations"
    assert result["color"] == "green"
    assert result["message"] == "10"


def test_build_badge_data_zero():
    result = build_badge_data(0)
    assert result["message"] == "0"


def test_write_badge_json():
    badge = build_badge_data(99)
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir) / "test_badge.json"
        returned_path = write_badge_json(badge, out)
        assert returned_path == out
        with open(out) as f:
            data = json.load(f)
        assert data["message"] == "99"
        assert data["schemaVersion"] == 1
