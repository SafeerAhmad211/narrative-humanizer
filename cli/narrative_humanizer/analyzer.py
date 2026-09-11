"""LLM-driven scoring of a story against the narrative-choice checklist.

This deliberately does not try to reproduce StoryScope's own pipeline (a
304-feature taxonomy scored by a fine-tuned classifier over a curated corpus).
That's a research artifact, not something a single-story CLI tool can
replicate meaningfully. Instead, this asks an LLM to do what the paper's own
human annotators did reasonably well (mean human-model Cohen's kappa = 0.84
in the paper's validation study): read the whole story and judge, per axis,
whether the AI-leaning default is present, with a quoted excerpt as evidence.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass

from .checklist import CHECKLIST

SYSTEM_PROMPT = """You are a careful literary analyst reviewing a piece of fiction for \
signs of AI-typical narrative construction, as distinct from AI-typical prose style. \
You are NOT looking at word choice, sentence rhythm, or vocabulary -- only at \
structural/discourse-level narrative choices: plot shape, chronology, how theme is \
handled, how emotion is rendered, how references are made, whether the narrator \
acknowledges the reader, and how conventional the overall combination of choices is.

For each checklist axis, decide whether the AI-leaning default is present in this \
story, quote the strongest piece of evidence (a short excerpt, or "whole-story" if \
it's a structural judgment that isn't localized to one passage), and suggest one \
concrete structural edit if the AI-leaning default is present.

Respond ONLY with a JSON array, one object per axis, in this exact shape:
[
  {"id": "<axis id>", "ai_leaning_present": true/false, "evidence": "<quote or 'whole-story'>", "suggested_edit": "<concrete edit, or empty string if not present>"}
]
"""


@dataclass
class AxisResult:
    id: str
    ai_leaning_present: bool
    evidence: str
    suggested_edit: str


def _build_user_prompt(story_text: str) -> str:
    axes = "\n".join(
        f"- id: {item.id}\n  name: {item.name}\n  AI-leaning default: {item.ai_default}\n  Human-leaning alternative: {item.human_leaning}"
        for item in CHECKLIST
    )
    return (
        f"Checklist axes:\n{axes}\n\n"
        f"Story to analyze:\n\"\"\"\n{story_text}\n\"\"\"\n\n"
        "Return the JSON array now, nothing else."
    )


def _extract_json_text(raw_text: str) -> str:
    """Strip a Markdown code fence around a JSON payload, if present.

    Models sometimes wrap JSON in ```json ... ``` or plain ``` ... ``` fences
    despite instructions not to. This is intentionally a standalone, pure
    function (no API calls) so the fence-stripping logic -- the most fragile
    part of parsing a free-form model response -- can be unit tested directly
    against many response shapes, not just exercised incidentally by a live
    API call.
    """
    text = raw_text.strip()
    if not text.startswith("```"):
        return text

    # Drop the opening fence line (```json or ```) and the closing fence line.
    lines = text.splitlines()
    lines = lines[1:]  # drop opening ``` (with optional language tag) line
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]  # drop closing ``` line
    return "\n".join(lines).strip()


def _parse_axis_results(parsed: object) -> list[AxisResult]:
    """Validate and convert the model's parsed JSON into AxisResult objects.

    Raises RuntimeError with a specific, actionable message on any shape
    mismatch, rather than letting a bare KeyError/TypeError from a malformed
    model response surface to the CLI user.
    """
    if not isinstance(parsed, list):
        raise RuntimeError(
            f"Expected a JSON array of axis results, got {type(parsed).__name__}: {parsed!r}"
        )

    results: list[AxisResult] = []
    for i, entry in enumerate(parsed):
        if not isinstance(entry, dict):
            raise RuntimeError(f"Axis result #{i} is not a JSON object: {entry!r}")
        missing = [key for key in ("id", "ai_leaning_present") if key not in entry]
        if missing:
            raise RuntimeError(
                f"Axis result #{i} is missing required field(s) {missing}: {entry!r}"
            )
        results.append(
            AxisResult(
                id=entry["id"],
                ai_leaning_present=bool(entry["ai_leaning_present"]),
                evidence=entry.get("evidence", ""),
                suggested_edit=entry.get("suggested_edit", ""),
            )
        )
    return results


def analyze_story(story_text: str, model: str = "claude-sonnet-5") -> list[AxisResult]:
    """Score a story against the checklist using the Anthropic API.

    Requires the ``anthropic`` package and an ``ANTHROPIC_API_KEY`` environment
    variable. Raises RuntimeError with a clear message if either is missing,
    or if the model's response can't be parsed into axis results.
    """
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover - import guard
        raise RuntimeError(
            "The 'anthropic' package is required for analysis. Install with: "
            "pip install anthropic"
        ) from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set the ANTHROPIC_API_KEY environment variable to run analysis."
        )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(story_text)}],
    )

    raw_text = "".join(
        block.text for block in response.content if getattr(block, "type", None) == "text"
    ).strip()

    json_text = _extract_json_text(raw_text)

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Could not parse model output as JSON. Raw output was:\n{raw_text}"
        ) from exc

    return _parse_axis_results(parsed)
