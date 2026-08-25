## MATCHUP 9
WINNER: A
DECIDED BY: A hands the persona a physically altered document it cannot un-alter, while B hands it an instruction not to resolve — and a resolved output looks identical to an unresolved one, so nothing catches the failure.

### Distance
VERDICT: A significantly better
REFERENCE: A sits at High — it does not forbid the problem's vocabulary but forbids its *support structure*, which is the same class of move applied one layer deeper; the persona reads a document whose evidence has been mechanically excised. B sits between Low and Mid: two voices arguing under one name is a staging change. The vocabulary is intact, the domain priors fire normally, and both halves reach the persona's ordinary conclusions.
PREDICATE: A forbids the journalist writing "this plan is well-supported — it cites the 2024 benchmark showing 40% improvement," because the citing clause was severed before the persona saw it; it also forbids the monk's review addressing the document's strongest claim, since the strongest claims are the superlative ones and those sentences were deleted from the input. B forbids "a single closing recommendation delivered in one farmer voice." Both nameable; A's forbidden set is structural, B's is cosmetic.

### Mechanism
VERDICT: A significantly better
REFERENCE: A sits at High and touches Ceiling — the persona "reads only the transformed artifact," which is not a checklist it self-verifies against but information removed without its consent. B has no position on this table at all; it is the Floor reference wearing technical vocabulary. The lens flags that "forcibly bisected" and "stochastic" are both asserted with no seed, no selector, and no artifact.
PREDICATE: A names `transforms/investigative-journalist.py`, `transforms/farmer.py`, `transforms/franciscan-monk.py`. The lead's honest audit: only the monk's runs deterministically (regex over a superlative wordlist). "Re-sort every line by how long it will still be true" requires a durability judgment no Python script makes — that file is a wrapper around the model it claims to bypass, which is this repo's own procedure-theater anti-pattern, and it caps A below Ceiling. B names no file, and the fault line is said to be "named in its own profile" when no roster entry has such a field. Scores as exhortation.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A is the High reference implemented — withholding from the context window, uncopyable by a model that has seen the whole document. B is the Low reference verbatim: hand the model a persona file, real but promptable.
PREDICATE: A — a base model given only `Read the attached document as an investigative journalist and list its unsupported claims.` reproduces about 15%, because it still sees every supporting clause and will silently reinstate it. B — a base model given only `You are the farmer from this profile. Split into two sub-personas along a tension in your own principles — patience against the seasonal deadline — argue, and do not resolve.` reproduces about 80%. Self-dialogue is a native register.

### Compounding
VERDICT: A slightly better
REFERENCE: A sits at Mid — a library of transforms that accumulates and, more interestingly, composes. B sits at Floor-to-Low: the fault lines live in the profiles, so they are fixed and exhaustible. Neither reaches High; no permitted-answer space narrows here, and A is weak on this axis in absolute terms.
PREDICATE: A — use #10 has ten transforms, and journalist∘monk produces naked claims with every superlative deleted, a view neither transform yields alone; use #1 produced one view. B — use #10 produces the farmer's patience-against-deadline argument again, because that fault line was written into the profile once. The same thing. That is the floor and I am calling it the floor.

### Generative failure
VERDICT: A significantly better
REFERENCE: A sits at High and argues toward Ceiling — the over-stripped artifact is itself a de facto claims audit. B sits at Floor: "the pass silently produces the default answer," reached by the most dangerous route, where failure is visually indistinguishable from success.
PREDICATE: A's failure output, verbatim, is the transformed artifact `1. Revenue grew. 2. The team was right. 3. It scaled.` followed by the persona replying "I cannot assess claims 1-3; none carries attached evidence." That names the hidden assumption: the artifact's persuasive force lived entirely in its subordinate clauses. B's failure output is `Ultimately the farmer holds both — patience *is* the discipline that meets the deadline.` A fluent synthesis in the final beat, which is exactly where the lens says the method gets exposed: the audience cannot tell a failed fracture from a successful one, and neither can a reviewer.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Mine each persona's profile for its internal contradiction and use that named fault line as the operator.
SAME-THESIS: FAIL — A's claim is that mechanical alteration of the *artifact* changes what a persona can see; B's is that models flatten *voice* into a coherent register. Importing the fault line makes A assert both. The charitable merge (apply two transforms to one document and hand the persona both views) does not need the persona's contradiction at all — any two transforms compose — which shows the fault-line part is the removable piece.
DELETION: FAIL — merely smaller. Delete fault-line-naming six months out and the transforms still run, still mutilate, still withhold. A loses a feature, not a capability.
ONE-SENTENCE: FAIL — "Each persona ships a deterministic transform that mutilates the artifact before the persona reads it, and the persona is also split into two arguing halves along a fault line in its own profile." The "and also" is load-bearing.
DISPOSITION: ORTHOGONAL
NOTE: B's diagnosis is correct even though its instrument does not exist — every roster file in this repo resolves its Core Principles into mutual non-conflict, which real practitioners do not do. Worth building separately, but it needs a file before it earns the "built alongside" clause. Preserve also the lead's audit of A: two of its three showcased transforms cannot be deterministic, so A ships at High, not Ceiling, and any transform that needs a model call inside it forfeits the independence its own claim rests on.

