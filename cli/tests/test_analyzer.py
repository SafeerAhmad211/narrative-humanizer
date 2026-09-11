import json
import sys
import types

import pytest

from narrative_humanizer.analyzer import (
    _extract_json_text,
    _parse_axis_results,
    analyze_story,
)
from narrative_humanizer.checklist import CHECKLIST


# --- _extract_json_text -----------------------------------------------------

def test_extract_json_text_passthrough_when_no_fence():
    raw = '[{"id": "a"}]'
    assert _extract_json_text(raw) == raw


def test_extract_json_text_strips_plain_fence():
    raw = "```\n[{\"id\": \"a\"}]\n```"
    assert _extract_json_text(raw) == '[{"id": "a"}]'


def test_extract_json_text_strips_json_language_tag():
    raw = "```json\n[{\"id\": \"a\"}]\n```"
    assert _extract_json_text(raw) == '[{"id": "a"}]'


def test_extract_json_text_handles_surrounding_whitespace():
    raw = "  \n```json\n[{\"id\": \"a\"}]\n```\n  "
    assert _extract_json_text(raw) == '[{"id": "a"}]'


def test_extract_json_text_multiline_payload_survives_fence_stripping():
    raw = '```json\n[\n  {"id": "a"},\n  {"id": "b"}\n]\n```'
    result = _extract_json_text(raw)
    assert json.loads(result) == [{"id": "a"}, {"id": "b"}]


# --- _parse_axis_results -----------------------------------------------------

def test_parse_axis_results_happy_path():
    parsed = [
        {
            "id": "thematic_explicitness",
            "ai_leaning_present": True,
            "evidence": "the narrator explains the moral",
            "suggested_edit": "cut the last line",
        },
        {"id": "chronology", "ai_leaning_present": False},
    ]
    results = _parse_axis_results(parsed)
    assert len(results) == 2
    assert results[0].id == "thematic_explicitness"
    assert results[0].ai_leaning_present is True
    # missing optional fields default to empty string, not KeyError
    assert results[1].evidence == ""
    assert results[1].suggested_edit == ""


def test_parse_axis_results_rejects_non_list():
    with pytest.raises(RuntimeError, match="Expected a JSON array"):
        _parse_axis_results({"id": "not a list"})


def test_parse_axis_results_rejects_non_dict_entry():
    with pytest.raises(RuntimeError, match="not a JSON object"):
        _parse_axis_results(["just a string"])


def test_parse_axis_results_rejects_missing_required_field():
    with pytest.raises(RuntimeError, match="missing required field"):
        _parse_axis_results([{"ai_leaning_present": True}])  # no 'id'


def test_parse_axis_results_coerces_truthy_ai_leaning_present():
    # Some models emit "true"/"false" strings or 0/1 instead of real booleans.
    results = _parse_axis_results([{"id": "a", "ai_leaning_present": 1}])
    assert results[0].ai_leaning_present is True


# --- analyze_story (integration, with a fake Anthropic client) --------------

class _FakeTextBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeResponse:
    def __init__(self, text):
        self.content = [_FakeTextBlock(text)]


class _FakeMessages:
    def __init__(self, response_text):
        self._response_text = response_text
        self.last_call_kwargs = None

    def create(self, **kwargs):
        self.last_call_kwargs = kwargs
        return _FakeResponse(self._response_text)


class _FakeAnthropicClient:
    def __init__(self, response_text, api_key=None):
        self.messages = _FakeMessages(response_text)


def _install_fake_anthropic(monkeypatch, response_text):
    fake_module = types.SimpleNamespace(
        Anthropic=lambda api_key=None: _FakeAnthropicClient(response_text, api_key=api_key)
    )
    monkeypatch.setitem(sys.modules, "anthropic", fake_module)


def test_analyze_story_requires_api_key(monkeypatch):
    _install_fake_anthropic(monkeypatch, "[]")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        analyze_story("once upon a time...")


def test_analyze_story_parses_fenced_response_end_to_end(monkeypatch):
    payload = [{"id": item.id, "ai_leaning_present": False} for item in CHECKLIST]
    fenced = "```json\n" + json.dumps(payload) + "\n```"
    _install_fake_anthropic(monkeypatch, fenced)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    results = analyze_story("once upon a time...")

    assert len(results) == len(CHECKLIST)
    assert all(not r.ai_leaning_present for r in results)


def test_analyze_story_raises_clear_error_on_unparseable_output(monkeypatch):
    _install_fake_anthropic(monkeypatch, "not json at all")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    with pytest.raises(RuntimeError, match="Could not parse model output"):
        analyze_story("once upon a time...")
