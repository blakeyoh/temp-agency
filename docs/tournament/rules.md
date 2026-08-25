# Tournament Rules

## The 99th-Idea Rubric

Every matchup is scored on five axes, 1–10 each, 50 possible. The axes are chosen to
reward *distance from the median output*, not implementability. A cheap idea that pushes
the model somewhere it would never go beats an expensive idea that produces a better
version of where it already goes.

| Axis | Question | What a 10 looks like | What a 3 looks like |
|---|---|---|---|
| **Distance** | How far from the median AI answer does this push? | The output is unrecognizable as a model's default | The output is the default, better organized |
| **Mechanism** | Does something *execute*, or is this exhortation? | A program, a ledger, a parser, a deletion | A paragraph asking the model to try harder |
| **Irreducibility** | Could the base model already do this if simply asked? | No — it requires state, tools, or weights the model lacks | Yes — "be more creative" gets 80% of it |
| **Compounding** | Does it get weirder with use, or wear off? | The tenth use is stranger than the first | Novelty effect; identical every time |
| **Generative failure** | When it breaks, what does it produce? | A different kind of insight | Noise, or nothing |

**Irreducibility is the load-bearing axis.** It is this repo's own doctrine — *encoded
preference over capability uplift* — applied to mechanisms instead of personas. A
mechanism the model can simulate when asked politely is not a mechanism.

## The absorption rule

The winner does not merely advance. It **takes the single strongest mechanism from the
loser** and carries it forward as part of its own definition. This is what separates a
bracket from a ranking: ranking discards 31 ideas, absorption keeps the best part of all
of them.

Absorption budget by round:

| Round | Absorptions granted | Composite size on exit |
|---|---|---|
| Round of 32 | 1 | 2 originals |
| Sweet 16 | 1–2 | 3–4 originals |
| Elite Eight | 2 | 5–6 originals |

Later rounds grant more because the loser is itself a composite — a winner may absorb a
mechanism the loser had inherited from someone else. Those inherited mechanisms are
tracked in the lineage line of each survivor, so a Final Four entrant can be traced back
to every original entrant that contributed to it.

**What may not be absorbed:** a mechanism that contradicts the winner's own core move.
If the winner is defined by *removing* something and the loser by *adding* something,
the absorption must be reframed as a removal or refused. Refused absorptions are recorded
— they are evidence that two ideas are genuinely incompatible, which is useful.

## Seeding

Four regions of eight, seeded 1–8 within region, standard 1v8 / 2v7 / 3v6 / 4v5 bracket.
Seeds reflect *initial* estimated strength on the rubric, before any absorption. Seeds
are frequently wrong, and the upsets are the interesting part: a 1-seed that loses is
usually an idea that was easy to *state* and hard to make execute.

Regions are thematic rather than arbitrary, so a regional champion represents a coherent
philosophy of forcing creativity, and the Final Four is four rival theories rather than
four unrelated tricks.

| Region | Theory of creativity | Enemy |
|---|---|---|
| **Entropy** | Inject genuine outside material or genuine randomness | The model's simulated randomness, which is retrieval |
| **Constraint** | Take away the thing the model always reaches for | The signature move, always available, always taken |
| **Apparatus** | Make the lens execute instead of asking it to | Markdown that requests behavior and hopes |
| **Memory** | Make the repo remember, so it cannot repeat itself | The fresh context window |

## Stopping point

The tournament runs Round of 32 → Sweet 16 → Elite Eight, then **stops at the Final
Four** for owner review. Semifinals and the championship are not run without a decision
on the four surviving philosophies — by that point each survivor is a composite of five
or six originals, and which one wins determines the repo's next architecture.
