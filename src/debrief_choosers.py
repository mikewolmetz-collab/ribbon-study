"""Targeted, exploratory follow-up: ask the four trials that chose SIN FRONTERAS
why they chose it.

Not part of the design's Sec 6 debrief protocol (which asks only about passed-over
ribbons, across a large stratified sample, and deliberately never names the target
phrase). This is a distinct, much smaller question: of the four trials that DID choose
WITHOUT BORDERS - SIN FRONTERAS, what does the model say when asked why, continuing
each trial's own conversation. No contamination concern here since we're asking about
a choice the model actually made, not suggesting one it didn't make.

Same interpretive caution as the main debrief applies: this is text the model generates
when asked, not introspective access to why the sampling actually landed there.
"""
import json
import run_trials as rt

QUESTION = "What led you to choose that one over the others?"


def main():
    trials = [json.loads(l) for l in open("data/trials.jsonl")]
    chosen = [t for t in trials if t.get("choice") == "p1"]
    print(f"{len(chosen)} trials chose WITHOUT BORDERS - SIN FRONTERAS\n")

    out = []
    for t in chosen:
        msgs = [
            {"role": "user", "content": t["prompt"]},
            {"role": "assistant", "content": t["raw"]},
            {"role": "user", "content": QUESTION},
        ]
        raw = rt.call(t["model"], msgs, t["temperature"], max_tokens=500)
        rec = {
            "trial_id": t["trial_id"], "framing": t["framing"],
            "persona_id": t["persona_id"], "persona_dims": t["persona_dims"],
            "question": QUESTION, "response": raw,
        }
        out.append(rec)
        print(f"=== {t['trial_id']} ({t['framing']}, persona {t['persona_id']}) ===")
        print(raw)
        print()

    with open("data/chooser_debrief.jsonl", "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    print("wrote data/chooser_debrief.jsonl")


if __name__ == "__main__":
    main()
