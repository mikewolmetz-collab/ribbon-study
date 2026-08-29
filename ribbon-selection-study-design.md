# Ribbon Selection Study: Design Specification

**Status:** draft design, pre-implementation
**Revision:** 3 — harness implemented; ready to run
**Status of the phrase set:** the five phrases below are treated as the complete Glenstone set.
**Purpose:** specification for implementing and running the experiment. Intended as input to Claude Code.

---

## 1. Background

Andrea Bowers' *Political Ribbons (Glenstone)*, 2026, is a participatory installation. Silkscreened satin ribbons printed with short political phrases hang on racks near the gallery. Visitors are invited to take one home, and many wear the ribbon for the rest of the visit.

A gallery guide reported that the ribbon reading "WITHOUT BORDERS – SIN FRONTERAS" was taken far less often than the others, possibly to the point of being pulled from the display. There is no published data on per-phrase take rates and no documentation of visitor reception for this or other installations of the piece.

The anecdote is the motivating observation, not the object of study. This experiment cannot determine why real visitors behaved as they did. It can characterize how a language model conditioned on visitor-like personas distributes its choices across the same five phrases, and whether that distribution shifts under framings that correspond to candidate mechanisms.

## 2. Research questions

Two tracks, kept separate in analysis and in any writeup.

**Track A — model behavior (answerable here):**

- A1. When agents assigned Glenstone-visitor personas choose one ribbon, is the selection distribution uniform, or skewed by phrase?
- A2. Does the skew survive removal of the persona? How much of the pattern is persona-driven versus a property of the phrases themselves?
- A3. Does the distribution shift under a framing that makes public display salient, relative to one asking only about private agreement? This is the primary analysis.
- A4. When asked to explain a non-choice, what categories of reason does the model produce, and do those categories differ by phrase or only by persona?

**Track B — human behavior (not answerable here):**

- B1. Why did real Glenstone visitors leave that ribbon on the rack?

Track B is stated only to mark it out of scope. The most this study can produce for B1 is candidate hypotheses needing independent testing: a visitor survey, observational take-rate counts, or comparison across installations.

## 3. Stimuli

### 3.1 Phrase set

The full Glenstone set, confirmed from photographs of the installation:

1. WITHOUT BORDERS – SIN FRONTERAS  *(target phrase)*
2. NOT HERE TO BE LIKED
3. PLANET BEFORE PROFITS
4. FREE SPEECH MAKES FREE PEOPLE
5. WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE

Present all five in every trial. Preserve capitalization and the en-dash in the target phrase as shown; the bilingual formatting is part of the stimulus.

**Note on the target phrase:** it is bilingual and English-first. Language is therefore not a comprehension barrier — any visitor who could read the other ribbons could read this one. The Spanish half may still carry a marking effect, signaling alignment with a specific movement, but that is a different mechanism from access and should be described as such.

**Note on attribution:** phrase 5 is closely associated with Ruth Bader Ginsburg. Phrase 2 is associated with feminist and protest usage but is not a single attributed quote. Whether a phrase reads as a recognized quotation from a public figure may affect selection independently of topic, and should be recorded, though with five items it cannot be tested statistically.

### 3.2 Phrase attribute coding

Code before running, blind to results. With only five items these attributes **cannot support a regression** — they are a qualitative frame for interpreting which phrases cluster together, and a record of the design team's priors.

| Phrase | Topic | Specificity | Language | Attributed |
|---|---|---|---|---|
| WITHOUT BORDERS – SIN FRONTERAS | immigration | movement-identified | bilingual | no |
| NOT HERE TO BE LIKED | gender / general stance | general | English | loosely |
| PLANET BEFORE PROFITS | climate | general | English | no |
| FREE SPEECH MAKES FREE PEOPLE | civil liberties | general | English | no |
| WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE | gender | general | English | yes (RBG) |

Also record `char_length` and a 1–5 `abstractness` rating per phrase as surface controls.

The structure worth noting: four phrases are general value statements, three of which are close to consensus positions when stated abstractly. One names a live policy dispute in a form that reads as a position rather than a sentiment. The specificity contrast is therefore visible without a model fit.

## 4. Personas

### 4.1 Generation

Sample personas along dimensions that plausibly vary among Glenstone visitors. Glenstone is a free-admission contemporary art museum in Montgomery County, Maryland, drawing heavily from the DC metro area.

Dimensions: age band, occupation, art-world familiarity, reason for visiting (art interest, grounds and architecture, accompanying someone, tourism), political orientation (coarse self-description), local versus visitor, visiting alone versus with family versus with friends.

