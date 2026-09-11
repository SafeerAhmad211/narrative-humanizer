# Contributing

Thanks for looking at this. Two areas most worth contributions right now:

- **The checklist itself** ([`cli/narrative_humanizer/checklist.py`](cli/narrative_humanizer/checklist.py) /
  [`skill/narrative-humanizer/SKILL.md`](skill/narrative-humanizer/SKILL.md)) — if you find a narrative-structure
  signal from the StoryScope paper (or a closely related study) that isn't represented, or evidence that one of
  the existing axes is stated imprecisely, open an issue or PR with the citation.
- **The CLI** ([`cli/`](cli/)) is explicitly a v2/work-in-progress heuristic layer on top of the checklist. It's
  functional and tested, but rougher than the paper's own classifier pipeline — ideas for making the analysis
  more reliable (e.g. multiple samples per axis, disagreement detection) are welcome.

## Running the CLI's test suite

```bash
cd cli
pip install -e . pytest pytest-cov
python -m pytest --cov=narrative_humanizer --cov-report=term-missing
```

CI (`.github/workflows/tests.yml`) runs this same suite on Ubuntu and Windows, across two Python versions, and
also does a clean `python -m build` + CLI smoke test — both of those were added specifically because a
`pyproject.toml` path bug and a Windows-console encoding crash slipped past `pytest` alone during initial
development. If you add a new failure mode, prefer adding a regression test over just fixing it inline (see
`tests/test_encoding.py` for the pattern).

## Pull requests

- Keep PRs focused; one fix or one feature per PR is easier to review than a mix.
- Add a test for anything that fixes a bug — see `tests/` for the existing style (plain `pytest`, no fixtures
  framework beyond what `pytest` itself provides, fakes over mocks where reasonable).
- If you touch `checklist.py`, keep the `stat` field's percentages traceable back to the paper
  (arXiv:2604.03136) or `docs/research-summary.md`.

## Reporting a bug

Please include: what you ran, what you expected, what happened instead, and your OS + Python version — the
Windows-console encoding bug fixed in this repo's history only showed up on certain codepages, so environment
details matter more here than in a typical CLI tool.
