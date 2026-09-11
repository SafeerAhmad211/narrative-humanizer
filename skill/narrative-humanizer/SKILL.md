---
name: narrative-humanizer
description: Humanize AI-generated or AI-assisted fiction, stories, and long-form narrative writing by fixing structural/discourse-level "AI tells" (tidy plots, over-explained themes, over-described bodies, vague references, chronological linearity) — not just word choice. Grounded in the StoryScope (COLM 2026) research finding that narrative *choices* alone detect AI authorship at 93.2% macro-F1, even after all stylistic AI tics have been edited away. Use whenever the user asks to humanize, de-AI-ify, or make more natural a short story, novel chapter, creative-writing piece, screenplay, or narrative essay written or drafted by an LLM — especially after they've already run a sentence-level pass (or the `humanizer` skill) and the text still "reads AI." Also apply a lighter, explicitly-flagged version of these principles to non-fiction prose (papers, essays, reports) where AI tends toward the same over-tidy, over-explicit, over-linear defaults. Trigger phrases: "make this story sound human," "this still reads like AI," "fix the plot so it doesn't feel AI-generated," "humanize my narrative/paper," "this feels too neat/tidy," "de-AI my fiction."
metadata:
  type: reference
  source: "StoryScope: Investigating idiosyncrasies in AI fiction (Russell, Rajendhran, Pham, Iyyer, Wieting — COLM 2026), arXiv:2604.03136v6; code/data at https://github.com/jenna-russell/storyscope"
---

# Narrative Humanizer

## The core finding, and why it matters here

Most "humanize this text" work — including the companion `humanizer` skill — targets **surface style**: word choice (delve, tapestry), em-dash overuse, sentence rhythm, filler phrases. That's necessary but not sufficient. StoryScope (COLM 2026) shows that once you strip *all* stylistic cues away and look only at **narrative choices** — how a story handles plot, agency, time, character, setting, intertextuality — AI-written and human-written fiction remain separable at **93.2% macro-F1**, and a compact set of just **30 core features** still gets **84.8%**. Worse for anyone doing a light copy-edit pass: when AI stories were run through a professional-grade stylistic rewriter (removing cliché, purple prose, redundant exposition), narrative-based detection barely moved — **93.9% vs. 95.5%** macro-F1. Changing *what happens and how it's told* is structural work; changing *how it's phrased* is not enough.

So: if a draft still "reads AI" after a style pass, the problem is almost certainly in the narrative decisions themselves, not the prose. This skill is a checklist + workflow for finding and fixing those decisions.

**Scope honesty:** the underlying research is about fiction (10,272 human short stories vs. five LLMs, evaluated with a narratological feature taxonomy). The fiction-specific findings below are strong, quantified evidence. Section "Applying this to non-fiction" extrapolates the same *shape* of finding (AI defaults to tidy, explicit, linear) to expository writing — that part is a reasoned generalization, not something the paper measured, and should be presented to the user as such.

## Workflow

