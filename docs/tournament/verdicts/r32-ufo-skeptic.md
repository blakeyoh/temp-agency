## MATCHUP 13
WINNER: A
DECIDED BY: B is a prompt that resets every session; A is cross-session state a prompt cannot fabricate, and B's own text concedes ideas 1-6 will be mediocre every single time.

### Distance
VERDICT: A slightly better
REFERENCE: A between Mid and High — it forbids the persona's own vocabulary, and the forbidden set grows monotonically. B between Low and Mid — the non-adjacency test bites only at the tail of one list and the forbidden set is erased at session end.
PREDICATE: A forbids the investigative-journalist from writing "follow the money — who benefits from this framing?" on dispatch #2, because it is verbatim in knowledge/investigative-journalist/positions.md and would land in the ledger on dispatch #1. B forbids "add a KPI review cadence" at item 12 if "add a metrics dashboard" was item 3 — same mechanism, same actor. A's ban is permanent; B's expires at the end of the response.

### Mechanism
VERDICT: A significantly better
REFERENCE: A between Mid and High — the ledger is external state read at dispatch, though nothing rejects. B at Low, one step above the Floor paragraph.
PREDICATE: A names ledger/<slug>.jsonl. Checked: no ledger/ directory exists in this repo and the only executable files are docs/tournament/tally.py and docs/tournament/build_box_score.py — so the append step is currently unbuilt, and A is a named-but-absent file. B names no file at all; the relatedness test is adjudicated by the same model that generated the items, which is self-grading with no artifact.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A between High and Mid — the ledger's contents are a fact about the model's own past that the model cannot generate. B at the Floor, because B IS the prompt.
PREDICATE: A base model prompted "Give me 19 improvements to this plan; each must be unrelated to every previous one on a stated axis — different mechanism, actor, failure mode, or timescale — and declare the axis" reproduces ~95% of B. Prompted "You are the farmer; do not repeat yourself" reproduces ~20% of A at N=1 and near 0% at N=10, because it cannot know which fourteen positions were already banked.

### Compounding
VERDICT: A significantly better
REFERENCE: A at High, short of Ceiling only because a human can prune the ledger. B at the Floor.
PREDICATE: A's use #10 produces a position the persona is structurally barred from reaching by nine banked claims — it must extend, reverse, or refuse, and refusal is itself new output. B's use #10 produces the same first six mediocre items as use #1, because nothing carries between sessions; the toll B describes is paid in full again every time.

### Generative failure
VERDICT: Tie
REFERENCE: Both between Mid and High. Neither reaches Ceiling.
PREDICATE: A fails as a paraphrase laundered as growth — "Extending my earlier position: incentives should be mapped before intentions are credited" logged as new when the ledger already holds "follow incentives, not intentions"; that failure is checkable against the ledger and reveals the persona had one real move. B fails as a fabricated axis — "Idea 12 (unrelated axis: timescale)" attached to idea 3 with a new noun; that failure is checkable against the item text and locates the exact index where the model ran out.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The requirement that each new item name the axis on which it is unrelated to all previous ones.
SAME-THESIS: PASS — A's rule "you may not restate any of these; you may extend, reverse, or refuse" is undefined without a relatedness test; the axis declaration is the adjudication A already needs, not a second claim. Only the axis test is taken; the quantity mandate of 19 is not.
DELETION: PASS — worse, not smaller. Without a stated axis, "restate vs. extend" is judged by vibes, the ledger fills with certified paraphrases, and the narrowing mechanism stops narrowing. The remaining apparatus keeps running while producing nothing.
ONE-SENTENCE: PASS — "A persona's past positions are handed back to it, and each new position must name the axis on which it departs from them or be refused as a restatement."
DISPOSITION: ABSORBED
NOTE: This is the rare absorption where the loser supplies the missing predicate of the winner's own rule rather than a second feature.

---

## MATCHUP 14
WINNER: B
DECIDED BY: B changes the weights — the Irreducibility ceiling — while A is a paragraph any competent prompt already produces, and A's characteristic failure silently returns the default answer with a clean bill of health.

