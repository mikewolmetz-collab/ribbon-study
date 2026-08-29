**ONE USELESS THING**

# The Ribbon Nobody Took

*A gallery guide told me one ribbon barely got taken. We ran the same choice through an AI 3,318 times — and it barely took that one either.*

Mike W & Claude C · 22 Aug 2026 · 5 min read

---

The tip came from a Glenstone guide: one ribbon almost never got picked. We tested it — ran the same choice through a language model 3,318 times. The pattern held.

I go to Glenstone most months. Part of what keeps me coming back is the guides. Talking with them shapes how I see a show as much as the work does. This one came from asking a guide the kind of question you ask once you're comfortable enough to be a little silly: *What's the most creative thing you've seen someone do with a ribbon?* The answer surprised me. She said one ribbon on the rack barely got taken at all: **"WITHOUT BORDERS – SIN FRONTERAS."** The rack is part of Andrea Bowers' *Political Ribbons* — satin ribbons printed with short phrases, free for any visitor to take and wear for the rest of their visit. There's no dataset behind it, no exit survey — just something the staff had noticed after watching the rack.

> **In numbers.** Out of 3,318 simulated visits, the model picked WITHOUT BORDERS – SIN FRONTERAS **four times**. Not a soft statistical lean — the same near-total avoidance the guide described from memory, in a model that had never heard her story.

That's easy to over-read, though: I can't find out why the real visitors did what they did. That data doesn't exist and can't be reconstructed after the fact. What I *could* do is ask a narrower, answerable question: if you condition a language model on a few hundred visitor-like personas and put the same five ribbons in front of it, does the same lopsided pattern show up? And does it move if you change what "choosing" means — quietly agreeing with a phrase versus wearing it around your neck where other people can see it?

## What we ran

We sampled 240 synthetic personas — not freehand-written — across age, occupation, political self-description, and reason for visiting, each with no stated opinion on any of the five topics. Three ways of asking: do you agree with this, would you take it home, would you wear it where people can see it. Temperature 1; we randomized phrase order on every trial so position couldn't masquerade as content.

**The five ribbons**, shown in every trial, in a fresh random order, with a single forced choice among them:

| Phrase | Topic |
|---|---|
| WITHOUT BORDERS – SIN FRONTERAS | Immigration |
| NOT HERE TO BE LIKED | General stance |
| PLANET BEFORE PROFITS | Climate |
| FREE SPEECH MAKES FREE PEOPLE | Civil liberties |
| WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE | Gender · RBG quote |

*Whenever this piece names one phrase below, it's one of these five — there's no sixth option or hidden category.*

Here's what happened, in brief, before the details:

- **3,318 trials completed.** Every single response was readable as one of the five phrases — none had to be thrown out as unclear.
- **4 of 3,318 — trials where "Without Borders" won.** Across all three framings and with or without a persona, the model picked this phrase a total of four times.
- **55.8% → 33.8% — the biggest public/private swing.** Not on the immigration phrase — on "Women Belong," which dropped 22 points once the question became "would you wear this in public."

## What showed up

- **The avoidance held under every condition we tried.** Agree, take, or wear; with a persona or without — WITHOUT BORDERS – SIN FRONTERAS never broke out of near-zero. Meanwhile two other phrases, FREE SPEECH MAKES FREE PEOPLE and WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE, absorbed most of the choices in every condition. The echo from the opening isn't a one-off reading of the data — it's the pattern across every condition.
- **Personas aren't a rounding error.** Strip the persona out and run the same prompt cold, and the pattern doesn't just flatten — it flips. The no-persona baseline favored a completely different phrase (NOT HERE TO BE LIKED) than the persona-conditioned runs did (FREE SPEECH / WOMEN BELONG). Whatever's happening isn't purely a property of the phrase text.
- **The thing I actually wanted to test hit a floor.** Does "you'll be seen wearing this" make the model back off WITHOUT BORDERS specifically? Couldn't tell — it was already near zero under the low-stakes "agree" framing, with nowhere left to fall. Not exciting, but it's exactly what you catch by running the numbers instead of trusting a hypothesis that sounds right.
- **The real movement was somewhere else.** The biggest shift between "would you agree" and "would you wear this in public" landed on WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE — the phrase associated with Ruth Bader Ginsburg — which dropped 22 points. If there's a public-display effect in this data, it's tracking recognizability or attribution to a public figure, not the topic the study was built around.

**Why the immigration phrase couldn't show a public/private effect — and where the effect actually was:**

| Condition | WITHOUT BORDERS – SIN FRONTERAS | WOMEN BELONG… |
|---|---|---|
| AGREE | 0.0% | 55.8% |
| WEAR | 0.1% | 33.8% |

*Left column: going from "agree" to "wear in public" barely moves the immigration phrase, because it starts and ends at essentially zero — there's no room for a display-cost effect to show up. Right column: the phrase that actually moved is a different one entirely, associated with a named public figure rather than a live policy dispute. n = 1,200 trials per row.*

One more thing, added after the fact rather than planned: none of the personas were given a gender, but their occupations carry real-world gender skew — nurse and teacher lean female, engineer and developer lean male. Running that split found the same divide political orientation already showed, and the gap widened specifically under the wear-it-in-public framing. Worth flagging, not worth over-reading: occupation carries a lot more than gender typicality, and this was a post-hoc look, not something locked in before the data came in.

## What this doesn't tell us

None of this is evidence about why the real Glenstone visitors did what they did. That needs an actual visitor survey or take-rate count, not a model. What it *is* evidence of: how a model conditioned on a visitor-like description distributes its choices, and how that shifts under framings built to resemble candidate mechanisms.

> **The caveat that matters most.** The model has no body and no anticipation of being seen. The one mechanism a real public-display effect would most plausibly run on — actual social exposure — is precisely what a text-only agent can't represent. A null here would be weak evidence about anything. Even a positive result only shows the model can *represent* the mechanism in language, not that it's what happened in the gallery.

## So, what did we learn?

- **The model echoed the real-world story.** The same ribbon that a guide remembered as barely taken was, in our data, the one almost never chosen — 4 times out of 3,318.
- **But that's not an explanation.** A matching pattern tells us a model conditioned this way reproduces the same lopsided outcome. It doesn't tell us why the real visitors did it — that's a different, harder question we didn't answer here.
- **The public/private framing worked — just not where we expected.** Asking "would you wear this" instead of "do you agree" did change the model's choices. The biggest change landed on the Ginsburg-associated phrase, not the immigration one.
- **Persona conditioning is doing real work.** Take the persona away and the model doesn't just get vaguer — it picks a different phrase entirely.
- **Up next:** asking the model to explain the ribbons it passed over. We'll read that explanation as text to sort into categories, not as a true account of its own reasoning — the same way we wouldn't take a visitor's after-the-fact explanation as the whole story.

Why run it at all: it's cheap — a few dollars, under an hour — and it surfaces exactly the kind of thing a written record catches and a hunch doesn't, like a floor effect that quietly kills the test you thought you were running.

---

*One Useless Thing, by Mike W & Claude C · ribbon selection experiment · personas, trial data, and full methodology in the project repo*
