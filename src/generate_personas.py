"""Generate Glenstone-visitor personas by sampling a fixed dimension space.

Deliberately NOT model-generated: freehand generation collapses toward a modal
art-museum visitor. Sampling keeps the distribution a recorded design choice.
"""
import itertools, json, random, argparse, os

DIMS = {
    "age_band": ["early 20s", "early 30s", "mid 40s", "late 50s", "late 60s"],
    "occupation": [
        "a public school teacher", "a federal contractor", "a nurse",
        "a small business owner", "a graduate student", "a retired engineer",
        "a software developer", "a nonprofit program officer",
    ],
    "art_familiarity": [
        "You visit contemporary art museums often and follow the field closely.",
        "You go to museums a few times a year and enjoy them without following art news.",
        "You rarely visit art museums and are not sure what to expect from contemporary work.",
    ],
    "visit_reason": [
        "You came mainly for the art.",
        "You came mainly for the grounds and the architecture.",
        "You came because someone else wanted to go and you came along.",
        "You are visiting the area and this was on a list of things to see.",
    ],
    "politics": [
        "You describe yourself as politically liberal.",
        "You describe yourself as politically conservative.",
        "You describe yourself as politically moderate.",
        "You describe yourself as not very political.",
        "You describe yourself as politically progressive and active.",
    ],
    "locality": [
        "You live nearby in Montgomery County.",
        "You live in DC.",
        "You drove in from elsewhere in the region.",
        "You are from out of state.",
    ],
    "company": [
        "You are visiting alone.",
        "You are visiting with your partner.",
        "You are visiting with family, including a teenager.",
        "You are visiting with two friends.",
    ],
}

TEMPLATE = (
    "You are {age}, {occ}. {locality} {company} {reason} {fam} {pol}"
)


def build(sample):
    return TEMPLATE.format(
        age=sample["age_band"], occ=sample["occupation"],
        locality=sample["locality"], company=sample["company"],
        reason=sample["visit_reason"], fam=sample["art_familiarity"],
        pol=sample["politics"],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=240)
    ap.add_argument("--seed", type=int, default=20260822)
    ap.add_argument("--out", default="stimuli/personas.jsonl")
    a = ap.parse_args()

    rng = random.Random(a.seed)
    seen, rows = set(), []
    while len(rows) < a.n:
        s = {k: rng.choice(v) for k, v in DIMS.items()}
        key = tuple(sorted(s.items()))
        if key in seen:
            continue
        seen.add(key)
        rows.append({"persona_id": f"P{len(rows):04d}", "dims": s, "text": build(s)})

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} personas to {a.out}")


if __name__ == "__main__":
    main()
