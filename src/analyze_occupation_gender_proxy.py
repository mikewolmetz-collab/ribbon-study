"""Exploratory, post-hoc: occupation as a gender-stereotype proxy.

NOT part of the locked pre-debrief analysis (design Sec 5.3) -- personas were never
assigned a gender (see generate_personas.py DIMS and design Sec 4.1, which lists no
gender dimension). This script does not measure persona gender; it buckets the eight
sampled occupations by their real-world U.S. labor-force gender skew (approximate,
widely reported figures -- BLS-type composition stats, not exact citations) and asks
whether selection differs by that bucket.

This conflates gender-typicality with everything else that differs between occupations
(income, sector, caregiving vs. technical orientation, education field, etc.). A pattern
here is evidence about occupation-linked stereotype content in the model's responses,
not evidence about how it would respond to an explicitly-gendered persona. Report it
as such.
"""
import json, csv, argparse, collections, math, datetime

try:
    from scipy.stats import chi2_contingency
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

# Approximate U.S. labor-force gender composition by occupation, used only to bucket
# the eight sampled occupation strings. High-confidence assignments have well-known,
# large (>70/30) skews; anything closer to balanced, or spanning too many actual roles
# to have one skew, is left "ambiguous" and excluded from the two-bucket comparison.
OCCUPATION_GENDER_LEAN = {
    "a nurse":                     ("female", "high",   "~85-90% female (RNs)"),
    "a public school teacher":     ("female", "high",   "~75-80% female (K-12 teachers)"),
    "a nonprofit program officer": ("female", "medium", "~65-70% female (nonprofit sector workforce)"),
    "a software developer":        ("male",   "high",   "~75-80% male (software developers)"),
    "a retired engineer":          ("male",   "high",   "~80-85% male (engineers)"),
    "a federal contractor":        ("ambiguous", "low", "spans many fields; no single occupational skew"),
    "a small business owner":      ("ambiguous", "low", "~60/40 male/female-owned; weak skew, broad category"),
    "a graduate student":          ("ambiguous", "low", "field unspecified; roughly balanced nationally"),
}


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
    ap.add_argument("--out", default="results/occupation_gender_proxy_analysis.md")
    a = ap.parse_args()

    phrases = list(csv.DictReader(open(a.phrases)))
    pid = [p["id"] for p in phrases]
    label = {p["id"]: p["text"] for p in phrases}

    trials = [json.loads(l) for l in open(a.trials)]
    ok = [t for t in trials if t.get("choice") and t.get("persona_dims")]

    for t in ok:
        occ = t["persona_dims"]["occupation"]
        if occ not in OCCUPATION_GENDER_LEAN:
            raise SystemExit(f"unmapped occupation: {occ!r}")

    L = ["# Occupation-as-Gender-Proxy Analysis (exploratory, post-hoc)",
         f"\nGenerated {datetime.datetime.now().isoformat(timespec='seconds')}",
         "\n**Not part of the locked pre-debrief analysis.** Persona gender was never "
         "sampled (see `generate_personas.py`; design Sec 4.1 lists no gender "
         "dimension). This analysis buckets the eight occupation strings by their "
         "real-world labor-force gender skew and looks for a selection difference "
         "between buckets. Any effect found is evidence about occupation-linked "
         "content in the model's responses, confounded with everything else that "
         "differs between e.g. nurse and software-developer personas -- it is not "
         "evidence about how the model would respond to an explicitly-gendered "
         "persona.\n",
         f"\nPersona trials analyzed: {len(ok)}\n",
         "\n## Occupation -> stereotype-lean mapping used\n",
         table(["occupation", "lean", "confidence", "basis"],
               [[occ, lean, conf, basis]
                for occ, (lean, conf, basis) in OCCUPATION_GENDER_LEAN.items()]),
         "\n\n## 1. Selection frequency by occupation\n"]

    by_occ = collections.defaultdict(list)
    for t in ok:
        by_occ[t["persona_dims"]["occupation"]].append(t)

    hdr = ["occupation", "lean", "n"] + [label[i][:24] for i in pid]
    rows = []
    for occ, (lean, conf, basis) in OCCUPATION_GENDER_LEAN.items():
        sub = by_occ.get(occ, [])
        c = collections.Counter(t["choice"] for t in sub)
        rows.append([occ, lean, len(sub)] +
                    [f"{pct(c.get(i, 0), len(sub)):.0f}" if sub else "-" for i in pid])
    L.append(table(hdr, rows))

    L.append("\n## 2. Selection frequency by gender-lean bucket "
             "(ambiguous occupations excluded)\n")
    buckets = collections.defaultdict(list)
    for t in ok:
        lean = OCCUPATION_GENDER_LEAN[t["persona_dims"]["occupation"]][0]
        if lean != "ambiguous":
            buckets[lean].append(t)

    rows = []
    for lean in ("female", "male"):
        sub = buckets.get(lean, [])
        c = collections.Counter(t["choice"] for t in sub)
        rows.append([lean, len(sub)] +
                    [f"{pct(c.get(i, 0), len(sub)):.1f}" for i in pid])
    L.append(table(["lean", "n"] + [label[i][:24] for i in pid], rows))

    if HAVE_SCIPY and buckets.get("female") and buckets.get("male"):
        tab = [[sum(t["choice"] == i for t in buckets["female"]) for i in pid],
               [sum(t["choice"] == i for t in buckets["male"]) for i in pid]]
        try:
            chi2, p, _, _ = chi2_contingency(tab)
            L.append(f"\nfemale-lean x male-lean independence: chi2={chi2:.1f}, "
                     f"p={p:.2g}")
        except ValueError:
            L.append("\nfemale-lean x male-lean independence: not computed "
                     "(a phrase has zero selections across both buckets)")
    elif not HAVE_SCIPY:
        L.append("\n(install scipy for an independence test on the bucket table above)")

    L.append("\n\n## 3. Same breakdown, by framing\n")
    for f in ["AGREE", "TAKE", "WEAR"]:
        L.append(f"\n### {f}\n")
        rows = []
        for lean in ("female", "male"):
            sub = [t for t in buckets.get(lean, []) if t["framing"] == f]
            c = collections.Counter(t["choice"] for t in sub)
            rows.append([lean, len(sub)] +
                        [f"{pct(c.get(i, 0), len(sub)):.1f}" if sub else "-"
                         for i in pid])
        L.append(table(["lean", "n"] + [label[i][:24] for i in pid], rows))

    open(a.out, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