### Distance
VERDICT: B slightly better
REFERENCE: A between Floor and Low — the recommendation survives untouched and a diagnostic section is appended. B between Mid and High, discounted because a 0.6B's off-distribution output may be degenerate rather than usefully far.
PREDICATE: A forbids delivering "here are three ways to improve onboarding" without an adjacent statement that this answers a retention problem nobody posed — but it does not forbid the recommendation itself, only its unlabeled delivery. B forbids the transcript from containing only house register: "That's a fair challenge — let me synthesize both views" cannot be the persona's reaction, because the reaction is not generated by the model that writes that sentence.

### Mechanism
VERDICT: B significantly better
REFERENCE: A between Low and Mid. B at High, short of Ceiling because nothing rejects the large model's response to the reaction.
PREDICATE: A names no file — the reverse brief is an additional prose section produced by the same model in the same pass. B names no file either, but its artifact class is unambiguous and inspectable: a checkpoint plus an inference call, one per persona. B's gap to a running file is a training script; A's gap is unbridgeable because there is nothing to run.

### Irreducibility
VERDICT: B significantly better
REFERENCE: A at Floor-to-Low. B at the Ceiling reference ("change the weights"), discounted one notch for the contamination described below.
PREDICATE: A base model prompted "Now write the problem statement for which your recommendation would be the perfect answer, then diff it against the actual problem" reproduces ~95% of A. Prompted "React as the Franciscan monk — blunt, no solutions" reproduces perhaps 30% of B. Checked against the repo: the packs are 663-1,687 words each (knowledge/investigative-journalist/ is 665 words; knowledge/franciscan-monk/ is 1,228), far too little to fine-tune a voice, so the actual training signal is the synthetic in-character dialogue — generated by the large aligned model. B's stated claim ("separate weights cannot regress toward a house they do not have") is therefore partly false: the house voice is distilled in through the training set. The residue that survives — genuine incapacity to be diplomatic — is still unpromptable.

### Compounding
VERDICT: Tie
REFERENCE: A at Floor. B at Low, which is not better in kind.
PREDICATE: A's use #10 produces a different gap because the input differs, but the mechanism carries nothing forward — no gap register, no accumulation, no narrowing. B's use #10 produces a reaction from a fixed checkpoint whose repertoire is small precisely because the model is small; by use #10 the reader has seen most of its moves. The property that guarantees B's irreducibility — tiny weights — also guarantees a narrow repertoire.

### Generative failure
VERDICT: B significantly better
REFERENCE: A at the Floor. B between Mid and High.
PREDICATE: A fails as "Reverse brief: how do we improve onboarding? Diff against stated problem: no material gap." The same model wrote both the answer and the brief, so it reverse-engineers the brief it was handed rather than the one its answer implies — the output is the default recommendation now stamped as validated. That is worse than an error; it launders. B fails as degenerate in-character output — "What is enough. What is enough. Brother Sun." — which the large model must respond to; the response is often graceful nonsense, discarded cheaply, and occasionally forces it to name what "enough" would mean here. B's failure cannot silently become the default answer, because a reaction is always injected.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Derive the problem statement for which the recommendation would be the perfect answer, then diff it against the real one.
SAME-THESIS: FAIL — B's single claim is that voice must live in separate weights or it regresses. The reverse brief is a claim about problem-framing fidelity and says nothing about voice; it is a second thesis wearing the same jacket.
DELETION: FAIL — merely smaller. Delete the reverse brief and the oracle still reacts in a register the large model cannot produce.
ONE-SENTENCE: FAIL — the "and also" cannot be removed: two mechanisms, two outputs, no shared object.
DISPOSITION: ORTHOGONAL
NOTE: The reverse brief is a good move belonging to someone else's thesis; bolting it onto the oracle turns a single claim into a bundle.

---

## MATCHUP 15
WINNER: A
DECIDED BY: A sits at the Distance ceiling on every sentence it produces, while B's gate — the only thing lifting it above a prompt — certifies a property that still permits a fully median delivered answer.

