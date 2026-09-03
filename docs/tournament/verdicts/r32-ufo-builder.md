## MATCHUP 13
WINNER: A
DECIDED BY: A carries facts across sessions that no prompt can put back — a fresh model cannot know what its signature move was last Tuesday — while B is a large number plus a relatedness test the same model grades itself on inside one pass.

### Distance
VERDICT: B slightly better
REFERENCE: A between Mid and High — but only at ledger depth; at depth 0 it sits at Floor, since session one is the unmodified default. B at Mid-to-High for every pass, since items 13-19 cannot be reached by the default four-real-ideas-plus-rephrasings behavior.
PREDICATE: A forbids nuclear-reactor-operator from writing "hold; verify the restore, not backup completion; name a stop-work owner who is not the script author" a second time — verbatim the move in its own profile's Example Output, so the ledger would burn that move on first use. B forbids improvement #12 being "add alerting on the migration" when #3 was "add a migration dashboard" — same mechanism, same actor, same timescale. B's forbidding is immediate and uniform; A's is retrospective and starts empty.

### Mechanism
VERDICT: A slightly better
REFERENCE: A between Low and Mid — persistent state but no enforcement. B at Low, with no artifact of any kind.
PREDICATE: A names ledger/<slug>.jsonl. Checked against the repo: no ledger/ directory exists (top level is .claude-plugin, commands, docs, hooks, knowledge, references, roster, skills). More important than its absence — nothing is named that writes it. "Every position a persona takes is appended" is passive voice with no extractor; a jsonl file is data, not an executable, and no gate rejects a restatement. B names no file at all; "each must fail a stated relatedness test" is the model marking its own homework. Both are exhortation; A at least leaves a residue on disk.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A at High — the reference is "withhold a fact from the context window"; A is the mirror, injecting a fact a fresh session structurally cannot have. B at Low; the entire idea is one prompt sentence.
PREDICATE: A base model prompted "don't repeat your signature move" reproduces ~5% of A — it will perform novelty against a history it does not possess. Prompted "give me 19 improvements; each must differ from every previous one in mechanism, actor, failure mode, and timescale, and declare which axis" reproduces ~70% of B, and the missing 30% is compliance drift, not capability.

### Compounding
VERDICT: A significantly better
REFERENCE: A between High and Ceiling — it tightens automatically but is relaxable by editing or deleting the file. B between Floor and Low: each pass restarts at item 1.
PREDICATE: Use #10 of A produces a position the persona must reach around nine recorded prior positions, so the reachable answer space is nine claims smaller than at use #1. Use #10 of B produces the same 19-slot shape as use #1, with the same first six mediocre items; the only thing that accumulates is the operator's boredom.

### Generative failure
VERDICT: A slightly better
REFERENCE: A between High and Ceiling. B at Mid.
PREDICATE: A fails as nine ledger rows reading "verify the restore, not backup completion (v2)", "confirm restore rather than backup success (v3)" — paraphrase escaping an undefined no-restate rule. That artifact is itself the finding: a readable proof the persona has become a macro, which is the idea's own thesis, printed. A's second failure output is worse and unbarriered: forbidden from its correct position, the operator persona writes "prior position reversed — ship with monitoring," a written recantation of a safety-critical claim with nothing crediting a barrier against it. B fails as items 13-19 reading "hold the review on a Tuesday — unrelated axis: timescale," strained but tagged, visible, and free to discard.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The four-axis non-adjacency test — a new item must differ from every prior one on a declared axis (mechanism, actor, failure mode, timescale), and the axis must be named.
SAME-THESIS: PASS — A's single claim is "the signature move becomes unavailable after first use," and A currently has no operative definition of "restate," which is the hole the paraphrase failure walks through. The test supplies that definition. Only the test travels; the quantity 19 does not.
DELETION: PASS — worse, not smaller. Remove the test and "you may not restate any of these" reverts to an unenforceable phrase; the ledger keeps growing while the constraint silently stops binding. A rule that appears to bind and does not is the worst state of the three.
ONE-SENTENCE: PASS — "A persona is handed its own recorded prior positions and may not add a new one unless it differs from every prior one on a declared axis: mechanism, actor, failure mode, or timescale."
DISPOSITION: ABSORBED
NOTE: This is an absorption of a predicate, not of an idea — B's actual invention (the toll of 19) stays behind, and the merged thing is still a single-claim mechanism.

---

