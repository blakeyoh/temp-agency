# Enactment Harness — Plan v3

> **Status:** draft for commissioner authorization. Supersedes v2.
> **Commissioner decision on record:** the non-PROMISE Sweet 16 entrants move from
> `MANUAL PROTOTYPE` to `RUNNABLE`. Ruling 24 formalizes this before Phase 2.
> **Staffed by `/temp-agency-plan`:** LEAD `physics-professor`, LENS
> `magician-illusionist`, dispatched in isolation.
> **v2 → v3:** re-ordered by commissioner priority rather than build tier, which exposed
> a three-way consolidation. Entrant count corrected from 13 to **14** (E5 leaves
> PROMISE). E3 re-priced. A5's deception path removed. See §11.

---

## 1. Problem

The Sweet 16 is drawn, seeded, paneled and frozen. No official game has run. Only E9 is
`RUNNABLE`. `MANUAL PROTOTYPE` means the mechanism has no executable, so a dispatched
subagent must hand-enact it.

Four pieces of in-repo evidence say hand-enactment fails:

1. E1's contracted enforcer `bin/draw` does not exist. There is no `bin/` directory.
2. E1's scrimmage produced a real draw only because its dispatch prompt named the literal
   shell command (`scrimmages/s16-e1.md:67`). Enactment was recorded `PARTIAL`.
3. Nothing carries that directive into the official round. `grep -rli 'enactment
   directive' docs/tournament/` returns nothing.
4. Ruling 23 established that a model asked to be random duplicates strings across
   isolated subagents and recites the alphabet under length pressure.

## 2. Goal

Every non-PROMISE entrant gets a real executable. The dispatch subagent runs the tool and
submits an artifact that **provably derives from** the tool's output.

## 3. What v1 and v2 got wrong

- **v1 secured the middle of the pipe.** It proved the tool ran. It did not prevent the
  agent calling the receipt writer directly, and it did not bind the submitted prose to
  the receipt. A verifiable receipt around a fabricated artifact is worse than no receipt,
  because the fabrication arrives dressed in rigor.
- **v2 ordered the work by build tier.** Easy-first is the wrong sequence. Ordering by
  "can this entrant even function" reaches a legitimate tournament sooner, and it revealed
  that four separate builds are one architecture (§7).

## 4. Guarantees — ranked by what the panel's score depends on

The panel scores the artifact, so binding ranks above cryptography.

| # | Guarantee | Mechanism | Strength |
|---|---|---|---|
| **G1** | **Artifact binding** — the record derives from the tool's output | `artifact_sha256` + per-tool binding rule + `bin/verify --bind` | **Partial and bounded.** Exact for the receipt-determined span. Prose beyond it is declared unverifiable. |
| **G2** | **Receipt authenticity** — the tool really ran | Capability token + deterministic replay | Strong for `replay-exact`. Bounded for `hash-attested`. |
| **G3** | **Tamper evidence** | Hash-chained log + single-use receipt IDs | Strong. |
| **G4** | **Seed provenance** — entropy from the OS, not the model | `secrets` inside the tool | Strong. Ruling 23 applied field-wide. |
| **G5** | **Contract fidelity** — the tool does what the contract claims | **UNSOLVED by automation.** Phase 8 independent read only. | None until Phase 8. |

## 5. Architecture

### 5.1 Receipt writer access control

`lib/receipt.py` is the only receipt writer. Enforcement is a **capability token** — an
unguessable one-time string proving the caller is the tool, not the agent.

- `bin/<toolname>` mints a token immediately before calling the writer.
- The token is single-use and bound to the calling process.
- The writer rejects any call without a live token.

Without this an agent can `import lib.receipt` directly and the hash chain will faithfully
record a fabrication.

### 5.2 Receipt schema

`docs/tournament/receipts/<code>/<n>-<id>.json`:

    entrant, tool, tool_sha256, repo_commit,
    argv, inputs, input_sha256,
    seed { value, source },
    output, output_sha256,
    artifact_sha256, binding_rule,
    verification_class,        # replay-exact | hash-attested
    external_attestation,      # required when hash-attested
    started_utc, completed_utc,
    receipt_id, consumed, chain_prev, chain_hash

`verification_class` replaces a single `deterministic_replay` boolean, which was carrying
two different guarantees — "an independent re-execution byte-matched" versus "some bytes
exist that hash to this value." The second does not prove the code ran. `consumed` makes
receipt IDs single-use, so one honest invocation cannot be cited for every later claim.

### 5.3 External attestation

Every `hash-attested` receipt carries at least one fact the agent cannot generate: a
server-assigned identifier, a response header, or a separate-process invocation record.

### 5.4 `bin/verify` modes