### Distance
VERDICT: A significantly better
REFERENCE: A at the Ceiling reference and its own text states it verbatim: "the output is unrecognizable as an answer to the question until it is translated back." B between Low and Mid, because it constrains the composition of a candidate pool, not the form of any output.
PREDICATE: A forbids "we should consider a phased approach, balancing speed against quality" — a docket has no slot for it; you must name the moving party, the motion, and the ruling, and a knitting pattern has no stitch for "stakeholder alignment." B forbids nothing at the sentence level: it forbids only a pass in which no top-decile-weird candidate survived. A final answer consisting of four median bullets plus one strange one passes B's audit intact.

### Mechanism
VERDICT: B significantly better
REFERENCE: A between Low and Mid. B between High and Ceiling — the rerun is a gate that regenerates without the model's consent, discounted because the trigger is model-scored.
PREDICATE: A names no file and needs none; the notation is authored in-pass and the model certifies its own compliance. B names no file either, but its three movements are separate calls with a programmatic retry, which is an orchestrator. Load-bearing gap: B never says who computes "top decile of weirdness." If it is a third agent's judgment, the gate is scored against the model's own median and the mechanism is circular; if it is a computable metric (perplexity, embedding distance from the HOT centroid), it is genuine. B leaves its single most important detail unstated.

### Irreducibility
VERDICT: B significantly better
REFERENCE: A at Low. B between Mid and High.
PREDICATE: A base model prompted "Express your position as a court docket — parties, motion, ruling — then translate it back to prose" reproduces ~90% of A. Prompted "Generate 20 wild short samples, prune them in a separate step, keep at least one of the weirdest, and start over if you didn't" reproduces ~50% of B: HOT and COLD are both promptable, and the model will silently conflate generate-and-prune, but a model asked to decide whether to rerun itself decides not to. B's irreducible core is the rerun alone — real, but thin relative to its footprint.

### Compounding
VERDICT: A slightly better
REFERENCE: A at Low. B at the Floor.
PREDICATE: A's use #10 produces a knitting pattern demanding gauge and repeats where use #1 produced a docket demanding a ruling — a genuinely different commitment set, though nothing narrows and the listed menu holds seven notations, so the eighth pass starts recycling. B's use #10 produces the identical three-movement pass with identical thresholds; the weirdness decile is recomputed within each pass and is therefore relative to that pass, so nothing tightens across uses.

### Generative failure
VERDICT: A significantly better
REFERENCE: A at High. B between Low and Mid, and the waste is the expensive kind.
PREDICATE: A fails as prose in costume — "Row 1: consider stakeholder needs. Row 2: repeat as needed." That output is unusable and is simultaneously the finding: the position contained no quantity, no order, and no actor, which is precisely what the notation was there to expose. B fails as a rerun that reproduces the same distribution because nothing about the pass changed — 2x tokens for the same result, with no stated termination condition, so the pathological case is an audit loop that never clears.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: An audit that reruns the whole pass unless a top-decile-weird candidate survived pruning.
SAME-THESIS: FAIL — A's claim is that prose permits evasions a notation makes structural. The audit's claim is that generation and judgment must be separated so discards become auditable. A constrains form, the audit constrains sampling variance.
DELETION: FAIL — merely smaller. Remove the audit and the docket still demands parties and a ruling; the recipe still demands quantities and an order.
ONE-SENTENCE: FAIL — the "and also" is load-bearing; the two halves share no noun.
DISPOSITION: ORTHOGONAL
NOTE: A validator that rejects a knitting pattern which is secretly prose would genuinely serve A's thesis — but that is an invention of ours, not B's mechanism, and absorbing an idea we had to redesign is not absorption.

---

## MATCHUP 16
WINNER: B
DECIDED BY: A's selection pressure runs toward user approval, which retires exactly the personas whose friction is the product — it gets tamer with use, which is the opposite of the axis it is competing on.

### Distance
VERDICT: B significantly better
REFERENCE: B between Mid and High, because the imported constraint comes from another persona's epistemology rather than a domain the model selects, and literal obedience blocks the graceful drop. A at Low, and below the Floor over time: budget pressure shortens output without moving it, and terseness is not distance.
PREDICATE: B forbids the anthropologist's field-observation memo from omitting soil when "Ask what the soil requires" is drawn — the bad-fit obedience is mandatory, and the persona cannot quietly drop it. A forbids the 800-word persona monologue that restates the brief. Shortening a median answer leaves a median answer; A names no output whose content becomes impermissible.

