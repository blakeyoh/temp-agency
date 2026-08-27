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

## Round of 32 · Bracket 3 (Moat)

### Games 9 and 10 — no ruling required
Both were routs, unanimous across all three panels, all absorptions refused.

| Game | Result | Margin |
|---|---|---|
| G9 | **Lens Transformers** 37, Stochastic Persona Fracture 2 | 35 — the widest of the tournament |
| G10 | **Make the Problem Strange First** 30, Committee of Strangers 2 | 28 |

Lens Transformers took four of five axes at **+9 unanimous and maximal**. The losing side
scored on Compounding alone in both games.

### Ruling 7 — Game 11: ABSORPTION RATIFIED 2–1
**Panel result:** Roster Mutation 17, Failure Archaeology 14. All three panels named
Roster Mutation the winner. Absorption 2–1 for ABSORBED (Builder, Ecologist; Skeptic
dissenting).

Archaeology won **Irreducibility +9 unanimous** and **Compounding +5 unanimous** — its two
strongest axes, both maximal or near — and still lost, because Mutation won Mechanism +9
unanimous and every panel reached the same structural conclusion independently:

> **Skeptic:** *"A is a filter on the existing generative process that reliably moves you
> from #12 to #13 and structurally never further, while B is a **different generative
> process**, which is what the frame says reaching #99 requires; A wins my own bias axis
> and I still vote against it on this ground."*

That is the second bias-defying vote of the tournament, and on the axis the Skeptic exists
to defend.

**What is absorbed — narrowly scoped:** killed hybrids with a recorded cause of death.
**Not** Failure Archaeology's full claim over every rejected idea in the repo.

> **Ecologist:** *"A breeding program with no record of what died is not performing
> selection; it is performing memoryless random search over a finite seed space it will
> re-draw forever."*
>
> **Builder:** *"B already contains a kill step whose corpses currently vanish… evolution
> without differential survival memory is drift, not selection."*

**Dissent preserved (Skeptic):** under the governing frame, efficiency is explicitly not
the goal. Re-rolling a combination that died is *waste*, not a defect — *"B gets slower,
not worse."* The deletion test, honestly applied, turns on whether wasted draws count as
harm in a project that has disclaimed efficiency. Reasonable people differ.

**Advances as THE BREEDING PROGRAM.**

### Ruling 8 — Game 12: OVERRULE + ENTRANT AMENDED
**Panel result:** Telegram Constraint 18, Homogeneity Auditor 11 on the five-axis
aggregate. Panels split **1–2 the other way**: Builder for the Telegram, Skeptic and
Ecologist for the Auditor. CONTESTED on aggregate-versus-majority.

**Ruling:** **The Homogeneity Auditor advances**, with the commissioner siding with the
panel majority over the aggregate — the same call as Ruling 1, and again a ruling rather
than a precedent.

**Entrant amended, per the Ecologist's identified edit:**

> *"The residual is the process boundary; it would be nearer 15% if the auditor were
> denied sight of the real output, **which is the single edit that would most improve this
> entry**."*

The auditor currently receives the near-final output *before* reconstructing the median it
will be compared against — so the instrument is coupled to the thing it measures. Blinding
it also answers the Builder's dissent directly, which was that the gate is *"applied by
the same model that wrote the text, reading text it has already seen."*

**Advances as THE BLIND AUDITOR:** *"A separate agent that has never seen the real output
reconstructs the answer an unskilled model would give; any section of the real output that
overlaps it is rejected and regenerated."*

**This ruling settles the open question about amending entrants mid-tournament.** An
entrant may be amended when a panel identifies a specific improving edit, the edit serves
the entrant's existing thesis, and the amendment is recorded here with its source.

**Defect carried forward, unaddressed by the amendment (Skeptic):**

> *"The Auditor's gate cannot distinguish 'median because unimaginative' from 'median
> because correct.' It rejects overlap, and correct-and-obvious answers overlap by
> definition, so it systematically punishes right answers for being reachable."*

Blinding the auditor does not fix this. It is the sharpest open objection to the Sweet 16's
newest entrant and should be resolved before it advances further.

---

## Three defects the panels found in the field itself

These are authoring defects in how entrants were written, not findings against the ideas.
Recorded because a future session will otherwise re-inherit them silently.

**1. Persona Toolbelts names two tools that are not tools.** `bin/claims` and
`bin/who-benefits` are model judgments dressed as executables — *"a prompt wearing an
executable's name."* The entrant's whole claim is that a mandatory tool run replaces an
assertion with an observation; that holds only when the tool is a genuine outside source of
fact. Four of six are. The other two launder a model judgment into apparent measurement,
which is worse than stating the judgment plainly.

**2. Stochastic Persona Fracture cites a fault line that does not exist.** The Skeptic
checked `roster/franciscan-monk.md` and found no "simplicity against obligation to the
poor" tension named anywhere in it — the profile states five Core Principles and four
Anti-Patterns and no conflict between them. The entrant's *"named in its own profile"* is a
sourcing claim that fails on inspection. The panel added that this is a finding about the
**repo**, not just the entrant: every roster file resolves its principles into mutual
non-conflict, which real practitioners do not do.