1. **Read the whole draft first**, not paragraph by paragraph — several of these features (subplot count, resolution type, temporal order, allusion specificity) are only visible at the whole-story level.
2. **Run the Signature Checklist below** against the draft. For each item, note whether the draft shows the AI-leaning default. You don't need instrumentation — these are things a careful reader can judge directly, the same way the paper's human annotators did (their model-vs-human agreement was Cohen's κ = 0.84).
3. **Pick 2–4 of the checklist items that are most present and most fixable** given the story's premise — don't try to invert all ten at once, or you'll overcorrect into a different set of AI-like defaults (forced quirkiness, allusion-dropping for its own sake). Ask the user which axes matter most if the story has constraints (length, audience, genre) that make some inversions awkward.
4. **Edit narrative structure, not just wording.** Concretely this usually means: cut or add a scene, reorder chronology, change what the resolution depends on, swap a vague reference for a specific one, add or remove a subplot, change who has agency in the climax. These are structural edits — expect to touch multiple scenes, not just tweak sentences.
5. **If a sentence-level pass hasn't happened yet**, do that too (or point the user at the `humanizer` skill) — the two layers are complementary and the paper's own numbers show style still adds real signal on top of narrative (96.0% vs. 93.2% macro-F1 combined vs. narrative-only).
6. **Don't claim detector-proofing.** These are population-level tendencies from one benchmark, not a guarantee against any given detector. Frame the work as "making the story read like it was actually imagined by someone," not "beating AI detection" — that framing also keeps you clear of trying to help someone misrepresent AI-written work as human where disclosure is required (the paper opens with a publisher pulling a novel over exactly this).

## The Signature Checklist

For each axis: the AI-leaning default (with the paper's measured rate where available), the human-leaning alternative, and what a fix looks like.

### 1. Thematic explicitness — *stop moralizing*
- **AI default:** the narrator or an ending beat spells out the theme/lesson outright (77% of AI stories vs. 52% of human stories); dialogue is used for open philosophical debate (59% vs. 34%); a story's moral center stays singular and tidy.
- **Fix:** cut the sentence that states the lesson. Let the theme live in the final image or action instead of a stated conclusion. Let two threads of meaning coexist without the narrator reconciling them.

### 2. Plot linearity and single-track resolution — *let it stay a little messy*
- **AI default:** tight causal chains, resolutions driven by protagonist choice rather than external/ambiguous forces (69% vs. 46%), far fewer subplots (79% of AI stories have "no subplots" vs. 57% of human stories).
- **Fix:** add a subplot that doesn't fully resolve, or let an outcome hinge partly on chance/other characters rather than the protagonist's clean decision. Leave one thread loose. Humans favor ambiguous endings and internal acceptance over neat external resolution (47% vs 27% "internal understanding/acceptance").

### 3. Chronology — *break the timeline*
- **AI default:** stories proceed in strict chronological order with few time jumps.
- **Fix:** add a flashback, flash-forward, or reveal something out of order that forces the reader to re-contextualize an earlier scene. Human stories use nonlinear structure specifically to delay key revelations — consider whether a reveal would land harder told out of sequence.

### 4. Sensory/bodily over-description — *name the feeling sometimes*
- **AI default:** emotion is conveyed almost entirely through physical sensation and bodily metaphor (81% vs. 38%) and smell-based imagery (82% vs. 57%) — fear becomes "a tightening chest, cold sweat," never just "she was afraid." Only 8% of AI stories use a direct emotion label vs. 29% of human stories.
- **Fix:** you don't need to remove all embodied description — but reintroduce a few plain, direct emotion labels. Not every feeling needs to be rendered through the body; sometimes "he was afraid" is the human choice, not the lazy one.

### 5. Vague, unnamed intertextual references — *be specific*
- **AI default:** when a story alludes to other works, it favors vague allusion over specific named reference (72% vs. 50%), and references outside works at roughly half the human rate (24% vs. 47%).
- **Fix:** if a character would plausibly know a specific book, song, film, or brand, name it. Specificity here is itself a human-leaning signal, not just flavor.

### 6. No fourth-wall break / no reader address — *let the narrator acknowledge someone's there*
- **AI default:** narration proceeds as though no one is reading (7% direct reader address vs. 28% for humans); the fourth wall almost never breaks (39% vs. 67%).
- **Fix:** this doesn't fit every story or genre, but where the voice allows it, an aside to the reader ("you, dear reader, already suspect...") or a narrator who register-shifts to acknowledge an audience is a human-leaning move, not a gimmick.

### 7. Narrow narrative range — *don't default to the safe combination*
- **AI default:** fewer locations, lower dialogue-to-narration ratio, fewer subplots feeding into the main theme (42% vs. 21%), more morally settled protagonists (comfortable, "good" choices) rather than morally ambivalent ones (59% human vs. 38% AI keep the protagonist morally ambivalent).
- **Fix:** the underlying pattern the paper measures is that human stories are statistically *rarer* combinations of narrative choices — they don't cluster around a "generically safe" default the way AI stories do (mean rarity percentile 0.71 human vs. 0.49 AI; AI models occupy a tight, shared region of narrative-choice space while human stories spread out). Practically: when a scene has an obvious, default way to write it, ask whether an atypical combination of choices (setting + who has power + how the scene ends) would still serve the story. You're not looking for novelty for its own sake — you're avoiding the converged AI center of narrative-choice space.

## Per-model fingerprints (diagnostic, not prescriptive)

If you know or suspect which model produced the draft, these specific tics from the paper are worth a targeted look — but treat this as a hint about what to check, not a checklist to blindly apply to every draft:

- **Claude:** flat event escalation (avoids "avalanche" endings), quiet/restrained endings, reverent toward literary convention rather than subverting it, avoids dream sequences.
- **GPT:** overuses gossip/rumor as a plot mechanism, favors ensemble/social-network-heavy casts, frames stories as retrospection from years/decades later.
- **Gemini:** tidiest endings and most extended denouements; settings skew bleak/oppressive (88% tagged that way).
- **DeepSeek:** front-loads context that other sources reveal later (i.e., under-uses delayed revelation).
- **Kimi:** sits closest to the generic AI center — fewest distinctive tics, so treat it as the default checklist case.

## Applying this to non-fiction (papers, essays, reports) — extrapolation, flag it as such

The paper doesn't test expository prose, but the same underlying failure mode — AI converging on a small set of "safe," over-explicit, over-linear defaults — shows up in non-fiction AI writing too. When adapting these ideas to a paper or essay, be upfront with the user that this is reasoning by analogy, not measured:

- **Thematic explicitness → over-signposted argument.** AI essays tend to state their conclusion, restate it in the intro, and then restate it again in a summary paragraph. Trust the reader to carry the thread; cut at least one of the three restatements.
- **Tidy single-track resolution → false confidence.** AI prose tends to resolve every tension it raises rather than leaving a genuinely open question or an acknowledged limitation stated in the writer's own voice, not a boilerplate "future work" paragraph.
- **Vague references → cite specifically.** Prefer naming the specific paper, dataset, or claim over "prior work has shown."
- **Chronological/linear default → structure by argument, not chronology.** A literature review or methods section written by AI often narrates work in the order it thought of it. Human experts more often structure around the argument's logic.

Do not use this section to help someone misrepresent AI-drafted academic or professional writing as fully human-authored where disclosure is required — that's the exact scenario (a novel pulled by its publisher over undisclosed AI generation) that motivates the source paper.

## Source

StoryScope: Investigating idiosyncrasies in AI fiction. Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. Published as a conference paper at COLM 2026. arXiv:2604.03136v6. Code, prompts, and data: https://github.com/jenna-russell/storyscope (MIT-licensed; the `assets/` folder itself only holds the project's pipeline diagram — the substantive artifacts are the `storyscope/` package, `config/models.yaml`, and the released `taxonomy.json` / `storyscope_features.parquet` describing the 304-feature taxonomy referenced above).