- `--replay <receipt>` — re-run and byte-compare. Pins and validates `repo_commit` first.
- `--chain <code>` — validate one entrant's hash chain.
- `--bind <record> <receipt>` — check the bound span and run the binding rule's negative checks.
- `--all` — everything, plus `consumed` enforcement.

### 5.5 The gate

`build_s16_packets.py` rejects a source record unless all four hold:

1. The cited receipt ID resolves to a real file.
2. Its chain hash validates against its predecessor.
3. `bin/verify --replay` ran since the trace was written, or a valid
   `external_attestation` is present.
4. `bin/verify --bind` passes.

### 5.6 Gate placement — resolved

Mechanism traces release only after Pass 1 seals, so a release-time gate protects the
archive, not the judgment. **The binding check therefore runs before Pass 1 sealing.** It
is a mechanical linter that reveals no entrant identity to any human, so blind judging
survives. Automated verification and blind judging are compatible.

## 6. Priority-ordered field

Commissioner rating, then build.

| Rating | Entrant | Tool | Class | Cost |
|---|---|---|---|---|
| 10 | **A1** Lens Transformers | pre-persona pipeline | replay-exact | shared |
| 9 | **C8** Make the Problem Strange First | pre-persona pipeline + mask map | replay-exact | shared |
| 9 | **A5** The Hostile Environment | pre-persona pipeline + degrade | replay-exact | shared |
| 9 | **A3** Persona Toolbelts | required-skill layer | hash-attested | shared |
| 9 | **C5** Notation Transposition | `bin/notation` | replay-exact | L |
| 9 | **E2** Cross-Repo Foraging | `bin/forage` | hash-attested | L |
| 8 | **E1** The Entropy Well | `bin/draw` | replay-exact | S |
| 7 | **E6** The Oblique Deck | `bin/oblique` + distiller | replay-exact | M |
| 6 | **E4** The Breeding Program | `bin/breed` | replay-exact | M |
| 6 | **M1** The Blind Auditor | required-skill layer + similarity | hash-attested | shared |
| 5 | **E5** The Dated Specialist | date fields + era lexicon | replay-exact | M |
| 5 | **E3** The Wrong Expert on Purpose | `bin/route` | replay-exact | M |
| 4 | **E9** String Seed of Thought | `bin/seed-string` | replay-exact | S |
| 3 | **A6** The Understudy | deferred — see §9 | — | — |
| 2 | **M5** The Binding Map | parked `PROMISE` | — | — |
| 0 | **A2** The Voice Oracle | parked `PROMISE` | — | — |

**14 entrants become runnable. 2 stay parked.** E5 leaves `PROMISE`, so Ruling 24 must
say 14, not 13. M3 remains benched.

## 7. The consolidation

Priority ordering exposed that the top four are not four builds. They are one
architecture: *something happens to the input before the persona sees it, or the persona
is required to invoke something.*

**7.1 Pre-persona context pipeline** — serves A1 (10), C8 (9), A5 (9).

One engine that modifies a payload before the persona's context is assembled, plus one
negative-check runner. Three adapters:

- **A1 transform** — deterministic artifact transforms per persona.
- **C8 mask** — a **frozen mask map**, an explicit noun-to-token dictionary committed
  with the run. Chosen over a model-based noun tagger because a model masker is not
  replayable, which forfeits the property the whole harness rests on.
- **A5 degrade** — see §8.

Scope to the **six personas already pinned to Sweet 16 panels**: nuclear-reactor-operator,
magician-illusionist, civil-rights-activist, systems-thinker, behavioral-psychologist,
franciscan-monk. They are the personas actually in play, so the choice needs no defending
in a ruling.

**7.2 Frozen wordlist checker** — serves C8 (9) and E5 (5).

Both are "committed wordlist plus negative grep." C8 checks that masked nouns never
appear unmasked in the reasoning span. E5 checks that no post-date term appears. One
checker, two lists.

**7.3 Required-skill invocation layer** — serves A3 (9) and M1 (6).

Each persona gets a skill it is required to invoke. This is better than bespoke per-tool
builds for a specific reason: **the harness already logs skill invocations**, which turns
A3's contracted "no tool output, no pass" into something mechanically checkable rather
than asserted. M1's blind response becomes a skill on the same layer.

## 8. Entrant notes where the design changed

### A5 — no deception

The plant-a-false-statement path is **removed**. Tournament records are reused as context
in later rounds, so a planted falsehood could survive downstream and corrupt a ruling
nobody connects back to it. Two mechanisms replace it:

- **Targeted withholding.** Remove one specific load-bearing fact and seal it as the
  ground-truth key. Negative check: the fact must be absent from the output. Random
  n-percent word deletion is rejected — it tests reading comprehension, not
  decision-making, and it breaks the ground-truth key, because you cannot check whether a
  model used a fact you did not deliberately choose.
- **Real source conflict.** Two authentic sources that genuinely disagree. Hostile with
  zero invented content.

