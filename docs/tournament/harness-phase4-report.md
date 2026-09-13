# Phase 4 development report

Status: C5 complete; E2 fetch adapter and deletion gate in progress. No official dispatch.

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
receipts or constitute a selected official artifact. The one-module GLM adapter request
is pending review. The fetch alone does not close E2: a substantive deletion/rejection
gate and its calibration remain required.

Sources checked: https://www.mediawiki.org/wiki/API:Random and
https://www.mediawiki.org/wiki/API:Revisions.