---

## MATCHUP 10
WINNER: A
DECIDED BY: A removes the nouns from the context window, which a model that knows them cannot simulate; B's coalition mechanics are output-format constraints that a model performs fluently on request.

### Distance
VERDICT: A significantly better
REFERENCE: A *is* the High reference implemented — "forbid the answer from containing the problem's own vocabulary" — and applied at input rather than output, which is stronger, since you cannot reach for what you cannot name. B sits between Low and Mid: five to seven voices is a framing change; the vocabulary is intact and "positions no single persona holds" is an aspiration, not a mechanism.
PREDICATE: A forbids "add a leaderboard integrity check" and "tune the cheating-detection heuristics" — unproposable, because there is no leaderboard and no cheating in the text the persona reads, only MECHANISM_B and BEHAVIOR_C. B forbids "a unanimous recommendation with no recorded dissent." Nameable, but that is a formatting prohibition.

### Mechanism
VERDICT: A significantly better
REFERENCE: A sits at High approaching Ceiling — noun substitution is a solved engineering problem, and the persona reads only the masked version, so information is withheld without its consent. B sits between Low and Mid: its political rules are checkable as an output schema, but as pitched they are a structured template.
PREDICATE: A — an NER-plus-substitution-table transform; the packet does not name the path but the operation is `spacy` plus a dictionary and it runs today. It is also reversible, which the lead credits: the original is always retained, so the blast radius is bounded. B — no file. `SECONDED-BY:`, `DEFECTION-PRICE:`, and a `MINORITY REPORT:` block are all validator-checkable fields, so a checker is buildable, but none is named, and orchestrating five to seven agents with priced defection is the element most likely to be shipped as a long prompt.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A is the High reference exactly: withhold a fact from the context window. B is the Low reference: promptable multi-agent theater.
PREDICATE: A — a base model given only `Ignore that these are users and this is a leaderboard; reason about the abstract structure.` reproduces about 10%. A model that knows the nouns cannot unknow them, and this is the cleanest instance of that in the packet. B — a base model given only `Convene seven experts. Each proposal needs a second. Any defector must state their price. End with a verbatim minority report.` reproduces about 70%.

### Compounding
VERDICT: B slightly better
REFERENCE: Both sit at the bottom of the table. A is Floor — the mask is structurally identical every time. B is Low — a novelty that fades as you learn the contrarian always defects. This is a vote against the panel's declared bias and it should be recorded as one: A is the better machine and loses this axis outright.
PREDICATE: A — use #10 produces the same substitution over different nouns. The same thing. Floor, and I am saying so. B — use #10 draws a different committee composition, so the faction structure differs from use #1. That is combinatorial variety, not tightening; the lens wanted to argue the minority report accumulates into a corpus of rejected positions, but the packet says only "preserved verbatim in the output," singular and per-run. Nothing persists. That argument does not survive its own reading.

