# Phase 3 commissioner decision: what counts as M1 overlap?

Status: decision requested; no comparator or official threshold has been selected.
Phase 2 implementation is committed as `56ebe7f` and passes 119 tests on Python
3.9.6 and 3.13.12. This note does not amend an entrant or authorize a dispatch.

## Evidence

- `evidence-contracts-s16.md`, M1: reconstruct the median in isolation, label claims
  FORCED/CHOSEN, reject overlap on CHOSEN claims, and regenerate rejected sections.
- `commissioner-rulings.md`, Open items carried into the Sweet 16: the commissioner
  approved FORCED/CHOSEN annotation, but the fix was untested.
- `scrimmages/s16-m1.md`, Pre-run declaration and Pass 3: the intended gate is
  described as semantic overlap; the scrimmage used manual judgment and explicitly
  disclosed the absence of a numeric threshold and reproducible comparator.
- `enactment-harness-plan.md` sections 8.3 and 9 require `bin/overlap` to perform a
  real computation over committed inputs and a threshold. They do not name a metric,
  calibration set, or threshold value. The implementation floor is Python 3.9 stdlib.

## Why this changes behavior

An exact-token metric detects reused wording. It does not reliably detect a generic
idea expressed in different words. Selecting that metric would let M1 retain ideas
its mechanism is intended to reject merely by paraphrasing them. Conversely, a broad
semantic metric can reject distinct proposals that happen to share the brief's subject.
The threshold and calibration examples must be frozen before official generation.

Illustration using lowercased word-set Jaccard similarity (intersection / union):

| Median | Candidate | Score |
|---|---|---:|
| Submit complaints without names through a shared form. | Report disturbances anonymously using one common questionnaire. | 0.000 |
| Submit complaints without names through a shared form. | Submit complaints without names through a shared form. | 1.000 |

The first pair expresses substantially the same proposal with different vocabulary.
This example illustrates the limitation; it is not a calibrated semantic benchmark.

## Recommended direction: preserve meaning-level overlap

Use a pinned local semantic representation model and a deterministic numerical
comparison. Pin model files, version, preprocessing, thresholds and calibration cases
before official dispatch. The runtime must not silently fall back to word overlap.
Keep FORCED/CHOSEN labels as separately frozen, disclosed model judgments, and require
the replacement pass to be rechecked. The host verifies all resulting artifacts.

This direction needs an explicit exception to the stdlib-only implementation floor
for the semantic scorer. It adds dependencies and model-artifact management. It does
not eliminate the carried defect: a necessary claim mislabeled CHOSEN can still be
wrongly rejected. Detailed model selection and threshold calibration follow this
architecture decision; no specific model or quality claim is being assumed here.

## Alternative: authorize a text-overlap proxy

Keep Python stdlib only and freeze an explicitly named lexical metric with a numeric
threshold and calibration cases. Document it as a text-overlap proxy, including the
paraphrase escape. This is simpler and replay-exact, but narrows what M1 enforces.
It must not be represented as measuring semantic overlap.

## Boundary

This choice changes which proposals survive the rejection loop, so the host has
stopped before making it. A6 distinctness (Ruling 25), entrant standing and official
start authorization remain deferred; this note rules on none of them.
