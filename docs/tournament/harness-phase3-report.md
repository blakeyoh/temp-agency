# Phase 3 development report

Status: Phase 3 implemented and host-reviewed, including the M1 median seal and
semantic comparison integration. No official dispatch occurred.

## A3

The four executables (`churn`, `seasons`, `units`, `orders`) compute real results and
write replay-exact receipts. History comes from a committed orchestrator snapshot of
114 reachable commits at `192581631d646dadfbdc5c0e120d2b060b618b0f`, covering exactly two
calendar years ending at that commit's timestamp. Every non-root commit is compared
with its first parent, retaining merge changes. Replay consumes the frozen snapshot;
it does not independently authenticate source history or inspect a live `.git` tree.

Units uses pinned Pint 0.26.1, including offset-temperature conversion. Unsupported
units produce failed receipts. The order tool computes positive decimal ratios and
base-10 gaps. Explicit tool-credit blocks bind invocation and raw result to cited
successful A3 receipts. Missing or invented credits fail binding.

Host review corrected entrant enforcement, relative input paths, calendar-window and
UTC validation, first-parent merge handling, offset-unit conversion, and missing-library
handling. The native worker supplied the initial implementation; its quota ended before
final verification, which the host completed. Focused verification: 13 tests passed in
9.96 seconds using the Python 3.13 pinned environment. Tests include all four archive
replays, full dispatch gate, tampered outputs/hashes, false credits, malformed history,
wrong entrants, Celsius conversion and a real temporary git merge.

## M1

The offline NLI comparator uses individually hashed model assets, exact runtime pins,
a fixed rule prefix, bidirectional entailment maximum and a committed 0.7 threshold.
Only CHOSEN median claims trigger rejection. The 16 development calibration/holdout
examples all satisfy their expected decisions; this is a limited fixture, not an
accuracy benchmark. Including schema and real CLI/replay/gate checks, 19 focused tests
passed in 27.53 seconds. One upstream Torch deprecation warning remains.

Host review tightened binding to require exact numbered final proposal items; copying
scored text only into the trace cannot satisfy it. The sealed-median attestation is now integrated: the comparator requires exactly one
cited authenticated seal with matching median bytes. The candidate path must be absent
at the earlier seal commit. The seal verifier reloads immutable git blobs, validates
context hashes and strict ancestry, and checks CLI argument values. It does not claim
cryptographic proof of what the worker saw.

## Runtime

The existing core retains its Python 3.9 syntax floor. Full advanced-tool verification
uses Python 3.13.12, `requirements-harness.lock`, and the local model cache identified by
`HARNESS_MODEL_CACHE`. Libraries are explicitly welcome under the user's policy.
Model inference makes no network requests. Missing assets or runtime drift fail closed.

Full current harness verification: 151 tests passed in 78.12 seconds on Python 3.13.12
with the pinned local model cache; one upstream Torch deprecation warning. This does
not close the pending median attestation integration or Phase 3 as a whole.

## Integrated verification, 2026-09-13

The full suite passes 182 tests in 95.38 seconds on Python 3.13.12 with the real model
cache, including the C5 tests added during Phase 4. One upstream Torch deprecation
warning remains. M1 has an explicit reject-then-regenerate binding test, missing-seal
rejection, and an honest combined seal/comparator full-gate fixture. A3's checks remain
green. The actual isolated Luna fixture at seal commit
`2a21fc45957c03628e55eede5ed421742a4d6ff5` also validates against its committed invocation
and context files; that check did not issue an official receipt.

The Phase 6 authenticity requirement is exercised early: a fabricated median seal is
issued with internally consistent output hashes and chain linkage through the real
receipt writer. Its chain passes, but the full gate rejects its nonexistent external git
seal. This demonstrates why the local nonce/chain is a guardrail, not an authenticity
boundary. Successful hash-attestation hooks run in the gate independently of binding.

Rejected comparison attempts are retained as development negative fixtures. The final
passing gate fixture uses its own valid receipt set; regeneration tests do not pretend a
rejected prior attempt is an accepted final receipt. Official regeneration transcript and
receipt disposition must be specified in Phase 8 directives before dispatch.

Python 3.9 core compatibility: 163 passed, six model-dependent tests skipped, excluding
the Pint-dependent toolbelt suite. This is distinct from the full 182-test runtime check.
