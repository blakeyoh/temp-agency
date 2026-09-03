# Tournament Rules v2

> v1 produced a clean narrative and a dishonest result. Three of its design choices
> conspired: mandatory absorption manufactured composites nobody wanted, absolute
> 1–10 scoring compressed into unfalsifiable 8s and 9s, and thematically pure regions
> *guaranteed* a Final Four of four rival philosophies regardless of merit. v2 fixes
> all three, adds an independent judging panel, and puts a commissioner in the room.

---

## 1. The absorption standard

**Absorb only what the winner would miss.**

Absorption in v1 was mandatory, which meant the question was never *whether* to merge —
only *what* to merge. That guarantees Frankensteins. In v2 the default is **refusal**,
and a merge must earn its way in by passing all three tests.

### The three tests (all must pass)

**1 · Same-thesis test.** Every idea makes one claim about *why* output is homogeneous.
Does the mechanism serve the winner's existing claim, or import a second one? A winner
defined by *"remove the vocabulary"* may absorb a better way to remove vocabulary. It may
not absorb *"and also keep a ledger."*

**2 · Deletion test.** *(the sharp one)* Delete the absorbed part six months from now.
Does the winner get **worse**, or just **smaller**? Smaller-but-not-worse means it was
decoration. Only "worse" passes.

**3 · One-sentence test.** Can the merged idea still be stated in one sentence with no
conjunction? If the description needs an *"and also"*, you have built two ideas wearing
one name.

### Three dispositions, not one

Every loser gets a disposition. Only the first is a merge.

| Disposition | Meaning | Where it goes |
|---|---|---|
| **ABSORBED** | Passed all three tests; the winner is now stronger | Into the winner's definition |
| **ORTHOGONAL** | Failed the same-thesis or deletion test. The two ideas are genuinely independent axes | `parallel-track.md` — build it *alongside*, never inside |
| **SUBSUMED** | The winner already does this; the loser was a special case of it | Dropped, with the recognition recorded |

**A refusal is a finding, not a failure.** ORTHOGONAL is the most valuable disposition in
the tournament: it identifies mechanisms that should exist in the repo but must never be
merged. v1 had no way to say this, so it merged them.

### Applied retroactively to v1

Spot-checking the standard against the 28 absorptions already recorded suggests roughly
**a third survive**:

- *Temporal Displacement absorbs structural crossover* → **ORTHOGONAL.** Breeding is a
  second thesis. Delete it and displacement works exactly as well.
- *Lens Transformers absorbs "cost"* → **ORTHOGONAL.** Delete it and the transforms run
  identically. Pure decoration.
- *The Bred Oracle absorbs The Understudy* → **SUBSUMED.** A 0.6B model already *is* an
  understudy. Nothing was merged; a redundancy was recognized. v1 mislabeled this.
- *Make the Problem Strange First absorbs the 19-ways quota* → **ABSORBED.** Delete the
  quota and it gets worse, not smaller: with the nouns stripped you still produce three
  ideas and stop. The quota is what forces you past the abstracted-obvious.
- *Priced Transformers absorbs degradation-as-transform* → **ABSORBED.** `redact.py`
  literally *is* a transform; the library is less capable at its own job without it.

---

## 2. Anchoring the score

v1's complaint is fair: the categories were sound and then the reasoning trail vanished
into a number. v1 scores ranged 25–47 out of 50 — almost everything landed between 50%
and 94%, which is the signature of absolute scoring with nothing to compare against.

Three anchors, composed. Each fixes a different failure.

### Anchor A — Comparative, never absolute *(fixes compression)*

Never score an idea alone; score the **gap**. Per axis, one of five verdicts:

| Verdict | Points |
|---|---|
| A significantly better | **+3 A** |
| A slightly better | **+1 A** |
| Tie | 0 |
| B slightly better | **+1 B** |
| B significantly better | **+3 B** |

Five axes → a maximum margin of 15. A game decided 4–2 is genuinely close; a 12–0 is a
rout. No idea ever carries a standalone number it did not earn against a specific opponent.

### Anchor B — Reference set with fixed values *(fixes scale drift)*

"Significantly better" is meaningless without a ruler. Each axis pins named reference
points at known positions, and a judgment is made by asking **which references the idea
sits between** — the way a difficulty table works in a judged sport, not the way an
impression works.

**Worked example — Irreducibility** *(full ruler for all five axes lives in `reference-sets.md`, the single source judges score against; this is illustration, not a second copy):*

