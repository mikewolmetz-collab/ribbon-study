"""Pre-debrief analysis. Writes results/selection_analysis.md.

Covers items 1-5 of Section 5.3. Stdlib only; scipy used if available for
exact p-values, otherwise chi-square statistic is reported without one.
"""
import json, csv, argparse, collections, math, datetime

try:
    from scipy.stats import chisquare, chi2_contingency
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


def chisq_uniform(counts):
    n, k = sum(counts), len(counts)
    exp = n / k
    stat = sum((c - exp) ** 2 / exp for c in counts)
    p = None
    if HAVE_SCIPY and n:
        p = float(chisquare(counts).pvalue)
    return stat, p, [(c - exp) / math.sqrt(exp) for c in counts]


def pct(c, n):
    return 100.0 * c / n if n else 0.0


def table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", default="data/trials.jsonl")
    ap.add_argument("--phrases", default="stimuli/phrases.csv")
    ap.add_argument("--out", default="results/selection_analysis.md")
    a = ap.parse_args()

    phrases = list(csv.DictReader(open(a.phrases)))
    pid = [p["id"] for p in phrases]
    label = {p["id"]: p["text"] for p in phrases}

    trials = [json.loads(l) for l in open(a.trials)]
    ok = [t for t in trials if t.get("choice")]
    bad = [t for t in trials if not t.get("choice")]

    L = ["# Selection Analysis",
         f"\nGenerated {datetime.datetime.now().isoformat(timespec='seconds')}",
         f"\nTrials: {len(trials)} total, {len(ok)} parsed, {len(bad)} unparseable.",
         f"\nModel: {trials[0]['model']}, temperature {trials[0]['temperature']}."
         if trials else ""]

    # --- 1. distribution per framing, persona trials ---
    L.append("\n## 1. Selection frequency by framing (persona trials)\n")
    for f in ["AGREE", "TAKE", "WEAR"]:
        sub = [t for t in ok if t["framing"] == f and t["persona_id"]]
        if not sub:
            continue
        c = collections.Counter(t["choice"] for t in sub)
        counts = [c.get(i, 0) for i in pid]
        stat, p, resid = chisq_uniform(counts)
        L.append(f"\n**{f}** (n={len(sub)}) — chi2={stat:.1f}"
                 + (f", p={p:.2g}" if p is not None else " (install scipy for p)"))
        L.append("")
        L.append(table(["phrase", "n", "%", "std. residual"],
                       [[label[i], c.get(i, 0), f"{pct(c.get(i,0), len(sub)):.1f}",
                         f"{r:+.2f}"] for i, r in zip(pid, resid)]))

    # --- 2. persona vs baseline ---
    L.append("\n## 2. Persona vs. no-persona baseline\n")
    L.append("If these are close, the skew is a property of the phrases, not of "
             "simulated visitor variation, and persona-based interpretation weakens.\n")
    rows = []
    for i in pid:
        pers = [t for t in ok if t["persona_id"]]
        base = [t for t in ok if not t["persona_id"]]
        rows.append([label[i],
                     f"{pct(sum(t['choice']==i for t in pers), len(pers)):.1f}",
                     f"{pct(sum(t['choice']==i for t in base), len(base)):.1f}"])
    L.append(table(["phrase", "persona %", "baseline %"], rows))

    # --- 3. PRIMARY: AGREE vs WEAR ---
    L.append("\n## 3. PRIMARY ANALYSIS — AGREE vs. WEAR shift\n")
    L.append("Reported for all five phrases. A shift concentrated on one phrase "
             "is the result of interest; a global change means the framing "
             "altered choice strategy generally.\n")
    ag = [t for t in ok if t["framing"] == "AGREE" and t["persona_id"]]
    we = [t for t in ok if t["framing"] == "WEAR" and t["persona_id"]]
    rows = []
    for i in pid:
        a_pct = pct(sum(t["choice"] == i for t in ag), len(ag))
        w_pct = pct(sum(t["choice"] == i for t in we), len(we))
        rows.append([label[i], f"{a_pct:.1f}", f"{w_pct:.1f}", f"{w_pct-a_pct:+.1f}"])
    L.append(table(["phrase", "AGREE %", "WEAR %", "shift"], rows))
    if HAVE_SCIPY and ag and we:
        tab = [[sum(t["choice"] == i for t in ag) for i in pid],
               [sum(t["choice"] == i for t in we) for i in pid]]
        try:
            chi2, p, _, _ = chi2_contingency(tab)
            L.append(f"\nAGREE x WEAR independence: chi2={chi2:.1f}, p={p:.2g}")
        except ValueError:
            L.append("\nAGREE x WEAR independence: not computed (a phrase has "
                     "zero selections across both conditions -- likely a small "
                     "sample; re-check at full scale)")

    # --- 4. position effects ---
    L.append("\n## 4. Position-effect check\n")
    posc = collections.Counter(t["position"][t["choice"]] for t in ok)
    n = sum(posc.values())
    L.append(table(["list position", "n", "%"],
                   [[k, posc.get(k, 0), f"{pct(posc.get(k,0), n):.1f}"]
                    for k in range(len(pid))]))
    stat, p, _ = chisq_uniform([posc.get(k, 0) for k in range(len(pid))])
    L.append(f"\nchi2={stat:.1f}" + (f", p={p:.2g}" if p is not None else ""))

    # --- 5. persona dimension breakdown (descriptive) ---
    L.append("\n## 5. Selection by persona dimension (descriptive only)\n")
    for dim in ["politics", "age_band", "visit_reason", "art_familiarity"]:
        L.append(f"\n### {dim}\n")
        vals = sorted({t["persona_dims"][dim] for t in ok if t["persona_dims"]})
        rows = []
        for v in vals:
            sub = [t for t in ok if t["persona_dims"] and t["persona_dims"][dim] == v]
            rows.append([v[:52], len(sub)] +
                        [f"{pct(sum(t['choice']==i for t in sub), len(sub)):.0f}"
                         for i in pid])
        L.append(table(["value", "n"] + [label[i][:22] for i in pid], rows))

    if bad:
        L.append(f"\n## Unparseable responses ({len(bad)})\n")
        for t in bad[:10]:
            L.append(f"- `{t['trial_id']}`: {(t.get('raw') or t.get('error'))[:160]!r}")

    open(a.out, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
