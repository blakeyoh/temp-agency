# Phase 3 development report

Status: A3 implemented and host-reviewed; M1 semantic comparison implemented, median
attestation and end-to-end integration still in progress. No official dispatch occurred.

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

## M1 work in progress

The offline NLI comparator uses individually hashed model assets, exact runtime pins,
a fixed rule prefix, bidirectional entailment maximum and a committed 0.7 threshold.
Only CHOSEN median claims trigger rejection. The 16 development calibration/holdout
examples all satisfy their expected decisions; this is a limited fixture, not an
accuracy benchmark. Including schema and real CLI/replay/gate checks, 19 focused tests
passed in 27.53 seconds. One upstream Torch deprecation warning remains.

Host review tightened binding to require exact numbered final proposal items; copying
scored text only into the trace cannot satisfy it. M1 is not complete until the separate
sealed-median attestation, chronology and final comparator binding are integrated.

## Runtime

The existing core retains its Python 3.9 syntax floor. Full advanced-tool verification
uses Python 3.13.12, `requirements-harness.lock`, and the local model cache identified by
`HARNESS_MODEL_CACHE`. Libraries are explicitly welcome under the user's policy.
Model inference makes no network requests. Missing assets or runtime drift fail closed.

Full current harness verification: 151 tests passed in 78.12 seconds on Python 3.13.12
with the pinned local model cache; one upstream Torch deprecation warning. This does
not close the pending median attestation integration or Phase 3 as a whole.