**3. Make the Problem Strange First overstates its own claim.** *"Removing the nouns
removes the priors"* is false as stated, because verbs and adjectives carry priors too:
*"Users **game** the leaderboard to gain **unearned** status"* becomes *"ENTITY_A **games**
MECHANISM_B to gain **unearned** status"* — and the prior survives. The entrant advanced
anyway, 30–2, but its stated mechanism is broader than its real one.

---

## Round of 32 · Bracket 4 (UFO) — round complete

### Ruling 9 — Game 13: ABSORPTION RATIFIED 3–0
**Panel result:** The Grudge Ledger 29, The 19th Way 1. Unanimous, and the **only
unanimous absorption of the tournament** — all three panels independently selected the
same mechanism and passed it on all three tests without seeing each other.

The 19th Way scored **one point across five axes**, all three panels placing it at or near
the Irreducibility floor for the same reason: it is its own prompt. A base model handed the
instruction verbatim reproduces 70–95% of it.

**Ruling:** absorption accepted. **The non-adjacency test only** — the count of 19 and the
mediocrity-as-toll argument stay behind, as all three panels specified.

> **Ecologist:** *"A's rule is 'you may not restate any of these' with no definition of
> 'restate,' which leaves the ledger self-graded; the four axes supply exactly that
> definition and add no second claim."*
>
> **Builder:** *"A rule that appears to bind and does not is the worst state of the three."*
>
> **Skeptic:** *"the rare absorption where the loser supplies the missing predicate of the
> winner's own rule."*

**Merged definition:** *"A persona is handed its own past claims and may not restate any of
them, where 'restate' means failing to differ in mechanism, actor, failure mode, or
timescale."*

**Advances as THE ADJUDICATED LEDGER.**

**Carried defect — the ledger does not exist.** All three panels checked: no `ledger/`
directory, and nothing named that would write it. Recorded on the entrant in
`field-of-32.md`. This entrant reached the Sweet 16 on a promise.

### Ruling 10 — Game 16: OBLIQUE DECK ADVANCES
**Panel result:** The Oblique Deck 15, Scarcity Economy 10. Panels 2–1 for the Deck;
aggregate agrees. CONTESTED on the panel split.

**Ruling:** **The Oblique Deck advances. Scarcity Economy to the wildcard bench.**

**Note for the record:** the dissenting Ecologist wrote the sharpest argument *against its
own pick*, and it belongs in the bench entry rather than being lost —

> *"'Contrarian — balance 0, RETIRED.' The persona whose entire function is disagreement is
> the persona most often marked noise… personas optimize for what gets marked decisive,
> which is a reinforcing loop toward the user's own taste. A mechanism sold as 'economize
> on relevance' will in practice teach personas to economize on **approval**, and an
> approval-selected roster converges on the median-of-this-user answer. That is
> homogenization with a ledger attached."*

**Carried defect on the winner:** the Deck's corpus claim is overstated. Only 16 of 24
specialists have a `positions.md`; of its three sample cards, one fairly distils real text,
one appears in no `positions.md`, and one appears **nowhere in the repo**. The real corpus
is ~139 bullets across 16 files, and the Contrarian — the designated default lens — has no
pack at all. Tracked in issue #21.

### Games 14 and 15 — no ruling required
| Game | Result | Note |
|---|---|---|
| G14 | **The Voice Oracle** 31, Reverse Brief 0 | A shutout. Every panel at the Irreducibility **ceiling** — the only entrant in 32 that changes weights. Parked as a future state in issue #21 |
| G15 | **Notation Transposition** 19, Temperature Choreography 16 | Unanimous on the winner, closest unanimous game of the round |

---

## Two claims verified against the repo

The panels made claims about this repo rather than about entrants. Both were checked
directly rather than taken on the panel's word.

### VERIFIED — the roster resolves all internal tension

The Skeptic checked one profile (`roster/franciscan-monk.md`) and found no tension named
between its own principles. Checked across the whole roster: **0 of 24 built profiles name
any internal tension, conflict, or trade-off within their Core Principles.** Six files use
words like "tension" elsewhere — in methodology or voice, describing tension the specialist
observes *in others* — but none names a fault line inside its own commitments.

This is a repo problem independent of the tournament, and a significant one. A profile
whose principles never conflict is not a person; it is a checklist. Real practitioners are
constituted by their unresolved tensions — the farmer's patience against the season's
deadline, the journalist's duty to publish against the duty to protect a source. The
current profiles have had exactly that removed, which is plausibly a direct cause of the
smoothness this whole tournament exists to fight.

**Recommended, not ruled:** add a required `## Internal Tensions` section to
`roster/TEMPLATE.md` naming at least two of the profile's own principles that pull against
each other, and backfill the 24. This is worth doing whatever wins the bracket.

### CHECKED — the Skeptic's charge against the format is not holding up

