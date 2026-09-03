# Judging Packet — Bracket 4 of 4

Four matchups. For each, decide which idea is more creative on each of the five
axes, using the reference sets in `docs/tournament/reference-sets.md`.

You are not told which idea is favored, where either sits in the bracket, who
wrote either, or what any other reviewer thinks. Judge only what is on this page.


---

## MATCHUP 13

### IDEA A — The Grudge Ledger

A persona that repeats itself has stopped being a specialist and become a macro. Every position a persona takes is appended to ledger/<slug>.jsonl as a canonical claim statement. On future dispatch the persona is handed its own past positions with one rule: you may not restate any of these; you may extend, reverse, or refuse. The persona must grow or explicitly recant.

**Its claim about why output is homogeneous:** every session starts fresh, so the persona reaches for its signature move forever. A persistent ledger makes the signature move unavailable after its first use.

### IDEA B — The 19th Way

The persona produces 19 improvements to the plan, and each must fail a stated relatedness test against all previous ones — different mechanism, different actor, different failure mode, different timescale. Idea 12 cannot be idea 3 with a new noun. The persona declares the axis on which each is unrelated. Ideas 1–6 will be mediocre; that mediocrity is the toll paid to reach 19.

**Its claim about why output is homogeneous:** asked for 19 ideas, a model produces four real ones and fifteen rephrasings. The non-adjacency test is what makes the 19 cost something.


---

## MATCHUP 14

### IDEA A — The Reverse Brief

Derive the question the answer is actually answering. After producing a recommendation, the persona writes the problem statement for which that recommendation would be the perfect answer, then diffs it against the real problem. The gap is a first-class output. Very often, the recommendation turns out to be a perfect answer to a problem nobody has.

**Its claim about why output is homogeneous:** models validate answers against the question. This inverts the arrow and exposes the reframing that was smuggled in during the answering.

### IDEA B — The Voice Oracle

Decouple voice from problem-solving so voice cannot be smoothed away. A tiny fine-tuned model (Qwen3-0.6B/1.7B class) is trained on the persona's knowledge/ pack plus synthetic in-character dialogue, and its only job is to produce persona-voice reactions — never solutions. The large model solves; the small model reacts in character; the large model must respond to the reaction. The small model is too small to be diplomatic, and that is the feature.

**Its claim about why output is homogeneous:** a large aligned model regresses toward its house voice under any pressure. Separate weights cannot regress toward a house they do not have.


---

## MATCHUP 15

### IDEA A — Notation Transposition

Force the position through a notation that cannot hold prose — a recipe, a court docket, a knitting pattern, a chess annotation, a liturgical rubric, a flight checklist, a circuit diagram — and only then translate back. The notation's structural requirements make commitments prose lets you skip: a recipe demands quantities and an order; a docket demands parties, a motion, and a ruling; a checklist demands a challenge and a response.

**Its claim about why output is homogeneous:** models translate prose into diagrams, preserving the prose's evasions. Authoring the notation first makes the gaps structural and visible.

### IDEA B — Temperature Choreography

The sampling schedule is currently invisible and flat. Choreograph it into three movements. HOT: many short high-variance samples, quantity mandated, no quality filter permitted. COLD: a separate agent that may only prune, never generate. AUDIT: a third agent that verifies at least one survivor came from the top decile of weirdness in the HOT pass — if the weirdest survivor is missing, the whole pass reruns.

**Its claim about why output is homogeneous:** a single pass silently converges and no one can see what it discarded. Separating generation from judgment makes the discard auditable.


---

## MATCHUP 16

### IDEA A — Scarcity Economy

Personas speak for free, so they always speak. Give each a finite lifetime token budget recorded in the repo. Being staffed costs; speaking costs by the word. A persona whose contribution the user marks as noise pays a penalty; one marked decisive earns. Personas bid to be staffed, and the bid is a one-line claim of what they will see that no one else will. Bankrupt personas retire.

**Its claim about why output is homogeneous:** nothing in a prompt makes a model economize on relevance. A real ledger with a real balance does.

### IDEA B — The Oblique Deck

Brian Eno's Oblique Strategies, compiled from this repo's own roster and obeyed literally. Every knowledge//positions.md is distilled into single-line imperatives — "Ask what the soil requires." "Name who pays and isn't in the room." "Restart from the last honest state." One card is drawn per pass, and the persona must obey it literally even when it is a bad fit. The friction of a card that doesn't belong is the generator.

**Its claim about why output is homogeneous:** a model given a suggestion applies it where it fits and quietly drops it where it doesn't. Literal obedience to a bad-fit instruction is not a default behavior.
