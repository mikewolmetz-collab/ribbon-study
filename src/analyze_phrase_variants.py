"""Compare take rate of four immigration-phrase variants, holding the other four
phrases constant. Group 1 (WITHOUT BORDERS - SIN FRONTERAS) is pulled from the main
study's data/trials.jsonl rather than re-collected -- same persona set, same framings,
just a larger sample (5/5/3 replicates vs. 1 for the new groups). Selection rate is a
percentage, so comparing across groups of different size is valid; Group 1 simply has
tighter precision.

Exploratory, post-hoc: not part of the locked pre-debrief analysis.
"""
import json, csv, argparse, collections, math

try:
    from scipy.stats import chi2_contingency
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

GROUPS = [
    ("WITHOUT BORDERS – SIN FRONTERAS", "extreme", "data/trials.jsonl", None),
    ("NO ONE IS ILLEGAL", "extreme-leaning", "data/trials_variant_noone.jsonl",
     "stimuli/variants/phrases_noone_illegal.csv"),
    ("WE ARE A NATION OF IMMIGRANTS", "moderate", "data/trials_variant_nation.jsonl",
     "stimuli/variants/phrases_nation_of_immigrants.csv"),
    ("IMMIGRANTS MAKE AMERICA STRONGER", "reasonable",
     "data/trials_variant_stronger.jsonl",
     "stimuli/variants/phrases_immigrants_stronger.csv"),
]


def pct(c, n):
    return 100.0 * c / n if n else 0.0


def table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def load(path):
    return [json.loads(l) for l in open(path)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/phrase_variant_analysis.md")
    a = ap.parse_args()

    L = ["# Immigration Phrase Variants — Take-Rate Comparison",
         "",
         "Exploratory, post-hoc follow-on. Same four base phrases (NOT HERE TO BE "
         "LIKED, PLANET BEFORE PROFITS, FREE SPEECH MAKES FREE PEOPLE, WOMEN "
         "BELONG...) held constant across all four groups; only the immigration "
         "phrase changes. Group 1 is the original study's data (larger n, more "
         "replicates); groups 2-4 are new, matched-persona, 1-replicate runs.",
         ""]

    overall_rows = []
    by_framing = {}

    for label, tier, path, _ in GROUPS:
        trials = load(path)
        pers = [t for t in trials if t.get("choice") and t.get("persona_id")]
        n = len(pers)
        p1_n = sum(1 for t in pers if t["choice"] == "p1")
        overall_rows.append([label, tier, n, p1_n, f"{pct(p1_n, n):.2f}%"])

        for f in ["AGREE", "TAKE", "WEAR"]:
            sub = [t for t in pers if t["framing"] == f]
            c = sum(1 for t in sub if t["choice"] == "p1")
            by_framing.setdefault(f, []).append(
                [label, tier, len(sub), c, f"{pct(c, len(sub)):.2f}%"])

    L.append("## Overall take rate of the immigration phrase, by variant\n")
    L.append(table(["phrase", "tier", "n", "chosen", "%"], overall_rows))

    for f in ["AGREE", "TAKE", "WEAR"]:
        L.append(f"\n## {f}\n")
        L.append(table(["phrase", "tier", "n", "chosen", "%"], by_framing[f]))

    # chi-square: does variant identity predict choosing the immigration phrase vs not
    if HAVE_SCIPY:
        tab = []
        for label, tier, path, _ in GROUPS:
            trials = load(path)
            pers = [t for t in trials if t.get("choice") and t.get("persona_id")]
            n = len(pers)
            p1_n = sum(1 for t in pers if t["choice"] == "p1")
            tab.append([p1_n, n - p1_n])
        try:
            chi2, p, _, _ = chi2_contingency(tab)
            L.append(f"\nVariant x (chose immigration phrase / did not): "
                     f"chi2={chi2:.1f}, p={p:.2g}")
        except ValueError:
            L.append("\nVariant independence test: not computed (a cell is zero)")

    open(a.out, "w").write("\n".join(L) + "\n")
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
