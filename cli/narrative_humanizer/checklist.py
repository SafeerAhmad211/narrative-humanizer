"""The narrative-choice signature checklist.

Each entry summarizes one axis where StoryScope (arXiv:2604.03136) found a
statistically significant gap between AI-generated and human-written fiction,
measured over 61,608 stories (10,272 human, five LLMs). Percentages are as
reported in the paper; see docs/research-summary.md for full citations and
context per finding.

This data structure exists so the checklist is a single source of truth used
by both the analyzer (LLM-driven scoring) and any future rule-based checks —
it deliberately holds no code, just facts + guidance, so it stays easy to
audit against the paper.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ChecklistItem:
    id: str
    name: str
    ai_default: str
    human_leaning: str
    fix: str
    stat: str


CHECKLIST: list[ChecklistItem] = [
    ChecklistItem(
        id="thematic_explicitness",
        name="Thematic explicitness",
        ai_default=(
            "The narrator or an ending beat states the theme/lesson outright; "
            "dialogue doubles as open philosophical debate."
        ),
        human_leaning=(
            "The theme lives in the final image or action; two threads of "
            "meaning can coexist unreconciled."
        ),
        fix="Cut the sentence that states the lesson. Don't let the narrator moralize.",
        stat="Explicit theme-statement: 77% AI vs. 52% human. Dialogue-as-debate: 59% vs. 34%.",
    ),
    ChecklistItem(
        id="plot_linearity",
        name="Plot linearity / single-track resolution",
        ai_default=(
            "Tight causal chains; resolution driven cleanly by the "
            "protagonist's choice; no subplots."
        ),
        human_leaning=(
            "A subplot that doesn't fully resolve; an outcome partly "
            "dependent on chance or other characters; ambiguous endings."
        ),
        fix="Add an unresolved subplot, or let the climax hinge partly on something outside the protagonist's control.",
        stat='"No subplots": 79% AI vs. 57% human. Protagonist-driven resolution: 69% vs. 46%.',
    ),
    ChecklistItem(
        id="chronology",
        name="Chronological rigidity",
        ai_default="The story proceeds in strict chronological order.",
        human_leaning="Flashbacks, flash-forwards, or an out-of-order reveal.",
        fix="Consider whether a reveal lands harder told out of sequence; add one deliberate time jump.",
        stat="Human stories use significantly more chronological discontinuity (temporal-structure dimension).",
    ),
    ChecklistItem(
        id="sensory_overdescription",
        name="Sensory / bodily over-description",
        ai_default=(
            "Emotion is conveyed almost entirely through physical sensation "
            "and bodily metaphor; heavy smell-based imagery."
        ),
        human_leaning="A plain, direct emotion label used unapologetically.",
        fix='Reintroduce a few direct emotion labels ("she was afraid") instead of always rendering feeling through the body.',
        stat="Physical-sensation emotion: 81% AI vs. 38% human. Smell imagery: 82% vs. 57%. Direct emotion label: 8% AI vs. 29% human.",
    ),
    ChecklistItem(
        id="vague_references",
        name="Vague intertextual references",
        ai_default="Allusions to other works are vague and unnamed.",
        human_leaning="Allusions name a specific book, film, song, or brand.",
        fix="If a character would plausibly know the specific work, name it.",
        stat="Vague allusion: 72% AI vs. 50% human. Outside-work reference rate: 24% AI vs. 47% human.",
    ),
    ChecklistItem(
        id="no_reader_address",
        name="No fourth-wall break",
        ai_default="Narration proceeds as if no one is reading.",
        human_leaning="The narrator occasionally acknowledges the reader directly.",
        fix='Where the voice allows it, let the narrator break the fourth wall once ("you, dear reader...").',
        stat="Direct reader address: 7% AI vs. 28% human. Fourth-wall break: 39% vs. 67%.",
    ),
    ChecklistItem(
        id="narrow_range",
        name="Narrow narrative range / safe defaults",
        ai_default=(
            "Fewer locations, lower dialogue-to-narration ratio, morally "
            "settled protagonists, subplots that all feed the same theme."
        ),
        human_leaning=(
            "A rarer combination of narrative choices — humans occupy a "
            "statistically more dispersed region of 'narrative-choice space.'"
        ),
        fix="Where a scene has an obvious default treatment, try an atypical combination of setting/power/outcome instead — not novelty for its own sake, just avoiding the converged AI center.",
        stat="Mean rarity percentile: 0.71 human vs. 0.49 AI. Morally ambivalent protagonist: 59% human vs. 38% AI.",
    ),
]

MODEL_FINGERPRINTS: dict[str, str] = {
    "claude": "Flat event escalation, quiet/restrained endings, reverent toward literary convention, avoids dream sequences.",
    "gpt": "Overuses gossip/rumor as a plot device, ensemble/social-network-heavy casts, frames stories as retrospection from years later.",
    "gemini": "Tidiest endings, extended denouements, settings skew bleak/oppressive (88% tagged that way).",
    "deepseek": "Front-loads context that other sources reveal later (under-uses delayed revelation).",
    "kimi": "Closest to the generic AI center; fewest distinctive tics.",
}
