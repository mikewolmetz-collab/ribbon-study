"""Code debrief text into reason types and analyze the DISTRIBUTION of types.

Two stages:
  --sample   dump 20 responses for you to read and revise the category list
  (default)  code all responses, then write results/debrief_analysis.md

Individual explanations are not evidence of mechanism. The analysis reports
type distributions and, critically, whether reasons given for passing over the
target phrase differ structurally from reasons given for the other four.
"""
import json, csv, argparse, collections, threading, datetime
from concurrent.futures import ThreadPoolExecutor
import run_trials as rt

CATEGORIES = [
    "personal_relevance", "disagreement", "too_abstract", "too_specific",
    "aesthetic", "social_discomfort", "redundant_with_choice", "no_clear_reason",
]

CODER_PROMPT = """You are coding text for a research study. Below is a response \
in which someone explains why they passed over certain ribbons at an art \
installation.

The ribbons are:
{phrases}

Categories:
{cats}

For each ribbon the person discusses passing over, assign one category. Reply \
with ONLY a JSON array, no other text, in the form:
[{{"phrase_id": "p3", "category": "too_abstract"}}, ...]

Use phrase_id values from this mapping: {mapping}

Response to code:
---
{text}
---"""

_lock = threading.Lock()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--debrief", default="data/debrief.jsonl")
    ap.add_argument("--phrases", default="stimuli/phrases.csv")
    ap.add_argument("--out", default="data/coded.jsonl")
    ap.add_argument("--report", default="results/debrief_analysis.md")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    phrases = list(csv.DictReader(open(a.phrases)))
    label = {p["id"]: p["text"] for p in phrases}
    recs = [json.loads(l) for l in open(a.debrief) if json.loads(l).get("debrief_raw")]

    if a.sample:
        print("=== First 20 responses. Read these and revise CATEGORIES before coding. ===\n")
        for r in recs[:20]:
            print(f"[{r['trial_id']} | {r['framing']} | chose {label[r['choice']]}]")
            print(r["debrief_raw"][:900], "\n" + "-" * 70)
        return

    pmap = {p["id"]: p["text"] for p in phrases}
    fh = open(a.out, "w")

    def work(r):
        prompt = CODER_PROMPT.format(
            phrases="\n".join(f"- {p['text']}" for p in phrases),
            cats="\n".join(f"- {c}" for c in CATEGORIES),
            mapping=json.dumps(pmap), text=r["debrief_raw"])
        try:
            raw = rt.call(a.model, [{"role": "user", "content": prompt}], 0.0, 600)
            codes = json.loads(raw[raw.find("["):raw.rfind("]") + 1])
        except Exception as e:
            codes, raw = [], repr(e)
        out = dict(r)
        out["codes"], out["coder_raw"] = codes, raw
        with _lock:
            fh.write(json.dumps(out) + "\n")
            fh.flush()

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        list(ex.map(work, recs))
    fh.close()

    coded = [json.loads(l) for l in open(a.out)]

    # reason-type distribution per passed-over phrase
    grid = collections.defaultdict(collections.Counter)
    for r in coded:
        for c in r.get("codes", []):
            if c.get("phrase_id") in label and c.get("category") in CATEGORIES:
                grid[c["phrase_id"]][c["category"]] += 1

    L = ["# Debrief Analysis",
         f"\nGenerated {datetime.datetime.now().isoformat(timespec='seconds')}",
         "\n**These are categories of text the model generates when asked, not "
         "reports of why choices occurred.** No claim below should be phrased "
         "as a statement about the model's actual decision process, and none "
         "bears on real visitor behavior.\n",
         f"\nDebriefs coded: {len(coded)}",
         f"\nSpontaneous mention of the target phrase: "
         f"{sum(r.get('mentions_p1') for r in coded)}/{len(coded)} "
         f"({100*sum(r.get('mentions_p1') for r in coded)/max(1,len(coded)):.0f}%)\n",
         "\n## Reason types by passed-over phrase (row %)\n",
         "The key comparison is whether the target phrase's row differs in shape "
         "from the others. If every row looks alike, the explanation generator "
         "is not tracking anything phrase-specific.\n"]

    hdr = ["phrase", "n"] + CATEGORIES
    L.append("| " + " | ".join(hdr) + " |")
    L.append("|" + "|".join("---" for _ in hdr) + "|")
    for i in [p["id"] for p in phrases]:
        row, n = grid[i], sum(grid[i].values())
        L.append("| " + " | ".join(
            [label[i][:30], str(n)] +
            [f"{100*row.get(c,0)/n:.0f}" if n else "-" for c in CATEGORIES]) + " |")

    # social_discomfort by framing -- ties back to the AGREE/WEAR manipulation
    L.append("\n## social_discomfort rate by framing\n")
    L.append("| framing | codes | social_discomfort % |")
    L.append("|---|---|---|")
    for f in ["AGREE", "TAKE", "WEAR"]:
        cs = [c for r in coded if r["framing"] == f for c in r.get("codes", [])]
        n = len(cs)
        d = sum(c.get("category") == "social_discomfort" for c in cs)
        L.append(f"| {f} | {n} | {100*d/n:.0f} |" if n else f"| {f} | 0 | - |")

    open(a.report, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out} and {a.report}")


if __name__ == "__main__":
    main()