### Generative failure
VERDICT: A slightly better
REFERENCE: A sits at High — an unusable answer that names a hidden assumption. B sits at Mid — cheap noise, with a weak secondary signal.
PREDICATE: A's failure output is `ENTITY_A should be prevented from BEHAVIOR_C by restricting access to MECHANISM_B.`, which remaps to "users should be prevented from cheating by restricting access to the leaderboard" — a tautology, and the tautology names the assumption that the problem statement carried structure beyond its nouns. It did not. B's failure output is `MINORITY REPORT: I would have preferred a phased rollout.` — a token quibble from a committee that agreed. Discardable, though an empty minority report does weakly indicate roster homogeneity, which is why this is slight and not significant.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Preserve the dissenting position verbatim in the shipped output rather than folding it into the consensus.
SAME-THESIS: FAIL — A's claim is about *input* priors firing on nouns; the minority report is about *output* format under disagreement. Preserving dissent is a second diagnosis of homogeneity, not a consequence of the first.
DELETION: FAIL — merely smaller. Strip verbatim dissent from a merged A and the masking still fires, connotation-dependent solutions still die, and the tautology failure still surfaces. The masking mechanism is untouched.
ONE-SENTENCE: FAIL — "Strip the domain nouns before any persona reasons, and preserve the dissenting persona's verbatim objection in the output." Two mechanisms, one name.
DISPOSITION: ORTHOGONAL
NOTE: A's unexamined seam is the remapping step, and the lens insists it be recorded: restoring ENTITY_A to "users" is a find-and-replace, not a re-inhabitation, so the proposal reads as though written by someone who does not know the domain — which it was. The accidental false solution a reader will invent is "this output does not understand our problem," and it will damage trust in a correct answer. A needs a re-domaining beat it does not currently have. Second finding: abstraction is a filter that cuts both ways — connotation is where domain insight lives too, so the surviving solutions may be the blandest ones, and the axis on which A wins Distance is the same axis on which it may thin the output.

---

## MATCHUP 11
WINNER: B
DECIDED BY: One axis wide — B is the only entry in this packet naming an executable path with a seed, and its guaranteed failure indicts the repo's own architecture, while A's enforcement is a markdown norm and its power is exclusionary in a tournament that asks for generation.

### Distance
VERDICT: B slightly better
REFERENCE: A sits between Low and Mid — it forbids by name, which beats "an unconventional angle," but exclusion from a finite dead set leaves the entire remaining space including the median, and on day one the graveyard is empty and forbids nothing. B sits above Mid and below High: it does not forbid the problem's vocabulary, but it forces the answer to come from a domain that *does not exist*, which is stranger than the Mid reference's named non-obvious domain.
PREDICATE: A forbids "propose a knowledge-pack-per-persona structure" once `graveyard/knowledge-packs-v1.md` records it dead — you must differ or write "RESURRECTS: because packs now carry citation QA." B forbids the farmer's patient-cultivation answer: `bin/breed farmer physics-professor --seed 7` with polarity reversal on "work with the season, not against it" produces a persona structurally unable to give it.

