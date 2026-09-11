"""Command-line entrypoint: narrative-humanizer <story.txt>"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from .analyzer import analyze_story
from .checklist import CHECKLIST
from .report import to_markdown


def _cmd_check(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.story)
    if not path.exists():
        print(f"error: no such file: {path}", file=sys.stderr)
        return 1

    story_text = path.read_text(encoding="utf-8")

    try:
        results = analyze_story(story_text, model=args.model)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        payload = [
            {
                "id": r.id,
                "ai_leaning_present": r.ai_leaning_present,
                "evidence": r.evidence,
                "suggested_edit": r.suggested_edit,
            }
            for r in results
        ]
        print(json.dumps(payload, indent=2))
    else:
        print(to_markdown(results, story_name=path.stem))

    return 0


def _cmd_list_checklist(_: argparse.Namespace) -> int:
    for item in CHECKLIST:
        print(f"[{item.id}] {item.name}")
        print(f"  AI default:   {item.ai_default}")
        print(f"  Human-leaning: {item.human_leaning}")
        print(f"  Stat:         {item.stat}")
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="narrative-humanizer",
        description="Detect AI-typical narrative-structure defaults in a story, and suggest structural fixes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Analyze a story file against the checklist.")
    check.add_argument("story", help="Path to a plain-text story file.")
    check.add_argument(
        "--model",
        default="claude-sonnet-5",
        help="Anthropic model id to use for analysis (default: claude-sonnet-5).",
    )
    check.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    check.set_defaults(func=_cmd_check)

    listc = sub.add_parser("list-checklist", help="Print the checklist axes and exit (no API call).")
    listc.set_defaults(func=_cmd_list_checklist)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
