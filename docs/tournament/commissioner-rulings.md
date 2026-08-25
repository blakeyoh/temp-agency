# Commissioner Rulings

Per `rules-v2.md` §4, every override is printed **as an override**, with the
commissioner's reason attached, never folded into the panel's verdict. Visible rigging
is honest; invisible rigging is the thing this repo exists to prevent.

---

## Round of 32 · Bracket 1 (Fence)

### Ruling 1 — Game 1: OVERRULE
**Panel result:** The Understudy 12, The Wrong Expert on Purpose 8 (five-axis aggregate).
Panels split 2–1 the other way: Skeptic and Ecologist both named Wrong Expert the
overall winner; Builder named the Understudy.

**Ruling:** **The Wrong Expert on Purpose advances.** The commissioner sides with the
panel majority over the axis sum.

**Reason:** *"It's hard not to keep both."* The two ideas defeat different reflexes —
all three panels said so independently, which is why all three refused the merge.

**Consequence:** The Understudy is **not eliminated**. It is placed on the
**wildcard bench** (§4, REVIVE) and may be brought back into a later round.

### Ruling 2 — Game 3: TIEBREAK
**Panel result:** 16–16. A genuine dead heat, unanimous on four of five axes and split
cleanly down the middle: Foraging took Distance (+7) and Irreducibility (+9, unanimous
and maximal); the Novelty Gate took Compounding (+9, unanimous and maximal), Mechanism,
and Generative failure. Panels leaned 2–1 to Foraging.

**Ruling:** **Cross-Repo Foraging advances.** The commissioner breaks the tie.

**Reason:** *"I prefer foraging over gate."* Consistent with the panel lean.

**Note for the record:** this game is the sharpest statement in the bracket of the
tournament's central trade-off — **irreducibility versus compounding**. Foraging is the
most irreducible entrant seen so far (a base model reproduces 5–8% of it) and is
memoryless. The Novelty Gate compounds automatically and is satisfiable with vocabulary.
The tie was information, not a failure of the rubric.

### Ruling 3 — Game 2: ABSORPTION RATIFIED
**Panel result:** The Idea-Space Map 23, Persona Grammar 8. Builder and Ecologist
independently returned **ABSORBED** with near-identical reasoning and near-identical
merged sentences, having never seen each other's work. Skeptic returned ORTHOGONAL.

**Ruling:** **Absorption accepted, 2–1.**

**What is absorbed:** the parser's **rejection primitive** only — explicitly *not* the
per-persona grammar, which both panels named as a second claim and refused.

**Merged definition:** *"Cluster every output the repo has ever produced and reject any
new output that lands in a region the corpus has already filled."*

**The winner advances as THE BINDING MAP.** The map was the thesis; the gate is what
makes it binding rather than advisory.

**Dissent preserved (Skeptic):** the Map's own text disclaims enforcement, and a
rejection threshold imports novelty-over-correctness — *"punishing the right answer for
being the answer already given… a map that forbids is a fence, and a fence refuses the
small repair in front of you on the grounds that someone already repaired one like it."*

### Game 4 — no ruling required
Persona Toolbelts 26, Idea Bankruptcy 5. Unanimous across all three panels, unanimous
and maximal on Irreducibility. Advances clean.

---

## Round of 32 · Bracket 2 (Dog)

### Ruling 4 — Game 5: ABSORPTION ACCEPTED, MODIFIED
**Panel result:** Temporal Displacement 17, Constraint Compiler 13. Panels 2–1 for
Displacement; aggregate agrees. Absorption split 1–2: Builder returned ABSORBED,
Skeptic and Ecologist returned ORTHOGONAL.

The two panels ran the *same* deletion test on the *same* merge and reached opposite
conclusions:

> **Builder:** remove the checker and Displacement *"degrades to period diction carrying
> modern concepts, which is precisely the failure it names in its own claim."*
>
> **Ecologist:** *"Delete the anachronism linter six months out and A gets **better**, not
> worse. The leaked modern term is A's highest-scoring feature; linting it away destroys
> the diagnostic."*

**Ruling:** merge, **conditional on it hardening the work** — commissioner's instruction.

**Assessment (Claude's call, not either panel's):** it hardens only in a modified form.
The Ecologist's objection is not to the checker; it is to *linting the leak away*. Both
positions hold if the checker **logs before it rejects**. The leaked term is captured as
evidence, then the output is regenerated — the diagnostic survives and the barrier is
real.

**Merged definition:** *"Instantiate the specialist at a named year and reject any output
containing a term that postdates it, recording each rejection as evidence of which modern
concept the answer could not be built without."*

Passes the one-sentence test: one thesis (era-limitation forces re-derivation), with the
leak log a byproduct rather than a second mechanism. What is absorbed is the **era-lexicon
checker only** — the compile-from-Anti-Patterns half is explicitly refused, as the Builder
required, because that half carries the Compiler's rival diagnosis that voice prose is the
homogeneity source.

**The winner advances as THE DATED SPECIALIST.**

### Ruling 5 — Game 7: ABSORPTION REFUSED
**Panel result:** Hostile Environment 27, Ratchet 13 — the only unanimous five-axis sweep
of the tournament, three axes maximal. Absorption split 1–2: Ecologist returned ABSORBED
(monotonic escalation applied to the input), Builder and Skeptic returned ORTHOGONAL.