## MATCHUP 14
WINNER: B
DECIDED BY: B is the only idea in this packet where something outside the answering model's own distribution actually executes; A is the answering model auditing itself with a step it wants to pass.

### Distance
VERDICT: B slightly better
REFERENCE: A between Low and Mid — it adds a second artifact but does not touch how the first was generated. B at Mid: the injected reaction is genuinely off-distribution text the large model must continue from.
PREDICATE: A forbids delivering a recommendation with no accompanying derived-brief and diff — it forbids no sentence of the recommendation itself, which can be entirely median and still pass. B forbids the smoothed close: the large model cannot end on "both approaches have merit" while a blunt in-character objection sits unanswered in the transcript. Note the ceiling on B: the large model may answer the objection politely and still deliver the median recommendation, so this is Mid, not High.

### Mechanism
VERDICT: B significantly better
REFERENCE: A between Low and Mid. B at High — "a script that runs, whose output the model must consume" is almost a literal description — but not Ceiling, because no gate rejects a perfunctory response to the oracle.
PREDICATE: A names nothing; the reverse brief is a required section written by the same model that produced the answer, i.e. the script author verifying his own script. In defense-in-depth terms it is one barrier, and it is the same component as the thing it protects. B names a checkpoint and an inference call — separate weights, separate process, output the large model consumes. Two operator findings on B, neither fatal: nothing filters oracle output before the mandate to respond attaches; and "the large model must respond" has no enforcement.

### Irreducibility
VERDICT: B significantly better
REFERENCE: A at Floor-to-Low. B between High and Ceiling — it literally changes weights, just a satellite model's.
PREDICATE: A base model prompted "after you answer, write the problem statement your answer would perfectly solve, then diff it against the real one" reproduces ~85% of A. Prompted "react in this persona's voice, bluntly, never propose a solution" reproduces ~30% of B and drifts back to house register within two exchanges — that drift is precisely what separate weights prevent. Two checks against this repo, both discounts on B that it survives: the persona knowledge packs are far too small to be the training corpus (knowledge/nuclear-reactor-operator/ totals ~12.6KB across three files), so the real corpus is synthetic in-character dialogue — generated by the large aligned model, meaning the separate weights inherit the house voice by distillation. What actually survives is capability collapse: a 0.6B cannot execute the hedge. That is still not promptable. Second check: only 18 of 24 roster personas have a knowledge/ directory and only 16 have the three-file pack (civil-rights-activist has 1960s-us.md, missiologist has evangelical.md, and anthropologist, chief-of-staff, contrarian, executive-coach, left-fielder, pediatric-occupational-therapist have none), despite CLAUDE.md stating packs are "required per-specialist as of v2" and the roster is "complete 24/24." B is trainable for two-thirds of the roster today.

### Compounding
VERDICT: B slightly better
REFERENCE: A at Floor. B at Low.
PREDICATE: Use #10 of A produces the same shaped gap paragraph as use #1 — no state, no accumulation, no narrowing. Use #10 of B produces a reaction you can predict, because a 0.6B fine-tune has a small number of moves and its tics surface fast; the checkpoint is frozen and nothing retrains it on the accumulating dialogue.

### Generative failure
VERDICT: B slightly better
REFERENCE: A between Floor and Low. B at Mid, with occasional High.
PREDICATE: A fails as "Reverse brief: How do we improve onboarding retention? Real problem: How do we improve onboarding retention? Gap: none material." A null diff, produced by the model with every incentive to produce it, indistinguishable on the page from a pass that worked — the Floor reference with a heading on it. B fails as an oracle reply like "HOLD. Steam generator level is 47 percent." to a marketing question: hallucinated, off-domain, discardable in one glance, and occasionally a usable accidental metaphor. B's failure is visible; A's is invisible, and invisible failure is the one an operator cannot hold on.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Derive the problem statement for which the produced recommendation would be the perfect answer, and treat the diff against the real problem as a first-class output.
SAME-THESIS: FAIL — B's single claim is that voice cannot be smoothed away if it lives in separate weights. The reverse brief is a claim about problem framing. Different organ entirely.
DELETION: FAIL — merely smaller. Delete the reverse brief and the oracle still reacts, the large model still must answer, the voice mechanism is untouched.
ONE-SENTENCE: FAIL — the two halves share no subject.
DISPOSITION: ORTHOGONAL
NOTE: The reverse brief would sit equally well on any of the other seven entrants in this packet, which is the tell that it belongs to none of them.

