# Pre-locked Hypotheses

**Draft generated:** 2026-08-22T11:16:08Z
**Status: DRAFT — not yet locked.** Written by Claude from `results/selection_analysis.md`
alone, before any debrief data existed or was read. Per design §5.3, this record exists
to separate hypotheses that came from the selection distribution from any narrative a
model produces later when asked to explain its choices in §6. Edit freely, then replace
this status line with `**Status: LOCKED** — reviewed and approved by <name>, <timestamp>`
before running `run_debrief.py`. The pre-lock gate in `run_debrief.py` only checks that
this file exists — it does not enforce the "locked" line, so the discipline of not
running debrief until you've actually reviewed this is on us, not the code.

Source: `data/trials.jsonl` (3,318 trials, 0 unparseable, 0 errors) and
`results/selection_analysis.md`, generated 2026-08-22T01:00:09.

---

## H1 — Overall distribution is far from uniform, dominated by two phrases

Selection is concentrated almost entirely on FREE SPEECH MAKES FREE PEOPLE and WOMEN
BELONG IN ALL PLACES WHERE DECISIONS ARE MADE across every condition (AGREE, TAKE,
WEAR), while WITHOUT BORDERS – SIN FRONTERAS, PLANET BEFORE PROFITS, and NOT HERE TO
BE LIKED are rarely chosen under persona conditioning. §1's chi-square rejects
uniformity in every framing at p « .001.

*Candidate explanation:* the two dominant phrases are the most general, least
specific value statements in the set (per the §3.2 coding, both rated "general"
specificity); the model may default to broadly agreeable statements over ones that
take a specific policy position. This is a phrase-property hypothesis, not yet
distinguished from a persona-behavior hypothesis (see H2).

## H2 — Persona conditioning substantially changes the distribution, and the direction reverses on two phrases

§2 shows persona and no-persona baseline are **not close**. No-persona baseline favors
NOT HERE TO BE LIKED (62.6%) and almost never selects FREE SPEECH (0.5%).
Persona-conditioned trials invert this: FREE SPEECH jumps to 44.6%, NOT HERE TO BE
LIKED drops to 7.0%.

*Candidate explanation:* the reversal suggests personas are not just adding noise
around a phrase-intrinsic baseline — persona content is doing real work in shifting
which phrase reads as the "default" choice. Under this design's own interpretive rule
(§9.5), this strengthens rather than weakens persona-based readings of the other
results. Worth checking in the debrief whether "no clear reason" / aesthetic-type
explanations are more common in the no-persona condition, consistent with the model
falling back on a different heuristic without a persona to anchor to.

## H3 — Target phrase shows a floor effect under AGREE/WEAR, not an interpretable display-cost signal

The primary manipulation (§3) cannot detect a WEAR-specific drop on the target phrase
because it is already at ~0% under AGREE (0.0% → 0.1%, +0.1 points). There is no room
for the hypothesized "reluctance to publicly display" mechanism to manifest as a
*target-specific* drop when the baseline rate is already floored.

*Candidate explanation:* this run's AGREE/WEAR contrast is uninformative about A3 for
the target phrase specifically — not because the mechanism doesn't exist, but because
the target's overall unpopularity swamps it. A future revision that measures relative
odds rather than raw percentage-point shift (or conditions on distinguishing choices
among only the target and a matched low-frequency phrase) might have power the current
design lacks.

## H4 — The largest AGREE→WEAR shift lands on the attributed quote, not the target phrase

WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE (the RBG-attributed phrase) drops
22 points from AGREE to WEAR (55.8% → 33.8%) — the single largest shift of any phrase
in either direction. NOT HERE TO BE LIKED rises 12.2 points over the same contrast.
The AGREE×WEAR independence test is significant (chi2=243.9, p≈1.4e-51).

*Candidate explanation:* if a "social display" mechanism exists in this data at all, it
may be tracking recognizability/attribution of a phrase to a specific public figure or
position, rather than topic salience or policy specificity per se — a different
candidate mechanism from the one the target phrase was designed to isolate (§3.1's
attribution note flags this as untestable statistically with five items, but it is the
largest single effect in the primary analysis and is worth naming explicitly).

## H5 — Political self-description cleanly predicts the FREE SPEECH / WOMEN BELONG split

§5 (descriptive) shows liberal/progressive personas pick WOMEN BELONG ~85% of the time
and almost never FREE SPEECH (0–2%); conservative/moderate/apolitical personas invert
this (FREE SPEECH 58–97%, WOMEN BELONG 0–29%).

*Candidate explanation:* the model appears to be running a fairly literal
stereotype-consistent mapping from stated political self-description onto phrase
choice, with little of the more general uniformity/genericness pattern from H1
surviving once political self-description is conditioned on. This is descriptive only
(§5.3 item 5) and cannot be tested statistically with this design, but the size and
cleanliness of the split is worth naming before debrief text is read.

## H6 — Position (recency) effect is real but should not by itself explain phrase-level results

Last list position is selected far more often than first (26.5% vs. 12.5%,
chi2=187.7, p≈1.7e-39). Because phrase order is randomized independently per trial
(§5.2), this should average out across phrases at this sample size rather than
systematically inflate or deflate any one phrase's aggregate rate — but it is a
substantial effect and is recorded here so any phrase-level claim can be checked
against it if position and phrase identity turn out to be correlated in this
particular random draw.

---

## What to watch for in the debrief (§6), given these hypotheses

- Under H2: does reason-type distribution differ between... — not applicable, debrief
  is persona-trials only per `run_debrief.py`; instead compare reason types by framing
  and by political-orientation dimension once coded.
- Under H3/H4: since the target phrase is almost never chosen, debrief responses about
  *why it was passed over* (not named directly, per §6.2) are the main source of
  information about it at all — pay attention to whether it is spontaneously mentioned
  more under WEAR than AGREE/TAKE (the spontaneous-mention rate `mentions_p1` in
  `code_debrief.py`'s output), and whether the reasons given for it differ in shape from
  reasons given for other low-frequency phrases (PLANET BEFORE PROFITS, NOT HERE TO BE
  LIKED) or look the same (per §6.3's key comparison).
- Under H5: political-orientation-linked reasoning would be visible as
  disagreement-type codes clustering opposite the phrase the persona's political
  self-description predicts it *would* choose.
