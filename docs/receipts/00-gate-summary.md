# Phase 0 — Evidence Gate: Summary

**Question:** Does a staffed LEAD + LENS pass materially change real plan/review outcomes vs an unstaffed baseline?

**Method:** 3 real tasks from the owner's live projects, each run through 3 isolated Sonnet subagents (baseline / LEAD / LENS) with identical inputs and no cross-visibility, followed by a synthesis diff. 2026-07-02.

## Result: GATE PASSED — 3 of 3 tasks showed the lens materially changing the decision.

| # | Task | Staffing | What the lens caught that baseline missed |
|---|---|---|---|
| [01](01-invisible-ink-forged-scores.md) | invisible-ink #141 — forged classification scores (plan) | systems-thinker + behavioral-psychologist | The planned fix would make cheating harder to *see*, not *do* (in-range forgery is less detectable than the unbounded kind); and a server-side rewrite could destroy the reveal-screen social auditing that moderates the game for free. |
| [02](02-mycelium-boot-states.md) | mycelium #70 — first-time vs returning boot (plan) | behavioral-psychologist + franciscan-monk | The issue's premise deserved cross-examination — the "fix" imports loss-aversion retention mechanics into a game whose identity is contemplative sameness; the minimal honest version is one boolean + one line of copy, not 60 lines. |
| [03](03-mycelium-leaderboard-review.md) | mycelium #82+#83 — leaderboard spec drift (review) | investigative-journalist + farmer | Baseline would implement against acceptance criteria citing a function that doesn't exist, patch the 4th symptom of a 4-site pattern without touching the duplicate-writing root, and ship against a test suite that can't run. |

## Observations that shape the build

1. **Baselines were competent, not weak.** Every unstaffed pass was correct and shippable. The lens value was not "catch the obvious miss" — it was reframing (Shifting-the-Burden archetype), premise-challenge (is this even the right fix?), and second-order constraints (social contract, maintenance root). This is the durable claim: strong models already reason well; the lens changes *what question gets asked*.

2. **Cross-agent convergence is a signal.** In task 01, LEAD (systems) and LENS (behavioral) independently flagged `hasSpeedBonus` as the next exploit via different reasoning paths. Independent convergence from isolated subagents is evidence the finding is real, not stylistic — and only visible because they ran in isolation.

3. **The LENS earning disagreement is the product.** Task 02's monk directly contradicted both baseline and LEAD on the streak-on-boot feature (load-bearing vs refuse-outright). That visible, unsmoothed contradiction is exactly the decision-point friction the skill exists to create.

4. **Isolation matters.** Because LENS never saw LEAD's draft, it attacked the premise rather than anchoring to the lead's framing. Confirms the Phase 2 subagent-topology decision (isolated parallel, not sequential-in-one-context).

5. **Persona-to-task fit was legible.** investigative-journalist as review LEAD produced verification behavior (tips-not-facts) a generic reviewer didn't; farmer surfaced maintenance-root + process-cadence flags no code review would. Selection protocol (contextual shortlist + forced contrast) should preserve this fit.

**Verdict:** premise proven. Proceed with the full revamp (Phases 1–6), not the descoped minimum. Remove `blocked-by-phase-0` labels from the Phase 3 and Phase 6 issues; the strongest performers here (systems-thinker, investigative-journalist, behavioral-psychologist, franciscan-monk, farmer) are the priority set for Phase 3 knowledge-pack backfill.