*Volume burial* — keep every fact, bury the critical one in genuine but irrelevant
material — is recorded as a third option, not built in v1.

### E2 — two-stage draw, and a better attestation

`mangle.ca` supplied the pattern: ten orthogonal random corpora (webpage, wiki article,
news, book, movie, TV show, and four image sources). The design takes the pattern, not the
dependency — an opaque third-party service whose randomization cannot be attested is the
wrong foundation.

- **Stage 1:** `bin/draw` picks the corpus. Seeded, replay-exact.
- **Stage 2:** that corpus's own random endpoint picks the artifact.

**Wikipedia's `Special:Random` returns a server-assigned revision ID.** That is a
monotonic integer the agent cannot invent and any third party can verify later. It is a
far stronger external attestation than a generic response header, and it partly closes
E2's `hash-attested` weakness.

**Budget the gate, not the fetch.** E2's contract names the enforcer as *"seeded fetch
plus load-bearing review with rejection authority."* Fetching is the easy half. The gate
that rejects a foraged artifact which did not change the output is the mechanism. Without
it E2 forages something real and decorative, which is its own recorded failure mode.

### E6 — distiller, 30-minus-10

`field-of-32.md` lists E6's build gap as *"a distiller turning `knowledge/*/positions.md`
into single-line [imperatives]."* The commissioner's independent proposal matches it:
generate ~30 imperatives per roster, **delete the first 10**, then draw from the
remainder. Deleting the first ten operationalizes the tournament's own thesis — the first
ten are the fence, the dog, and the camera.

**Carried defect:** only **16 of 24** specialists have knowledge packs, so the distiller
covers 16 rosters. Adequate for the Sweet 16. State it rather than discover it later.

**Weak binding, declared.** E6's check is verbatim presence of the drawn imperative. There
is no mechanical test for literal obedience.

### E5 — leaves PROMISE

A displacement-date field with era ranges per roster supplies the metadata half.
`field-of-32.md` lists E5's remaining gaps as *"a dated term lexicon per era band, a
post-generation checker, a leak log"* — which §7.2 already builds. Having a subagent
rewrite a roster concept for its era carries the same honesty problem as everything else,
so **the lexicon checker is what makes it real and is not optional.**

### M1 — numeric threshold

A skill produces the blind unskilled-median response in isolation. The dispatcher then
compares lead and lens against it. The comparison must be a **computed similarity score
against a committed threshold**, not the agent's judgment that answers "look too similar."
Otherwise the agent is judging itself and the receipt means nothing.

### E3 — re-priced upward

Rated 2/10 on the theory that a subagent can pick the polar-opposite specialist from the
prompt. That is Ruling 23's failure one level up: a model asked to select "the opposite"
returns the same few obvious opposites, which is the homogeneity problem the tournament
exists to attack. v2 also over-priced the fix as L — keyword overlap scored across 24
markdown files is stdlib work. **Re-rated 5/10, re-priced M.** Build it.

### E9 — check only

Verify the generator ran and the string appears verbatim. Ruling 23 already recorded the
manipulation-honesty gap as open. Do not reopen it here.

### E4 — crossover only

Structural crossover with a light contract check. Child promotion is a selection-rule
question that only matters if E4 advances, so it is out of scope.

## 9. A6 — a distinctness question, not a build

A6 is deferred, and the commissioner has observed that as written it *"seems like A5 with
more work."* That is not a scheduling note. It is a **§1 three-test absorption question**
— same-thesis, deletion, one-sentence — of exactly the kind Ruling 22 ran on E9 against E1.

The candidate distinction: A5 degrades the **environment**, A6 degrades the **performer**.
Whether that survives the three tests is a commissioner call.

Separately, substituting haiku-tier subagents for A6's contracted *frozen degradation
recipe* (phase-order error, signature-move overuse, load-bearing-principle
misidentification) is degradation-by-capability, not degradation-by-recipe. **That is an
amendment requiring a ruling, not a shortcut.**

**Recommendation: open Ruling 25 on A6 distinctness before building anything for it.** If
it absorbs into A5, the build disappears.

## 10. Phases

