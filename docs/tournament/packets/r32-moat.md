# Judging Packet — Bracket 3 of 4

Four matchups. For each, decide which idea is more creative on each of the five
axes, using the reference sets in `docs/tournament/reference-sets.md`.

You are not told which idea is favored, where either sits in the bracket, who
wrote either, or what any other reviewer thinks. Judge only what is on this page.


---

## MATCHUP 9

### IDEA A — Lens Transformers

Make the lens a program that runs on the artifact, not a request to see it differently. Each persona ships transforms/<slug>.py, a deterministic text transformer applied to the artifact before the persona reads it. The investigative-journalist transform strips every assertion of its supporting clause and returns a numbered list of naked claims. The farmer transform re-sorts every line by how long it will still be true. The monk transform deletes every sentence containing a superlative. The persona reads only the transformed artifact.

**Its claim about why output is homogeneous:** "read this like a journalist" changes tone. Handing a model a document where every claim has been mechanically severed from its support changes what it can see.

### IDEA B — Stochastic Persona Fracture

Real experts contain contradictions; a persona file resolves them into a coherent voice. Mid-pass, the persona is forcibly bisected along a fault line named in its own profile — the farmer's patience against the farmer's seasonal deadline, the monk's simplicity against the monk's obligation to the poor. Two sub-personas argue, and the unresolved argument is part of the output. One roster entry, two disagreeing voices.

**Its claim about why output is homogeneous:** models resolve internal tension into a single coherent register. This forbids the resolution and ships the tension.


---

## MATCHUP 10

### IDEA A — Make the Problem Strange First

Defamiliarize the input, not the output. Before any persona sees the task, a transform strips its domain nouns and replaces them with variables: users → ENTITY_A, leaderboard → MECHANISM_B, cheating → BEHAVIOR_C. Personas reason about the abstracted structure, propose against it, and only afterward is the mapping restored. Solutions that worked only because of a noun's connotations die in the abstraction.

**Its claim about why output is homogeneous:** the model's domain priors fire on the nouns before reasoning begins. Removing the nouns removes the priors — you cannot pattern-match what you cannot name.

### IDEA B — The Committee of Strangers

Two voices average; five to seven voices form factions. Replace the dyad with an N-body deliberation carrying explicit political mechanics: a proposal needs a second, a defection must state its price, and a minority report is preserved verbatim in the output. Positions no single persona holds emerge from coalition-forming.

**Its claim about why output is homogeneous:** naive multi-agent prompting converges to consensus. Coalition and defection rules make the disagreement itself the output format.


---

## MATCHUP 11

### IDEA A — Failure Archaeology

Keep the dead. Every rejected idea, losing bracket entrant, and abandoned plan is preserved in graveyard/ with a cause of death. It becomes mandatory reading before new work: a new proposal must either differ from the graveyard or explicitly resurrect — stating what changed to make the dead idea live. The repo accumulates a negative space as informative as its positive one.

**Its claim about why output is homogeneous:** models do not remember what did not work. A graveyard turns the repo's own failures into a constraint on its future.

### IDEA B — Roster Mutation

Personas breed. bin/breed <a> <b> --seed N performs structural crossover on two profiles — Principles from A, Methodology from B, Anti-Patterns interleaved — then applies point mutations: reverse a principle's polarity, delete a methodology phase, import a foreign Voice register. The child is a one-off used for a single task, scored, then promoted to roster/f1/ or killed. The roster evolves instead of being authored.

**Its claim about why output is homogeneous:** asked to combine two personas, a model averages toward the generic. Structural crossover with mutation produces combinations no author would choose.


---

## MATCHUP 12

### IDEA A — The Telegram Constraint

Make expression cost something per unit. The persona delivers under a priced medium: a 1904 telegram at one dollar per word against a forty-dollar budget; a single index card; a thirty-second voicemail; a woodblock with a fixed glyph count. The economics of the medium, not a word-limit instruction, decide what survives — and what a persona sacrifices under real cost reveals what it actually believes.

**Its claim about why output is homogeneous:** models treat "be concise" as a style note and compress uniformly. A priced budget is an optimization problem with a different, revealing solution.

### IDEA B — The Homogeneity Auditor

Name the median answer out loud so it cannot be delivered. A dedicated adversarial subagent receives the near-final output and produces exactly one artifact: "Here is the answer a competent model with no skill installed would have given." If the auditor's reconstruction overlaps the real output past a threshold, the overlapping sections are rejected and regenerated. The auditor never proposes; it only accuses.

**Its claim about why output is homogeneous:** a model cannot see its own median from inside. A separate agent explicitly generating the median makes it visible and therefore avoidable.
