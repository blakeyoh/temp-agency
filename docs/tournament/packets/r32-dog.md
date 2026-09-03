# Judging Packet — Bracket 2 of 4

Four matchups. For each, decide which idea is more creative on each of the five
axes, using the reference sets in `docs/tournament/reference-sets.md`.

You are not told which idea is favored, where either sits in the bracket, who
wrote either, or what any other reviewer thinks. Judge only what is on this page.


---

## MATCHUP 5

### IDEA A — Temporal Displacement

Every persona is silently contemporary. Date them. A --era flag instantiates the specialist at a specific year with only that year's primitives. A 1911 systems thinker has no feedback-loop vocabulary and must reach for hydraulics, railway signalling, and stockyards. A 2140 one has vocabulary we have not invented and must invent it. The anachronism forbids retrieval and forces re-derivation.

**Its claim about why output is homogeneous:** a model will happily write in a period style while keeping every modern concept. This forbids the concept, not the diction — a much harder constraint.

### IDEA B — The Constraint Compiler

bin/compile-constraints <slug> reads a profile's Anti-Patterns and Voice sections and emits a machine-checkable constraint set: banned n-grams, required section shapes, a minimum count of domain-specific nouns, a forbidden-hedge list. Constraints are injected as hard rules and verified post-hoc by a linter — compliance is checked, not trusted.

**Its claim about why output is homogeneous:** the profile currently describes its anti-patterns in prose the model may or may not honor under pressure. A compiled, checked constraint is enforced.


---

## MATCHUP 6

### IDEA A — The Entropy Well

Randomness in this repo is currently rhetorical. Make it literal, seeded, and auditable. bin/draw is a real PRNG that emits a seed; every stochastic choice in a dispatch — which lead, which lens, which constraint card, which mutation — derives from that one seed. The seed is stamped in the output header. Same seed, same world; no seed, a different world. Creativity becomes reproducible, and therefore debuggable.

**Its claim about why output is homogeneous:** models simulate randomness by reaching for the most-likely random-sounding option. A real PRNG has no favorite number.

### IDEA B — The Anti-Roster

A persona defined entirely by refusal. anti-roster/<slug>.md contains no principles, no methodology, no voice — only a prohibition list: two hundred phrases, moves, and framings this persona may not use. The anti-monk cannot say simplicity, enough, presence, creation, or poverty. Stripped of its vocabulary, the persona must find its position again from somewhere else, and the somewhere-else is the product.

**Its claim about why output is homogeneous:** given a persona, a model reaches first for that persona's signature vocabulary. Banning the vocabulary bans the shortcut.


---

## MATCHUP 7

### IDEA A — The Ratchet

Monotonic creativity: the floor only rises. Every accepted output sets a novelty floor, and nothing may be accepted afterward that scores below it on the same axis. The bar moves up permanently and never down. When the ratchet locks — when nothing can clear the floor — that is the signal to change the mechanism, not to lower the bar.

**Its claim about why output is homogeneous:** quality bars drift downward under deadline pressure, invisibly. A ratchet that cannot descend converts silent drift into an explicit, dated crisis.

### IDEA B — The Hostile Environment

Personas currently work in a laboratory. Put them in weather. The harness injects real adverse conditions: a key fact is withheld from context; a stakeholder statement in the brief is a deliberate lie; a hard token deadline cuts the pass short; a "budget cut" removes the persona's best tool mid-task. A persona's response to degradation differs from its response to comfort, and the difference reveals its actual priorities.

**Its claim about why output is homogeneous:** models reason about hypothetical constraints while retaining full capability. A fact genuinely absent from context cannot be reasoned around.


---

## MATCHUP 8

### IDEA A — Adversarial Collaboration Contract

Make disagreement falsifiable and dated. Before the work ships, lead and lens co-sign a written prediction: "If the lens is right, X will be observable by date D; if the lead is right, Y." It is recorded in bets/ with a resolution date, and the repo periodically resolves them. Personas accumulate track records, and one that is consistently wrong loses standing.

**Its claim about why output is homogeneous:** model disagreements evaporate the moment the session ends. A dated, resolvable bet makes them accountable — and, more importantly, forces the disagreement to be about something observable.

### IDEA B — Bracket as a Primitive

The tournament is not a one-off; it is the repo's core operation. /bracket <question> --field 32 generates a field, seeds it, runs single-elimination with an absorption rule — the winner takes the loser's strongest mechanism — and emits a box score. Absorption is what distinguishes this from ranking: ranking discards, absorption compounds, and the champion is a chimera that no round-one entrant resembles.

**Its claim about why output is homogeneous:** models rank, and ranking throws away everything below the top. A bracket with absorption forces combination, and combination is where non-obvious ideas live.
