# narrative-humanizer (CLI)

Python CLI/library for the `narrative-humanizer` checklist — see the
[repo root README](../README.md) for full context, the Claude skill, and the research
this is based on ([StoryScope, COLM 2026](https://arxiv.org/abs/2604.03136)).

## Install

```bash
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

```bash
narrative-humanizer list-checklist          # no API call
narrative-humanizer check path/to/story.txt # runs the checklist via the Anthropic API
```

## Tests

```bash
pip install -e . pytest
python -m pytest
```