---

## MATCHUP 15
WINNER: A
DECIDED BY: B's only forcing element reads an instrument nobody can calibrate — "top decile of weirdness" has no named measurement — so the rerun gate certifies a pass rather than forcing one, while A's missing commitment is visible in the artifact itself with no instrument required.

### Distance
VERDICT: A significantly better
REFERENCE: A between High and Ceiling — the intermediate artifact is at Ceiling; the mandated translate-back step pulls the delivered output down to High. B between Low and Mid.
PREDICATE: A forbids "we recommend a phased rollout with stakeholder alignment and clear success metrics." That sentence cannot be written in a flight checklist; the form demands "CHALLENGE: canary gate 1 — RESPONSE: 5% for 30 minutes, abort on p99 > 400ms." A docket forbids a recommendation existing with no moving party and no ruling; a recipe forbids "improve gradually" because it demands a quantity and a step order. B forbids only one thing: a pass whose entire surviving set is the four safe candidates. It forbids no sentence. High temperature perturbs token selection, not conceptual frame.

### Mechanism
VERDICT: B significantly better
REFERENCE: A at Mid, arguably Mid+ because the verification is externally legible. B between High and Ceiling.
PREDICATE: Neither names one, and the panel weights this heavily. A has no file; its enforcement is the form — a docket with an empty RULING and a recipe with no quantities are broken to any reader, which is more than a checklist offers, but no gate rejects anything. A's real hole, which it does not address: nothing selects the notation, so the model picks the notation that already fits what it intended to say — the flight checklist for the ops plan, the recipe for the process — and the distance collapses to zero at the moment of choosing. B has three separated agents, a mandated count with no quality filter, a pruner that structurally may not generate (a set-membership check anyone could actually run, and the most genuinely mechanical thing in this packet), and a rerun gate. The discount: the gate's trigger is "top decile of weirdness in the HOT pass" with no measurement named. If an LLM judges it, the barrier is an opinion held by a component that wants the pass to succeed — a credited barrier reading a fabricated indication is not a barrier.

### Irreducibility
VERDICT: B significantly better
REFERENCE: A at Low. B between Mid and High.
PREDICATE: A base model prompted "write your recommendation as a court docket, then translate it back" reproduces ~75% of A; the missing 25% is the model quietly choosing a docket-shaped problem. Prompted "generate twenty wild ideas at high temperature, then prune conservatively" reproduces ~35% of B, because a single pass pre-filters during generation — the model cannot make itself not-judge while generating. Separate sampling schedules and an agent that structurally cannot generate are architecture, not instruction.

### Compounding
VERDICT: A slightly better
REFERENCE: A at Low. B at Floor.
PREDICATE: Use #10 of A draws a notation not yet spent — a liturgical rubric after nine others — so it is not identical, but nothing narrows and by use #10 the translations begin to rhyme. Use #10 of B is structurally identical to use #1, and worse than static: the audit threshold is relative to the pass it is auditing, so on a converged pass the "top decile of weirdness" is simply the least-converged converged item. A relative threshold re-anchors and can never ratchet.

### Generative failure
VERDICT: A significantly better
REFERENCE: A at High, occasionally Ceiling. B between Floor and Low.
PREDICATE: A fails as a knitting pattern for a hiring decision that reaches "CAST OFF: ___" and cannot fill it — the artifact is garbage and the empty slot is the finding, because nobody had defined the exit criterion. A docket that reaches RULING with no moving party named tells you the decision has no owner. B fails two ways, both bad: the audit trips, the whole pass reruns, and compute is burned for nothing; or the COLD agent keeps one token-weird survivor to satisfy the audit, and the pass is certified creative while the delivered content stays median. The second is the magician's finding — the audit manufactures a decoy. Apparatus that emits a badge instead of an output is the failure this panel exists to catch.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: A separate agent that may only prune and never generate — role asymmetry that is mechanically checkable as subset membership against the generated pool.
SAME-THESIS: FAIL — A's single claim is that authoring in a notation that cannot hold prose makes the evasions structural and visible. A prune-only second agent asserts something else: that generation and judgment must be performed by different components. That is a good claim; it is not A's claim.
DELETION: FAIL — merely smaller. Delete the pruner and the docket still demands a ruling, the recipe still demands quantities.
ONE-SENTENCE: FAIL — two subjects, two verbs, two theses.
DISPOSITION: ORTHOGONAL
NOTE: The absorption A actually needs is one neither idea offers — a rule that draws the notation rather than letting the model pick the one that already fits, which is A's live defect and B has nothing that repairs it.

