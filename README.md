# narrative-humanizer

[![tests](https://github.com/SafeerAhmad211/narrative-humanizer/actions/workflows/tests.yml/badge.svg)](https://github.com/SafeerAhmad211/narrative-humanizer/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Fix the *structural* reasons AI-written fiction still "reads AI" after a style pass —
tidy plots, over-explained themes, over-described bodies, vague references,
chronological linearity — instead of just swapping words.

This project is grounded in the published findings of **StoryScope** (Russell,
Rajendhran, Pham, Iyyer, Wieting; COLM 2026; [arXiv:2604.03136](https://arxiv.org/abs/2604.03136);
[code/data](https://github.com/jenna-russell/storyscope)), which found that AI and
human fiction remain separable at **93.2% macro-F1** using *only* narrative-structure
features — with all stylistic cues (word choice, sentence rhythm) removed — and that
this signal barely drops (95.5% → 93.9% macro-F1) even after a professional-grade
stylistic rewrite pass. In other words: most "humanizer" tools fix the prose surface.
This targets the layer underneath it — the actual narrative decisions.

**This is an independent, community project, not affiliated with the StoryScope
authors or their codebase.** It re-implements a small, human-readable checklist
inspired by their reported findings; it does not reuse their code, data, or feature
taxonomy. See [`docs/research-summary.md`](docs/research-summary.md) for the full
summary and citations, and go read the actual paper for the real methodology.

## What's in this repo

- **[`skill/narrative-humanizer/`](skill/narrative-humanizer/SKILL.md)** — a
  ready-to-use [Claude Code](https://github.com/anthropics/claude-code) / Claude
  skill. Drop it in `~/.claude/skills/` (or your project's `.claude/skills/`) and
  Claude will use it whenever you ask to humanize, de-AI-ify, or fix the plot of a
  story that "still reads like AI."
- **[`cli/`](cli/)** — a small Python CLI/library, `narrative-humanizer`, that runs
  the same checklist against a story file via the Anthropic API and produces a
  Markdown or JSON report of which axes are flagged, with evidence and suggested
  structural edits. **This part is a v2 / work in progress** — it's functional and
  tested, but the checklist-as-heuristic approach is inherently rougher than the
  paper's own 304-feature classifier pipeline. Contributions welcome.
- **[`docs/research-summary.md`](docs/research-summary.md)** — a summary of the
  paper's headline numbers, the concrete narrative-choice gaps between AI and human
  fiction, and per-model fingerprints (Claude, GPT, Gemini, DeepSeek, Kimi).

## Quickstart: the Claude skill

```bash
cp -r skill/narrative-humanizer ~/.claude/skills/
```

Then, in Claude Code or Claude with skills enabled, ask something like: *"this short
story still reads like AI even after a style edit, can you fix the plot?"*

## Quickstart: the CLI

```bash
cd cli
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
narrative-humanizer check path/to/story.txt
```

```bash
# see the checklist itself, no API call needed
narrative-humanizer list-checklist
```

Run the tests:

```bash
cd cli
pip install -e ".[dev]" 2>/dev/null || pip install -e . pytest
python -m pytest
```

## The checklist (short version)

| Axis | AI-leaning default | Human-leaning alternative |
|---|---|---|
| Thematic explicitness | States the lesson outright (77% vs 52%) | Theme lives in the final image, unstated |
| Plot linearity | Tidy, protagonist-driven, no subplots (79% vs 57%) | An unresolved subplot; outcome partly out of the protagonist's hands |
| Chronology | Strict chronological order | Flashbacks / out-of-order reveals |
| Sensory over-description | Emotion always rendered through the body (81% vs 38%) | A plain, direct emotion label sometimes |
| Intertextual references | Vague, unnamed allusions (72% vs 50%) | Names the specific book/film/song |
| Reader address | Narrator never acknowledges the reader (7% vs 28%) | An occasional fourth-wall break |
| Narrative range | Safe, converged defaults | A rarer, more dispersed combination of choices |

Full detail, stats, and fixes: [`docs/research-summary.md`](docs/research-summary.md)
and [`skill/narrative-humanizer/SKILL.md`](skill/narrative-humanizer/SKILL.md).

## Ethics note

This is meant for making your own genuinely-drafted, AI-assisted writing read
naturally — not for helping anyone misrepresent wholly AI-generated work as
human-authored where disclosure is required. The paper that motivates this project
opens with a real example of exactly that going wrong: a publisher pulling a novel
after it was flagged as AI-generated.

## License

MIT — see [LICENSE](LICENSE). This project is independent of, and not derived from,
the StoryScope authors' MIT-licensed codebase; only the *published findings* of their
paper are used here (as facts, summarized and cited, not copied code or text).
