"""Run ribbon-selection trials against the Anthropic API.

Resumable: completed trial_ids are read from data/trials.jsonl and skipped.
Raw model output is always preserved.
"""
import csv, json, os, random, argparse, threading, urllib.request, urllib.error, time
from concurrent.futures import ThreadPoolExecutor

API = "https://api.anthropic.com/v1/messages"
KEY = os.environ.get("ANTHROPIC_API_KEY")

FRAMING = {
    "AGREE": ("Which of these phrases do you most agree with?"),
    "TAKE": ("You may take one ribbon home to keep. Which do you take?"),
    "WEAR": ("You may take one ribbon and wear it around your neck for the "
             "rest of your visit, where other visitors will see it. "
             "Which do you take?"),
}

PREAMBLE = (
    "You are at Glenstone Museum in Potomac, Maryland, looking at an artwork "
    "by Andrea Bowers. Satin ribbons are hanging on a rack, each printed with "
    "a phrase. A label invites visitors to take one.\n\n"
    "The ribbons available are:\n{options}\n\n{question}\n\n"
    "Reply with the exact text of the one ribbon, and nothing else."
)

_lock = threading.Lock()


def call(model, messages, temperature, max_tokens=200, retries=5):
    body = json.dumps({"model": model, "max_tokens": max_tokens,
                       "temperature": temperature, "messages": messages}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "content-type": "application/json",
        "x-api-key": KEY,
        "anthropic-version": "2023-06-01",
    })
    for i in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read())
            return "".join(b.get("text", "") for b in d.get("content", []))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and i < retries - 1:
                time.sleep(2 ** i + random.random())
                continue
            raise
        except Exception:
            if i < retries - 1:
                time.sleep(2 ** i)
                continue
            raise


def parse_choice(text, phrases):
    """Match against known phrases. Normalized, longest-first to avoid
    substring collisions. Returns None if unparseable."""
    norm = lambda s: " ".join(
        "".join(c for c in s.upper() if c.isalnum() or c.isspace()).split())
    t = norm(text)
    hits = [p for p in sorted(phrases, key=lambda x: -len(x["text"]))
            if norm(p["text"]) in t]
    if len(hits) == 1:
        return hits[0]["id"]
    # fall back: try Spanish/English halves of the bilingual item separately
    if not hits:
        for p in phrases:
            for part in p["text"].split("–"):
                if part.strip() and norm(part) in t:
                    return p["id"]
    # more than one full phrase mentioned (e.g. reasoning despite the
    # "reply with nothing else" instruction) is ambiguous, not resolvable
    # by picking the longest match -- record as unparseable
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phrases", default="stimuli/phrases.csv")
    ap.add_argument("--personas", default="stimuli/personas.jsonl")
    ap.add_argument("--out", default="data/trials.jsonl")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--replicates", type=int, default=5,
                    help="replicates per persona-framing cell for AGREE and WEAR "
                         "(the primary manipulation; see design §5.1)")
    ap.add_argument("--replicates-take", type=int, default=3,
                    help="replicates per persona for TAKE, the reference "
                         "condition; kept lower than --replicates (but still "
                         "within the design's 3-5 floor) per design §5.1 "
                         "('prioritize samples ... in AGREE and WEAR over breadth "
                         "in TAKE')")
    ap.add_argument("--baseline-n", type=int, default=200)
    ap.add_argument("--framings", default="AGREE,TAKE,WEAR")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=20260822)
    a = ap.parse_args()

    if not KEY:
        raise SystemExit("Set ANTHROPIC_API_KEY")

    phrases = list(csv.DictReader(open(a.phrases)))
    personas = [json.loads(l) for l in open(a.personas)]
    framings = a.framings.split(",")

    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try:
                done.add(json.loads(l)["trial_id"])
            except Exception:
                pass

    reps_for = lambda f: a.replicates_take if f == "TAKE" else a.replicates

    jobs = []
    for f in framings:
        for p in personas:
            for r in range(reps_for(f)):
                jobs.append((f"{p['persona_id']}|{f}|{r}", p, f, r))
        for r in range(a.baseline_n // len(framings)):
            jobs.append((f"BASE|{f}|{r}", None, f, r))
    jobs = [j for j in jobs if j[0] not in done]
    print(f"{len(jobs)} trials to run ({len(done)} already done)")

    fh = open(a.out, "a")
    rng_master = random.Random(a.seed)
    seeds = {j[0]: rng_master.randrange(1 << 30) for j in jobs}

    def work(job):
        tid, persona, framing, rep = job
        rng = random.Random(seeds[tid])
        order = phrases[:]
        rng.shuffle(order)
        opts = "\n".join(f"- {p['text']}" for p in order)
        prompt = PREAMBLE.format(options=opts, question=FRAMING[framing])
        if persona:
            prompt = persona["text"] + "\n\n" + prompt
        msgs = [{"role": "user", "content": prompt}]
        try:
            raw = call(a.model, msgs, a.temperature)
        except Exception as e:
            raw, err = "", repr(e)
        else:
            err = None
        rec = {
            "trial_id": tid, "framing": framing, "replicate": rep,
            "persona_id": persona["persona_id"] if persona else None,
            "persona_dims": persona["dims"] if persona else None,
            "persona_text": persona["text"] if persona else None,
            "order": [p["id"] for p in order],
            "position": {p["id"]: i for i, p in enumerate(order)},
            "prompt": prompt, "raw": raw, "error": err,
            "choice": parse_choice(raw, phrases) if raw else None,
            "model": a.model, "temperature": a.temperature,
        }
        with _lock:
            fh.write(json.dumps(rec) + "\n")
            fh.flush()

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(work, jobs))
    fh.close()
    print("done")


if __name__ == "__main__":
    main()