Target N: 200–300 personas. Generate programmatically by sampling the dimension space. Do not ask a model to freehand "a range of Glenstone visitors" — freehand generation collapses toward a modal art-museum visitor and toward stereotype.

**Limitation to record:** the persona set encodes assumptions about who visits Glenstone, not measured demographics. Results are conditional on that choice.

### 4.2 Persona representation

Each persona is a short second-person paragraph, consistent in length and structure across the set. Include no statement of opinion on immigration, climate, speech, or gender — that writes the answer into the prompt. Political orientation, where included, stays at the level of self-description, not a list of positions.

## 5. Design

### 5.1 Conditions

**Factor 1 — Persona:** persona-assigned vs. no-persona baseline.

**Factor 2 — Framing (3 levels):**

- `AGREE`: "Which of these phrases do you most agree with?"
- `TAKE`: "You may take one ribbon home to keep. Which do you take?"
- `WEAR`: "You may take one ribbon and wear it around your neck for the rest of your visit, where other visitors will see it. Which do you take?"

The AGREE/WEAR contrast is the primary manipulation. TAKE matches the actual installation and serves as the reference condition.

Because the attribute regression is not available with five items, the framing manipulation carries most of the design's inferential weight. Allocate sampling accordingly: prioritize samples per persona in AGREE and WEAR over breadth in TAKE.

### 5.2 Trial structure

Each trial: one persona (or none), one framing, all five phrases in randomized order, forced single choice. Record choice, randomized list position of each phrase, persona ID, framing, temperature, and raw model output.

Randomize order independently per trial. With five items, position effects are a live risk and would otherwise be indistinguishable from content effects.

Run at nonzero temperature and record it. Multiple samples per persona-framing cell; with five options and a 20% chance baseline, 3–5 samples per cell is a reasonable starting point.

### 5.3 Analysis, locked before debrief

Complete and record all of the following before reading any debrief output.

1. Selection frequency per phrase, per condition. Test against uniform (20% each). With five categories, chi-square is appropriate; report per-phrase residuals, not just the omnibus test.
2. Persona vs. no-persona comparison. If distributions are close, the skew is a phrase property rather than a simulated-visitor property, and every persona-based interpretation weakens.
3. **AGREE vs. WEAR shift, per phrase.** Primary analysis. Report the shift for all five phrases, not just the target. A target-specific drop under WEAR is the result of interest. A global flattening or sharpening means the framing changed choice strategy generally and says little about display cost specifically.
4. Position-effect check: selection rate as a function of randomized list position, collapsed across phrases.
5. Persona-dimension breakdown: selection rate by political orientation, age band, and visit reason. Descriptive only.

**Write down candidate hypotheses from these results alone and timestamp them before running Section 6.** The purpose is a record of which hypotheses came from the distribution and which came from the model's prose.

## 6. Debrief protocol

Run only after 5.3 is complete and recorded.

### 6.1 Sampling

Debrief 100–150 trials, sampled across the persona space and all framings. Observing the range of reason types does not require full N, and less generated prose means less anchoring on subsequent interpretation.

### 6.2 Prompt

Continue the original trial conversation. Ask about passed-over ribbons generally:

> You passed over the other ribbons. Pick two or three you considered and did not take, and say what led you to leave each one.

Do **not** name the target phrase. Naming it produces an explanation for a choice the agent may not have made on those grounds and contaminates the comparison. Record whether the target phrase is spontaneously mentioned; the spontaneous mention rate is itself a measure.

### 6.3 Coding

Code explanations into reason types. Develop categories from a first pass over 20 responses, then apply to the full set. Starting categories, to be revised on contact with the data: personal relevance, disagreement with the message, too abstract, too specific, aesthetic or color preference, social discomfort or unwillingness to display, redundancy with the chosen ribbon, no clear reason.

Analyze the **distribution of reason types**, not individual explanations. Key comparison: are reasons for passing over the target phrase structurally different from reasons for passing over the other four? If identical, the explanation generator is not tracking anything phrase-specific — that is a finding.

### 6.4 Interpretive stance

Debrief responses are text to categorize, not testimony. A model asked why it chose produces a plausible narrative fitted to the choice; there is no introspective access to the process that generated it. Every claim from debrief data must be phrased as a claim about what the model generates when asked, not about why the choice occurred.

## 7. Follow-up: mechanistic interpretability

Out of scope here, noted for planning.

If AGREE/WEAR produces a target-specific shift, the natural follow-up is to look for internal features related to social observation or public display, and test whether ablating or steering them changes the selection distribution. That speaks to A3 in a way neither the behavioral data nor the debrief can.

It still says nothing about B1.

