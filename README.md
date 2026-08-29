# Ribbon Selection Study — harness

Implements the design in `ribbon-selection-study-design.md`.

Andrea Bowers' *Political Ribbons* at Glenstone lets visitors take a printed political
ribbon home. A gallery guide mentioned that one ribbon — "WITHOUT BORDERS – SIN
FRONTERAS" — almost never got taken. This project tests whether that same pattern
shows up when AI personas, standing in for museum visitors, are given the same choice
— and digs into a few candidate explanations for why, including a follow-on experiment
with reworded versions of the ribbon (`src/interview_nonchoosers.py`,
`src/debrief_choosers.py`, `analyze_phrase_variants.py`, `stimuli/variants/`).

This is a fast, low-stakes exploration — not a rigorous study — meant to generate
hypotheses, not validate a method. Everything here is meant to be replicated or
extended; the full harness, stimuli, and raw trial data (every prompt, every raw
model response) are included.

## Related, more rigorous work

This is loosely related to my day job: I manage the Frontier Intelligent Systems
program at the Johns Hopkins University Applied Physics Laboratory (JHU/APL), where
colleagues and I work on more rigorous methods for using AI as a behavioral stand-in
for humans. Two relevant papers, for anyone who wants the academic version of this idea:

- Ogg, M., Bose, R., Scharf, J., Ratto, C.R., & Wolmetz, M. (2026). *A flexible
  behavioral method for measuring human and artificial intelligence alignment using
  representational similarity analysis.* iScience, 29, 116400.
  https://doi.org/10.1016/j.isci.2026.116400
- Bose, R., Ogg, M., Wolmetz, M., & Ratto, C. (2024). *Assessing Behavioral Alignment
  of Personality-Driven Generative Agents in Social Dilemma Games.* NeurIPS 2024
  Workshop on Behavioral Machine Learning.
  https://openreview.net/forum?id=WCa25ExtbJ

## Setup
```bash
export ANTHROPIC_API_KEY=sk-...
cd ribbon-study
```
Optional: `pip install scipy` for exact p-values. Everything else is stdlib.

## Run order

```bash
# 1. personas (no API calls; deterministic given --seed)
python src/generate_personas.py --n 240 --seed 20260822

# 2. trials — AGREE/WEAR are the primary manipulation and get more replicates
#    per persona than TAKE (design §5.1): 240 personas x (5 + 5 + 3 reps)
#    + 200 baseline ≈ 3320 calls
python src/run_trials.py --replicates 5 --replicates-take 3 --baseline-n 200 --workers 8
# resumable: re-run the same command to pick up after a failure

# 3. locked analysis
python src/analyze_selection.py
# -> results/selection_analysis.md

# 4. WRITE results/prelocked_hypotheses.md BY HAND, from the distribution alone.
#    run_debrief.py refuses to run until this file exists.

# 5. debrief a subset
python src/run_debrief.py --n 120

# 6. inspect responses, revise CATEGORIES in code_debrief.py, then code
python src/code_debrief.py --sample
python src/code_debrief.py
# -> results/debrief_analysis.md
```

## Smoke test first
```bash
python src/generate_personas.py --n 6
python src/run_trials.py --replicates 1 --baseline-n 3 --framings AGREE,WEAR --workers 2
python src/analyze_selection.py
```
Check `data/trials.jsonl` for unparseable responses before scaling up.

## Notes
- Every trial stores its full prompt, raw output, and randomized phrase order.
- Phrase order is randomized per trial; position effects are checked in §4 of the analysis.
- The debrief prompt never names the target phrase. Spontaneous mention rate is recorded.
- The pre-lock gate on step 4 is enforced in code, not by intention. `--force` bypasses it and is recorded as a deliberate abandonment of the design.
