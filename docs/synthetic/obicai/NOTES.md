# ObiCai run — notes

Third run of the `tools/synthetic-panel` pipeline, and the one that answers the
question the second run raised. `questions.json` is byte-identical to both prior
runs, so every difference below comes from the respondents.

## The panel

Twelve people are named in the source research; the ten with real biographies are
simulated. Alyssa Gross and David Khan appear only as names in an org chart, so
there was nothing to build a respondent from — the same rule that excluded
Pyromation's Director of Sales and Marketing.

| # | Employee | Role | Tier | Persona |
|---|---|---|---|---|
| 01 | James Bashir A. Khan | President & Managing Partner | exec | Systems Thinker |
| 02 | Peter Shuey | Director of Operations | exec | Michelin-Star Chef |
| 03 | Nancy Khan | Procurement Specialist & Office Mgr | corporate | Investigative Journalist |
| 04 | Jaimi Grahovac | Executive Assistant & Project Manager | corporate | Chief of Staff |
| 05 | Shelbi Ankenbruck | Training Coordinator | corporate | Pediatric Occupational Therapist |
| 06 | Carrie Gerke | GM, BakerStreet Steakhouse | unit | Magician-Illusionist |
| 07 | Magali Ort | Executive Chef, BakerStreet | unit | Nuclear Reactor Operator |
| 08 | Jacob Sanchez Franklin | GM, Próximo | unit | Soccer Referee |
| 09 | Alejandro Ivey | Executive Chef, Próximo | unit | Missiologist |
| 10 | Eric Millan | Executive Head Chef, Hoppy Gnome | unit | Left Fielder |

This is the first panel with real frontline depth. Five of ten run a dining room or
a kitchen, hold genuine end-user authority, and hold no budget authority at all.

## The convergence broke

After two runs the four group means sat within 0.16 of each other and I could not
tell whether that was a fact about Midwest organizations or a center of gravity in
the method. The third org separates them.

| Group | CHFB | Pyromation | ObiCai |
|---|---:|---:|---:|
| Direction Focus (ladder) | 1.89 | 1.79 | 1.62 |
| Agility Focus (ladder) | 1.35 | 1.41 | 1.39 |
| Sensing vs. Creating (spectrum) | 1.30 | 1.46 | **1.72** |
| Direction vs. Agility (spectrum) | 2.60 | 2.63 | 2.58 |

At the group level ObiCai still looks like the others — Sensing vs. Creating moves
+0.42 from the first run, just past the ±0.35 noise floor, and nothing else does.
But the group mean is hiding the actual result. At the question level:

**XT1 — "when it comes to moving from thinking to doing, our organization tends to…"**

| | mean |
|---|---:|
| Community Harvest + Pyromation | 1.21 |
| ObiCai | **2.90** |

A gap of **+1.69**, roughly five times the noise floor, and the largest single
effect anywhere in this project. Nine of ten ObiCai respondents picked *"we lean
toward action and getting started, and build in reflection as we go."* The food bank
and the sensor manufacturer clustered on *"we prefer to be thorough before
committing."*

That is not noise and it is not a persona artifact — it is the difference between
organizations whose work is a service that either happened tonight or didn't, and
organizations that ship a calibrated instrument or a federal commodity allocation.
The instrument detected a real sector difference. That is the strongest evidence so
far that it measures something.

**So the honest answer to the two-run question:** the method does have a center of
gravity, but it is not so strong that a genuinely different organization can't move
off it. Both readings were partly right. Where the orgs actually differ in kind, the
instrument says so loudly; where they differ only in degree, it returns them to the
same place.

Second-largest gaps, all in the same direction and all consistent with a hospitality
group: AS3 technology readiness **+0.63** (they adopted Panelz and a griddle system
and it shows), DS2 problem-solving **−0.57**, AC3 distributed decision authority
**−0.55** — the last being the most centralized score in the whole project, which is
exactly what the source research says about this company.

## Spread went up, not down

| Run | n | mean spread | unanimous items |
|---|---:|---:|---:|
| Community Harvest | 10 | 0.81 | 7/26 |
| Pyromation | 7 | 0.73 | 8/26 |
| ObiCai | 10 | **0.96** | **5/26** |

I flagged after the second run that if every panel landed near 0.75 the spread would
be an artifact. It didn't. The panel with five frontline respondents disagrees with
itself more than the two leadership-only panels did — which is what should happen
when you add people who see a different part of the organization.

## Where this panel splits

- **AC1 and TS2** — James Khan is alone at the top on both. On AC1 (path from idea to
  experiment) he scores 3 against a panel of mostly 1s. The owner-operator experiences
  centralized authority as speed; nobody below him describes it that way. This is the
  cleanest single-respondent dissent in three runs, and it is the company's named
  weakness showing up as a disagreement rather than as a low score.
- **AS3** — Ankenbruck alone at 3. The person who has to make new technology stick with
  300 staff rates the appetite for it highest. Whether that is insight or optimism is
  the sort of thing a real follow-up interview would settle.
- **AC3** (decision authority) — panel mean 0.50, the lowest score of any question in
  any of the three runs. Nine of ten scored it 0 or 1.
- **Tier means are nearly flat**: exec 1.75, corporate 1.78, unit 1.74. The org chart
  does *not* predict overall optimism here. It predicts *which questions* people split
  on — the disagreement is targeted, not global. That is a better result than a clean
  tier gradient would have been, and it is only visible because individual scores are
  retained.

## Method notes

No parser failures this run — all ten files carried every required field, which is the
`**Persona:**` fix from the Pyromation run working as intended. One agent's reply text
listed 24 scores for a file that correctly contained 26 rows; as before, validation ran
against the files and caught nothing, because there was nothing wrong with the files.
Never trust the reply summary.
