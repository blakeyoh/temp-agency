# Pre-Sweet-16 Readiness Gate

> **Status:** Commissioner docket complete; execution freeze remains. No scrimmage, A/B draw,
> panel draw or Sweet 16 game may begin until the applicable execution items are checked and
> the resulting commit is recorded here.

## Completed preparation

- [x] Governing rules, reference sets and commissioner ledger reconciled.
- [x] Sweet 16 / Elite 8 live-evidence protocol documented.
- [x] Sixteen pre-scrimmage evidence contracts drafted.
- [x] Collision Residue ledger created with G9 sourced disagreement, G10 priced defection and
  G12 forced-versus-chosen claims.
- [x] Parallel track reconstructed from Round-of-32 relationships.
- [x] Issue #20 implemented in all 24 profiles, the template, authoring flow and dispatcher.
- [x] Sacrifice Receipt added to the verdict protocol and template.
- [x] Issue #21 disposition recorded: full expansion deferred; panel pack guardrail active.
- [x] Unscored scrimmage record and Sweet 16 verdict template created.
- [x] Tally parser generalized to round-specific panels, yield votes and enactment flags while
  retaining the R32 legacy default.

## Commissioner docket — complete

Rulings 11 and 12 in `commissioner-rulings.md` close this pre-scrimmage docket.

- [x] **Persona Toolbelts:** carry the prompt-in-costume defect into its scrimmage.
- [x] **Make the Problem Strange First:** carry the noun-masking overclaim into its scrimmage.
- [x] **Blind Auditor:** carry the approved but untested forced/chosen fix and remaining
  correct-answer objection into its scrimmage.
- [x] **Adjudicated Ledger:** retain `PROMISE`; the scrimmage may expose the missing runtime
  without fabricating it.
- [x] **Oblique Deck:** carry the overstated corpus claim into its scrimmage; any grounded-only
  deck would still require a recorded amendment, so the scrimmage uses the flagged entrant
  as written and discloses every unavailable operation.
- [x] **Reseed method:** random reseed ordered; the consultant's diagnostic pairings have no
  bracket authority.

## Execution freeze

- [x] Choose and hash one small neutral scrimmage brief shared by all sixteen entrants.
  **Brief:** *"List 10 distinct ways to open a conversation with a stranger at a
  conference."* **SHA-256:**
  `4e57b482fac9a7f2c5aacda93b9f4e77f6816b104ddac056c1edc59821a3785a`.
- [x] Assign an operator and matched base model / context allowance. **Operator:**
  `codex:codex-rescue` (one isolated spawn per entrant). **Model:** `gpt-5.6-luna`,
  `--effort xhigh`, write-capable — identical for all sixteen. Each spawn receives the
  entrant's `roster/<slug>.md`, `knowledge/<slug>/`, its `evidence-contracts-s16.md`
  section, this brief verbatim, and `scrimmage-template.md` as the record format.
- [x] Freeze each evidence contract with its carried flag by commit. **Commit:** `f4288ed`
  (current HEAD of `claude/ai-creativity-randomness-tournament-e609ek`; unchanged since).
- [x] Record the roster and knowledge-pack commit. **Commit:** `f4288ed` (same — `roster/`
  and `knowledge/` are unmodified as of this HEAD).
- [x] Run sixteen unscored scrimmages using `scrimmage-template.md`. **Records:**
  `docs/tournament/scrimmages/s16-<code>.md` for all 16 (E3, M5, E2, A3, E5, E1, A5, A6,
  A1, C8, E4, M1, M3, A2, C5, E6). 14 propose one amendment candidate each; A2 and M5
  propose none.
- [x] Rule on at most one scrimmage-derived amendment per entrant. **Rulings:**
  `commissioner-rulings.md` "Post-scrimmage amendment rulings" (Rulings 13–19). Five
  accepted, promoted to `rules-v2.md` §4 as Amendments 3–7 (1: A1/C8/M1, 2: E1, 3: E2/E3,
  4: A6, 7: E6); two rejected (5: E4, 6: M3).
