# E2 deletion gate: independent evaluator approved

The commissioner approved the independent evaluator with binding rejection authority
on 2026-09-13. Implementation and validation follow this recorded decision.

## Contract

Amendment 5 requires an item to be rejected and regenerated when removing the external
artifact leaves its substance unchanged. A pass needs at least three surviving
artifact-dependent items. A real fetch followed by operator self-review was explicitly
insufficient in the scrimmage.

## Evidence from the current comparator

The four development pairs in `deletion-probe.json` compare complete versus manually
ablated proposals using the same pinned NLI model used by M1. They are small authored
architecture probes, not a benchmark, and are not claimed to be generated from a real
foraged article. Two references are decorative; two remove a concrete operating rule.

At the existing 0.7 threshold, using the maximum directional entailment score calls all
four similar (>0.99), rejecting the two changed mechanisms. Using the minimum calls all
four different (<0.001), accepting the two decorative references. This is expected to be
a difficult transfer: NLI detects omitted propositions, including decorative source facts;
it does not directly judge whether a borrowed mechanism is load-bearing. These results
rule out simply reusing M1's metric/threshold. They do not prove that no deterministic
classifier or other model could work.

## Recommended implementation: independent evaluator with binding veto

An isolated evaluator sees only the frozen brief, verified artifact, numbered candidate
items and an explicit deletion-test rubric. It must return one structured verdict for
every item: survives deletion unchanged, artifact-dependent, or indeterminate. Every
verdict includes quoted proposal spans and a concrete account of the operating change
that disappears when the artifact is removed. Indeterminate does not pass.

The host records the exact evaluator context hashes, prompt, model/provider, response and
request receipt. Its verdict is hash-attested rather than replay-exact. A deterministic
gate enforces coverage, rejects unchanged/indeterminate items, requires regeneration and
re-evaluation, and permits a final record only with at least three surviving dependent
items. The evaluator has actual veto power; its output is not advice the generator can
ignore. The host continues reviewing all implementation code and tests.

This changes the amended gate from a wholly deterministic semantic decision into
mechanical enforcement of a disclosed independent model judgment. The model can still
be wrong; isolation and reasoning evidence are auditable, not proof of causality.
Commissioner approval was given for this E2 interpretation of Amendment 5. This note
does not resolve deferred Rulings 24/25 or authorize official dispatch.

## Alternative: keep the semantic decision fully deterministic

Leave E2 NOT ENACTED while a purpose-built dependency classifier or causal comparison
protocol is developed and validated on a larger set of decorative and substantive
examples. Do not lower a threshold merely to make these four probes pass. Other entrant
work could proceed after the commissioner explicitly chooses to defer E2.

## Current code boundary

`bin/forage` obtains a real server-selected revision after a committed `bin/draw` corpus
selection. Attestation independently resolves its revision and exact text on the server.
The binding intentionally fails `deletion_gate` until this decision is resolved, even
when every source check passes. No fetch-only record can pass as enacted E2.

## Competition framing (commissioner suggestion)

The commissioner compared foraging to art competitions in which randomly selected
required elements must visibly shape the finished work. Use that framing to encourage
visible incorporation of the artifact's specific structure, behavior or constraints.
The evaluator still asks whether removing those borrowed elements changes the proposed
operation; visibility alone cannot substitute for dependence. Preserve E2's one-artifact
corpus/server draw. The analogy is not an instruction to add three independent draws.
