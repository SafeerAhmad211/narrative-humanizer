# Research summary: StoryScope (COLM 2026)

**Paper:** Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting.
*StoryScope: Investigating idiosyncrasies in AI fiction.* Published as a conference
paper at COLM 2026. arXiv:2604.03136.
Code & data: https://github.com/jenna-russell/storyscope (MIT license).

This document summarizes the findings this repo's checklist is built on. It is a
summary, not a reproduction — for the full methodology, read the paper.

## The question

Can AI-generated fiction be told apart from human-written fiction *without* relying on
stylistic tells (word choice, sentence rhythm, em-dash overuse) — i.e., using only
*narrative* choices like plot structure, character agency, and chronology?

## The method, briefly

The authors built a parallel corpus: 10,272 human-written short stories (from Books3),
each mirrored by prompting five LLMs (Claude Sonnet 4.6, GPT-5.4, Gemini 3 Flash,
DeepSeek V3.2, Kimi K2.5) to write a story from a reverse-engineered prompt for the
same premise — 61,608 stories total. They converted each story into a structured
template across 10 narrative dimensions (grounded in the NarraBench taxonomy: agent,
social network, event, plot, structure, setting, time, revelation, perspective,
style), then used an LLM pipeline to discover 304 discriminating features and score
every story against them. An XGBoost classifier was trained on the resulting feature
vectors.

## Headline results

| Task | Narrative features only | Narrative + style | Text-based baselines (e.g. ModernBERT) |
|---|---|---|---|
| Binary human vs. AI detection | 93.2% macro-F1 | 96.0% macro-F1 | ~99.7–99.9% macro-F1 |
| Six-way authorship attribution | 68.4% macro-F1 | 77.3% macro-F1 | ~99.5–99.8% macro-F1 |

A compact set of **30 "core" features** (stable and important across all five AI
models) retains **84.8%** macro-F1 on the binary task — most of the signal, from a
tenth of the features.

**Robust to stylistic editing.** The authors ran 278 AI stories through a
professional-grade span-level rewriting framework (LAMP) that removes cliché, purple
prose, and redundant exposition. Narrative-based detection barely moved: **93.9%**
macro-F1 on edited stories vs. **95.5%** on the originals — a 1.6-point drop. Style
edits don't touch the underlying narrative decisions.

## What actually separates AI from human stories

- **AI over-explains its themes.** Explicit theme statement: 77% AI vs. 52% human.
  Dialogue used for open philosophical debate: 59% vs. 34%. AI spells out meaning
  rather than trusting the reader to infer it.
- **Human authors subvert linearity.** Tighter causal chains and more
  protagonist-driven resolutions in AI (69% vs. 46%); far fewer subplots (79% "no
  subplots" in AI vs. 57% human). Humans use more time jumps, flashbacks, and
  nonlinear structure to delay revelations.
- **AI over-writes the body and senses.** Emotion conveyed through physical
  sensation/bodily metaphor: 81% AI vs. 38% human. Smell-based imagery: 82% vs. 57%.
  Direct emotion labels ("she was afraid"): only 8% AI vs. 29% human.
- **Human authors engage the outside world.** Reference specific texts/authors at
  nearly double the AI rate (47% vs. 24%); break the fourth wall far more often (67%
  vs. 39%); address the reader directly more (28% vs. 7%).
- **AI writing has less diverse narrative features.** Human stories span more
  locations, carry more dialogue relative to narration, and present morally
  ambivalent protagonists more often (59% vs. 38%).
- **Human narratives are statistically rarer.** Mean rarity percentile (nearest-25
  Euclidean distance in feature space): 0.71 human vs. 0.49 AI. The five AI models
  cluster tightly together in narrative-choice space; human stories are more
  dispersed and occupy a distinct region entirely.

## Per-model fingerprints (six-way attribution)

- **Claude:** flat event escalation, quiet/restrained endings, reverent toward
  literary convention, avoids dream sequences.
- **GPT:** overuses gossip/rumor as a plot device, ensemble/social-network-heavy
  casts, frames stories as retrospection from years/decades later, subverts
  expectations more than other AI sources.
- **Gemini:** tidiest endings and extended denouements; settings skew
  bleak/oppressive (88% tagged that way).
- **DeepSeek:** front-loads context that other sources reveal later.
- **Kimi:** fewest distinguishing fingerprints — sits at the generic center of the
  AI distribution.
- Gemini, DeepSeek, and Kimi form the most-confused cluster in attribution (most
  common AI-AI confusion: Gemini↔DeepSeek, 222+207 stories); Claude and human are the
  most distinctive/separable sources.

## Scope and limits

- This is a fiction-specific study (short stories, ~5,000 words on average). The
  `docs/` and `skill/` material in this repo flags where ideas are extrapolated
  beyond fiction (e.g. to essays/papers) as reasoned analogy, not measured findings.
- These are population-level statistical tendencies from one benchmark and one
  snapshot of five models, not a guarantee about any individual story or any
  particular AI detector.
- The paper's own framing: differences in narrative *construction*, not just
  writing style, can separate human-written original work from AI-generated fiction
  — which matters for authorship, originality, and copyright questions as AI-authored
  work becomes harder to distinguish by surface style alone.
