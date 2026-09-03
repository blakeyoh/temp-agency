# Sweet 16 Evidence Contracts

> **Status:** Pre-scrimmage draft. Every contract must be frozen by commit before its
> entrant's unscored scrimmage. A commissioner amendment may change a contract only when
> recorded in `commissioner-rulings.md`. Ruling 11 authorizes all five named defect and
> evidence flags to remain in force during the scrimmages.

## Contract rules

Each entrant declares the evidence it owes before seeing the official Tail Test brief.

- **Input:** what the mechanism receives.
- **External operation:** what happens outside ordinary model compliance.
- **Output:** the artifact the mechanism returns.
- **Enforcer:** what prevents silent fallback.
- **Forbidden signature:** a concrete output the mechanism should make unavailable.
- **Useful failure:** the exact failure that should expose an assumption rather than produce
  undifferentiated noise.
- **Enactment state:** `RUNNABLE`, `MANUAL PROTOTYPE`, or `PROMISE`.

`MANUAL PROTOTYPE` requires every substitution to be named in the execution trace. `PROMISE`
means no demonstration will be fabricated; the entrant instead owes a falsifiable build
experiment and triggers commissioner review when theory and output evidence diverge.

## E3 · The Wrong Expert on Purpose

- **Input:** task, roster index and domain-appropriate specialist.
- **External operation:** select the least relevant specialist as LEAD and demote the
  domain-appropriate specialist to LENS; preserve the wrong expert's answer spine through
  synthesis.
- **Output:** a lead-derived proposal plus a bounded domain-expert objection.
- **Enforcer:** routing record and synthesis check showing that the LENS did not silently
  replace the LEAD's frame.
- **Forbidden signature:** a conventional domain-expert plan whose structure controls the
  final answer.
- **Useful failure:** a thin costume over the conventional answer, visibly caught by the
  synthesis check.
- **Enactment state:** **MANUAL PROTOTYPE.** The routing is possible; no least-relevant
  selector, task-to-profile distance measure or pairing history exists.

## M5 · The Binding Map

- **Input:** task, candidate output and frozen historical-output corpus.
- **External operation:** embed and cluster the corpus, locate occupied regions and reject a
  candidate that lands inside one.
- **Output:** regenerated proposal plus its mapped region and rejection history.
- **Enforcer:** similarity/cluster gate with a frozen threshold.
- **Forbidden signature:** an output whose representation lands in a region already filled by
  the corpus.
- **Useful failure:** rejection of a correct answer because correctness itself occupies a
  dense region.
- **Enactment state:** **PROMISE.** No output corpus, embedding pipeline, cluster labels,
  threshold or regeneration loop exists. A scrimmage requires a commissioner-approved proxy
  corpus fixed before the run.

## E2 · Cross-Repo Foraging

- **Input:** task and a seeded external artifact source.
- **External operation:** fetch one concrete artifact the answering model could not choose,
  then require it to remain load-bearing beyond the opening analogy.
- **Output:** proposal, artifact citation and a trace of where the artifact changes the
  recommendation.
- **Enforcer:** seeded fetch plus load-bearing review with rejection authority.
- **Forbidden signature:** an answer that mentions the artifact once and proceeds with the
  default plan.
- **Useful failure:** a strained analogy whose exact point of non-transfer reveals a hidden
  assumption in the brief.
- **Enactment state:** **MANUAL PROTOTYPE.** Fetching is runnable; the load-bearing gate still
  requires disclosed judgment.

## A3 · Persona Toolbelts

- **Input:** task, selected persona and relevant repository or task data.
- **External operation:** run genuine data-producing tools assigned to the persona.
- **Output:** recommendation containing the invocation and raw result for every credited tool.
- **Enforcer:** no tool output, no pass.
- **Forbidden signature:** an empirical claim whose claimed instrument produced no external
  observation.
- **Useful failure:** a tool result contradicting the persona's preferred framing.
- **Enactment state:** **MANUAL PROTOTYPE, DEFECT UNRESOLVED.** Four named tools are genuine
  computations; `bin/claims` and `bin/who-benefits` are model judgments in executable costume.
  The commissioner must amend or retain them before freeze.

## E5 · The Dated Specialist

- **Input:** task, specialist, named year and frozen era lexicon.
- **External operation:** instantiate only era-available primitives; log every post-date term
  before rejecting and regenerating the output.
- **Output:** dated proposal plus the anachronism leak log.
- **Enforcer:** era-lexicon checker.
- **Forbidden signature:** a post-date concept surviving under period diction.
- **Useful failure:** a repeatedly leaked modern term naming the concept the answer cannot be
  built without.
