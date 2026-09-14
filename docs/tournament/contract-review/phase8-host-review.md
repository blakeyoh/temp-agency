# Phase 8 host review — 2026-09-13

Reviewer: the host agent (Claude), stepping in mid-session. GLM was not used because the
OpenRouter key was not exported in the resumed shell. Scope: the uncommitted Phase 8 tree
on top of `2953905` — `lib/verify/packet.py`, `lib/bindings/proposal.py`, the Phase 7
fixes in `lib/bindings/prepare.py`, `draw.py`, `seed_string.py`, the renderer wiring in
`build_s16_packets.py`, `official-runs/README.md`, `official-run-template.md`, and
`enactment-directives-s16.md`. This is a code and document review, not start authorization.

## Verdict

Phase 8 meets its exit condition. The renderer refuses a record with no valid receipt, and
the directives exist for all sixteen slots. Five real (unpatched) admission tests in
`tests/test_packet_admission.py` cover tamper, late dispatch log, missing receipts, the
receipt-free baseline path, and the Entropy Well's missing-counterfactual case. No blocking
defect found. Four items are worth knowing before Phase 9.

## Findings

**R1 — Runtime is environment-fragile (action before start).** The only interpreter with
the pinned libraries, and the only verified Blind Auditor model cache, both live under
`/private/tmp`. A reboot erases them. System `python3` is 3.9 without Pint, and Persona
Toolbelts' `bin/units` fails there with a real failed receipt. Phase 9 step 1 must either
rebuild the venv and cache to a durable path or record the exact temp paths and
`HARNESS_MODEL_CACHE` value in `pre-s16-readiness.md` on the day of start.

**R2 — Dispatch-log path drift (fixed in this review).** The plan §5 G4 row named
`official-runs/dispatch-log.json`. The renderer, `packet.py` and the README all use
`docs/tournament/dispatch-log.json`. The plan wording is corrected to match the code. The
file itself does not exist yet; it is created in Phase 9 step 3 before the first
invocation. `validate_sources` will raise "packet admission" until it exists and is clean.

**R3 — Every official receipt must be cited (strict, intended).** `packet.py:95-97`
requires the set of cited receipt IDs to equal the set of all receipts in the official
directory. Combined with the directive "keep all rejected attempts in the chain," this
means an operator who regenerates an item must cite the rejected receipt too, or the
render fails. That is the correct fail-closed behaviour, but it is easy to trip. The
README already says so; the operator should read it before the first regeneration.

**R4 — `PARTIAL` is narrower than its name.** `packet.py:60-62` requires the full set of
required tools with `status: ok` for both `FAITHFUL` and `PARTIAL`. So `PARTIAL` cannot
mean "one tool failed"; a failed tool forces `NOT ENACTED`. `PARTIAL` is reserved for a
record whose tools all ran but whose prose enactment is incomplete. The template does not
say this. Recommend one sentence in `official-runs/README.md` when Phase 9 opens.

**R5 — README added The Hostile Environment to Amendment 3 (accepted).** Ruling 13 was
sourced from Lens Transformers, Make the Problem Strange First and The Homogeneity Auditor.
The amendment text itself covers any "transformed, masked, or withheld" view, so The
Hostile Environment's withhold adapter was always inside it. The README change is a
clarification, not a new rule. No ruling needed.

## Things checked and found sound

- `proposal.py` reads numbered items only from `## Pass 1 proposal artifact` (legacy
  `Openers` / `Mechanism output` accepted for development records) and returns nothing
  when the heading is duplicated. Execution trace can no longer supply labels. Closes
  Phase 7 F3.
- `prepare.py` `_sections` now seeds an unnamed section and scans text before any
  heading, so preamble and `## Reasoning` / `## Approach` are covered by the negative-word
  scan. The decoded Pass 1 for Make the Problem Strange First is the only exemption.
  Closes Phase 7 F1. Regressions parametrize across both adapters and three headings.
- Renderer requires an explicit `--phase output` or `--phase mechanism` to write, and
  requires the draw map, field and contracts to be clean and committed on every render.
- The Understudy has no `REQUIRED` entry and no `PROMISE` entry, so admission fails closed
  with "resolve deferred entrant first." That is the correct state until the Ruling 25
  build lands.
- The Voice Oracle and The Idea-Space Map are admitted only as `PROMISE ONLY` with
  `Pass 1 provenance: baseline` and an empty Receipts section.
- Full suite: 310 passed on Python 3.13.12 with the pinned libraries and model cache.
