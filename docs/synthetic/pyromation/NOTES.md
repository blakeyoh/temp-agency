# Pyromation run — notes

Second run of the `tools/synthetic-panel` pipeline. Same instrument, same prompt
(variant B), different organization. `questions.json` parsed from the source
`.docx` files is byte-identical to the Community Harvest run, so anything that
differs between the two panels comes from the respondents, not the instrument.

## The panel

Seven named leaders appear in the source research and all seven are included —
this is the first run that did not hit the ten-person cap. Excluded, and why:
founders Dick Wilson and Bill Lewis (historical), Pete Wilson (retired 2023–24),
and the Director of Sales and Marketing (named only by title, so there is no
biography to simulate). John Norris is included but sits at the corporate parent:
he answers about Pyromation as a business unit he governs rather than runs, and
his prompt says so.

| # | Employee | Role | Persona |
|---|---|---|---|
| 01 | Eric Sawyer | Senior Managing Director / GM | Military Three-Star General |
| 02 | Mark Beckman | Chief Financial Officer | Soccer Referee |
| 03 | John Norris | CEO, TASI Measurement | Business Development Director |
| 04 | Chris Moritz | Director of IT and Quality | Nuclear Reactor Operator |
| 05 | Michael Lackey | Engineering Manager | Physics Professor |
| 06 | Kimberly A. Trygg | Human Resources Manager | Trauma-Informed Practitioner |
| 07 | Greg Craghead | Marketing Manager | Anthropologist |

## Findings

**Direction sits above Agility again.** 1.79 vs 1.41 on the ladders, and every
single respondent scored it that way — no dissenters. The Community Harvest panel
did the same thing (1.89 vs 1.35, also unanimous). Two organizations with almost
nothing in common produced the same ordering.

**This panel is tighter than the last one.** Mean per-question spread 0.73 against
0.81, and 8 of 26 questions were unanimous against 7 of 26. A seven-person
single-site leadership team that mostly grew up inside the company agrees with
itself more than a food bank's cross-functional staff did. That is a plausible
result, not a suspicious one, but it is worth watching: if every future panel
lands near 0.75 regardless of the org, the spread is an artifact of the method
rather than a fact about the organization.

**The convergence deserves suspicion, not celebration.** Across the two runs the
four group means land within 0.10–0.16 of each other on every group:

| Group | Community Harvest | Pyromation |
|---|---:|---:|
| Direction Focus (ladder) | 1.89 | 1.79 |
| Agility Focus (ladder) | 1.35 | 1.41 |
| Sensing vs. Creating (spectrum) | 1.30 | 1.46 |
| Direction vs. Agility (spectrum) | 2.60 | 2.63 |

Two readings, and this run cannot distinguish them. Either mid-size Midwest
organizations really do cluster here, or the method has a center of gravity that
any org gets pulled toward. The A/B established a noise floor of roughly ±0.35 per
respondent on an identical rerun — every gap in that table is *inside* that floor.
So the honest statement is that these two panels are not measurably different from
each other, and a third org is the cheapest way to find out which reading is right.

**Where the panel actually splits.** The aggregate hides the useful part:

- **DT1** (strong plan → what we do next) drew a 3 from six of seven, and a 2 from
  Craghead alone. Twenty years of marketing is the one seat that watches plans meet
  the outside world.
- **DT2** and **AT2** pulled 0s from Moritz, Lackey, and Craghead — the three people
  whose jobs depend on verifying things personally. The quality director, the
  engineering manager, and the person who writes the catalog all sit at the same end.
- **AS4** (frontline observations reaching leadership) split 2/1: Sawyer and Trygg
  scored it 2, everyone else 1. The GM and the HR manager are the two people whose
  jobs are literally to receive that signal — a self-report worth noting rather than
  trusting.
- **TX1** and **TC2** were fully unanimous at 3. Nobody in this leadership team
  disagrees about the direction/agility tradeoff at all.

Individual scores stay in for exactly this reason: the group means above are nearly
identical across two very different organizations, and everything that distinguishes
them lives at the per-respondent layer.

## A bug this run found

Four of seven agents omitted the `**Persona:**` line and started the file with
`**Persona fit (2 sentences):**`. `parse_answers.py` accepted all four silently —
its `FIELD_RE` used `[^:]*` after the label, which let the `Persona` pattern match
the `Persona fit` line. The persona field quietly filled with two sentences of prose
and rendered as a wall of monospace on four roster cards.

Fixed: the label may now carry a parenthetical suffix and nothing else. The four
files were repaired by hand. The Community Harvest run re-parses byte-identical, so
the fix is not a behavior change for well-formed input — it only converts a silent
wrong answer into a loud failure, which is what the parser is for.
