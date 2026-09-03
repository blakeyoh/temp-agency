## MATCHUP 9
WINNER: A
DECIDED BY: A is the only one of the two that removes information from the context window before the persona reads; B asks a model to perform an internal disagreement, which is a thing models are already excellent at simulating.

### Distance
VERDICT: A significantly better
REFERENCE: A sits at **High** — "forbid the answer from containing the problem's own vocabulary" — enforced on the input side rather than the output side, which is the stronger version: the monk transform deletes every superlative sentence, so the superlative vocabulary is not available to be inherited. B sits at **Mid** — "require the answer to come from a named non-obvious domain." A bisected farmer is still a farmer answering a farmer's question in a farmer's register; the answer stays recognizable as an answer.
PREDICATE: A forbids "adoption is flat because the Q3 campaign underperformed, per the 14% CTR" — the journalist transform severed "per the 14% CTR" before the persona read, so the persona cannot ground a recommendation in a number it never saw. B forbids "The farmer's view: be patient, conditions decide" — it forbids any single-register farmer paragraph. Both nameable; A's is a ban on evidence, B's is a ban on tone.

### Mechanism
VERDICT: A significantly better
REFERENCE: A sits at **High** and reaches toward **Ceiling** — a script runs and the persona "reads only the transformed artifact," which is rejection without the model's consent, since the original never arrives. B sits at **Floor** — "a paragraph in a markdown file asking the model to try harder." "Forcibly bisected" names no forcing agent.
PREDICATE: A names three: `transforms/investigative-journalist.py`, `transforms/farmer.py`, `transforms/franciscan-monk.py`. B names none — the bisection is an instruction inside the pass, so it scores as exhortation. Panel note against A: only `franciscan-monk.py` is honestly deterministic (a superlative wordlist). "Re-sorts every line by how long it will still be true" cannot be written without a judgment call, so `transforms/farmer.py` is a script wrapping a model — a file that runs, but not the deterministic one the entry claims.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A sits at **High** — "withhold a fact from the context window — cannot be simulated by a model that knows it." This is the reference verbatim, not an approximation. B sits at **Low** — "hand the model a persona file: real, but promptable." Self-bisection is a prompt behavior.
PREDICATE: A — a base model given only `"Rewrite this document so every claim appears without its supporting clause, then read the rewrite as an investigative journalist and respond."` reproduces about **30%**, because the model that performed the strip still holds the originals in its own context; the un-simulatable part requires two processes. B — a base model given only `"You are the farmer. Split into farmer-as-patience and farmer-as-seasonal-deadline, argue, do not resolve."` reproduces about **80%**.

### Compounding
VERDICT: B slightly better
REFERENCE: A sits at **Floor** — "identical on use #10 as on use #1." A deterministic transform is deterministic; nothing accrues. B sits at **Low** — "a novelty effect that fades as the pattern becomes familiar." The fault-line set is fixed by the profile, so the arguments start repeating by roughly use #6.
PREDICATE: A — use #10 produces **the same thing** as use #1. Stating that plainly: this is the floor, and it is the panel's own bias axis, so we say it against the idea we are otherwise voting for. B — use #10 produces an argument along a fault line already used at uses #2, #5, and #7, but paired to a different task, so the *pairing* is new even though the fault line is not. That is a hair above nothing, and a hair is the whole margin.

