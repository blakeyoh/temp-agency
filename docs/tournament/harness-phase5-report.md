# Phase 5 development report

E6's committed deck and executable are implemented. E4, E5 and E3 executables are now
implemented at the scopes documented below. The commissioner has settled E4/E5 scope and approved the small E3 evaluator.
Full independent contract review and packet/directive integration remain. No official
dispatch. The integrated suite passed 250 tests in 122.46 seconds with one upstream
Torch warning; final E3 label hardening additionally passed nine focused tests.
The partial independent E3/E4/E5 contract read is recorded in
`contract-review/phase5-host-findings.md`.

## E6 oblique deck

The host reviewed GLM's full sixteen-pack, 480-card distillation against all source
positions. The first ten cards per pack are excluded mechanically, leaving 320 eligible
cards. The executable samples source packs from the full counted corpus, then a card
from their eligible cards. Missing/extra packs, source drift, bad card counts, duplicates
within a pack and changes to the ten-card exclusion fail closed. It pins every pack and
the deck as receipt inputs, and performs no model distillation at dispatch time.

Ten focused tests pass, including honest full-gate acceptance, archive replay despite
working-tree deck replacement, rejection of a merely related card, missing/added/removed
packs, source edits, illegal first-card eligibility and deterministic full-corpus
reachability. The actual committed deck validates with all sixteen sources. The prior
integrated suite passed 220 tests before E6 was added.

The declared bound span is the real corpus draw and verbatim selected imperative.
Literal semantic obedience is not mechanically established. See `deck/README.md` and
`harness-delegations.json` for source and model provenance.

## E4 crossover builder

`bin/breed` implements the executable crossover portion of E4. It takes `Core Principles`
from parent A, `Methodology` from parent B, and interleaves both parents' `Anti-Patterns`
with seeded deterministic ordering. It requires distinct parents and at least two numbered
methodology phases, pins both parent hashes, and replays exactly from the committed archive.

Five focused E4 tests pass. The implementation is deliberately crossover-only: point
mutation, child scoring, promotion, and death history from the full original breeding
contract are not implemented. The commissioner explicitly confirmed this intended stage scope.

## E5 dated specialist checker

`bin/lexicon-check` implements the frozen 1911 checker over all 24 real roster profiles.
It validates structured candidate items against the model-authored 1911 surface blacklist,
using NFKC normalization and punctuation, underscore, and whitespace-tolerant term matching.
`--previous` retains rejected rounds in a regeneration chain; the binding requires stable
IDs, changed leaking items, a single non-forked chain, and an exact final proposal match.

Nine focused E5 tests pass. The checker measures the frozen surface list and its normalized
variants. It cannot detect hidden modern concepts or every conceptual anachronism. This is
a limitation the commissioner accepted without adding another review step.

## E3 opposite-specialist routing

`bin/route` validates the complete 24-profile roster against the built-profile index, then
computes unique-token Jaccard overlap after NFKC normalization and frozen stopwords. It
selects the lowest-overlap profile eligible for LEAD, excluding the orchestrator-supplied
domain specialist recorded as LENS, with slug-ascending tie-breaking. The receipt pins the
brief, index, and every profile hash.

Nine focused E3 tests pass, including three adversarial label-hardening cases.
The route binding now requires the small independent frame gate. `bin/frame-gate` reuses
E2's sealed verdict and regeneration enforcement, validates the exact routed profile and
brief, and matches the final candidate after LENS input. Three focused integration tests
cover an accepted complete chain, rejection/regeneration, altered final prose, missing
prior rounds, substituted frames and self-review. The full suite passed 256 tests in
139.05 seconds; the plain-text frame normalization was then checked with the focused suite.