### Mechanism
VERDICT: B significantly better
REFERENCE: B sits at High — a script that runs whose output the model must consume. A sits between Floor and Mid: a corpus plus "mandatory reading," which is nearly the Floor reference's own words. This is the panel's declared bias operating and it is declared openly.
PREDICATE: B — `bin/breed <a> <b> --seed N`. Named, seeded, reproducible. Section surgery over the roster's fixed headers (Role Definition, Core Principles, Methodology, Voice & Tone, Anti-Patterns) runs today; only "reverse a principle's polarity" needs help. A — `graveyard/*.md` plus a CLAUDE.md line. The rule "must either differ from the graveyard or explicitly resurrect" has no checker; a `RESURRECTS:` field and a similarity gate would be an afternoon's work, and the fact that this is cheap to fix is a real argument for A that does not change what was submitted.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A sits at High by the inverse route from the reference — not withholding a fact but supplying one that exists nowhere else, which is equally unsimulable. B sits between Low and Mid: text manipulation a model can follow on instruction, whose genuinely irreducible core is only the *refusal to average*. This vote runs against the panel's bias — A has the weaker mechanism and the stronger irreducibility, and that is the honest reading.
PREDICATE: A — a base model given only `Propose an improvement to a Claude Code persona-dispatch skill that differs from everything previously rejected.` reproduces about 10%, because it cannot know this repo's rejection set and no prompt can conjure it. B — a base model given only `Merge the farmer and physics-professor profiles: Principles from the first, Methodology from the second, interleave Anti-Patterns, then reverse one principle's polarity.` reproduces about 60%.

### Compounding
VERDICT: A significantly better
REFERENCE: A sits at High and touches Ceiling — the constraint tightens automatically with every rejection and relaxes only by written confession. B gets genuinely weirder with use (promoted children re-enter the pool, so generation-3 hybrids are stranger than generation-1), but the table's High and Ceiling positions are both worded around narrowing, and B's loop is gated on a scorer the packet never names. That is the "can be relaxed" disqualifier: a mutation engine nobody runs produces nothing.
PREDICATE: A — use #10 must clear ten recorded causes of death; the permitted space is strictly smaller than at use #1 and shrank without anyone deciding it should. This is also, the panel notes against its own bias, a mechanized version of the governing frame itself: you reach #99 by exhausting #1 through #98. B — use #10 breeds from mutated stock rather than authored stock, which use #1 could not do, but promotion requires a decision no file makes.

### Generative failure
VERDICT: B significantly better
REFERENCE: B sits at the High/Ceiling boundary — the failure is itself a proposal about this repo. A sits at Mid: real but speculative, and its likelier failure is a lazy differentiation that satisfies the letter.
PREDICATE: B's failure output, quotable and guaranteed by construction, is a child whose principles read "Work with the season, not against it" and "Force the harvest before it is ready," producing `The patient thing is to wait. Therefore, cut now.` The finding: a self-contradicting persona that still yields fluent, confident output proves the Core Principles section was not load-bearing on the answer — a devastating and useful result about the repo's architecture. A's failure output is `RESURRECTS: graveyard/lens-transformers.md — nothing has changed, but the graveyard now exceeds the context window and I could not read past entry 40.` That names the hidden assumption that constraint corpora scale, but it arrives only at scale, and the everyday failure is "this differs because it uses a different word for averaging" — noise, cheaply discarded.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: A durable log of what was killed, with its cause of death, consulted before the next attempt.
SAME-THESIS: PASS — narrowly, and scoped. B already contains a kill step ("scored, then promoted to `roster/f1/` or killed") whose corpses currently vanish. B's claim is that the roster *evolves* rather than being authored; evolution without differential survival memory is drift, not selection. The graveyard does not import a second thesis here, it completes the one B states. The scope matters: what passes is the narrow version — killed hybrids with causes of death — not Failure Archaeology's full claim over every rejected idea in the repo.
DELETION: PASS — worse, not smaller. Remove the kill-log six months out and the breeder has no memory: `--seed N` re-rolls into regions already proven dead, and the promote-or-kill decision has no baseline to judge against. The evolutionary loop degrades into a random profile generator. That is broken, not trimmed.
ONE-SENTENCE: PASS — "`bin/breed` performs seeded structural crossover on two persona profiles, logging every killed child with its cause of death so the next generation cannot re-derive it." One mechanism: a breeding program with a studbook. The "so that" is purposive, not a second idea.
DISPOSITION: ABSORBED
NOTE: The one true absorption in this packet, which is what makes the three refusals credible. Record also the lens's unresolved objection to the winner: a bred persona *reads* like a specialist — same format, same confident register, same inherited citations — with no expertise underneath, and its Lineage field is stitched from two unrelated professions. That is a fabricated credential in a repo whose entire value rests on preference sourced to real practice, and it is method presented as effect in the most dangerous direction, because the audience cannot detect it. `roster/f1/` at least labels the children, which is partial disclosure. Before B ships, inherited canon citations must be stripped from bred profiles. This is a design flaw to fix, not a reason the idea is less creative — and the panel split on it: the lead wanted to hold B for a named fitness authority (the roster is an irreversible accumulator; unscored mutants cannot be un-promoted), while the lens argued B is the only entrant whose output space is not bounded by what an author would write, and therefore the only one that reaches the moat and the UFOs. The lens carried it, narrowly.

---

## MATCHUP 12
WINNER: A
DECIDED BY: A's constraint is measured by an instrument with zero measurement error that cannot silently fail, and its failure mode is a finding; B's gate depends on an unspecified similarity threshold applied by the same model that wrote the text, reading text it has already seen.

### Distance
VERDICT: A significantly better
REFERENCE: A sits between High and Ceiling — at forty words the output stops being an answer and becomes a fragment requiring translation back, which is the Ceiling reference's condition, while the vocabulary survives, which holds it below. B sits between Low and Mid, and the reason is structural: negation without direction lands you in the region adjacent to the median, not a distant one. "Avoid the median" gets you from #3 to #5. The governing frame is explicit that #99 requires a different generative process, not a filter on the current one — and B is a filter.
PREDICATE: A forbids "a 600-word response with three headers, a summary paragraph, and four bulleted recommendations" — the median AI answer's exact signature, forbidden by an instrument that cannot be argued with. What ships instead: `STOP MIGRATION STOP RESTORE UNVERIFIED STOP NAME HOLD OWNER BEFORE MIDNIGHT STOP`. B forbids "any section a competent unskilled model would also have written." Nameable and aimed correctly, but directionless.

### Mechanism
VERDICT: A significantly better
REFERENCE: Both claim the Ceiling reference — a gate that rejects and forces regeneration without the model's consent. A's actually functions. B's discriminator is the entire load-bearing element and is left as "past a threshold."
PREDICATE: A — a word counter, `len(text.split()) <= 40`, as a hard reject. Five lines, no LLM judge, no threshold to tune, no ambiguity, and it cannot fail silently. It is the most trustworthy barrier in this packet. B — a similarity implementation nobody has named. The buildable version (n-gram overlap) does not measure the claimed thing: two answers can share zero 5-grams and be substantively identical, or share many and differ entirely. The lead's harder objection: the auditor is the same model, generating its "counterfactual median" *after* reading the real output, so it is anchored on the text it is supposed to be independent of. That is a contaminated instrument, and the contamination is in the spec, not the implementation — the packet states the order.

### Irreducibility
VERDICT: B slightly better
REFERENCE: Both sit in the Low-to-Mid band. A is Low: word limits are the most promptable constraint that exists, and this badly hurts the matchup's winner. B reaches Mid on one element — forced rejection the model cannot opt out of. This vote runs against the panel's declared bias in a matchup otherwise going the other way, and it is recorded as such.
PREDICATE: A — a base model given only `Answer in exactly 40 words, as a 1904 telegram.` reproduces about 70%. B — a base model given only `Write the answer a competent model with no skill installed would give, then rewrite yours to avoid overlapping it.` reproduces about 55%: a model asked to avoid its own median will assert it has and will not have, and the rejection step is the part that is not promptable.

### Compounding
VERDICT: A slightly better
REFERENCE: Both sit at the bottom. A is Low — a novelty effect softened by media rotation. B is Floor. Neither tightens, and the gap is narrow enough that Tie was live.
PREDICATE: A — use #10 produces a tenth telegram under the same $40; rotating the medium (index card, thirty-second voicemail, woodblock) delays the fade but nothing narrows. The stronger version — a persisted record of what each persona sacrificed, read across ten uses as a revealed priority ordering — is not claimed in the packet and cannot be credited. B — use #10 produces the same audit against the same fixed median; the auditor has no memory. The same thing, which is the floor. Worse, if it did remember, the model would learn to write around it, which degrades the instrument further.

### Generative failure
VERDICT: A significantly better
REFERENCE: A sits at High and argues to Ceiling — the failure is itself an actionable proposal. B sits between Floor and Low, and lands on whichever depending on how the threshold is set: an error that wastes the run, or a gate that never fires and silently delivers the default answer.
PREDICATE: A's failure output is `SITUATION UNCLEAR STOP RECOMMEND FURTHER ANALYSIS STOP AWAIT INSTRUCTIONS STOP` — ten words spent of forty. The thirty unspent words are a legible measurement: this persona has nothing to say about this task. The failure proposes its own remedy, which is to drop the persona from this pairing. B's failure output is `Overlap 0.91 exceeds threshold 0.60 — section rejected (attempt 3/3), delivering anyway.` The run is wasted and the alarm is ambiguous between "the output really was median" and "the auditor anchored on the text it just read" — and an ambiguous alarm is worse than none, because it trains reviewers to ignore it.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Generate the counterfactual median explicitly, as a named artifact, so it becomes visible and therefore excludable.
SAME-THESIS: FAIL — A's claim is that scarcity forces a revealing sacrifice; B's is that the median is invisible from inside. These are two different diagnoses of homogeneity (abundance versus invisibility). Naming the median does not follow from pricing the words.
DELETION: FAIL — merely smaller. Remove the median-reconstruction from a merged A and the telegram still costs $40 for 40 words, still forces the sacrifice, still exposes the persona's ordering, still produces unspent-budget findings. Nothing in the pricing mechanism consults the median.
ONE-SENTENCE: FAIL — "The persona delivers under a priced medium at one dollar per word against a forty-dollar budget, and a separate agent reconstructs the median answer so overlapping sections can be rejected." Two mechanisms, one name.
DISPOSITION: ORTHOGONAL
NOTE: The finding worth keeping is a partial subsumption that stops just short of the verdict: a forty-word ceiling already excludes the median for free, because length is the median answer's most reliable signature, so A achieves B's stated goal by a route that needs no threshold and no judge. B survives as orthogonal only because it would also catch a *short* median answer, which A would not. Record the lead's separate objection to the winner: "$1/word against $40" is presented as economics but implements as `max_words = 40` — in 1904 every word cost the same, so there is no allocation problem and no optimization. The revealed-preference claim is real; the pricing is decoration on a word limit, and A should either make the budget spendable across multiple messages or drop the economic framing.