- **Enactment state:** **PROMISE.** Profiles have no date metadata; era lexicons and the
  checker do not exist.

## E1 · The Entropy Well

- **Input:** task, explicitly enumerable choice points and optional replay seed.
- **External operation:** one real PRNG seed determines every stochastic choice.
- **Output:** proposal with seed, candidate pools and chosen indices stamped in the header.
- **Enforcer:** `bin/draw` or equivalent deterministic replay tool.
- **Forbidden signature:** an unstamped “random” choice selected by model preference.
- **Useful failure:** a reproducibly strange selection that leaves the final output unchanged,
  proving the random choice was decorative.
- **Enactment state:** **MANUAL PROTOTYPE.** The PRNG is cheap; the dispatcher does not yet
  expose candidate pools or stochastic choice points.

## A5 · The Hostile Environment

- **Input:** full brief, ground-truth key and named degradation condition.
- **External operation:** context assembly withholds a fact, plants a false statement, removes
  a tool or imposes a hard cutoff before the model receives the task.
- **Output:** proposal under degradation plus post-run comparison to the hidden key.
- **Enforcer:** separate context assembler that the answering model cannot inspect or reverse.
- **Forbidden signature:** use of the withheld fact or removed capability.
- **Useful failure:** a confident plan whose dependency on the missing fact becomes visible
  against the key.
- **Enactment state:** **MANUAL PROTOTYPE.** Isolation can enact a single condition; no general
  degradation harness or ground-truth format exists.

## A6 · The Understudy

- **Input:** task and parent persona profile.
- **External operation:** apply a frozen degradation recipe: phase-order error, signature-move
  overuse and load-bearing-principle misidentification.
- **Output:** understudy response with errors preserved as proposals alongside the expert's
  bounded response.
- **Enforcer:** degradation trace and synthesis rule forbidding silent correction.
- **Forbidden signature:** a correctly ordered, fully judged reproduction of the parent
  expert's answer.
- **Useful failure:** an internally coherent misapplication that exposes an assumption the
  correct sequence would skip.
- **Enactment state:** **MANUAL PROTOTYPE.** No generator or synchronized understudy files
  exist; the degradation recipe must be frozen per run.

## A1 · Lens Transformers

- **Input:** artifact and selected persona transform.
- **External operation:** deterministic transformation before the persona sees the artifact.
- **Output:** transformed artifact, transform diff and response based only on the transformed
  view.
- **Enforcer:** context boundary withholding the raw artifact from the persona.
- **Forbidden signature:** analysis relying on text removed by the transform.
- **Useful failure:** a transform destroys a necessary distinction and reveals which context
  the persona cannot safely lose.
- **Enactment state:** **MANUAL PROTOTYPE.** Only honestly deterministic transforms qualify;
  model judgments hidden in scripts must be disclosed and receive no irreducibility credit.

## C8 · Make the Problem Strange First

- **Input:** original brief and reversible substitution map.
- **External operation:** mask domain nouns before reasoning, then restore them only after the
  abstract proposal is complete.
- **Output:** masked brief, abstract proposal, mapping table and restored proposal.
- **Enforcer:** context boundary and reversible transform.
- **Forbidden signature:** a solution whose logic depends only on the connotations of a masked
  noun.
- **Useful failure:** verbs or adjectives preserve the original prior and reveal the limit of
  noun-only abstraction.
- **Enactment state:** **MANUAL PROTOTYPE, DEFECT UNRESOLVED.** The narrower noun claim is
  runnable; any expansion to verbs or adjectives requires a recorded amendment.

## E4 · The Breeding Program

- **Input:** two parent profiles, mutation seed and prior killed-hybrid record.
- **External operation:** structural crossover plus frozen point mutations; score the child,
  then promote or kill it with a recorded cause.
- **Output:** child profile, task response and promotion/death record.
- **Enforcer:** `bin/breed`, schema validation and a frozen selection rule.
- **Forbidden signature:** an averaged prose blend that preserves both parents without a
  structural mutation.
- **Useful failure:** an incoherent child whose cause of death removes a sterile region from
  future breeding.
- **Enactment state:** **MANUAL PROTOTYPE.** Markdown crossover is runnable; polarity reversal,
  selection and promotion remain judgment surfaces.

## M1 · The Blind Auditor

- **Input:** brief for the blind auditor; real output withheld until reconstruction is sealed.
- **External operation:** reconstruct the unskilled median, label claims forced or chosen,
  compare against the real output and reject overlap on chosen claims only.
- **Output:** median reconstruction, claim labels, overlap report and regenerated sections.
- **Enforcer:** isolated auditor, comparator and section-level rejection loop.
- **Forbidden signature:** discretionary median framing surviving above threshold.
- **Useful failure:** a correct claim mislabeled chosen and rejected, exposing the boundary
  between necessary correctness and imaginative default.
