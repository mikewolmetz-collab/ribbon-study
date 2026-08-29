# Agent instructions

You're an AI coding agent that's been pointed at this repo to run, replicate, or
extend the experiment. Here's everything you need, without reading the full design
doc first (though `ribbon-selection-study-design.md` has the complete rationale if
you want it).

## What this is

A test of whether AI personas replicate an anecdotal pattern from Andrea Bowers'
*Political Ribbons* installation at Glenstone (one specific ribbon, "WITHOUT BORDERS
– SIN FRONTERAS," almost never got taken by real visitors) — plus several follow-on
experiments digging into candidate explanations. Full writeup, if useful for context:
see `results/without-bodies-sin-cuerpos.md`.

This is fast, low-stakes, hypothesis-generating research, not a validated method. Say
so if you write anything up from it.

## Setup

- Python 3, stdlib only. `pip install scipy` is optional (gives exact p-values in
  `analyze_selection.py`; without it, chi-square statistics still print, just no
  p-value).
- Needs `ANTHROPIC_API_KEY`. Create a local `.env` file (already gitignored) with:
  ```
  export ANTHROPIC_API_KEY=sk-ant-...
  ```
  Then `set -a; source .env; set +a` before any command that calls the API.
  **Never commit `.env`, print its contents, or echo the key value in output.**

## Quick start (smoke test, ~15 API calls)

```bash
python3 src/generate_personas.py --n 6
set -a; source .env; set +a
python3 src/run_trials.py --replicates 1 --baseline-n 3 --framings AGREE,WEAR --workers 2
python3 src/analyze_selection.py
```
Check `data/trials.jsonl` for unparseable responses before scaling up.

## Full run (~3,300 API calls, a few dollars)

```bash
python3 src/generate_personas.py --n 240 --seed 20260822
set -a; source .env; set +a
python3 src/run_trials.py --replicates 5 --replicates-take 3 --baseline-n 200 --workers 8
python3 src/analyze_selection.py
# write results/prelocked_hypotheses.md BY HAND, from the distribution alone,
# before running any debrief step below — see "Ground rules"
python3 src/run_debrief.py --n 120
python3 src/code_debrief.py --sample     # read output, revise CATEGORIES if needed
python3 src/code_debrief.py
```

All `run_*` scripts are resumable — completed `trial_id`s are read back from the
output file and skipped, so re-running the same command after an interruption or
rate limit just picks up where it left off.

## Repo layout

| Path | What's there |
|---|---|
| `src/generate_personas.py` | Samples 240 synthetic visitor personas (no API calls) |
| `src/run_trials.py` | The main trial runner — takes `--phrases` and `--personas` overrides |
| `src/analyze_selection.py` | Locked pre-debrief analysis → `results/selection_analysis.md` |
| `src/run_debrief.py`, `src/code_debrief.py` | The design's Section 6 debrief protocol |
| `src/interview_nonchoosers.py`, `src/debrief_choosers.py`, `src/interview_noone_choosers.py` | Ad hoc, targeted follow-up interviews (continue a completed trial's conversation and ask a new question) |
| `src/analyze_phrase_variants.py` | Compares take rate across reworded ribbon variants |
| `stimuli/phrases.csv` | The five base ribbon phrases + attribute coding |
| `stimuli/variants/*.csv` | Alternate phrase-set CSVs, same format, swap one phrase and keep the rest constant |
| `data/*.jsonl` | Raw trial/interview records — every prompt and raw model response, never summarized-only |
| `results/*.md` | Generated analyses and the blog writeup |

## Extending this

Ideas that fit the existing pattern, roughly in order of effort:

- **New phrase variant:** copy `stimuli/variants/phrases_noone_illegal.csv`, swap in a
  different wording for the phrase you want to test, run `run_trials.py --phrases
  <your-file> --out data/<new-name>.jsonl --replicates 1 --baseline-n 0`.
- **New persona dimension:** add a key to `DIMS` in `generate_personas.py` and to the
  `TEMPLATE` string; regenerate personas with a new `--seed` if you want a fresh draw.
- **Targeted interview:** write a script like `interview_nonchoosers.py` — load
  completed trials, filter to the ones you care about, continue each trial's
  conversation (`prompt` as user turn, `raw` as assistant turn, your new question as
  the next user turn) via `run_trials.call(...)`.
- **A different artwork or choice entirely:** the harness only assumes "N phrases,
  shown in random order, forced single choice, optional persona." Swap
  `stimuli/phrases.csv` for a different stimulus set and everything downstream still
  works.

## Ground rules

- **Never commit `.env`, print the API key, or include it in any output file.**
- If you run a debrief-style follow-up (asking the model to explain a choice), keep
  the discipline from the design doc's Section 6: write down what you expect *before*
  reading the debrief text, and report debrief output as "text the model generates
  when asked," never as evidence about why a choice actually happened. This
  distinction is the whole point of the project — don't blur it for a cleaner-sounding
  writeup.
- Small, cheap follow-up experiments (a few hundred calls) are fine to run without
  asking. A full rerun of the entire study, or anything that would run up a real bill,
  is worth flagging to whoever you're working with first.