## 8. Limitations to carry into any writeup

1. No ground truth. There are no measured take rates from Glenstone. The agent distribution cannot be validated against anything.
2. The persona set encodes assumptions about Glenstone visitors, not measurements.
3. Five items is too few for any model relating selection to phrase attributes. Attribute claims are interpretive, not tested.
4. The target phrase is confounded on topic, specificity, and bilingual marking simultaneously, and with one item per cell these cannot be separated.
5. Model agents have no body, no visual field, and no anticipation of being seen. The leading candidate mechanism for the real-world observation — reluctance to publicly display a position on a contested issue — is precisely what these agents are least able to represent. A null on A3 is weak evidence about anything; a positive result shows the model can represent the mechanism, not that it operated in the museum.
6. Results are conditional on the specific model, prompt wording, and temperature. Record all three.

## 9. Implementation

The harness is written and smoke-tested offline. It has not been run against the
API — no key was available in the authoring environment. All numbers below are
defaults, not results.

### 9.1 Structure

```
ribbon-study/
  README.md              # run order and smoke test
  config.yaml            # model, temperature, N, condition toggles
  stimuli/
    phrases.csv          # 5 phrases + attribute coding
    personas.jsonl       # generated by generate_personas.py
  src/
    generate_personas.py # samples the dimension space; no API calls
    run_trials.py        # trial runner + shared API call and choice parser
    analyze_selection.py # locked pre-debrief analysis
    run_debrief.py       # gated on prelocked_hypotheses.md
    code_debrief.py      # reason-type coding + distribution report
  data/
    trials.jsonl         # one record per trial, raw output preserved
    debrief.jsonl
    coded.jsonl
  results/
    selection_analysis.md
    prelocked_hypotheses.md   # written by hand before debrief
    debrief_analysis.md
```

Stdlib only. `scipy` is optional and used for exact p-values where present;
without it the chi-square statistics are still reported.

### 9.2 Run order

```bash
export ANTHROPIC_API_KEY=...

python src/generate_personas.py --n 240 --seed 20260822
python src/run_trials.py --replicates 3 --baseline-n 200 --workers 8
python src/analyze_selection.py
# write results/prelocked_hypotheses.md by hand, from the distribution alone
python src/run_debrief.py --n 120
python src/code_debrief.py --sample     # read, revise CATEGORIES
python src/code_debrief.py
```

Smoke test before scaling: `--n 6` personas, `--replicates 1`,
`--baseline-n 3`, `--framings AGREE,WEAR`. Inspect `data/trials.jsonl` for
unparseable responses before committing to the full run.

### 9.3 Defaults and cost

At the defaults, the full run is roughly 2,360 trial calls plus 120 debrief
calls plus 120 coding calls. A reduced first pass (100 personas, 1 replicate)
is about 500 calls and is enough to see whether the distribution departs from
uniform, at the cost of resolution on the AGREE/WEAR contrast.

Defaults: `claude-sonnet-4-6`, temperature 1.0, 240 personas, 3 replicates per
persona-framing cell, 200 no-persona baseline trials, seed 20260822.

### 9.4 Properties enforced in code

- Full prompt, raw output, and randomized phrase order stored per trial.
- Phrase order randomized independently per trial from a master-seeded RNG, so
  runs are reproducible.
- Runs are resumable: completed `trial_id`s are read back and skipped.
- Choices parsed by matching against the five known phrases, longest-first, with
  a fallback that matches either half of the bilingual target phrase alone.
  Unparseable responses are recorded, never discarded.
- `run_debrief.py` refuses to run until `results/prelocked_hypotheses.md`
  exists. `--force` bypasses the gate and is recorded as a deliberate
  abandonment of the pre-lock design.
- The debrief prompt never names the target phrase; spontaneous mention is
  recorded per response as its own measure.
- Personas are sampled programmatically rather than model-generated, and carry
  no stated opinion on any ribbon topic.

### 9.5 What to read first in the output

`results/selection_analysis.md` section 2, the persona vs. no-persona
comparison. If those columns are near-identical, the personas are not doing
work, the skew is a property of the phrases, and every persona-based reading of
the results weakens accordingly. Section 3, the AGREE/WEAR shift, is the primary
analysis and the only part of the design that can discriminate between
mechanisms rather than describe a distribution.

### 9.6 Open items

- Persona dimension space is a design choice, not a measurement. Revise if
  Glenstone visitor data becomes available.
- Reason-type categories in `code_debrief.py` are a starting list and are meant
  to be revised after reading the `--sample` output.
- Framing prompt wording should be frozen before the first full run and recorded
  with the results.
