"""Phase 1 (exploratory interview): ask a small, stratified sample of trials that did
NOT choose WITHOUT BORDERS - SIN FRONTERAS whether they considered it and why they
did or didn't take it.

Distinct from the design's Sec 6 debrief protocol: this names the target phrase
directly and gives explicit study context, trading contamination-avoidance for depth.
Sample: 5 trials per framing (AGREE/TAKE/WEAR), one from each of the 5 political-
self-description buckets per framing, so we're not just hearing from one slice of the
persona space. Read the output, pull out real categories, before designing any
closed-form Phase 2 survey.
"""
import json
import random
import run_trials as rt

QUESTION = (
    "We're trying to understand why people choose the ribbons they do. WITHOUT "
    "BORDERS – SIN FRONTERAS is rarely chosen. Did you consider choosing it? "
    "If not, why not? If so, why didn't you take it?"
)

POLITICS_BUCKETS = [
    "You describe yourself as politically liberal.",
    "You describe yourself as politically conservative.",
    "You describe yourself as politically moderate.",
    "You describe yourself as not very political.",
    "You describe yourself as politically progressive and active.",
]

SEED = 20260823


def main():
    trials = [json.loads(l) for l in open("data/trials.jsonl")]
    pool = [t for t in trials
            if t.get("choice") and t.get("choice") != "p1" and t.get("persona_id")]

    rng = random.Random(SEED)
    by_cell = {}
    for t in pool:
        key = (t["framing"], t["persona_dims"]["politics"])
        by_cell.setdefault(key, []).append(t)

    sample = []
    for framing in ["AGREE", "TAKE", "WEAR"]:
        for pol in POLITICS_BUCKETS:
            cell = by_cell.get((framing, pol), [])
            if not cell:
                print(f"WARNING: no trials for {framing} / {pol}")
                continue
            sample.append(rng.choice(cell))

    print(f"{len(sample)} trials sampled\n")

    out = []
    for t in sample:
        msgs = [
            {"role": "user", "content": t["prompt"]},
            {"role": "assistant", "content": t["raw"]},
            {"role": "user", "content": QUESTION},
        ]
        raw = rt.call(t["model"], msgs, t["temperature"], max_tokens=500)
        rec = {
            "trial_id": t["trial_id"], "framing": t["framing"],
            "persona_id": t["persona_id"], "persona_dims": t["persona_dims"],
            "chose": t["choice"], "question": QUESTION, "response": raw,
        }
        out.append(rec)
        pol_short = t["persona_dims"]["politics"].replace(
            "You describe yourself as ", "").rstrip(".")
        print(f"=== {t['trial_id']} | {t['framing']} | {pol_short} | "
              f"chose {t['choice']} ===")
        print(raw)
        print()

    with open("data/nonchooser_interview.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    print("wrote data/nonchooser_interview.jsonl")


if __name__ == "__main__":
    main()