### Generative failure
VERDICT: A significantly better
REFERENCE: A sits at **High** — "an unusable answer that nonetheless names a hidden assumption." B sits at **Floor** — "nothing; the pass silently produces the default answer," wearing two names.
PREDICATE: A — the journalist transform run on a document with no subordinate clauses returns the input unchanged: `"1. The lens must be enforced. 2. The lens must be enforced."` The transform's no-op *is* the finding — nothing was stripped because nothing was supporting anything. B — `"The farmer's patience says wait for the conditions; the farmer's deadline says the season closes in six weeks. Both are true, and the tension is real."` That is the median AI answer with a colon in it.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The persona is split along a fault line named in its own profile and the unresolved argument ships as part of the output.
SAME-THESIS: FAIL — A claims that changing what the model can *see* changes what it produces; B claims that models resolve internal tension into a single *register*. One is about input information, the other about output voice. A near-miss worth recording: running two different transforms on one persona and giving each half a differently-mutilated document would produce disagreement *caused by* differing evidence — but that is A's mechanism applied twice, not B's.
DELETION: FAIL — merely smaller. Delete the fracture six months on and A still strips supporting clauses, still deletes superlatives, still hands the persona a document that is not the document. Nothing A does depends on the persona being two.
ONE-SENTENCE: FAIL — "Each persona reads only a mechanically transformed artifact and ships the unresolved argument between its two halves." The "and" is load-bearing and cannot be removed; the two clauses operate on different objects.
DISPOSITION: ORTHOGONAL
NOTE: The absorption near-miss is the finding. Disagreement sourced from *differing evidence* (two transforms, two halves, two documents) is a different and better object than disagreement sourced from *instructed tension*, and only the first is un-simulatable. Build it under A's thesis, not B's.

---

## MATCHUP 10
WINNER: A
DECIDED BY: A is the only entry in the packet that lands on the Distance ceiling reference near-verbatim — the output is unrecognizable as an answer until the mapping is restored — while B's coalition mechanics are a governance protocol on top of a deliberation the model already knows how to write.

