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


def analyze_story(story_text: str, model: str = "claude-sonnet-5") -> list[AxisResult]:
    """Score a story against the checklist using the Anthropic API.

    Requires the ``anthropic`` package and an ``ANTHROPIC_API_KEY`` environment
    variable. Raises RuntimeError with a clear message if either is missing.
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

    # Models sometimes wrap JSON in a code fence despite instructions; strip it defensively.
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Could not parse model output as JSON. Raw output was:\n{raw_text}"
        ) from exc

    return [
        AxisResult(
            id=entry["id"],
            ai_leaning_present=bool(entry["ai_leaning_present"]),
            evidence=entry.get("evidence", ""),
            suggested_edit=entry.get("suggested_edit", ""),
        )
        for entry in parsed
    ]
