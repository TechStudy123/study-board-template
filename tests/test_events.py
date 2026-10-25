import json
from datetime import date
from pathlib import Path

import pytest

EVENTS = json.loads(Path(__file__).parent.parent.joinpath("data/events.json").read_text(encoding="utf-8"))
REQUIRED = {"id", "title", "date", "place", "capacity"}


def test_required_fields():
    for e in EVENTS:
        assert REQUIRED <= e.keys(), f"足りない項目があります: {e}"


def test_date_format():
    for e in EVENTS:
        try:
            date.fromisoformat(e["date"])
            ok = True
        except ValueError:
            ok = False
        if not ok:
            pytest.fail(f"日付の形が正しくありません（2026-12-10 のように書きます）: {e['date']}", pytrace=False)


def test_capacity_is_positive():
    for e in EVENTS:
        assert e["capacity"] > 0, f"定員は1以上にします: {e}"


def test_ids_are_unique():
    ids = [e["id"] for e in EVENTS]
    assert len(ids) == len(set(ids)), f"id が重なっています: {ids}"