### Mechanism
VERDICT: B slightly better
REFERENCE: Both between Low and Mid. B's required apparatus is one text file and one random draw; A's is a metering runtime plus a permanent human grading habit.
PREDICATE: Neither names one. A says the budget is "recorded in the repo" — checked: no balance file exists, nothing in the repo can decrement tokens, and the noise/decisive marking has no collection point anywhere, so the accounting is honor-system markdown maintained by hand. B implies a deck file whose source corpus verifiably exists — 16 positions.md files of roughly 5-10 bullets each, about 100 candidate lines — and needs only shuf -n1. B's unspecified randomizer is the real gap: a model asked to draw its own card draws one that fits, which is exactly the failure B targets.

### Irreducibility
VERDICT: A slightly better
REFERENCE: A between Low and Mid — the cross-session balance is genuine state, conditional on a human loop that does not exist. B at the Low reference explicitly: "hand the model a persona file — real, but promptable," which is literally what a card is.
PREDICATE: A base model prompted "Here are ~100 one-line imperatives from other personas; here is one at random; obey it literally even where it doesn't fit" reproduces ~65% of B — the obedience instruction transfers, the external draw does not. Prompted "You have 5,000 tokens left for your career; bid one line on what you'll see that no one else will, and spend sparingly" reproduces ~70% of A within a session and 0% of the cross-session balance. Verification note on B's repo claim: it says "Every knowledge/*/positions.md is distilled," but only 16 of 24 built specialists have one — civil-rights-activist and missiologist have knowledge directories without positions.md, and anthropologist, chief-of-staff, contrarian, executive-coach, left-fielder, and pediatric-occupational-therapist have no pack at all. Of the three exhibited cards, only "Ask what the soil requires" plausibly distills existing text (knowledge/farmer/positions.md); "Name who pays and isn't in the room" appears in no positions.md, and "Restart from the last honest state" appears nowhere in the repo — the nearest line is nuclear-reactor-operator's "Known state before action." Two of three sample cards are authored, not compiled. The deck is real but smaller and more hand-made than advertised.

### Compounding
VERDICT: Tie
REFERENCE: A at High on the mechanical reading and arguably Ceiling, since retirement cannot be relaxed — but the narrowing runs toward the median, so on the axis as written it fails while satisfying its predicate. B between Low and Mid.
PREDICATE: A's use #10 produces a bid from a persona at 40% of lifetime budget that has learned which claims got marked noise, drawn from a roster missing whoever went bankrupt first. B's use #10 produces the tenth distinct card from a ~100-line deck — different, but no tighter, and the deck repeats once drawn down. A narrows in the wrong direction; B varies without tightening.

### Generative failure
VERDICT: B significantly better
REFERENCE: A at the Floor, and worse than the Floor in one respect: the failure is self-reinforcing and irreversible. B between Mid and High.
PREDICATE: A fails with no error anywhere — the contrarian, the civil-rights-activist, and the franciscan-monk accumulate "noise" penalties because their contributions are unwelcome by design, go bankrupt, and retire, leaving an agreeable roster producing the median answer more cheaply than before. Nothing in the mechanism can distinguish a persona that was noisy from one that was uncomfortable and correct. B fails as "Ask what the soil requires" drawn for a database migration review, producing a strained paragraph about the schema's soil: obviously unusable, cheap to discard, labeled with the card that caused it, and occasionally naming the hidden assumption.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The one-line bid — a persona must state, before being staffed, what it will see that no one else will.
SAME-THESIS: FAIL — B's claim is that a model applies a suggestion where it fits and quietly drops it where it doesn't, so literal obedience to a bad fit is the generator. The bid is an argument about fit, made by the persona in its own favor; it imports a second claim about competitive staffing.
DELETION: FAIL — merely smaller. Delete the bid and a card is still drawn and still obeyed literally.
ONE-SENTENCE: FAIL — the two halves are contradictory selection principles: random imposition versus self-nomination by fit.
DISPOSITION: ORTHOGONAL
NOTE: A persona that must obey a randomly drawn card cannot honestly promise in advance what it will see, so the bid does not merely fail to help — it asserts a certainty B's mechanism removes.
