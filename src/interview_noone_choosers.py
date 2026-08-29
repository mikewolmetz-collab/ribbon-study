"""Ask every trial that chose NO ONE IS ILLEGAL (in the phrase-variant follow-on)
why they chose it, and whether they'd trade it for the original WITHOUT BORDERS -
SIN FRONTERAS ribbon.

Exploratory, post-hoc. Same interpretive caution as every other debrief step in this
project: text the model generates when asked, not introspective access to why the
original sampling landed there.
"""
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import run_trials as rt

QUESTION = (
    "What led you to choose that one? Separately: if you could trade it for a "
    "ribbon reading \"WITHOUT BORDERS – SIN FRONTERAS\" instead, would you? "
    "Why or why not?"
)

_lock = threading.Lock()


def main():
    trials = [json.loads(l) for l in open("data/trials_variant_noone.jsonl")]
    chosen = [t for t in trials if t.get("choice") == "p1"]
    print(f"{len(chosen)} trials to interview")

    fh = open("data/noone_chooser_interview.jsonl", "w")

    def work(t):
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
        with _lock:
            fh.write(json.dumps(rec) + "\n")
            fh.flush()

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, chosen))
    fh.close()
    print("wrote data/noone_chooser_interview.jsonl")


if __name__ == "__main__":
    main()
