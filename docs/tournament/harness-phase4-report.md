# Phase 4 development report

Status: C5 complete; E2 source acquisition and approved independent-evaluator gate implemented. Model calibration remains development evidence. No official dispatch.

## C5 notation transposition

`bin/notation --mode select` draws one of seven committed notation forms independently.
The selection receipt is committed before an authored JSON artifact exists. The validate
stage consumes that committed selection receipt, catalog and authored artifact, validates
its form-specific slots and emits a deterministic result. Slot violations produce an ok
receipt with `passed: false`; malformed data produces a failed receipt. Both stages
replay from their named git archives.

The binding rule recomputes the result, matches the selection input to the actual cited
receipt, checks prior commit ancestry and absence of the artifact path at selection time,
requires both outputs in the execution trace, and maps every numbered translated proposal
item to its notation item ID. This verifies structural compliance and recorded sequence;
it does not prove semantic correctness of the translation or hidden authoring causality.

The catalog covers recipe, court docket, knitting pattern, chess annotation, liturgical
rubric, flight checklist and circuit diagram. GLM supplied the catalog and slot validator
in 51.364 seconds for $0.0230762. Host review corrected recipe ingredient typing,
non-finite numeric acceptance and zero item counts, then added the CLI, binding and tests.
See `harness-delegations.json` for request IDs, manifests and usage.

Verification: 19 focused C5 tests pass, including valid/invalid fixtures for all forms,
two-stage archive replay, an honest full gate, false selection, altered translation
mapping and missing selection citation. The integrated suite passes 182 tests with one
upstream Torch deprecation warning. Configs may use smaller item counts for tests; the
committed Tail Test catalog requires 24.

## E2 work in progress

Live probes on 2026-09-13 reached both English and Simple English Wikipedia random
revision endpoints over HTTPS. Both returned a server revision ID, UTC revision timestamp,
HTTP Date and article text. Probes were development connectivity checks and did not issue
receipts or constitute a selected official artifact. The one-module GLM adapter returned in 36.717 seconds for $0.0183018. Host review
corrected redirects before following, suppressed-content markers and error handling.
`bin/forage` now consumes a committed corpus-selection receipt from `bin/draw`, invokes
the chosen server's random endpoint once, and emits a hash-attested receipt. Verification
independently resolves the selected revision, exact text and timestamps, with pinned
input/argv checks. Network failure produces a failed receipt without a substitute draw.

A live development check fetched page 2932986, revision 1365146037 (Francis S. Gabreski
Airport) at HTTP Date `Sun, 13 Sep 2026 12:22:01 GMT`; independent revision lookup passed.
Content SHA-256: `05cd340b352a1732628f05267be088496ea5873c62b83b2c93826f26b5258861`.
This was a connectivity/adapter check, not an official corpus draw or receipt.

The full suite passed 200 tests in 94.47 seconds, with one upstream Torch warning.
Final source-input hardening is covered by the focused E2 suite. Tests verify exact
revision lookup, forged IDs/text/times, malformed payloads, no redirect following,
network failure, source-input mismatch and a fetch-only full-gate rejection. A passing
source attestation alone cannot produce a passing E2 bind.

The commissioner approved an independent model evaluator with binding veto.
`bin/forage-gate` reads a prior git seal of the brief, source, candidate, rubric,
manifest, model response, invocation and actual fetch receipt. The verdict schema
requires exact source/proposal quotes. All items must be dependent and at least three
must survive. Unchanged or indeterminate items require regeneration under stable IDs;
all rounds remain cited, connected and visible in the trace. The final proposal must
match the last accepted candidate verbatim. Forks, missing predecessors, self-review,
extra context/instructions, changed sealed inputs and forged attestations fail closed.

The host owns code review, execution and source-grounding checks. A sealed model response
is an orchestrator attestation, not cryptographic proof of hidden context or causal
influence. Actual model calibration includes both useful rejections and evaluator errors;
see `forage/calibration/README.md`. The development subset is not the eventual 24-item
Tail Test and did not issue an official fetch/evaluation receipt.

Sources checked: https://www.mediawiki.org/wiki/API:Random and
https://www.mediawiki.org/wiki/API:Revisions.

Final gate verification: 220 tests pass on Python 3.13.12 in 118.40 seconds, with one
upstream Torch deprecation warning. The focused evaluator suite includes unchanged-item
resubmission, missing predecessor citations, forked lineages and hidden manifest instructions.