- [x] **M3 ledger bootstrap (action item, not an amendment — Ruling 18):** built the real
  ledger at `docs/tournament/ledger/m3.jsonl` and ran the commissioner-frozen two-dispatch
  fixture. **Dispatch 1** (empty history, `docs/tournament/ledger/m3-dispatch1-record.md`):
  wrote 4 real canonical claims, all correctly `extension` (nothing to compare against yet).
  **Dispatch 2** (fresh Codex thread, seeded only with the frozen `m3.jsonl` file — not
  dispatch 1's reasoning trace, `docs/tournament/ledger/m3-dispatch2-record.md`): one
  axis-identical restatement candidate correctly **REJECTED** (matched ledger item 1 on all
  four axes under different wording), one axis-changing candidate correctly **ACCEPTED** and
  appended as item 5. The rejection gate fired for real, closing the defect this action item
  existed to fix — this ledger is now live history for M3's actual Sweet 16 game, not a
  bootstrap fiction to be discarded.
- [x] Freeze final entrant definitions and official substitutions by commit. **Amended
  definitions:** `field-of-32.md` — A1, C8, M1 (Amendment 3), E1 (Amendment 4), E2, E3
  (Amendment 5), A6 (Amendment 6), E6 (Amendment 7), each folded into that entrant's own
  `Enhancements` field with its scrimmage-gap citation, not copy-pasted rule text. No
  official substitutions were made — all sixteen Sweet 16 entrants play as originally
  seeded.
- [x] Choose and seal the unseen Tail Test brief. **Amended and resealed by Ruling 20 before
  any official dispatch.** The canonical UTF-8 prompt is `tail-test-s16.txt`; it adds concrete
  stakeholder, resource, privacy, retaliation, and burden-allocation constraints so the test
  measures more than list extension. **SHA-256:**
  `0db8d3ebff02a96c949739a23c3f30f202756fc9b0727a781902e105c4275878`.
  The superseded brief and hash `a98def4e953e1d48c2553a1151922ae6fc689db07209f358d3ca18c1090b790d`
  remain recorded in Ruling 20. The official proposal artifact has a 2,000-token maximum;
  prompt/context and private reasoning do not count against that output ceiling.
- [x] After scrimmage amendments freeze, use an externally generated seed to shuffle the
  ledger's sixteen survivor codes and pair adjacent codes; record seed, algorithm and input
  order in `s16-draw-map.json`. **Seed:** `372500925`, drawn via `secrets.randbits(32)` (OS
  entropy) and applied deterministically via `random.Random(seed).shuffle(...)` — disclosed
  and independently reproducible. **Result:** 8 pairs recorded in `s16-draw-map.json`
  `games`.
- [x] Assign A/B positions using a second recorded seed. **Seed:** `2597142654`; the
  deterministic replay consumes `getrandbits(1)` once per adjacent pair. **Result:** A/B per
  game recorded in `s16-draw-map.json` `games`. The initial lower-case map could not satisfy
  the live tally schema and its stated A/B replay; it was corrected before any official
  dispatch, with pairs unchanged (Ruling 21).
- [x] Draw Builder-anchor and two fresh high-contrast panels; record pack completeness and
  redraw any fresh panel containing two incomplete-pack specialists. **Builder** (pinned,
  `tally.py` `ROUND_ANCHORS`): nuclear-reactor-operator / magician-illusionist, both
  complete-pack. **Advocate** (fresh, lead drawn via seed `3390074417`): civil-rights-activist
  (incomplete pack) / systems-thinker (complete pack) — valid, one complete member.
  **Architect** (fresh, lead drawn via the same seed): behavioral-psychologist (complete
  pack) / franciscan-monk (complete pack) — valid. No redraw needed; neither fresh panel has
  two incomplete-pack members. Lens for each fresh panel was hand-selected for contrast per
  `references/roster.md`'s High-Contrast Lens Pairings table, not drawn — only lead selection
  was randomized. Full disclosure in `s16-draw-map.json`'s `panel_seed_disclosure`.
- [ ] Generate output-only packets separately from mechanism-and-trace packets. Use
  `official-runs/README.md`: first commit all sixteen source records, then render anonymous
  Pass 1 packets and retain the A/B mapping, traces, enactment status, and PROMISE
  counterfactual notes for Pass 2.

## Start authorization

- **Readiness commit:** PENDING
- **Frozen roster / knowledge commit:** `f4288ed`
- **Final draw-map commit:** PENDING
- **Commissioner authorization:** PENDING
- **Authorized at (UTC):** PENDING
