"""Debrief a subset of trials. Gated on results/prelocked_hypotheses.md existing.

The gate is deliberate: hypotheses generated from the selection distribution
must be recorded before any model-generated explanation is read, so the two
sources stay distinguishable.

The prompt never names the target phrase. Spontaneous mention rate is a measure.
"""
import json, os, random, argparse, threading
from concurrent.futures import ThreadPoolExecutor
import run_trials as rt

GATE = "results/prelocked_hypotheses.md"

DEBRIEF = ("You passed over the other ribbons. Pick two or three you considered "
           "and did not take, and say what led you to leave each one.")

_lock = threading.Lock()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", default="data/trials.jsonl")
    ap.add_argument("--out", default="data/debrief.jsonl")
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=20260822)
    ap.add_argument("--force", action="store_true",
                    help="bypass the pre-lock gate (records the bypass)")
    a = ap.parse_args()

    if not os.path.exists(GATE) and not a.force:
        raise SystemExit(
            f"{GATE} not found.\n"
            "Run analyze_selection.py, write your candidate hypotheses from the\n"
            "distribution alone into that file, then re-run. Use --force only if\n"
            "you are deliberately abandoning the pre-lock design."
        )

    trials = [json.loads(l) for l in open(a.trials) if json.loads(l).get("choice")]
    pers = [t for t in trials if t["persona_id"]]

    # stratify across framing so all three are represented
    rng = random.Random(a.seed)
    by_f = {}
    for t in pers:
        by_f.setdefault(t["framing"], []).append(t)
    per_f = max(1, a.n // max(1, len(by_f)))
    picked = []
    for f, ts in by_f.items():
        rng.shuffle(ts)
        picked += ts[:per_f]

    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try:
                done.add(json.loads(l)["trial_id"])
            except Exception:
                pass
    picked = [t for t in picked if t["trial_id"] not in done]
    print(f"{len(picked)} debriefs to run")

    fh = open(a.out, "a")

    def work(t):
        msgs = [{"role": "user", "content": t["prompt"]},
                {"role": "assistant", "content": t["raw"]},
                {"role": "user", "content": DEBRIEF}]
        try:
            raw = rt.call(t["model"], msgs, t["temperature"], max_tokens=700)
            err = None
        except Exception as e:
            raw, err = "", repr(e)
        rec = {"trial_id": t["trial_id"], "framing": t["framing"],
               "persona_id": t["persona_id"], "persona_dims": t["persona_dims"],
               "choice": t["choice"], "debrief_raw": raw, "error": err,
               "mentions_p1": ("SIN FRONTERAS" in raw.upper()
                               or "WITHOUT BORDERS" in raw.upper())}
        with _lock:
            fh.write(json.dumps(rec) + "\n")
            fh.flush()

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(work, picked))
    fh.close()
    print("done")


if __name__ == "__main__":
    main()