---

## MATCHUP 16
WINNER: B
DECIDED BY: B removes the model's ability to choose the constraint that suits it — the only unsteerable step in either idea — while A's economy is scored by a human who will stop scoring, and its incentive gradient points at the median it claims to escape.

### Distance
VERDICT: B significantly better
REFERENCE: A at Low. B between Mid and High, pushed upward because the domain is selected against fit rather than for it.
PREDICATE: A forbids a persona speaking at length without a one-line differentiation claim — a gate on whether to speak, not on what is said. And the gradient runs the wrong way: cost-per-word plus a user-rated "decisive" bonus selects for the shortest defensible answer, which is the median answer. A mechanism that charges by the word rewards the compressed consensus. B forbids nuclear-reactor-operator, handed "Name who pays and isn't in the room" on a migration review, from producing its standard barriers-and-hold-points answer — it must first structure the review around the on-call engineer and the customers whose data is at stake, neither of whom appear in any runbook.

### Mechanism
VERDICT: B slightly better
REFERENCE: Both at Mid. A has more apparatus; B has less.
PREDICATE: A names a ledger "recorded in the repo" but names no scorer. Every debit that gives the balance meaning requires a human to mark a contribution noise or decisive, and this repo has nowhere for that to happen — commands/ holds three markdown commands and hooks/ holds one file. There is no rating surface, no scoring pass, no accounting step. The fraction of A that executes unattended is zero percent of the loop that matters. Two further operator findings: the bid must itself be generated, so the rationing pass costs tokens the ration was meant to save; and "bankrupt personas retire" is an irreversible operation whose sole credited barrier is a subjective human rating, with no restore path named. B names a deck derived from files that exist today, plus a draw. The draw is one line of code, runs unattended, and is the single step in this matchup the model cannot steer.

### Irreducibility
VERDICT: A slightly better
REFERENCE: A at High in shape. B between Low and Mid.
PREDICATE: A base model prompted "you have a limited lifetime budget; economize" reproduces ~20% of A — it will perform frugality against a balance it does not have and cannot go bankrupt. Prompted "obey this imperative literally even where it does not fit" reproduces ~45% of B, with compliance degrading exactly as the misfit widens, which is the case B cares about.

### Compounding
VERDICT: A slightly better
REFERENCE: A at High on the literal reference but the direction of narrowing cancels most of it. B at Low.
PREDICATE: Use #10 of A produces output from a smaller and differently-composed cast than use #1. But what use #10 produces that use #1 does not is a roster of survivors selected by the user's own ratings, and what a user marks decisive is what the user already agreed with. The axis asks whether it gets weirder with use; A gets narrower toward agreeable, which is homogenization with an audit trail. Use #10 of B produces a different card from a fixed deck. Repo check on B's source: the claim "every knowledge/<slug>/positions.md" is overstated — 16 of 24 roster personas have a positions.md; six have no knowledge directory at all. The substance survives the correction: 16 packs at eight to ten positions each is a deck of ~130-160 real cards.

### Generative failure
VERDICT: B slightly better
REFERENCE: Both between Mid and High.
PREDICATE: A fails as a line in a file reading "nuclear-reactor-operator: BANKRUPT" — a persona retired because its lens was uncomfortable rather than wrong. That artifact does name a hidden assumption, but it is a one-word status change that requires a human to interpret, and the idea names no restore path, so a wrong failure is permanent. B fails as "the soil is the disk; the disk is depleted; let it lie fallow" on a database migration — visibly silly, one paragraph, discarded in a glance. Same insight yield; B's failure costs a paragraph and A's costs a specialist.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The bid — before being staffed, a persona states in one line what it will see that no one else will.
SAME-THESIS: FAIL — B's single claim is that literal obedience to a bad-fit instruction is not a default behavior and that the misfit friction is the generator. The bid asserts something else: that personas should compete on declared distinctiveness. That is an economy claim wearing a one-line coat.
DELETION: FAIL — merely smaller. Delete the bid and the card still lands, still misfits, and still has to be obeyed literally.
ONE-SENTENCE: FAIL — the second clause is about selection, the first about execution.
DISPOSITION: ORTHOGONAL
NOTE: A pre-declaration about the drawn card would pass all three tests, but that is a new mechanism written in B's voice, not A's bid absorbed.
