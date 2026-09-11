"""narrative_humanizer: structural AI-tell detection for fiction, grounded in the
StoryScope (COLM 2026) narrative-feature findings.

This package is an independent, community implementation inspired by the published
findings of:

    Russell, Rajendhran, Pham, Iyyer, Wieting. "StoryScope: Investigating
    idiosyncrasies in AI fiction." COLM 2026. arXiv:2604.03136.
    Code/data: https://github.com/jenna-russell/storyscope

It is not affiliated with, endorsed by, or derived from the StoryScope authors'
codebase. It re-implements a small, human-readable subset of their reported
signal (the checklist in ``checklist.py``) as an LLM-driven analysis tool.
"""

from .checklist import CHECKLIST, MODEL_FINGERPRINTS

__all__ = ["CHECKLIST", "MODEL_FINGERPRINTS"]
__version__ = "0.1.0"