**Ruling:** **no merge.** Hostile Environment advances clean.

**Reason:** commissioner declined. The Builder had anticipated exactly the Ecologist's
merge and rejected it — *"that absorbs A's silhouette, not A's mechanism: it ratchets an
input condition where A ratchets an output score."*

### Ruling 6 — Game 8: REVIVE + OVERRULE
**Panel result:** Collaboration Contract 19, Bracket as a Primitive 7. Unanimous, all
three panels, all three ORTHOGONAL.

**Ruling:** **The Understudy is revived from the wildcard bench and takes this Sweet 16
slot.** The Collaboration Contract does not advance.

**Reason:** *"I like the understudy more than either collaboration contract or
bracket-as-primitive."*

**Consequence (Claude's inference, easily reversed):** the Collaboration Contract takes
the Understudy's former place on the wildcard bench rather than being eliminated —
symmetric with Ruling 1, and it was a unanimous winner on the merits.

### Game 6 — no ruling required
Entropy Well 18, Anti-Roster 13. Panels 2–1 for Entropy Well; aggregate agrees. All
absorptions refused (Skeptic SUBSUMED, two ORTHOGONAL). Advances clean.

**Noted:** the Builder — the panel with a *disclosed bias toward Mechanism* — voted
against the mechanism here: *"A PRNG constrains a distribution, not an output, and the
ruler asks for an output — that is a floor by the ruler's own rule."* A vote that defies
its own declared bias carries more weight, not less.

---

## The tournament eliminated itself

**Bracket as a Primitive** — the mechanism generating this entire document — lost 19–7 in
round one, unanimously, judged by panels blind to what they were evaluating.

> **Skeptic:** *"B is the entrant that most flatters the process now evaluating it, and an
> idea that rewards its own judging mechanism earns harder questions, not softer ones…
> 32 entrants with a refusal-by-default absorption rule means 24 of them contribute
> nothing at all."*
>
> **Ecologist:** *"B's cost per use — 31 matchups against five axes with two predicates
> each — is its own Limits to Growth loop whose limiting condition is judge attention, and
> **judge attention does not scale into year three**."*

The Ecologist's prediction was confirmed within the hour: the session paused for usage
limits after two of four brackets.

**This is an open finding against the format, not against any entrant.** It is recorded
here rather than resolved, because the Skeptic's charge lands on a live design decision:
refusal-by-default absorption may make a 32-entrant field mostly decorative. The
counter-argument is that the ORTHOGONAL list is itself a deliverable — a set of mechanisms
identified as independent axes worth building side by side. Unresolved.

---

## Standing procedural decisions

### Precedence: deliberately unset
When the five-axis aggregate disagrees with the panel majority, **neither automatically
governs**. The disagreement raises a CONTESTED flag and escalates to the commissioner, who
rules case by case. Game 1 is the only instance so far; the commissioner chose the panel
majority. That is a ruling, not a precedent.

### Absorption default
1–2 against carries as a refusal unless the commissioner rules otherwise. Both bracket-2
absorptions were 1–2; one was accepted (modified), one refused. The vote count is a
signal, not a rule.

### The wildcard bench
Eliminated ideas the commissioner is not ready to discard. Revivable into any later round.

| Idea | Left in | Held because |
|---|---|---|
| The Collaboration Contract | R32 · G8 | Unanimous winner on the merits; displaced by a revive, not beaten |
| The Constraint Compiler | R32 · G5 | Commissioner not ready to discard; its checker already partly absorbed |
| The Anti-Roster | R32 · G6 | Took Distance +9 unanimous; lost on mechanism, not on ambition |
| ~~The Understudy~~ | *revived* | Took the G8 Sweet 16 slot |

---

## Open item — a defect in the field, found by the panels

Two panels independently flagged that **`bin/claims` and `bin/who-benefits`** in Persona
Toolbelts are not tools:

> **Builder:** *"an LLM judgment printed behind a shell prompt is method exposure, not measurement."*
> **Skeptic:** *"a prompt wearing an executable's name."*

Four of six named tools are real computations; two are prompts in costume. An authoring
defect in the entrant as written, not a finding against the idea. **Persona Toolbelts
advances as written, with the defect on the record.** Whether an entrant may be amended
mid-tournament remains an open commissioner decision.

---

## Sweet 16 field so far (8 of 16 R32 games judged)

| Advancing | From | How |
|---|---|---|
| **The Wrong Expert on Purpose** | Fence G1 | Commissioner overrule |
| **The Binding Map** | Fence G2 | 23–8, absorption ratified 2–1 |
| **Cross-Repo Foraging** | Fence G3 | Commissioner tiebreak from 16–16 |
| **Persona Toolbelts** | Fence G4 | 26–5 unanimous, defect noted |
| **The Dated Specialist** | Dog G5 | 17–13, absorption accepted modified |
| **The Entropy Well** | Dog G6 | 18–13, clean |
| **The Hostile Environment** | Dog G7 | 27–13 unanimous sweep, absorption refused |
| **The Understudy** | Dog G8 | Revived from bench by commissioner |

**Not yet run:** Bracket 3 (Moat, games 9–12) and Bracket 4 (UFO, games 13–16).
