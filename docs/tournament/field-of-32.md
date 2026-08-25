# The Field of 32

> **Premise.** In a creative workshop, groups are asked for 100 ways to protect a home.
> The first ten are a fence, a dog, a camera. The last ten are a moat and a UFO. The
> value is not in the moat — it is in the fact that reaching idea #99 *requires* a
> different generative process than reaching idea #3.
>
> temp-agency v2 reliably reaches idea #12: a competent lead, a competent lens, a
> disagreement that is genuinely useful and entirely legible. The evidence gate proved
> the lens changes decisions. It did not prove the lens produces anything *strange*.
> This field is 32 mechanisms for pushing the repo from #12 to #99.

**Provenance:** entries marked ◆ are the owner's, expanded where flagged as vague enough
to split. Entries marked ◇ are generated to fill the field to 32.

**Distinctness rule:** no two entries may share a primary mechanism. Several entries
attack the same target (the model's prior) but must do so by different means —
prohibition, entropy, execution, and memory are four different means, and the field is
organized around them.

---

## ENTROPY REGION
*Mechanisms that inject genuine randomness or genuine outside material into the process.
The shared enemy: a model asked to "be random" retrieves the most-likely random-seeming
answer from its own prior.*

### E1 · The Entropy Well ◆
*(owner idea 2, split: "scripts and shells")*

Randomness in this repo is currently rhetorical. Make it literal, seeded, and auditable.
`bin/draw` is a real PRNG that emits a seed; every stochastic choice in a dispatch —
which lead, which lens, which constraint card, which mutation — derives from that one
seed. The seed is stamped in the output header. Same seed, same world; no seed, a
different world. Creativity becomes reproducible, and therefore debuggable.

**Not native:** models simulate randomness by reaching for the most-likely
random-*sounding* option. A real PRNG has no favorite number.

### E2 · Cross-Repo Foraging ◇

Import a real object from outside, not a remembered one. Before the persona speaks, the
harness fetches one concrete external artifact — a random file from an unrelated local
repo, a random paragraph from the persona's own `knowledge/canon.md`, a random line from
a book, a random Wikipedia page. The persona must make it **load-bearing**: if the
foraged object appears only in the opening paragraph and does no work thereafter, the
pass is rejected.

**Not native:** a model asked to bring in something unexpected retrieves from its own
priors. Genuinely foraged text is outside the prior by construction.

### E3 · The Wrong Expert on Purpose ◇

The weirdness currently lives in the LENS, and the LENS is the junior role. Invert it.
Staff the *least* relevant specialist as LEAD and let the domain-appropriate expert be
the LENS. The soccer referee leads the database migration; the systems thinker gets to
object. The wrong expert has to derive the whole answer from their own primitives, and
that derivation is where non-obvious structure comes from.

**Not native:** the model's strongest reflex is domain-appropriate matching. This is a
deliberate defeat of that reflex, at the position of maximum authority.

### E4 · Roster Mutation ◇

Personas breed. `bin/breed <a> <b> --seed N` performs structural crossover on two
profiles — Principles from A, Methodology from B, Anti-Patterns interleaved — then
applies point mutations: reverse a principle's polarity, delete a methodology phase,
import a foreign Voice register. The child is a one-off used for a single task, scored,
then promoted to `roster/f1/` or killed. The roster evolves instead of being authored.

**Not native:** asked to combine two personas, a model averages toward the generic.
Structural crossover with mutation produces combinations no author would choose.

### E5 · Temporal Displacement ◇

Every persona is silently contemporary. Date them. A `--era` flag instantiates the
specialist at a specific year with **only that year's primitives**. A 1911 systems
thinker has no feedback-loop vocabulary and must reach for hydraulics, railway
signalling, and stockyards. A 2140 one has vocabulary we have not invented and must
invent it. The anachronism forbids retrieval and forces re-derivation.

**Not native:** a model will happily write in a period *style* while keeping every modern
concept. This forbids the concept, not the diction — a much harder constraint.

### E6 · The Oblique Deck ◇

Brian Eno's *Oblique Strategies*, compiled from this repo's own roster and obeyed
**literally**. Every `knowledge/*/positions.md` is distilled into single-line imperatives
— "Ask what the soil requires." "Name who pays and isn't in the room." "Restart from the
last honest state." One card is drawn per pass, and the persona must obey it literally
*even when it is a bad fit*. The friction of a card that doesn't belong is the generator.

**Not native:** a model given a suggestion applies it where it fits and quietly drops it
where it doesn't. Literal obedience to a bad-fit instruction is not a default behavior.

### E7 · Stochastic Persona Fracture ◇

Real experts contain contradictions; a persona file resolves them into a coherent voice.
Mid-pass, the persona is forcibly bisected along a fault line named in its own profile —
the farmer's patience against the farmer's seasonal deadline, the monk's simplicity
against the monk's obligation to the poor. Two sub-personas argue, and the **unresolved**
argument is part of the output. One roster entry, two disagreeing voices.

**Not native:** models resolve internal tension into a single coherent register. This
forbids the resolution and ships the tension.

### E8 · Temperature Choreography ◆
*(owner idea 4, split: "workflows to force creativity")*

The sampling schedule is currently invisible and flat. Choreograph it into three
movements. **HOT:** many short high-variance samples, quantity mandated, no quality
filter permitted. **COLD:** a separate agent that may only prune, never generate.
**AUDIT:** a third agent that verifies at least one survivor came from the top decile of
weirdness in the HOT pass — if the weirdest survivor is missing, the whole pass reruns.

**Not native:** a single pass silently converges and no one can see what it discarded.
Separating generation from judgment makes the discard auditable.

---

## CONSTRAINT REGION
*Mechanisms that force creativity by taking something away. The shared enemy: the model's
signature move, which is always available and therefore always taken.*

### C1 · The 19th Way ◆
*(owner idea 1)*

The persona produces 19 improvements to the plan, and each must **fail a stated
relatedness test** against all previous ones — different mechanism, different actor,
different failure mode, different timescale. Idea 12 cannot be idea 3 with a new noun.
The persona declares the axis on which each is unrelated. Ideas 1–6 will be mediocre;
that mediocrity is the toll paid to reach 19.

**Not native:** asked for 19 ideas, a model produces four real ones and fifteen
rephrasings. The non-adjacency test is what makes the 19 cost something.

### C2 · The Anti-Roster ◇

A persona defined entirely by refusal. `anti-roster/<slug>.md` contains no principles, no
methodology, no voice — only a prohibition list: two hundred phrases, moves, and framings
this persona may not use. The anti-monk cannot say *simplicity*, *enough*, *presence*,
*creation*, or *poverty*. Stripped of its vocabulary, the persona must find its position
again from somewhere else, and the somewhere-else is the product.

**Not native:** given a persona, a model reaches first for that persona's signature
vocabulary. Banning the vocabulary bans the shortcut.

### C3 · Idea Bankruptcy ◇

You may not deliver anything from your own first quartile. The persona generates N ideas;
the first N/4 are **destroyed unread** by the harness before any synthesis agent sees
them. Not deprioritized — deleted. The persona is told this in advance, which changes
what it generates from the first token.

**Not native:** models front-load their best-known answer. Guaranteed destruction of the
front-load makes producing the front-load pointless.

### C4 · The Telegram Constraint ◇

Make expression cost something per unit. The persona delivers under a **priced medium**: a
1904 telegram at one dollar per word against a forty-dollar budget; a single index card; a
thirty-second voicemail; a woodblock with a fixed glyph count. The economics of the
medium, not a word-limit instruction, decide what survives — and what a persona sacrifices
under real cost reveals what it actually believes.

**Not native:** models treat "be concise" as a style note and compress uniformly. A priced
budget is an optimization problem with a different, revealing solution.

### C5 · Notation Transposition ◇

Force the position through a notation that cannot hold prose — a recipe, a court docket, a
knitting pattern, a chess annotation, a liturgical rubric, a flight checklist, a circuit
diagram — and only then translate back. The notation's structural requirements make
commitments prose lets you skip: a recipe demands quantities and an order; a docket demands
parties, a motion, and a ruling; a checklist demands a challenge and a response.

**Not native:** models translate prose *into* diagrams, preserving the prose's evasions.
Authoring the notation *first* makes the gaps structural and visible.

### C6 · The Constraint Compiler ◆
*(owner idea 2, split: "text transformers")*

`bin/compile-constraints <slug>` reads a profile's Anti-Patterns and Voice sections and
emits a machine-checkable constraint set: banned n-grams, required section shapes, a
minimum count of domain-specific nouns, a forbidden-hedge list. Constraints are injected
as hard rules *and* verified post-hoc by a linter — compliance is checked, not trusted.

**Not native:** the profile currently *describes* its anti-patterns in prose the model may
or may not honor under pressure. A compiled, checked constraint is enforced.

### C7 · Persona Grammar ◇

Stop trusting vibes; write a parser. Each persona gets a formal output grammar (BNF/PEG).
The investigative journalist's grammar requires every claim node to carry a `SOURCE` child
or be tagged `TIP`. The nuclear operator's requires every action node to carry `LIMIT`,
`INDICATION`, and `STOP` children. Output that fails to parse is rejected and regenerated.
The epistemology becomes syntactically enforced.

**Not native:** a model asked to cite sources cites some. A parser that rejects an
unparented claim node makes the citation structural rather than aspirational.

### C8 · Make the Problem Strange First ◇

Defamiliarize the **input**, not the output. Before any persona sees the task, a transform
strips its domain nouns and replaces them with variables: *users* → `ENTITY_A`,
*leaderboard* → `MECHANISM_B`, *cheating* → `BEHAVIOR_C`. Personas reason about the
abstracted structure, propose against it, and only afterward is the mapping restored.
Solutions that worked only because of a noun's connotations die in the abstraction.

**Not native:** the model's domain priors fire on the nouns before reasoning begins.
Removing the nouns removes the priors — you cannot pattern-match what you cannot name.

---

## APPARATUS REGION
*Mechanisms that make the repo executable — code, weights, tools, topology. The shared
enemy: markdown that asks a model to behave differently and hopes.*

### A1 · Lens Transformers ◆
*(owner idea 2, split: "Python libraries to more strictly adopt the lens")*

Make the lens a **program that runs on the artifact**, not a request to see it
differently. Each persona ships `transforms/<slug>.py`, a deterministic text transformer
applied to the artifact *before* the persona reads it. The investigative-journalist
transform strips every assertion of its supporting clause and returns a numbered list of
naked claims. The farmer transform re-sorts every line by how long it will still be true.
The monk transform deletes every sentence containing a superlative. The persona reads only
the transformed artifact.

**Not native:** "read this like a journalist" changes tone. Handing a model a document
where every claim has been mechanically severed from its support changes what it can see.

### A2 · The Voice Oracle ◆
*(owner idea 3)*

Decouple voice from problem-solving so voice cannot be smoothed away. A tiny fine-tuned
model (Qwen3-0.6B/1.7B class) is trained on the persona's `knowledge/` pack plus synthetic
in-character dialogue, and its **only** job is to produce persona-voice reactions — never
solutions. The large model solves; the small model reacts in character; the large model
must respond to the reaction. The small model is too small to be diplomatic, and that is
the feature.

**Not native:** a large aligned model regresses toward its house voice under any pressure.
Separate weights cannot regress toward a house they do not have.

### A3 · Persona Toolbelts ◆
*(owner idea 2, split: "scripts and shells")*

An expert is partly defined by the tools they reach for. Each persona owns a small set of
real CLI tools it **must** run and cite. The journalist gets `bin/claims`,
`bin/who-benefits`, and `git log --follow`. The farmer gets `bin/churn` (which files have
been touched most over two years) and `bin/seasons` (commit cadence by month). The
physicist gets `bin/units` and `bin/orders`. The output must include the invocation and
its raw result. No tool output, no pass.

**Not native:** models assert without measuring. A mandatory tool run replaces an
assertion with an observation.

### A4 · The Committee of Strangers ◇

Two voices average; five to seven voices form factions. Replace the dyad with an N-body
deliberation carrying explicit political mechanics: a proposal needs a second, a defection
must state its price, and a minority report is preserved verbatim in the output. Positions
no single persona holds emerge from coalition-forming.

**Not native:** naive multi-agent prompting converges to consensus. Coalition and
defection rules make the disagreement itself the output format.

### A5 · The Hostile Environment ◇

Personas currently work in a laboratory. Put them in weather. The harness injects real
adverse conditions: a key fact is withheld from context; a stakeholder statement in the
brief is a deliberate lie; a hard token deadline cuts the pass short; a "budget cut"
removes the persona's best tool mid-task. A persona's response to degradation differs from
its response to comfort, and the difference reveals its actual priorities.

**Not native:** models reason *about* hypothetical constraints while retaining full
capability. A fact genuinely absent from context cannot be reasoned around.

### A6 · The Understudy ◇

The most interesting version of an expert is the person who watched them and got it
slightly wrong. Every persona has an understudy generated by deliberate degradation: it
has the methodology but not the judgment, applies phase 3 where phase 1 belongs,
over-uses the signature move, and misidentifies which principle is load-bearing. The
understudy runs alongside, and its errors are treated as proposals — applying a framework
where it doesn't belong is precisely what the left-fielder does on purpose.

**Not native:** a model asked to "make a mistake" makes a labeled, safe, obviously-wrong
mistake. A systematically degraded copy makes mistakes that have internal logic.

### A7 · Bracket as a Primitive ◆
*(owner idea 4, split: "workflows")*

The tournament is not a one-off; it is the repo's core operation. `/bracket <question>
--field 32` generates a field, seeds it, runs single-elimination with an **absorption
rule** — the winner takes the loser's strongest mechanism — and emits a box score.
Absorption is what distinguishes this from ranking: ranking discards, absorption
compounds, and the champion is a chimera that no round-one entrant resembles.

**Not native:** models rank, and ranking throws away everything below the top. A bracket
with absorption forces combination, and combination is where non-obvious ideas live.

### A8 · Scarcity Economy ◇

Personas speak for free, so they always speak. Give each a finite lifetime token budget
recorded in the repo. Being staffed costs; speaking costs by the word. A persona whose
contribution the user marks as noise pays a penalty; one marked decisive earns. Personas
**bid** to be staffed, and the bid is a one-line claim of what they will see that no one
else will. Bankrupt personas retire.

**Not native:** nothing in a prompt makes a model economize on relevance. A real ledger
with a real balance does.

---

## MEMORY REGION
*Mechanisms that use history, measurement, and accountability. The shared enemy: a fresh
context window, which lets the model make the same excellent point forever.*

### M1 · The Homogeneity Auditor ◆
*(owner idea 4, split: "evals")*

Name the median answer out loud so it cannot be delivered. A dedicated adversarial
subagent receives the near-final output and produces exactly one artifact: *"Here is the
answer a competent model with no skill installed would have given."* If the auditor's
reconstruction overlaps the real output past a threshold, the overlapping sections are
rejected and regenerated. The auditor never proposes; it only accuses.

**Not native:** a model cannot see its own median from inside. A separate agent
explicitly generating the median makes it visible and therefore avoidable.

### M2 · The Novelty Gate ◆
*(owner idea 4, split: "CI")*

CI should be able to fail a pull request for being boring. A GitHub Action runs the repo's
evals and computes a novelty score — semantic distance from an unstaffed baseline plus
lexical distinctness from the persona's own prior outputs. Below threshold, the check
fails, with the too-familiar passages annotated inline. Creativity becomes a build status.

**Not native:** nothing currently punishes a smoothed output. A red check does.

### M3 · The Grudge Ledger ◇

A persona that repeats itself has stopped being a specialist and become a macro. Every
position a persona takes is appended to `ledger/<slug>.jsonl` as a canonical claim
statement. On future dispatch the persona is handed its own past positions with one rule:
**you may not restate any of these; you may extend, reverse, or refuse.** The persona must
grow or explicitly recant.

**Not native:** every session starts fresh, so the persona reaches for its signature move
forever. A persistent ledger makes the signature move unavailable after its first use.

### M4 · Failure Archaeology ◇

Keep the dead. Every rejected idea, losing bracket entrant, and abandoned plan is preserved
in `graveyard/` with a cause of death. It becomes mandatory reading before new work: a new
proposal must either differ from the graveyard or **explicitly resurrect** — stating what
changed to make the dead idea live. The repo accumulates a negative space as informative as
its positive one.

**Not native:** models do not remember what did not work. A graveyard turns the repo's own
failures into a constraint on its future.

### M5 · The Idea-Space Map ◆
*(owner idea 4, split: "evals" — sharpened to coverage rather than score)*

Measure where the repo has **never** gone. Embed every output the repo has ever produced,
cluster them, and render a coverage map with the *empty regions labeled*. The deliverable
is not a score; it is a list of directions this repo has never once pointed. Future
dispatches are steered toward the voids. Exploration becomes navigable instead of hopeful.

**Not native:** a model has no view of its own output distribution. An external map of
what is missing is information it cannot generate from inside.

### M6 · The Ratchet ◇

Monotonic creativity: the floor only rises. Every accepted output sets a novelty floor, and
nothing may be accepted afterward that scores below it on the same axis. The bar moves up
permanently and never down. When the ratchet locks — when nothing can clear the floor —
that is the signal to change the mechanism, not to lower the bar.

**Not native:** quality bars drift downward under deadline pressure, invisibly. A ratchet
that cannot descend converts silent drift into an explicit, dated crisis.

### M7 · The Adversarial Collaboration Contract ◇

Make disagreement falsifiable and dated. Before the work ships, lead and lens co-sign a
written prediction: *"If the lens is right, X will be observable by date D; if the lead is
right, Y."* It is recorded in `bets/` with a resolution date, and the repo periodically
resolves them. Personas accumulate track records, and one that is consistently wrong loses
standing.

**Not native:** model disagreements evaporate the moment the session ends. A dated,
resolvable bet makes them accountable — and, more importantly, forces the disagreement to
be about something *observable*.

### M8 · The Reverse Brief ◇

Derive the question the answer is actually answering. After producing a recommendation, the
persona writes the problem statement for which that recommendation would be the *perfect*
answer, then diffs it against the real problem. The gap is a first-class output. Very
often, the recommendation turns out to be a perfect answer to a problem nobody has.

**Not native:** models validate answers against the question. This inverts the arrow and
exposes the reframing that was smuggled in during the answering.