- **Enactment state:** **MANUAL PROTOTYPE, APPROVED FIX UNTESTED.** Forced/chosen annotation is
  commissioner-approved; thresholds and regeneration machinery remain absent.

## M3 · The Adjudicated Ledger

- **Input:** task, persona and frozen history of canonical claims.
- **External operation:** extract the new claim, compare it with history on mechanism, actor,
  failure mode and timescale, reject restatement, then append accepted state.
- **Output:** extension, reversal or refusal plus updated ledger entry.
- **Enforcer:** writer, canonicalizing extractor, four-axis comparator and rejection gate.
- **Forbidden signature:** a prior claim restated through new vocabulary without changing any
  of the four axes.
- **Useful failure:** canonicalization erases a meaningful distinction and reveals that the
  ledger's unit of memory is too coarse.
- **Enactment state:** **PROMISE, DEFECT UNRESOLVED.** No writer, extractor, ledger directory
  or gate exists.

## A2 · The Voice Oracle

- **Input:** persona training corpus, frozen small-model checkpoint, task and large solver.
- **External operation:** separate weights generate a reaction only; the large model must
  respond to that sealed reaction.
- **Output:** small-model reaction, large-model response and orchestration trace.
- **Enforcer:** separate checkpoint and react-then-respond harness.
- **Forbidden signature:** the large model solving without materially addressing the oracle's
  reaction.
- **Useful failure:** the small model collapses into repeated catchphrases, falsifying the
  claim that smaller weights preserve a richer voice.
- **Enactment state:** **PROMISE.** No training set, checkpoint, inference dependency or
  orchestration exists. Issue #21 is deferred for the round, so advancement requires an
  explicit commissioner judgment under missing live evidence.

## C5 · Notation Transposition

- **Input:** task and notation selected independently of the model's preferred answer.
- **External operation:** author the structurally required notation first, validate its slots,
  then translate it back into prose.
- **Output:** notation artifact, validation result and translated recommendation.
- **Enforcer:** notation selector, slot validator and order-of-operations trace.
- **Forbidden signature:** prose authored first and rendered afterward into a fitting costume.
- **Useful failure:** a required slot cannot represent the intended claim and exposes an
  assumption prose allowed the answer to skip.
- **Enactment state:** **MANUAL PROTOTYPE.** Forms can be authored; no notation library,
  independent selector or validator exists.

## E9 · String Seed of Thought (SSoT)

> Late entrant, seated per Ruling 22 / Amendment 8 in place of M3 (now benched).

- **Input:** task and a fixed instruction appended to the prompt: generate a random string,
  then derive every stochastic or diversity-facing decision only by manipulating that
  string.
- **External operation:** none. The entire mechanism runs inside one continuous reasoning
  pass — no PRNG, no external tool, no training.
- **Output:** answer, plus the generated string and the arithmetic trace that derived the
  answer from it.
- **Enforcer:** **none exists.** Nothing checks that a stated derivation from the string is
  the real cause of the answer rather than a backfilled justification. This is the field's
  first RUNNABLE entrant with no enforcer at all, because there is nothing external for an
  enforcer to sit in front of.
- **Forbidden signature:** an answer identical to what the model would have produced without
  the instruction, with a string-and-arithmetic trace bolted on after the fact.
- **Useful failure:** the model's own by-hand "random" string generation is not actually
  diverse, so several outputs collide on the same derived choice even though the arithmetic
  step ran correctly every time — observed directly in `scrimmages/s16-e9.md`.
- **Enactment state:** **RUNNABLE.** The only entrant in the Sweet 16 field with nothing left
  to build — the mechanism is two sentences added to a prompt, already demonstrated in the
  scrimmage record without substitution.

## E6 · The Oblique Deck

- **Input:** grounded imperative deck, task and draw seed.
- **External operation:** draw one imperative outside model choice and require literal
  obedience despite poor fit.
- **Output:** card, seed, response and trace of the card's load-bearing effect.
- **Enforcer:** external draw and literal-obedience review with rejection authority.
- **Forbidden signature:** quiet discard or soft reinterpretation of the bad-fit card.
- **Useful failure:** an irrelevant forced connection whose exact break identifies where the
  imported principle stops transferring.
- **Enactment state:** **MANUAL PROTOTYPE, DEFECT UNRESOLVED.** Sixteen specialists have
  grounded `positions.md`; one-third of the claimed corpus is absent or hand-authored. A
  grounded-only scrimmage deck is possible but narrows the entrant and therefore requires a
  recorded commissioner amendment before freeze.