The charge: *"32 entrants with a refusal-by-default absorption rule means 24 of them
contribute nothing at all."* At 12 of 16 R32 games judged, with 13 entrants eliminated:

| Contribution | Count | Which |
|---|---|---|
| Mechanism absorbed into a winner | 3 | Persona Grammar, Constraint Compiler, Failure Archaeology |
| Held on the wildcard bench as a live option | 5 | Committee of Strangers, Collaboration Contract, Constraint Compiler, Anti-Roster, Telegram Constraint |
| Panel flagged a component as "worth building separately" | 2 | Committee of Strangers (priced defection), Persona Fracture (disagreement from differing evidence) |
| **Contributed nothing recorded** | **4** | Novelty Gate, Idea Bankruptcy, The Ratchet, Bracket as a Primitive |

**Four of thirteen eliminated entrants have contributed nothing — not twenty-four of
thirty-two.** The charge assumed absorption was the only contribution channel. It is not:
the bench, the orthogonal list, and the "build separately" flag are three more, and they
have carried nine entrants between them.

The charge is **not dismissed** — a 4/13 waste rate is real, the cost per matchup is real,
and the Ecologist's separate prediction that judge attention does not scale was confirmed
by this session pausing twice. But the specific quantitative claim is now measured and
wrong by a factor of five.

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
| The Committee of Strangers | R32 · G10 | Lost 30–2 as specified (5–7 bodies). Held for the **committee-of-3** variant — see note below |
| The Scarcity Economy | R32 · G16 | Only entrant in its matchup whose state differs at use #10 — but its own dissenting judge showed the selection pressure runs toward user approval, retiring the personas whose friction is the product |
| The Telegram Constraint | R32 · G12 | Won the aggregate 18–11 and lost to a commissioner overrule. Its failure mode is the most valuable object in its packet: an all-hedges telegram is a diagnostic on the **roster**, not on the pass |
| ~~The Understudy~~ | *revived* | Took the G8 Sweet 16 slot |

**Note on the Committee of Strangers (commissioner):** the entrant lost as written — five
to seven bodies with coalitions, defection and minority reports — and lost badly. The
commissioner holds it for a narrower variant at **three** bodies, on evidence generated by
this tournament itself: the three-panel structure judging these games *is* a committee of
strangers, and it has worked. Independent convergence between isolated panels has been the
single most reliable signal in the run. The 5–7 body version was blown out; the 3-body
version is running the tournament.

Two mechanisms the panels explicitly flagged as **worth building separately** rather than
merging, which belong with this note:
- **Priced defection** (Ecologist, G10): *"a price is a falsifiable commitment a persona
  can be held to later, which is the only thing in this matchup that could ever become a
  stock."*
- **Disagreement sourced from differing evidence** (Ecologist, G9): two transforms, two
  halves, two documents — *"a different and better object than disagreement sourced from
  instructed tension, and only the first is un-simulatable."*

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

## Sweet 16 field — COMPLETE (16 of 16 R32 games judged)

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
| **Lens Transformers** | Moat G9 | 37–2, the widest margin of the tournament |
| **Make the Problem Strange First** | Moat G10 | 30–2 unanimous, defect noted |
| **The Breeding Program** | Moat G11 | 17–14, absorption ratified 2–1 |
| **The Blind Auditor** | Moat G12 | Commissioner overrule, entrant amended |
| **The Adjudicated Ledger** | UFO G13 | 29–1, absorption ratified 3–0 |
| **The Voice Oracle** | UFO G14 | 31–0 shutout |
| **Notation Transposition** | UFO G15 | 19–16 unanimous |
| **The Oblique Deck** | UFO G16 | 15–10, panels 2–1, defect noted |

*(The Moat and UFO rows were ruled above but never added to this table; filled in
2026-08-26 from the rulings on this page. No result changed.)*

**Round of 32 complete.** All 16 games judged by three blind panels and ruled. Next round
is the **Sweet 16** — 8 games, field above, bracket not yet drawn.

Per-entrant status, what each winner absorbed, and what the repo would need to build each
one are recorded on the entrants themselves in `field-of-32.md`, whose front matter also
carries a shared-gap table and a list of collisions worth deciding on before the draw.

## Open items carried into the Sweet 16

1. **The Blind Auditor** cannot distinguish "median because unimaginative" from "median
   because correct." A fix has been proposed (have the blind auditor annotate each claim in
   its reconstructed median as *forced* or *chosen*, and reject overlap only on *chosen*
   claims) and **approved by the commissioner**, but is untested.
2. **The Adjudicated Ledger** names a `ledger/` directory that does not exist and no writer
   for it.
3. **The Oblique Deck's** corpus is one-third hand-authored, and the designated default
   lens has no pack.
4. **Persona Toolbelts** ships two tools that are prompts in costume.
5. **Make the Problem Strange First** overstates its mechanism — verbs and adjectives carry
   priors too.

Five of the sixteen survivors carry a known defect into the next round. That is worth
knowing before seeding.
