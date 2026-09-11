"""Regression test: CLI output must survive a legacy Windows console codepage.

A stock Windows cmd.exe console commonly uses cp437 (or another legacy
codepage), which has no em dash, curly quotes, or most other "smart"
typographic characters. Python's stdout under that codepage encodes with
errors='strict' by default, so printing any such character crashes the CLI
outright with UnicodeEncodeError -- discovered by actually reproducing it
against list-checklist, not by inspection.

The fix is to keep all *printed* strings ASCII-only. Encoding proactively
against cp437 here means this can't silently regress the next time someone
pastes a smart quote or em dash into checklist.py or report.py.
"""

import io
import sys

import pytest

from narrative_humanizer import checklist
from narrative_humanizer.analyzer import AxisResult
from narrative_humanizer.cli import main
from narrative_humanizer.report import to_markdown


def _assert_cp437_safe(text: str) -> None:
    try:
        text.encode("cp437")
    except UnicodeEncodeError as exc:
        pytest.fail(f"Non-cp437-safe character found: {exc}")


def test_checklist_strings_are_cp437_safe():
    for item in checklist.CHECKLIST:
        for field in (item.name, item.ai_default, item.human_leaning, item.fix, item.stat):
            _assert_cp437_safe(field)
    for fingerprint in checklist.MODEL_FINGERPRINTS.values():
        _assert_cp437_safe(fingerprint)


def test_markdown_report_is_cp437_safe():
    results = [
        AxisResult(id=checklist.CHECKLIST[0].id, ai_leaning_present=True, evidence="quote", suggested_edit="fix"),
    ]
    _assert_cp437_safe(to_markdown(results))


def test_list_checklist_survives_a_strict_cp437_stdout(monkeypatch, capsys):
    # Reproduce the real failure mode directly: wrap stdout in a strict-cp437
    # TextIOWrapper the way a stock Windows console would present it, and
    # confirm `narrative-humanizer list-checklist` doesn't raise.
    buffer = io.BytesIO()
    wrapped = io.TextIOWrapper(buffer, encoding="cp437", errors="strict")
    monkeypatch.setattr(sys, "stdout", wrapped)

    exit_code = main(["list-checklist"])
    wrapped.flush()

    assert exit_code == 0
    assert b"Thematic explicitness" in buffer.getvalue()