| # | Phase | Exit condition |
|---|---|---|
| 0 | **Ruling 24** + harness (capability token, schema, `bin/verify`) + `bin/draw` (E1) + `bin/seed-string` (E9) as reference implementations | Ruling committed. `bin/verify --all` green. |
| 1 | **Adversarial gate test** — an uninstructed subagent tries to pass the gate without invoking any tool | The attempt **fails**. If it succeeds, Phase 0 is not done. |
| 2 | **Pre-persona pipeline** (§7.1) — A1, C8, A5 across 6 personas | All three replay-exact and bind-clean. |
| 3 | **Binding fixture** on E1 or E6 | Prose that gestures at but does not derive from the draw is **rejected**. |
| 4 | **Required-skill layer** (§7.3) — A3, M1 | Skill-invocation log satisfies "no tool output, no pass." |
| 5 | `bin/notation` (C5), `bin/forage` (E2) | C5 slot validator enforces structure. E2 carries a revision-ID attestation and its load-bearing gate. |
| 6 | `bin/oblique` + distiller (E6), `bin/breed` (E4), E5 date fields + lexicon, `bin/route` (E3) | Replay-exact and bind-clean. |
| 7 | **Authenticity fixture** on A3 or M1 | A fabricated transcript is **rejected**. |
| 8 | **Independent contract read** — a fresh agent reads all 14 implementations against their evidence contracts | No tool exceeds or falls short of its contract. Closes G5. |
| 9 | Wire the gate into `build_s16_packets.py`; require receipt IDs in `official-run-template.md` and `official-runs/README.md`; write per-entrant Enactment Directives from each scrimmage's `## Exact input` | Gate rejects a record with no valid receipt. |
| 10 | Start authorization | Readiness commit, draw-map commit, sign-off, UTC timestamp. |

**Phase 1 runs before any entrant tool.** Testing the harness after building 14 tools on
top of it would mean rebuilding 14 tools.

**Two fixtures, not one.** The specialists diverged on where to aim the decisive test.
Phase 3 tests binding where a small tool output feeds a long hand-composed artifact.
Phase 7 tests authenticity where verification is `hash-attested` and weakest. Both were
right about different failure modes.

**Phase 8 is not Phase 7.** A harness fixture tests the harness. It says nothing about
whether `bin/breed` implements E4's contract.

### Fermi estimate

Assumptions: agent-built with review, tests included, no new external services.
S ≈ 1–2 h, M ≈ 3–4 h, L ≈ 6–10 h of focused build-and-review.

| Item | Hours |
|---|---|
| Harness + E1 + E9 (Phase 0) | 8–14 |
| Pre-persona pipeline, 3 adapters, 6 personas (Phase 2) | 12–16 |
| Required-skill layer (Phase 4) | 10–14 |
| C5 + E2 (Phase 5) | 12–20 |
| E6, E4, E5, E3 (Phase 6) | 12–16 |
| Fixtures, contract read, wiring (Phases 1, 3, 7, 8, 9) | 10–15 |
| **Total** | **~64–95** |

The consolidation in §7 saves roughly 10–15 hours against v2's per-entrant build.

## 11. Risks accepted in writing

1. **Agent-composed prose beyond the bound span is unverifiable.** Widest for E1 and E6.
2. **`hash-attested` is weaker than `replay-exact`.** External attestation bounds the gap.
   It does not close it. E2, A3 and M1 sit in this class.
3. **E2 is the riskiest square** — highest commissioner priority sitting on the weakest
   verification class.
4. **G5 stays open until Phase 8.**
5. **Building tools changes entrant standing.** An entrant that really runs will score
   better on Mechanism and Irreducibility than the same entrant hand-waved. Ruling 24 must
   state whether that is intended.
6. **Tool authorship is a security question, not a fairness one.** A merged tool is the
   most durable place to hide a permissive escape hatch, because it reads as
   infrastructure rather than as an entrant's claim. Phase 8 is the only control and is
   not optional.

## 12. Appendix — Ruling 24 skeleton, for commissioner authorship

**Ruling 24 — ENACTMENT HARNESS: 14 ENTRANTS MOVE TO RUNNABLE**

- **Ruling.** The 14 non-PROMISE Sweet 16 entrants move `MANUAL PROTOTYPE` → `RUNNABLE`
  on passing Phases 2–8. M5 and A2 remain `PROMISE`. M3 stays benched.
- **Why this is not a silent unfreeze.** Ruling 22 required a ruling to substitute one
  entrant. Changing the enactment state of 14 is larger and needs the same discipline.
- **Effect on scoring.** State whether a now-running entrant scoring higher on Mechanism
  and Irreducibility is the intended outcome or an artifact to correct for.
- **A5 amendment.** The contracted "plant a false statement" operation is removed on
  downstream-contamination grounds and replaced by targeted withholding and real source
  conflict. This is a definition change and needs recording.
- **E5 leaves PROMISE.** Records the count as 14.
- **Effect on frozen artifacts.** `evidence-contracts-s16.md` enactment states,
  `field-of-32.md` (A5), `official-run-template.md`, `official-runs/README.md`,
  `build_s16_packets.py`.
- **Standing procedure.** Whether this promotes to `rules-v2.md` §4 as Amendment 10.
- **Disclosed asymmetry.** Cheap tools reach `RUNNABLE` weeks before expensive ones.
  **State whether any game may dispatch before all 14 are runnable, or whether the field
  waits.**
