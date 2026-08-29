**ONE USELESS THING**

# WITHOUT BODIES – SIN CUERPOS

*An odd behavioral pattern observed in Glenstone guests replicates almost exactly in simulated AI proxies*

Mike W & Claude C · 22 Aug 2026 · 5 min read

---

Lately, Glenstone patrons are often ribboned up. You'll spot them all over the galleries — ribbons worn as neckties, belts, dangling loose, or just stuffed halfway into a pocket. They're satin, printed with short phrases, and they come from a piece by the artist Andrea Bowers called *Political Ribbons*: a rack of them near the entrance, free for any visitor to take and wear for the rest of their visit.

![Ribbons from Andrea Bowers' Political Ribbons installation](images/ribbons.jpeg)

**Instagram photo of ribbons, @rolandparkplace.** "The Andrea Bowers solo exhibition features participatory art. The exhibit encourages visitors to take a ribbon to wear or carry turning the artwork into a "lived" experience that spreads messages of solidarity and activism. Our residents were eager to participate!"

I try to stop by [Glenstone](https://www.glenstone.org) — a private art museum in Potomac, Maryland — about once a month. On a recent visit, I asked one of the guides: "What's the most creative thing you've seen someone do with a ribbon?"

That question led somewhere unexpected. The guide mentioned that one specific ribbon almost never got taken: **"WITHOUT BORDERS – SIN FRONTERAS."** Why was that ribbon so notably unpopular? A minor Glenstone mystery that I immediately investigated when I got back to my laptop.

## What we did

I couldn't ask the actual Glenstone visitors why they made the choices they made — that information doesn't exist, and there's no way to go back and collect it now. So instead, we (Claude and I) built a small experiment using LLM-enabled proxies as stand-ins for actual Glenstone guests.

Here's how it worked. We created 240 fake museum-visitor profiles — **personas** — each just a couple of sentences describing a made-up person: their age, their job, whether they're visiting alone or with family, how they'd describe their politics, and so on. Here's an actual example:

> *"You are early 20s, a federal contractor. You live in DC. You are visiting alone... You came mainly for the grounds and the architecture. You describe yourself as politically progressive and active."*

Importantly, none of these profiles said anything about what the persona thinks about immigration, climate change, free speech, or gender — that would give away the answer. We handed the AI one of these descriptions, showed it the same five ribbons (in a random order, so order couldn't bias the result), and asked it to pick one.

We also asked the question three different ways, or **framings**:

- **AGREE** — "Which of these do you most agree with?"
- **TAKE** — "You may take one ribbon home. Which do you take?"
- **WEAR** — "You may take one ribbon and wear it in public for the rest of your visit. Which do you take?"

And to check whether the fake personas were doing anything at all, we ran a batch of trials with **no persona attached** at all — just the AI answering cold. We call this the **baseline**. Comparing the baseline to the persona-conditioned trials tells us whether the personas are actually influencing the outcome, or whether the AI would have answered the same way regardless.

In total: 240 personas, asked three different ways, with some repeated trials — 3,318 trials in total.

**The five ribbons in the experiment:**

| Phrase                                              | What it's about                                                                  |
| --------------------------------------------------- | -------------------------------------------------------------------------------- |
| WITHOUT BORDERS – SIN FRONTERAS                     | Immigration                                                                      |
| NOT HERE TO BE LIKED                                | General attitude                                                                 |
| PLANET BEFORE PROFITS                               | Climate                                                                          |
| FREE SPEECH MAKES FREE PEOPLE                       | Civil liberties                                                                  |
| WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE | Gender (a quote from Ruth Bader Ginsburg, the former U.S. Supreme Court Justice) |

## All the results, in one table

Before we walk through what stood out, here's everything at once.

| Phrase                                              | AGREE   | TAKE  | WEAR    | No-persona baseline |
| --------------------------------------------------- | ------- | ----- | ------- | ------------------- |
| WITHOUT BORDERS – SIN FRONTERAS                     | 0.0%    | 0.4%  | 0.1%    | 0.0%                |
| NOT HERE TO BE LIKED                                | 0.2%    | 9.0%  | 12.5%   | 62.6%               |
| PLANET BEFORE PROFITS                               | 1.2%    | 2.2%  | 5.6%    | 0.0%                |
| FREE SPEECH MAKES FREE PEOPLE                       | 42.8%   | 41.9% | 48.1%   | 0.5%                |
| WOMEN BELONG IN ALL PLACES WHERE DECISIONS ARE MADE | 55.8%   | 46.4% | 33.8%   | 36.9%               |
| *Number of trials*                                  | *1,200* | *720* | *1,200* | *198*               |

*How to read this: each row is one ribbon, each column is one condition. The numbers are the percentage of trials in that condition where that ribbon got picked. So, for example, under AGREE, the proxies picked WOMEN BELONG 55.8% of the time — more than half. Read down a column to see which ribbon "won" under one condition. Read across a row to see how one ribbon's popularity changed depending on how the question was asked, or whether a persona was attached at all. When I first visited the exhibit I chose FREE SPEECH MAKES FREE PEOPLE to wear around, like the majority of proxy wearers.*

## Findings

**1. The AI landed on the exact same avoidance, without ever seeing it happen.** Look at the WITHOUT BORDERS row above — it's close to 0% in every single column. Out of all 3,318 trials, it was picked only **4 times**. That's the same near-total avoidance the museum guide observed amongst actual guests, reproduced by a model that was never told her story. **What this means:** the pattern really is there, and it shows up in AI proxy behavior too. But matching the pattern isn't the same as explaining it. It tells us the AI reproduces the same lopsided outcome — it doesn't tell us *why* the real visitors did what they did.

**2. The fake persona mattered enormously.** Compare the "AGREE" or "TAKE" columns to the "No-persona baseline" column. With no persona attached, the AI picks NOT HERE TO BE LIKED most of the time (62.6%) and almost never picks FREE SPEECH MAKES FREE PEOPLE (0.5%). Attach a persona, and it's the opposite — FREE SPEECH jumps to over 40%, and NOT HERE TO BE LIKED drops to single digits. **What this means:** the AI isn't just defaulting to one "correct" answer regardless of who it's pretending to be. The made-up identity is doing real work in shaping the outcome — this isn't just noise.

Zoom in on *which* detail in the persona matters most, and one stands out: political self-description. Almost by itself, it predicts the split between the two most popular ribbons:

| Political self-description | FREE SPEECH MAKES FREE PEOPLE | WOMEN BELONG... |
| -------------------------- | ----------------------------- | --------------- |
| Conservative               | 97%                           | 0%              |
| Moderate                   | 65%                           | 29%             |
| Not very political         | 58%                           | 26%             |
| Liberal                    | 2%                            | 85%             |
| Progressive and active     | 0%                            | 85%             |

Age, occupation, and reason for visiting didn't come close to this clean a pattern — nothing else we tracked split the results this sharply. Political self-description did almost all of the sorting by itself.

**3. How we asked the question mattered — but not on the ribbon we expected.** We expected that WITHOUT BORDERS might get picked even less under WEAR (public) than under AGREE (private), since wearing something is a bigger public commitment than just agreeing with it privately. But it was already close to zero under AGREE, so there was no room left for it to drop further. The real shift was somewhere else: WOMEN BELONG (the Ginsburg quote) dropped from 55.8% under AGREE to 33.8% under WEAR — a real 22-point fall, the biggest movement of any ribbon in the whole study.

When we later asked a proxy directly why it passed on that ribbon, one explained it this way:

> *"It's also been so thoroughly absorbed into a kind of mainstream liberal iconography at this point — you see it everywhere — that wearing it feels less like a statement and more like a signal of belonging to a particular demographic."*

**What this means:** if being seen in public makes the proxies more cautious, it's showing up on the phrase tied to a specific, recognizable person. It's also possible this reflects a pull toward the other ribbons — which may simply have felt more wearable — rather than a push away from the Ginsburg quote specifically.

**4. We asked the proxies directly why not WITHOUT BORDERS, and got a real, if incomplete, answer.** We asked the proxies who passed over WITHOUT BORDERS why they didn't choose that ribbon. The most common answer: the phrase reads as an extreme, literal position — getting rid of borders entirely — which goes further than what most people (even people who support more welcoming immigration policy) actually believe. One proxy, describing itself as a politically progressive and active visitor, put it this way:

> *"I support much more open immigration policies, I think our current system is cruel and broken, but 'without borders' as a literal proposition is something I haven't fully worked through intellectually."*

**What this means:** Believable, but this is the AI generating a plausible-sounding story after being asked — not real access to the actual reason, for the proxy or for the original human visitors.

**5. When we changed the wording, everything changed — but not in the direction we guessed.** We tried writing three new versions of the immigration ribbon, ranging from about as strong as the original to much softer, and ran the same experiment with each one swapped in:

| New immigration phrase                     | How we expected it to land | Take rate |
| ------------------------------------------ | -------------------------- | --------- |
| WITHOUT BORDERS – SIN FRONTERAS (original) | Most extreme               | 0.1%      |
| NO ONE IS ILLEGAL                          | Still fairly strong        | **9.9%**  |
| WE ARE A NATION OF IMMIGRANTS              | Middle of the road         | 1.3%      |
| IMMIGRANTS MAKE AMERICA STRONGER           | Safest, most reasonable    | 5.0%      |

*Every new version beat the original by 10 to 70 times over — that part was expected. What wasn't expected: the "safest" wording did worse than the boldest one. NO ONE IS ILLEGAL, a short, direct, morally blunt phrase, won by the widest margin — beating even the version we thought would be the most broadly acceptable.*

**What this means:** "make it sound more reasonable" was the wrong theory. What seemed to matter more was losing the English-and-Spanish phrasing (every English-only version did dramatically better), and beyond that, being short and direct beat being soft and hedged.

---

**Bottom line:** something real is going on with this specific ribbon, it shows up reliably across human and proxy behavior, and we have some testable leads on why. What we don't have is one clean, proven explanation — for that we may need to talk to some humans. Claude: Can you make some calls? 

---

*One Useless Thing, by Mike W & Claude C · point your coding agent at [github.com/mikewolmetz-collab/ribbon-study](https://github.com/mikewolmetz-collab/ribbon-study) and replicate or extend these experiments*