| Reference | Position |
|---|---|
| "Ask the model to be more creative" | floor — a prompt does all of it |
| "Hand the model a persona file" *(this repo, v1)* | low — real, but promptable |
| "Force output through a parser that rejects it" | mid — the model cannot opt out |
| "Withhold a fact from the context window" | high — cannot be simulated by a model that knows it |
| "Change the weights" | ceiling |

Each of the five axes gets its own reference set before the round is judged. Judges may
argue an idea sits *above* a reference — they may not skip the comparison.

### Anchor C — A falsifiable predicate per axis *(fixes the vanished reasoning trail)*

Every verdict must be accompanied by a sentence of fixed form that **could be wrong**.
This is the anchor that actually answers the complaint, because it converts a score into
a receipt someone else can check.

| Axis | Required predicate |
|---|---|
| **Distance** | "Name a specific output this forbids." No nameable forbidden output → the floor. |
| **Mechanism** | "Name the file that runs." No file → exhortation, and it scores as exhortation. |
| **Irreducibility** | "A base model given only the prompt `___` reproduces about ___% of this." Runnable. |
| **Compounding** | "State what use #10 produces that use #1 does not." "The same thing" → the floor. |
| **Generative failure** | "Describe the exact failure output." "It doesn't work" → the floor. |

A verdict submitted without its predicate is not counted.

---

## 3. The judging panel

Three cold reviewers, each staffed lead + lens per this repo's own contrast rule, each
carrying a **disclosed bias** toward a different axis so the biases are legible rather
than hidden. They dogfood the skill the tournament is trying to improve.

| Panel | Lead | Lens | Discloses a bias toward |
|---|---|---|---|
| **The Builder** | nuclear-reactor-operator | magician-illusionist | Mechanism — does it execute, and what does the audience *actually* see? |
| **The Skeptic** | investigative-journalist | franciscan-monk | Irreducibility — is this a claim or a tip, and would less be enough? |
| **The Ecologist** | systems-thinker | farmer | Compounding — what happens on the 50th use, and what does it cost to maintain? |

### What a reviewer sees

Only: the two ideas' definitions, the rubric with its reference sets, and the required
predicates. **Not** the seeds. **Not** the region. **Not** which entry belongs to the
owner. **Not** the other reviewers' verdicts. **Not** any prior round's results.

Seed-blindness matters — a visible seed anchors a judge toward the favorite. Owner-blindness
matters in the other direction: v1's round-one upset of the 19th Way may have been partly
an overcorrection *against* flattery, which is the same bias with the sign flipped.

### Voting

Reviewers vote **per axis**, not per matchup. Then:

| Pattern | Result |
|---|---|
| Unanimous on an axis | Verdict stands, high confidence |
| 2–1 split | Verdict stands; **the dissent is printed verbatim** in the box score |
| Reviewers on opposite sides of "significantly" | Matchup flagged **CONTESTED** and escalated to the commissioner |

**The contested flag is the point.** It makes the round gate cheap — instead of reviewing
sixteen games, the commissioner reviews the three the panel could not settle.

A second, coarser disagreement — the five-axis aggregate and the panel's majority call
naming different winners — is escalated the same way rather than resolved automatically;
see §4 Amendment 2.

---

## 4. The commissioner

The owner is the commissioner. The tournament halts after **every round** and does not
resume without a ruling. Available powers at each gate:

| Power | Effect |
|---|---|
| **OVERRULE** | Flip a result. The loser advances instead. |
| **FORCE ABSORPTION** | The panel refused a merge; merge it anyway. |
| **BLOCK ABSORPTION** | The panel merged; keep the winner clean. |
| **REVIVE** | Wildcard — pull one eliminated idea back into the next round. |
| **RESEED** | Reorder the next round's matchups. |

**Every override is printed as an override**, with the commissioner's stated reason,
never laundered into the panel's verdict. Visible rigging is honest; invisible rigging
is the thing this whole repo exists to prevent.

The round summary is built for a fast ruling: one screen, sixteen rows, contested games
flagged. Dig into three, ratify thirteen.

### Authority boundary

`rules-v2.md` is the only place a general rule lives. `commissioner-rulings.md` is an
append-only ledger of specific results, overrides, and their stated reasons — it records
what happened, not what the rules are. A ruling that settles something beyond the one game
it decided (a new eligibility test, a default disposition, a standing procedure) is not
itself a rule until the commissioner folds it back into this document as a dated, numbered
amendment; until then the ledger entry is marked **pending promotion** rather than treated
as governing future games. If this document and a ruling ever disagree about what the rule
*is* — as opposed to what a specific game's result was — this document governs.

