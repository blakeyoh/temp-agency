## MATCHUP 5
WINNER: B
DECIDED BY: Delete --era and you can still type "answer as a 1911 systems thinker"; delete bin/compile-constraints and nothing in the repo checks compliance at all.

### Distance
VERDICT: A significantly better
REFERENCE: A between High (forbid the problem's own vocabulary) and Ceiling — it bans the concept, not just the word. B between Low and Mid — banned n-grams strip surface tics while the recommendation survives intact.
PREDICATE: A forbids "the feedback loop between hiring and attrition is self-reinforcing" from a 1911 lead, and forbids reaching the same idea under a synonym, since the governor-on-a-steam-engine substitute is a different object with different failure behavior. B forbids "it's important to note this is a robust, holistic framework" but permits the identical recommendation restated as "this framework covers the whole system" — the banned string, not the banned thought.

### Mechanism
VERDICT: B significantly better
REFERENCE: B between High (a script whose output the model must consume) and Ceiling, stopping short because the linter checks post-hoc without forcing regeneration. A between Floor and Low — a flag that changes a string in a prompt.
PREDICATE: B names bin/compile-constraints plus a linter pass over the emitted constraint set. A names no file; there is no era lexicon, no year-gated wordlist, no anachronism checker — the --era flag hands the model a date and trusts it to police its own century.

### Irreducibility
VERDICT: B slightly better
REFERENCE: A at Low (a persona file — real, but promptable), because self-enforced ignorance is the entire mechanism. B between Low and Mid (a parser the model cannot opt out of), held below Mid because the parser rejects strings rather than substance.
PREDICATE: A base model prompted "You are a systems thinker in 1911; use only concepts available in 1911" reproduces ~75% of A — including its leaks, since the model polices anachronism inconsistently and nothing catches it. Prompted "Rewrite this avoiding your stated anti-patterns and hedge phrases" reproduces ~55% of B's constraint text and 0% of the post-hoc check, which is the only part of B that isn't a prompt.

### Compounding
VERDICT: A slightly better
REFERENCE: A at Low — a fresh era supplies genuinely different source material for several uses, then the move becomes legible as a costume change. B at Floor: identical on use #10 as on use #1.
PREDICATE: Use #10 of A instantiates a 1487 persona whose primitives (humoral medicine, guild ledgers, canon law) differ from 1911's, though the procedure is unchanged and nothing narrows. Use #10 of B emits a byte-identical constraint set, because the compiler reads an unchanged profile and no observed violation is ever added back to the ban list.

### Generative failure
VERDICT: B slightly better
REFERENCE: B between Mid and High. A between Floor and Mid.
PREDICATE: A fails as a period-costumed modern answer — "The 1911 systems thinker observes a feedback loop between hiring and attrition" — a leak nothing detects, so the failure ships. B fails as a linter report: banned n-gram 'leverage' line 14; domain-noun count 3 < required 8 — and repeated failure on the noun floor names a hidden assumption, that the profile has no vocabulary of its own, while the gamed case (nouns padded to quota) is noise dressed as compliance.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Dating the persona to a year so that its available concepts, not merely its diction, are period-limited.
SAME-THESIS: FAIL — B's single claim is that constraints must be compiled and checked; an era ban imports a second claim (that the concept is the target) which a string-matching compiler structurally cannot discharge, since banning "feedback loop" yields "self-reinforcing circuit."
DELETION: FAIL — merely smaller. Remove the era lexicon and the compiler still compiles anti-patterns, voice shapes, and hedge lists; it loses one constraint source among four.
ONE-SENTENCE: FAIL — the second clause requires an enforcement the first clause's mechanism does not possess.
DISPOSITION: ORTHOGONAL
NOTE: The monk's objection to the winner stands on its own record: four constraint types where a hedge linter would do, and a minimum-noun-count metric that will be gamed by the first output that meets it.

---

## MATCHUP 6
WINNER: A
DECIDED BY: B's artifact is a prompt — 200 banned phrases pasted into context is the whole mechanism — while a model cannot roll a real die or stamp a seed that regenerates the same world.

### Distance
VERDICT: B significantly better
REFERENCE: B at High and edging toward Ceiling, since banning moves and framings as well as phrases pushes toward output unrecognizable as monk output. A between Low and Mid — the distance comes from the roster being sampled, not from the sampler.
PREDICATE: B forbids the anti-monk from writing "what would be enough here?" — the single most characteristic sentence in his own profile — and forbids the retreat to "simplicity," "presence," and "poverty" behind it. A forbids the model from selecting the contrarian as lens for the fourth time running and from picking its favorite random number, but forbids nothing about what the selected pair then says.

### Mechanism
VERDICT: A significantly better
REFERENCE: A at High — a script that runs, whose output (a seed) the dispatch must consume. B between Floor and Low — structured prose in a markdown file, with no checker anywhere.
PREDICATE: A names bin/draw, which emits a seed stamped in the output header and reproduces the run. B names anti-roster/<slug>.md, which does not run; nothing detects the anti-monk saying "enough" on line 30.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A between Mid and High — external entropy cannot be simulated by a model that has no access to it, though it is not a withheld fact. B at Low, which is the exact reference merely inverted.
PREDICATE: A base model prompted "pick a lead and lens at random" reproduces ~35% of A — it clusters on its favorites and reproduces 0% of the seed-stamped reproducibility, which is not simulable in principle. A base model given the 200-line ban list verbatim as its prompt reproduces ~95% of B, because the file and the prompt are the same object.

### Compounding
VERDICT: A slightly better
REFERENCE: A between Low and Mid — a stamped seed archive accumulates material you may consult but need not obey. B at Floor.
PREDICATE: Use #10 of A produces a stamped world that can be diffed against runs 3 and 7 to show which draw caused which divergence — an audit trail use #1 could not have. Use #10 of B applies the same fixed 200 bans as use #1; the proposal never claims newly minted signature phrases get added, so nothing narrows.

### Generative failure
VERDICT: B slightly better
REFERENCE: B's best failure at High; its common failure at Floor. A at Mid — noise discarded cheaply, with the discount that the noise is reproducible.
PREDICATE: B fails as circumlocution — "the condition of possessing no more than is required" in place of "enough" — a thesaurus costume over the identical answer; but when it fails harder, the persona cannot find its position at all, which names the hidden assumption that the profile encoded vocabulary rather than a way of seeing. A fails as an off-target draw (soccer-referee lens on a soldering question) that is discarded and re-rolled, with the seed making the bad draw reproducible rather than instructive.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Banning the persona's own signature vocabulary, so the shortcut to its position is closed and the position must be re-found.
SAME-THESIS: PASS — A already declares "which constraint card" as one of its seeded draws, so a vocabulary-ban deck is a new deck for an existing draw, not a new claim.
DELETION: FAIL — merely smaller. Remove the ban deck and bin/draw still seeds lead, lens, and mutation selection and still stamps reproducible worlds; it loses one deck among several the mechanism already provides for.
ONE-SENTENCE: PASS — "Every stochastic choice in a dispatch, including which of the persona's own signature phrases are banned this run, derives from one stamped seed."
DISPOSITION: SUBSUMED
NOTE: The winner already contains the slot; what the loser contributes is the content of one deck, which is authoring work rather than absorption.

---

## MATCHUP 7
WINNER: B
DECIDED BY: A's two ceiling-level claims both draw on a novelty scorer the proposal never names, while B's core move is the ruler's own High reference for irreducibility, stated almost verbatim.

### Distance
VERDICT: B significantly better
REFERENCE: B at High, edging to Ceiling in the planted-lie case where the output must be about the discovered contradiction rather than the question asked. A between Low and Mid — it prevents regression rather than pushing any single output outward.
PREDICATE: B forbids the summary from containing the Q3 churn figure, because the figure is genuinely not in the window; the persona must reason from a fragment or declare the gap. A forbids accepting dispatch #4 if it reuses the "stakeholder map plus three risks" shape of dispatch #3 — but only if the unnamed scorer can detect shape reuse, which is nowhere specified.

### Mechanism
VERDICT: B significantly better
REFERENCE: B at High, approaching the Ceiling reference in kind — the model does not consent to a fact being absent and cannot opt back in. A at Floor: a paragraph asking the reviewer, rather than the model, to try harder.
PREDICATE: B's file is the harness's context-assembly step, which drops the fact before the model sees anything; unambiguously executable though the proposal names no path. A names no file, no scorer, and no store for the floor value — "every accepted output sets a novelty floor" has no subject that runs.

### Irreducibility
VERDICT: B significantly better
REFERENCE: B at High — this is the ruler's own reference ("withhold a fact from the context window"), stated by name. A at Low: real, but promptable.
PREDICATE: A base model prompted "pretend the Q3 churn number was never given to you" reproduces ~10% of B — it leaks, hedges, or reasons around the pretence, because it does know. Prompted "never accept an answer less novel than your last one" reproduces ~80% of A; the missing 20% is a persisted floor value across sessions, which is thin and unbuilt.

### Compounding
VERDICT: A significantly better
REFERENCE: A at Ceiling by construction — the constraint tightens automatically and, being monotonic, cannot be relaxed. B at Low — the novelty of degradation fades as the persona develops a stock posture toward it.
PREDICATE: Use #10 of A must clear a floor set by nine prior acceptances, so the permitted answer space is strictly narrower than at use #1 and cannot widen. Use #10 of B injects another draw from a fixed four-item menu (withheld fact, planted lie, token deadline, tool removal) at no greater severity than use #1, and the "degradation reveals priorities" insight was already extracted by run #3.

### Generative failure
VERDICT: A significantly better
REFERENCE: A at Ceiling — the failure is designed to be a proposal worth acting on. B between Low and Mid, dropping below Mid in the fabrication case, which is not cheaply discardable.
PREDICATE: A fails as a dated lock record — "run 14 rejected; floor uncleared by 6 candidates; mechanism exhausted 2026-11-02" — which is itself the instruction to change the mechanism. B fails as either "I cannot answer without the churn number" (a wasted pass) or, worse, a confident fabricated churn figure that reads as a normal answer and must be caught before it can be discarded.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: Monotonicity — a floor that only rises, and that declares the mechanism exhausted when nothing can clear it.
SAME-THESIS: FAIL — B claims a genuinely absent capability cannot be reasoned around; a rising acceptance floor is a second, independent claim about quality governance over time, which does nothing for what degradation reveals.
DELETION: FAIL — merely smaller. Remove the ratchet and the harness still withholds facts, plants lies, cuts deadlines, and still exposes what the persona protects under pressure.
ONE-SENTENCE: FAIL — "Inject real degradation into every run and never inject less than last time" is writable, but it describes escalating hostility, a different mechanism from a novelty floor on outputs; the sentence passes only by rewriting the loser's idea rather than importing it.
DISPOSITION: ORTHOGONAL
NOTE: The ratchet's best asset — a failure that is itself a proposal — is the strongest single design move in this bracket, and it is wasted on an idea with no scorer to ratchet.

---

## MATCHUP 8
WINNER: A
DECIDED BY: B is the most elaborate proposal in the packet and the one a single well-written prompt most nearly reproduces, while A requires a future date to arrive, which no prompt can simulate.

### Distance
VERDICT: A slightly better
REFERENCE: A between Mid and High — it bans the median model register (reasonable, hedged, unfalsifiable) outright. B's ceiling case reaches High (a champion no entrant resembles), but its realized case collapses to Floor, because B's own absorption rule refuses by default.
PREDICATE: A forbids "the lens raises concerns about onboarding scalability" and requires instead "if the lens is right, onboarding-tagged tickets exceed 40/week by March 1." B forbids the champion from being any round-one entrant — but only when absorption succeeds; when absorptions refuse, as they are designed to, B forbids nothing that a ranking would not, and the champion is simply the top seed.

### Mechanism
VERDICT: B significantly better
REFERENCE: B at High — a command that runs, whose box score the process must consume. A between Low and Mid — a structured template with required fields and an unnamed resolver.
PREDICATE: B names /bracket <question> --field 32, which generates a field, seeds it, runs the rounds, and emits an artifact. A names bets/ as a directory but hides its actor in the passive voice — "the repo periodically resolves them" identifies no file, no schedule, and no one who checks whether March 1 arrived.

### Irreducibility
VERDICT: A significantly better
REFERENCE: A between Mid and High — resolution requires a fact necessarily outside the context window, because it has not happened yet. B at Low: elaborate, but promptable end to end.
PREDICATE: A base model prompted "state your disagreement as a dated, falsifiable prediction" reproduces ~60% of A and 0% of the resolution — it cannot simulate having been wrong last quarter, and cannot manufacture a track record it did not live through. Prompted "generate 32 approaches, run single elimination, merge each loser's strongest mechanism into the winner, report the champion" reproduces ~80% of B in one pass today; the residue is judge isolation, which B does not claim.

### Compounding
VERDICT: A significantly better
REFERENCE: A at High, edging to Ceiling — each resolution narrows the space of framings a discredited persona may impose, and the record cannot be relaxed without falsifying it. B at Mid within a single run and Floor across runs.
PREDICATE: Use #10 of A carries resolved bets from use #1, so a persona that lost three predictions can be overruled on record rather than on impression. Use #10 of B is a fresh field with fresh seeds and a fresh champion; nothing from bracket #1 enters bracket #10, because re-entering champions is never specified.

### Generative failure
VERDICT: A significantly better
REFERENCE: A at High, edging to Ceiling. B below Floor in its common case: it produces the default answer with a scoreboard attached, which is worse than silence because it looks authoritative.
PREDICATE: A fails as a bets/ entry marked UNRESOLVABLE when March 1 arrives and "support quality improved" turns out to be unmeasurable — which names the hidden assumption that the disagreement was ever about something observable, and a folder of such entries is itself a proposal to stop staging disagreements about unobservables. B fails as a box score in which every absorption was refused and inconsistent judges produced a champion by seed order, presented with the full apparatus of scores and rounds — a legitimating artifact for an arbitrary result.

### ABSORPTION
LOSER'S STRONGEST MECHANISM: The absorption rule itself — the winner takes the loser's strongest mechanism, so combination replaces discard.
SAME-THESIS: FAIL — A claims disagreement must be dated, observable, and resolvable; absorption claims synthesis beats selection, a second and unrelated thesis about how ideas combine.
DELETION: FAIL — not even smaller. Remove absorption and A still records predictions, resolves them on date, and accumulates standing; absorption was never load-bearing in it.
ONE-SENTENCE: FAIL — grammatically writable but incoherent: resolving a bet produces a party who was right, not a mechanism to take, so the sentence names an object A's process does not produce.
DISPOSITION: ORTHOGONAL
NOTE: Cui bono is worth stating plainly — B is the entrant that most flatters the process now evaluating it, and an idea that rewards its own judging mechanism earns harder questions, not softer ones; the monk's question for it is what field size would be enough, since 32 entrants with a refusal-by-default absorption rule means 24 of them contribute nothing at all.