### Distance
VERDICT: A significantly better
REFERENCE: A sits at the **Ceiling** — "the output is unrecognizable as an answer to the question until it is translated back." The entry says this itself: "only afterward is the mapping restored." It also passes through **High** on the way (the problem's own vocabulary is gone). B sits between **Low** and **Mid** — the output *form* changes (a preserved minority report) but the content space is the same one seven ordinary voices already occupy.
PREDICATE: A forbids `"add a rate limit to the leaderboard to stop cheating."` The persona never sees "leaderboard" or "cheating," so the rate-limit prior that the word "cheating" summons never fires — it sees MECHANISM_B and BEHAVIOR_C. B forbids "a single-voiced recommendation with no dissent." That is a ban on a *shape*, not on a *content*; no specific proposal is made unreachable, which is why it scores nearer the floor than the ceiling.

### Mechanism
VERDICT: A slightly better
REFERENCE: Both sit below where they claim. A sits at **Mid–High**: a noun-substitution pass is deterministic and script-shaped (NER plus a substitution table plus an inverse map), so it *can* become a file. B sits at **Low**: "a proposal needs a second, a defection must state its price" is a structured prompt template with required sections — the model both proposes and adjudicates, so nothing external executes.
PREDICATE: **Neither entry names a file, and this is the packet's weakest spot on this axis.** A would be `transforms/abstract.py` plus its inverse; the packet says only "a transform." B has no candidate filename at all, because there is no operation in B that is not a model turn. The gap is that A's described operation is deterministic and B's is not: A can become a file, B can only ever become a template.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A sits at **High** — the persona genuinely does not hold the mapping, which is "withhold a fact from the context window." B sits at **Low** — a promptable behavior; committee transcripts are a genre the base model performs fluently.
PREDICATE: A — a base model given only `"Replace every domain-specific noun in this problem with a variable name, then solve the abstracted version."` reproduces about **25%**, because the model doing the substitution retains the mapping and its priors fire anyway; the asymmetry requires a second process that never receives the key. B — a base model given only `"Simulate a seven-person committee. A proposal needs a second. A defection must state its price. Preserve the minority report verbatim."` reproduces about **70%**.

### Compounding
VERDICT: B slightly better
REFERENCE: A sits at **Floor** — "identical on use #10 as on use #1." The substitution table is the substitution table. B sits at **Low** — the cast varies, so the factions vary, but nothing from uses #1–9 is carried into #10; the variety is re-rolled, not accumulated.
PREDICATE: A — use #10 produces **the same thing** as use #1: ENTITY_A, MECHANISM_B, BEHAVIOR_C, again. This is the floor and we name it against our own preferred entry. B — use #10 produces a coalition among a different 5–7 draw from a 24-roster, so the alliance that forms is one uses #1–9 could not have formed. That is genuine per-use variance and it is more than A has, and the panel's compounding bias does not get to pretend otherwise.

### Generative failure
VERDICT: A significantly better
REFERENCE: A sits at **High** and argues to **Ceiling** — "the failure is itself a proposal worth acting on." B sits at **Floor** — "nothing; the pass silently produces the default answer," with a certificate attached.
PREDICATE: A — over-abstraction produces `"ENTITY_A should be removed from MECHANISM_B entirely."` Mapped back: "remove users from the leaderboard." Unusable on its face, and it names the hidden assumption that a leaderboard must display users — a leaderboard of anonymized cohorts is a real proposal that no un-abstracted pass would reach. B — the seven voices converge and the minority report reads `"No minority position was recorded."` The pass produced the median and stamped it as deliberated, which is worse than producing nothing, because the stamp suppresses the pressure to look again.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: A defection must state its price.
SAME-THESIS: FAIL — A's claim is that domain priors fire on nouns, so removing the nouns removes the priors. A priced defection is a claim about *consensus dynamics among agents*, a second and independent account of why output is homogeneous. Running priced defection inside the abstraction ("I defect, my price is that MECHANISM_B survives") does not fuse the claims; it stacks them.
DELETION: FAIL — merely smaller. Delete priced defection six months on and A still strips nouns, personas still reason without their priors, the mapping still restores. A loses a feature, not a function.
ONE-SENTENCE: FAIL — "Personas reason about a noun-stripped abstraction of the problem and must state a price to defect from a coalition." Two objects (the problem, the deliberation), two verbs, an unremovable "and."
DISPOSITION: ORTHOGONAL
NOTE: The priced defection is the one part of B with real teeth, and it should be built separately: a price is a falsifiable commitment a persona can be held to later, which is the only thing in this matchup that could ever become a stock. The panel's farmer registers the maintenance asymmetry for the record — A costs one subprocess per pass and B costs seven persona invocations plus coalition bookkeeping, and in the season nobody has time, the seven-body pass is the first thing dropped while the one-script pass survives.

---

## MATCHUP 11
WINNER: B
DECIDED BY: B generates and A only filters — and the absorption test below shows the asymmetry is one-way: A's memory of the dead can be moved into B without loss, but you cannot breed with a graveyard.

### Distance
VERDICT: B slightly better
REFERENCE: A sits at **Mid** — it forbids the already-catalogued, which pushes you off the median exactly as far as the median has been written down, and no further. B sits at **Mid–High** — polarity reversal and phase deletion produce a profile that is internally incoherent by construction, which no author would write and no model asked to "combine these two" would ever emit.
PREDICATE: A forbids re-proposing `"rotate the lens persona randomly per pass"` once that sits in `graveyard/` with cause of death "personas ignored the rotation." Concrete and checkable. B forbids the sensible blend — it forbids `"farmer + contrarian = a patient skeptic."` What it produces instead is a profile whose Principles still say patience is intelligence while its Methodology has had the preparation phase deleted, a persona that believes in groundwork and has no way to do any.

### Mechanism
VERDICT: B significantly better
REFERENCE: A sits at **Low–Mid**. "Mandatory reading" is the Floor reference — a paragraph asking the model to try harder — lifted only to Mid by the concrete differ-or-resurrect self-check, which is a checklist the model verifies against itself. B sits at **High** — "a script that runs, whose output the model must consume." The child profile *is* the consumed output.
PREDICATE: A — **no file runs.** `graveyard/` is a directory; nothing checks a proposal against it. By the ruler's own rule, no file means it scores as exhortation. B — `bin/breed <a> <b> --seed N`. Named, seeded, and therefore reproducible by someone else, which is what the predicate is for.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A sits at **High** by mirror image of the reference — the reference withholds a fact the model would otherwise know; A supplies a fact the model cannot possibly know. Both are information asymmetries a base model cannot cross. B sits at **Mid** — closer to a generator than to a parser that rejects.
PREDICATE: A — a base model given only `"Propose a mechanism for this repo that has not already been tried and failed here."` reproduces about **5%**. It cannot know the repo's failures; nothing in the weights contains them. B — a base model given only `"Combine the farmer and contrarian profiles by taking Principles from one and Methodology from the other, then reverse one principle and delete a methodology phase."` reproduces about **50%**. It will do the splice, but it will smooth the seams into coherence, which is precisely the averaging the entry exists to forbid; the seeded, unsmoothed version is the irreducible part.

### Compounding
VERDICT: A slightly better
REFERENCE: A sits at **High** — "each use narrows the space of permitted answers" — and tightens without authoring, since the losers arrive on their own. It is held off the Ceiling by the resurrect valve, which is a deliberate relaxation. B sits at **Mid**, a little above it — `roster/f1/` is exactly "material you may consult but need not obey," raised by the kill/promote step, which is real selection pressure rather than mere accretion.
PREDICATE: A — use #10 produces `"REJECTED: duplicates graveyard/2026-05-rotate-the-lens.md, cause of death: nothing consumed the rotation."` Use #1 could produce no rejection at all, because the graveyard was empty. B — use #10 breeds from a pool containing F1 survivors of uses #1–9, producing a child three mutations deep from any authored profile; use #1 could only cross authored × authored. **The panel's systems thinker enters a dissent on its own verdict:** A's High position is unstable. The graveyard is an unbounded stock whose read cost is drawn from a fixed budget of attention, with no decay, no pruning, and no retrieval structure. That is a Limits to Growth with attention as the limiting condition; at roughly thirty headstones "mandatory reading" quietly becomes "grep the graveyard," and then it becomes skipping it. B's Mid is stable indefinitely, because its accumulation is consulted by a script and never competes for context.

### Generative failure
VERDICT: B slightly better
REFERENCE: Both sit at **High** — "an unusable answer that nonetheless names a hidden assumption." B argues toward **Ceiling**, because its failures are targetable rather than incidental.
PREDICATE: A — the failure output is `"REJECTED: differs from graveyard/lens-shuffle.md only cosmetically,"` applied to a proposal that differs in a way the cause-of-death never recorded. The author's rebuttal is the finding, and it improves the headstone. B — the failure output is `roster/f1/farmer-x-monk-seed-4409.md`: Principles from the farmer with "Patience is intelligence" reversed to "Delay is the expensive failure," Methodology from the monk with Phase 2 deleted. It emits a plan with no preparation step and an incoherent voice, and the specific incoherence names Phase 2 as load-bearing. That is a lesion experiment — you learn a section's function by removing it — and unlike A's failure it can be aimed on purpose at any section you want to interrogate.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Every dead idea is preserved with a recorded cause of death, and new work must differ from the record or explicitly resurrect.
SAME-THESIS: PASS — and this is the surprise of the packet. B as written has a kill step with no destination: children are "scored, then promoted to `roster/f1/` or killed," and killed children go nowhere. A breeding program with no record of what died is not performing selection; it is performing memoryless random search over a finite seed space it will re-draw forever. The graveyard is not a second claim imported into B — it is the missing half of B's own claim, because "structural crossover produces combinations no author would choose" is only true of combinations not yet drawn.
DELETION: PASS — worse, not smaller. Delete the record of dead children six months on and `bin/breed --seed N` re-draws lethal crossovers indefinitely, with no way to distinguish an unexplored region of the space from one already proved barren. The mechanism does not shrink; it degrades from selection to noise. This is the sharp test and it is the only clean pass in the packet.
ONE-SENTENCE: PASS — "The roster breeds by seeded structural crossover against a record of which crossovers already proved lethal." One sentence, one object, no conjunction.
DISPOSITION: ABSORBED
NOTE: **This vote defies the panel's declared bias and we say so plainly.** Our bias is compounding and maintenance; A won the Compounding axis; we voted against it. Two reasons. First, A fails the ruler's own sharpest question — name the file that runs — outright, and a constraint with no enforcer is a constraint that survives exactly as long as the enthusiasm does. Second, under the governing frame a filter cannot reach #99 however full it gets: knowing where #1 through #12 are and forbidding them delivers you to #13. B samples a space no author would enumerate. The farmer's residue, recorded so it is not lost: A's graveyard is a compost heap that is never turned. Howard's point is *return* — the humus has to go back into the ground — and A has a return step it cannot afford to perform past thirty entries. Absorbed into B, the record is read by a script instead of by a person, which is the only version of it that survives year three.

---

## MATCHUP 12
WINNER: B
DECIDED BY: B is the only entry in the packet that measures the quantity the tournament is actually about — distance from the median — instead of a proxy for it, and A's priced budget is a proxy (short is not far).

### Distance
VERDICT: B significantly better
REFERENCE: A sits at **Mid** — the sacrifice ordering does push toward a named non-obvious place (the persona's actual commitments), but a compressed median is still a median; the reader receives something plainly recognizable as an answer. B sits at **High** — it enforces non-overlap with the median as a measured quantity, which is the most literal implementation of this axis anywhere in the packet.
PREDICATE: A forbids `"It depends on the conditions — here are three factors to weigh."` At one dollar a word against forty, no persona can afford a caveat paragraph; concretely it forbids any output containing "however." B forbids `"the key is to align incentives with outcomes"` — the auditor will reconstruct that exact sentence as the median, and the section carrying it is rejected and regenerated. B's forbidden set is larger and is discovered per-run rather than fixed in advance.

### Mechanism
VERDICT: A slightly better
REFERENCE: Both designs sit at the **Ceiling** reference — "a gate that rejects the output and forces regeneration without the model's consent." They separate on reliability, not on category. A's gate rejects on word count, a dimension the model cannot argue with. B's gate rejects on similarity to a reconstruction produced by the same class of process it is policing.
PREDICATE: **Neither entry names a filename.** A's gate is `wc -w` against forty and a hard glyph count on the woodblock — trivially writable, and it executes correctly every time, though the thirty-second voicemail needs a separate instrument A does not supply. B's gate is a subagent plus an overlap threshold plus a regeneration loop, three executable components, none named. A takes this axis on ungameability: the packet says the auditor "receives the near-final output," so the instrument reads the answer before reconstructing the median it will be compared against. An anchored auditor reconstructs a conveniently different median and systematically understates overlap. That is a measuring instrument coupled to the thing it measures.

### Irreducibility
VERDICT: B slightly better
REFERENCE: A sits at **Low** — "hand the model a persona file: real, but promptable." The 1904 telegram is a beloved prompt genre. B sits at **Mid** — a separate agent is a real process boundary, but the coupling flaw above drags it down from the High it would otherwise claim.
PREDICATE: A — a base model given only `"Answer as a 1904 telegram, one dollar per word, forty dollar budget."` reproduces about **75%**. B — a base model given only `"Write your answer, then write the answer a competent model with no skill installed would give, then rewrite whatever overlaps."` reproduces about **40%**. The residual is the process boundary; it would be nearer 15% if the auditor were denied sight of the real output, which is the single edit that would most improve this entry.

### Compounding
VERDICT: B slightly better
REFERENCE: A sits at **Low** — "a novelty effect that fades." Four named media rotate, and by use #10 the telegram is a house style. B sits between **Floor** and **High**: the constraint never decays and cannot be relaxed *by the model*, which is most of the Ceiling's language — but it does not tighten, and nothing accumulates, because the packet does not store the reconstructed medians.
PREDICATE: A — use #10 produces a telegram, same as use #1, in one of four rotating registers the reader has now seen. B — use #10 produces a rejection measured against a median that has itself moved, because the repo's other mechanisms changed what the unskilled baseline looks like; that is tracking drift rather than accumulating, but a non-decaying constraint beats a fading one. **Farmer's dissent, entered against the verdict:** "cannot be relaxed by the model" is not the same as cannot be relaxed. A threshold is a number, and numbers in a repo drift toward whatever stops the complaints. In year three the threshold has been loosened once and never tightened, and the gate is a rubber stamp everybody still believes in — the fence everyone assumes is electrified. A costs `wc -w` forever and survives the bad season intact. **Systems thinker's answer, for the record:** A is cheap because A is a parameter, the lowest leverage point on Meadows' list. B is expensive because B is a feedback loop. A decaying high-leverage intervention still beats a durable low-leverage one when the goal is exploration rather than reliability. The panel does not resolve this; it ships it.

### Generative failure
VERDICT: A significantly better
REFERENCE: A sits at the **Ceiling** — "the failure is itself a proposal worth acting on." B sits at the **Floor** — "nothing; the pass silently produces the default answer" — with the aggravating feature that it issues a certificate saying otherwise.
PREDICATE: A — the failure output is a persona that spent thirty-eight of forty words hedging: `"CONDITIONS VARY STOP SOIL DEPLETED STOP RECOMMEND FURTHER STUDY STOP."` A persona that spends its entire budget on caveats has just confessed it holds no positions, and that is a directly actionable finding against `knowledge/<slug>/positions.md`. This is the best failure mode anywhere in the packet. B — the failure output is an anchored auditor producing a strawman median, overlap returning `8% — PASS`, nothing regenerating, and the default answer shipping with a green stamp on it. A gate that fails open and reports success is worse than no gate, because it removes the pressure to build one.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: A priced budget forces sacrifice, and what a persona sacrifices first reveals what it actually believes.
SAME-THESIS: FAIL — B claims a model cannot see its own median from inside, so a separate agent must generate it. A claims models treat "be concise" as a style note while a priced budget is an optimization problem. Median-blindness and compression-as-style are two different diagnoses. The steelman — run the auditor under a forty-word budget so the median is a sharper comparison target — is a real improvement to B, but it imports the compression claim, and it leaves A's actual payload (sacrifice reveals belief) entirely outside, since revealed preference has nothing to do with detecting a median.
DELETION: FAIL — merely smaller. Delete the priced budget six months on and B still runs the auditor, still computes overlap, still forces regeneration. The audits get longer and mushier; overlap on long text remains measurable. B loses tidiness, not function.
ONE-SENTENCE: FAIL — "An adversarial auditor reconstructs the median answer and each persona delivers under a priced word budget." Unmergeable in principle, not just in phrasing: one is a checker that never proposes, the other is a producer. They act on opposite ends of the pass.
DISPOSITION: ORTHOGONAL
NOTE: Preserve two facts from this matchup, and they point in opposite directions. First, A's failure mode is the most valuable object in the packet: the all-hedges telegram is a diagnostic on the *roster*, not on the pass, and it is the only mechanism here that audits whether a persona has positions at all. Build it as an elicitation instrument even though it lost. Second, B's failure mode is the most dangerous object in the packet, and it is fixable with one edit: **deny the auditor sight of the near-final output.** An auditor that reconstructs the median from the task alone is an unanchored instrument and moves this entry from Mid to High on irreducibility; an auditor that reads the answer first is measuring itself. The panel's own compounding bias favored A here on maintenance cost and we voted against it, because cheap-to-maintain is not the same as compounding and the ruler has an axis for one and not the other.