### Amendments

Ratified additions to this document, numbered and dated. Each supersedes any prior informal
practice on the same topic; the ruling that originated it is cited for the reasoning trail,
but this text — not the ruling — is the rule going forward.

**Amendment 1 (2026-08-30, ratified from `commissioner-rulings.md` Ruling 8).** An entrant
may be amended mid-tournament when (a) a panel identifies a specific improving edit, (b) the
edit serves the entrant's existing thesis rather than replacing it, and (c) the amendment is
recorded in `commissioner-rulings.md` with its source.

**Amendment 2 (2026-08-30, ratified from `commissioner-rulings.md` "Precedence: deliberately
unset").** When the five-axis aggregate and the panel's majority call disagree on a winner,
neither automatically governs. The matchup is flagged CONTESTED and escalates to the
commissioner, who rules case by case (see §3 Voting).

**Amendment 3 (2026-08-31, ratified from `commissioner-rulings.md` Ruling 13).** A mechanism
whose contract requires generation from a transformed, masked, or withheld view is enacted
only when the generating pass runs in a separate context that receives the transformed
artifact and nothing else; a same-context run records that operation as NOT RUN.

**Amendment 4 (2026-08-31, ratified from `commissioner-rulings.md` Ruling 14).** An official
E1 run must include one counterfactual replay: re-draw at least one opener's indices under a
second stamped seed and show materially different prose for that opener. If the changed draw
leaves the prose materially unchanged, the run records decorative randomness as a contract
failure.

**Amendment 5 (2026-08-31, ratified from `commissioner-rulings.md` Ruling 15).** Where an
entrant's contract claims a foreign frame — a foraged artifact, a wrong-expert derivation, or
similar — shapes the output, the enforcer must run a per-item deletion test: if removing the
foreign frame leaves an item's substance unchanged, the item is rejected and regenerated
under the frame. A pass requires at least three surviving frame-dependent items.

**Amendment 6 (2026-08-31, ratified from `commissioner-rulings.md` Ruling 16).** Before an A6
generation, a per-run degradation card must record the exact phase permutation, the one
overused signature technique, and the false load-bearing principle, each with one required
output consequence; the card travels with both outputs.

**Amendment 7 (2026-08-31, ratified from `commissioner-rulings.md` Ruling 19).** An official
E6 run must count the real `knowledge/*/positions.md` files at dispatch, and the seeded draw
must select both the source packs and the card from that full counted corpus; the operator
may not pre-select which packs feed distillation, and a missing requested pack fails the draw
closed.

**Amendment 8 (2026-09-03, ratified from `commissioner-rulings.md` Ruling 22).** A mechanism
discovered after the Round of 32 has closed may be substituted into an already-frozen
bracket only by: **(a)** naming the exact seeded slot it occupies and the entrant it
displaces; **(b)** passing it against every mechanism sharing its region through the §1
same-thesis test before entry — a *pass* on that test (a genuine rival thesis) is required
for entry as a new entrant, while a *fail* (it would in fact strengthen an existing
entrant's own thesis) routes it to absorption instead, per the existing three tests;
**(c)** running the same evidence-gathering step (unscored scrimmage, evidence contract)
already completed by its round's other entrants before it may be judged; and **(d)**
disclosing, rather than folding into the seeded draw, any difference in operator, base
model, or method between its evidence-gathering step and the round's other entrants. The
displaced entrant moves to the wildcard bench with full REVIVE eligibility — a substitution
is never an elimination.

---

## 5. Cross-pollinated regions

v1's regions were thematically pure, which quietly rigged the outcome: an Entropy idea
only ever met other Entropy ideas before the Final Four, so **the structure guaranteed one
champion per theory regardless of merit**. If Memory mechanisms are simply stronger than
Entropy mechanisms, pure regions cannot reveal it.

v2 gives every region **two entrants from each of the four categories**, with one hard
constraint: **no round-one matchup between two ideas of the same category.** Every game in
the opening round is a cross-theory argument.

**This makes the Final Four informative.** If three survivors turn out to be Constraint
ideas, that is evidence that subtraction beats addition — a finding the v1 structure was
incapable of producing.

**The cost, and why it is now safe.** Cross-theory matchups mean cross-theory absorptions,
which is exactly the Frankenstein risk in §1. The strict standard defuses it: most
cross-theory merges will fail the same-thesis test and land in **ORTHOGONAL**, which is
the right answer and a useful one. §1 and §5 need each other — either alone is worse than
both together.

Region names are drawn from the workshop story (Fence, Dog, Moat, UFO) and are arbitrary
labels, **not a difficulty ranking** — all four are balanced by construction.

### The v2 draw

Seeding prior is the v1 round-one score, treated as provisional; the panel is expected to
overturn it freely.

| Region | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| **Fence** | A6 | M5 | E2 | C3 | A3 | M2 | C7 | E3 |
| **Dog** | E5 | C2 | A5 | M7 | A7 | M6 | E1 | C6 |
| **Moat** | A1 | C8 | E4 | M1 | C4 | M4 | A4 | E7 |
| **UFO** | M3 | A2 | C5 | E6 | A8 | E8 | M8 | C1 |

### Round of 32 — all sixteen matchups are cross-category

| # | Region | Matchup | The argument |
|---|---|---|---|
| 1 | Fence | **A6** Understudy · **E3** Wrong Expert | Degraded copy vs. deliberate mismatch |
| 2 | Fence | **M5** Idea-Space Map · **C7** Persona Grammar | Know where you haven't gone vs. enforce how you speak |
| 3 | Fence | **E2** Cross-Repo Foraging · **M2** Novelty Gate | Import from outside vs. fail the build for boring |
| 4 | Fence | **C3** Idea Bankruptcy · **A3** Persona Toolbelts | Destroy your best guess vs. measure instead of assert |
| 5 | Dog | **E5** Temporal Displacement · **C6** Constraint Compiler | Remove the era vs. compile the prohibitions |
| 6 | Dog | **C2** Anti-Roster · **E1** Entropy Well | Strip the vocabulary vs. make the dice real |
| 7 | Dog | **A5** Hostile Environment · **M6** Ratchet | Take away the facts vs. raise the floor |
| 8 | Dog | **M7** Collaboration Contract · **A7** Bracket Primitive | Date the disagreement vs. compound by elimination |
| 9 | Moat | **A1** Lens Transformers · **E7** Persona Fracture | Transform what is read vs. split who is reading |
| 10 | Moat | **C8** Make Problem Strange · **A4** Committee of Strangers | Strip the problem vs. add more voices |
| 11 | Moat | **E4** Roster Mutation · **M4** Failure Archaeology | Breed forward vs. remember the dead |
| 12 | Moat | **M1** Homogeneity Auditor · **C4** Telegram Constraint | Name the median vs. price the words |
| 13 | UFO | **M3** Grudge Ledger · **C1** The 19th Way | *(v1's top scorer against the owner's own entry)* |
| 14 | UFO | **A2** Voice Oracle · **M8** Reverse Brief | Change the weights vs. invert the question |
| 15 | UFO | **C5** Notation Transposition · **E8** Temperature Choreography | Change the notation vs. choreograph the sampling |
| 16 | UFO | **E6** Oblique Deck · **A8** Scarcity Economy | Obey a bad-fit card vs. make speech cost something |

---

## 6. Sweet 16 evidence amendment

The Round of 32 judged mechanism definitions. Beginning with the Sweet 16, the tournament
also observes mechanism-produced output under the round-specific procedure in
`next-round-protocol.md`.

Four additions govern the next two rounds:

1. **Unscored scrimmage before competition.** Each entrant exposes undefined operations and
   manual substitutions, then freezes an evidence contract before seeing the official brief.
2. **Two sealed judging passes.** Panels vote on anonymized output yield first, then receive
   the mechanism definition and execution trace and apply the existing five axes. Yield remains
   a separate signal. Disagreement with aggregate or panel majority raises CONTESTED.
3. **Sacrifice Receipt.** Every panel names the internal principle or disclosed bias it honored,
   the competing commitment it sacrificed, and the cost it accepted.
4. **Collision Residue.** After sealing the verdict, a panel may name an independent third
   mechanism made visible by the collision. Residue cannot alter the game or enter the active
   field and is recorded in `collision-residue.md`.

Panel ecology also changes by round: one incumbent panel anchors calibration and two fresh
high-contrast panels are drawn after outputs are sealed. The issue #21 eligibility guardrail
and full Sweet 16/Elite 8 protocol live in `next-round-protocol.md`.
