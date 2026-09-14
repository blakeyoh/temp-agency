# Session Handoff — The 99th Idea Bracket

> Written mid-tournament, ~400k context into the session that started it, so a future
> agent can pick this up cold. Read this file first, then `rules-v2.md`, then
> `commissioner-rulings.md`. Everything else is reference.

---

## What this is, in one paragraph

The owner believes models are becoming harder to steer as they are trained toward
consistency — reliability up, diversity of thought down. This repo (temp-agency) staffs
tasks with a LEAD and a contrasting LENS persona, and it demonstrably produces *rigor* but
not *strangeness*. The tournament is a structured search for mechanisms that would push it
further. Thirty-two mechanisms, seeded into four cross-category brackets, judged head to
head by three independent panels, with the owner as commissioner ruling between rounds.

The owner's framing, which should govern every judgment call: a creative workshop asks for
100 ways to protect a home. The first ten are a fence, a dog, a camera. The last ten are a
moat and a fleet of UFOs. **Reaching idea #99 requires a different generative process than
reaching idea #3**, and this repo currently stops around #12.

---

## Current state

**Round of 32 · COMPLETE — 16 of 16 games judged and ruled.** All four brackets have been
judged by three blind panels and ruled by the commissioner: 12 rulings, 4 absorptions kept,
6 ideas on the wildcard bench.

**Sweet 16 preparation · COMPLETE.** All sixteen unscored scrimmages have run and their
post-scrimmage amendments are ruled (Rulings 13–19), the random reseed and A/B assignment
are drawn and recorded in `s16-draw-map.json`, and the three judging panels (one calibration
anchor, two fresh) are drawn. **Not yet done:** no Sweet 16 panel has been dispatched —
`build_s16_packets.py` has not been run to render the official Pass 1 packets, so no output
has been judged. `pre-s16-readiness.md` is the authoritative checklist; read it, not this
paragraph, for exactly which boxes are checked.

*(This section has been corrected twice. It originally read "12 of 16 games judged" with two
outstanding Moat rulings still open — both were ruled (G11 ratified 2–1, G12 overruled with
the entrant amended) and bracket 4 was dispatched, judged and ruled. It then read "No
scrimmage has run, a random reseed has been ordered but not drawn, A/B positions have not
been assigned" well after all of that had actually happened — `pre-s16-readiness.md` and
`COLD-START.md`, committed in the same PR, already showed every one of those steps complete.
A cold agent following the stale block instead of the checklist risks repeating scrimmages
or forking an already-frozen bracket. Trust `pre-s16-readiness.md` over this paragraph if
they ever disagree again.)*

The Sweet 16 field and the wildcard bench are in `commissioner-rulings.md`. That file is the
source of truth for every game result and override — not for what the rules are; that's
`rules-v2.md` (see its §4 Authority boundary). Do not re-derive results from the
verdicts — read the ledger.

**Late-breaking, 2026-09-03: one Sweet 16 slot changed after this section was written.**
`E9` (String Seed of Thought — an externally published mechanism, not owner- or
model-generated) was substituted into Game 8 position A in place of `M3` (The Adjudicated
Ledger, now on the wildcard bench), under **Ruling 22 / rules-v2.md Amendment 8**. E9 ran
its own unscored scrimmage (`scrimmages/s16-e9.md`) and has an evidence contract
(`evidence-contracts-s16.md` § E9, the field's only `RUNNABLE` entry). `s16-draw-map.json`,
`field-of-32.md`, and `tally.py`'s `S16_SURVIVOR_ORDER` are all updated and the tally test
suite passes. **Read Ruling 22 before dispatching Game 8** — the rest of the Sweet 16
(Games 1–7) is unaffected.

**Enactment harness · 2026-09-13 — Phases 0–8 implemented and verified within approved scope.**
There are 13 implemented entrants; A6 remains intentionally deferred, and A2/M5 have
explicit PROMISE baselines. E3 has the small independent frame gate, E4 is crossover
only, and E5 remains the frozen 1911 surface checker without extra concept review.

The full independent Phase 7 read covered the bin/lib snapshot at `2953905`. Its two
binding-scope findings are fixed: prepare scans non-trace reasoning, and E1/E9 item
labels must come from the proposal. Host disposition and original GLM response are in
`contract-review/phase7-host-findings.md` and its companion JSON. GLM cost $0.153531.

Phase 8 gates every packet render on real receipts, required tools, pre-invocation
input/seed commitments, fresh binding, replay and attestation. All sixteen source
scrimmages have an entry in `enactment-directives-s16.md`. A6 admission fails closed.
The official receipts directory still contains only `.gitkeep`; no official output
or judging has begun. Packet phase selection does not attest that a panel sealed Pass 1;
the operator still checks release order.

Verification: 271 tests passed on Python 3.13.12 in 151.70 seconds, including packet
renderer tests, with one upstream Torch warning. Five focused packet tests passed
with an additional E1 missing-counterfactual regression after that full run. All 16
directive sections match the frozen draw, and their source links resolve.

Next: `harness-readiness-docket.md` makes the remaining Ruling 25 (A6 distinctness),
Ruling 24 (standing/runtime), and Phase 9 start record concrete. No ruling has been
silently issued. Recommendation is to retain A6's degraded-performer recipe as distinct
from A5's degraded input, then build only if authorized.

The user welcomes libraries and authorizes external delegation throughout this session.
GLM has returned useful work; the newest draft attempt stopped before network access
because the resumed shell lacks exported `OPENROUTER_API_KEY`. The skill and wrapper
were re-read after the user's update notice and still require that environment variable.
Luna's recent documentation follow-up hit quota; the host completed the documentation.
Do not retry either blindly or change the frozen official model without a ruling.

**Session change of hands · 2026-09-13 — Rulings 24 and 25 made; Phase 8 host-reviewed; Phase 9 not started.**
A new agent took over mid-session with all Phase 8 work uncommitted on top of `2953905`.
What happened, in order, so the next agent can pick up cold:

1. The commissioner ruled on `harness-readiness-docket.md`. **Ruling 25:** The Understudy
   stays distinct from The Hostile Environment; a bounded recipe build is authorized under
   four conditions (frozen recipe, both responses preserved, no silent repair by synthesis,
   no weaker-model substitute). **Ruling 24:** thirteen entrants are `RUNNABLE`, The
   Understudy joins on evidence, Luna/xhigh stays the official generator, the field waits
   for capability. Both are in `commissioner-rulings.md`.
2. Phase 8 was reviewed by the host (Claude), not GLM, because the OpenRouter key was not
   exported. Findings are in `contract-review/phase8-host-review.md`.
3. Two isolated agents ran the capability checks. Results are in Ruling 24's capability
   record. Short form: interpreter, Wikipedia and the Blind Auditor model all PASS, but
   the venv and model cache live under `/private/tmp` and vanish on reboot. Run the suite
   with `HARNESS_MODEL_CACHE=/private/tmp/s16-model-cache /private/tmp/s16-harness-py313/bin/python -m pytest tests docs/tournament -q`
   (310 pass). System `python3` is 3.9 without Pint and fails five toolbelt tests.
4. Nothing official has been generated. `receipts/` still holds only `.gitkeep`.

**Later the same day:** (a) landed as `afc819f`. (b) The Understudy is built:
`bin/understudy` emits a seeded, replay-exact degradation card (phase permutation that
is never identity or Phase-1-first, one overused technique, one false principle);
`lib/bindings/understudy.py` binds nine checks including "Pass 1 still runs the card's
phase order beside a canonically ordered expert response"; `REQUIRED['A6']` is set;
directive § A6 rewritten; committed recipe at `understudy/behavioral-psychologist.json`.
The runtime is now durable at `~/.cache/temp-agency/harness-py313` and the default
model cache `~/.cache/temp-agency/models` needs no env var. Full suite: 322 passed,
0 skipped. The implemented count is 14.

**Next, in order:** (c) re-confirm Luna reachability on the day of start;
(d) then Phase 9 per the docket. Do not dispatch any game before (c).

**Before any scrimmage, read five more things after the governing four:**

1. `next-round-protocol.md` — approved preparation order and the Sweet 16/Elite 8 design.
2. `evidence-contracts-s16.md` — the evidence each survivor owes before competition.
3. `collision-residue.md` — the three R32 discoveries and the future entry standard.
4. `parallel-track.md` — the ORTHOGONAL architecture promised by the rules.
5. `pre-s16-readiness.md` — the blocking commissioner docket and execution freeze.

Five survivors carry a defect or missing evidence condition. Ruling 11 authorizes all five
to enter the unscored scrimmages with the flag visible; the scrimmages may supply evidence
for one later amendment per entrant.

---

## Round-of-32 record (historical — all 16 games complete)

**Nothing below is a pending task or a reusable command sequence.** All four brackets — Fence,
Dog, Moat, UFO — have been judged and ruled; do not re-dispatch them or run their tally.
The paths below preserve the R32 evidence only.

1. **Packets already exist** for the Round of 32: `docs/tournament/packets/r32-moat.md` and
   `r32-ufo.md`, both already judged, kept as reference for the packet format. They are
   anonymized — no codes, no seeds, no region labels, no marking of which entries are the
   owner's — and A/B position was flipped on 10 of 16 games from **seed 99**, logged in
   `r32-draw-map.json`. Do not regenerate them; the blinding and the flip are part of the
   evidence.

2. **Dispatch three panels per bracket**, isolated, in parallel. Each reads its two
   persona profiles plus `knowledge/<slug>/`, then `reference-sets.md`, then its packet.
   The exact prompt shape that worked is preserved in the verdict files' structure; the
   panels are:

   | Panel | Lead | Lens | Disclosed bias |
   |---|---|---|---|
   | Builder | nuclear-reactor-operator | magician-illusionist | Mechanism |
   | Skeptic | investigative-journalist | franciscan-monk | Irreducibility |
   | Ecologist | systems-thinker | farmer | Compounding |

3. **Have them return results inline, not write to a file.** See "What went wrong" below.

4. **Save each verdict** to `docs/tournament/verdicts/r32-<bracket>-<panel>.md`, matching
   the existing format exactly — the parser depends on it.

5. **Tally record**: R32 was tallied with `cd docs/tournament && python3 tally.py --round r32`.
   It reads `verdicts/r32-*-<panel>.md` relative to its own location. **Run it in place** — a copy
   moved elsewhere silently globs the wrong layout and reports a partial tally as if it
   were complete. That happened once and nearly lost a whole bracket's results. It parses verdicts, sums signed per-axis points across panels, flags
   CONTESTED, and writes `r32-results.json`. This command is for reproducing the R32 record;
   it must never be used for the Sweet 16.

6. **Historical stop point.** The bracket was presented to the commissioner for rulings.
   The owner explicitly wants to rig matches; that is a feature of this process, not an
   interruption of it.

## Sweet 16 setup — amended after the Round of 32

The Round-of-32 packet flow is historical evidence, not the full Sweet 16 procedure. Follow
`next-round-protocol.md`. Preparation precedes every scrimmage: documentation, collision and
parallel ledgers, sixteen evidence contracts, explicit defect rulings, issue #20, then a
frozen roster/knowledge commit. The defect rulings are complete: all five flags carry into
the scrimmages.

Issue #20 is implemented on this branch: `roster/TEMPLATE.md` and all 24 profiles now name at
least two unresolved internal tensions, and the authoring flow requires them for future
profiles. Issue #21 is deferred as a blocker under the guardrail in `next-round-protocol.md`;
all 24 profiles remain judge-eligible, but every fresh panel must include at least one
specialist with a conforming `positions.md`.

Each entrant then runs one **unscored scrimmage**. The commissioner rules on any amendment and
freezes the contracts before the official brief is revealed. The Sweet 16 uses a Tail Test
and two sealed judging passes: output-only yield first, existing five-axis mechanism scoring
second. A mismatch is CONTESTED.

Create round-specific artifacts without touching R32 evidence: `s16-draw-map.json`, sixteen
`official-runs/s16-<code>.md` source records, paired
`packets/s16-<game>-output.md` / `packets/s16-<game>-mechanism-trace.md` files, and
`verdicts/s16-<bracket>-<file_tag>.md`. The output packets stay anonymous until Pass 1 seals;
the mechanism-and-trace packet releases only afterward. The draw map contains the three panel
records described in `next-round-protocol.md`; `tally.py` uses their names and file tags, so
the two fresh panels do not masquerade as the retired Skeptic and Ecologist.
Once all three panels have returned their verdicts, run:

```bash
cd docs/tournament && python3 tally.py --round s16
```

The round argument determines every input and output path: it reads only `s16-draw-map.json`
and `verdicts/s16-*-<panel>.md`, then writes only `s16-results.json`. Any later round follows
the same pattern with its own prefix.

---

## Scoring, in brief

Read `reference-sets.md` for the full ruler. The shape:

- **Comparative only.** No standalone scores. Per axis: A/B significantly better (3),
  slightly better (1), or Tie (0). Panels vote per axis; raw signed sums aggregate across
  the three panels, so each axis ranges −9…+9 and a game ranges −45…+45.
- **Five axes**: Distance, Mechanism, **Irreducibility** (load-bearing), Compounding,
  Generative failure.
- **Every verdict carries a falsifiable predicate** or it does not count. The
  irreducibility predicate — *"a base model given only the prompt `___` reproduces about
  ___% of this"* — is runnable, and it is what makes the reasoning trail auditable.

**Absorption defaults to refusal.** Three tests, all must pass: same-thesis, deletion
(does the winner get *worse* or merely *smaller*?), one-sentence (no "and also"). Three
dispositions: ABSORBED / **ORTHOGONAL** / SUBSUMED. Orthogonal is a finding, not a
failure — it names two mechanisms as independent axes that should both exist and never
merge.

---

## What went wrong, so you don't repeat it

**Background agents died silently on interrupt.** Four panels dispatched across two turns
were killed when the owner interrupted a turn. They produced no output and no error; their
transcripts froze at 122 bytes. `TaskList` returned empty. I told the owner they were
"probably still deliberating" based on bracket 1's timing — that was wrong, and they had to
push back before I actually checked. **Check the filesystem and `TaskList` before reporting
agent status; never infer liveness from elapsed time.**

**Inline return beat file-write.** Bracket 1's panels returned verdicts inline and all
three succeeded. Bracket 2's first attempt was told to `Write` to a file and produced
nothing. The interrupt is the more likely cause, but the retry used inline return and
worked. Keep the proven path.

**Tally aggregation was wrong the first time.** The original version re-compressed each
axis's cross-panel sum back into 1 or 3 points, discarding magnitude and producing
misleading margins. It now uses raw signed sums. If you change the aggregation, re-run the
existing brackets so results stay comparable.

---

## What the tournament found out about itself

Two findings that a future session should not lose:

**1. The tournament eliminated itself.** "Bracket as a Primitive" — the mechanism running
this whole exercise — lost 19–7 in round one, unanimously, to judges blind to what they
were judging. The Ecologist predicted the exact failure mode this session then hit:
*"judge attention does not scale into year three."* The session paused for usage limits
after two brackets. The Skeptic predicted that 24 of 32 entrants might contribute nothing.
The completed record falsified that quantity: **5 of 32 contributed nothing recorded**.
The cost and attention objection remains valid. `parallel-track.md` now instantiates the
ORTHOGONAL deliverable instead of leaving it as a counter-argument in prose.

**2. The v1 run was badly mis-scored, and the v2 method caught it.** The first pass
(archived, see below) was judged by me alone with absolute 1–10 scores and mandatory
absorption. It scored "The Wrong Expert on Purpose" **25/50 — dead last in the field of
32**. Three blind panels then ranked it top of its bracket on Distance, unanimously. They
agreed with my *fact* (the left-fielder profile already does something similar) and
rejected my *conclusion*. Similarly, the Anti-Roster was a v1 regional finalist at 43
points and went out in round one here.

**Corollary worth internalizing:** absolute self-scoring by a single model produced
compressed, unfalsifiable numbers (everything landed 25–47 of 50) and a tidy narrative.
Comparative scoring against fixed reference points, by independent blind judges, produced
ties, routs, and reversals. The second is more useful and less flattering.

---

## Defects on the record

The Round of 32 found three entrant authoring defects and one repo-wide defect. The repo-wide
defect has been repaired before the Sweet 16; the historical finding remains part of the
evidence.

- **Persona Toolbelts** names two things that are not tools (`bin/claims`,
  `bin/who-benefits`). A model judgment dressed as an executable launders a judgment into
  apparent measurement, which is worse than stating it plainly. Four of six are real.
- **Stochastic Persona Fracture** cited a fault line that did not exist during R32: the Skeptic
  checked `roster/franciscan-monk.md` and found no such tension named. The panel escalated
  this to a finding about the **repo** — every roster file resolves its principles into
  mutual non-conflict, which real practitioners do not do. **Resolved before S16:** the
  template and all 24 profiles now carry unresolved internal tensions. The R32 result remains
  unchanged.
- **Make the Problem Strange First** overstates its mechanism: verbs and adjectives carry
  priors too, so stripping nouns does not strip the prior. Advanced 30–2 anyway.
- **The Blind Auditor** carries an unresolved objection the amendment does not fix: its
  gate cannot tell "median because unimaginative" from "median because correct," so it
  systematically punishes right answers for being reachable. Ruling 11 carries the objection
  into the scrimmage for observation.

## Two older defects

- **`bin/claims` and `bin/who-benefits`** in Persona Toolbelts are not tools — *"a prompt
  wearing an executable's name."* Found independently by two panels. Persona Toolbelts
  advanced with the defect noted. Ruling 11 carries it into the scrimmage unchanged; one
  evidence-based amendment may be ruled afterward.
- **v1's absorptions were mostly unjustified.** Applied retroactively, roughly a third
  survive the three tests. The v1 box score is kept as a record of the first method, not
  as a result to build on.

---

## File map

| File | What it is |
|---|---|
| `HANDOFF.md` | This file. Read first. |
| `commissioner-rulings.md` | **Source of truth for every result.** Overrides, tiebreaks, absorptions, the bench — not the rules themselves (that's `rules-v2.md`, see its §4 Authority boundary). |
| `field-of-32.md` | All 32 entrants with mechanism and "not native" claim — plus, since the Round of 32, a per-entrant **Status / Enhancements / Gaps** trailer and a result board, shared-gap table and collision list for seeding the Sweet 16. Annotated *from* `commissioner-rulings.md`; the ledger still wins any disagreement. |
| `next-round-protocol.md` | Approved preparation order plus Sweet 16 Tail Test, panel rotation, Sacrifice Receipt and Elite 8 Return Test. |
| `evidence-contracts-s16.md` | Pre-scrimmage evidence owed by all sixteen survivors; includes RUNNABLE / MANUAL PROTOTYPE / PROMISE state. |
| `collision-residue.md` | Independent third mechanisms produced by collisions; seeded with G9, G10 and G12 discoveries. |
| `parallel-track.md` | Durable ORTHOGONAL relationships and future Elite 8 coalitions. |
| `pre-s16-readiness.md` | Preflight gate: completed preparation, commissioner decisions and the final packet execution item. |
| `tail-test-s16.txt` | Canonical, hashed Sweet 16 Tail Test prompt, amended by Ruling 20 before official dispatch. |
| `official-runs/README.md` | Official-output conditions, PROMISE treatment, source-record format, and packet release order. |
| `enactment-harness-plan.md` | **Plan v4 for the enactment harness.** §4 trust boundary, §6 architecture, §11 phases and both Phase 1 results, §13 Ruling 24 skeleton. |
| `harness-fixtures/` | Phase 1 fixture records (`e1-honest`, `e9-honest`, `e1-tamper`, `e1-forger`, `e1-forger2`), the fixture dispatch log, the E1 pools file, and `receipts/` holding every fixture receipt. Gate them with `HARNESS_RECEIPTS_DIR=docs/tournament/harness-fixtures/receipts python3 bin/verify all --records 'docs/tournament/harness-fixtures/*.md' --dispatch-log docs/tournament/harness-fixtures/dispatch-log.json`. |
| `receipts/` | Live receipts directory for the official round. **Empty by design until dispatch.** |
| `../../bin/`, `../../lib/`, `../../tests/` | The harness itself. `lib/README.md` is the API. |
| `build_s16_packets.py` | Validates the 16 source records and renders the eight isolated output/mechanism packet pairs. `--write` requires `--phase output` or `--phase mechanism` — it refuses to write both phases in one call, so a mechanism packet can never reach disk before every panel has sealed Pass 1. |
| `amendment-candidates-s16.md` | 7 amendment candidates from the 16 scrimmages, pending commissioner ruling; rule here, then log to `commissioner-rulings.md` and promote accepted text into `rules-v2.md` §4. |
| `scrimmages/s16-<code>.md` | 16 completed unscored scrimmage records, one per surviving entrant. |
| `scrimmage-template.md` | Per-entrant unscored enactment record, including substitutions and amendment docket. |
| `verdict-template-s16.md` | Parser-compatible two-pass panel record with Sacrifice Receipt and Collision Residue. |
| `rules-v2.md` | Absorption standard, scoring anchors, panel design, commissioner powers, cross-pollinated draw. |
| `reference-sets.md` | The ruler — five axes, fixed reference points, required predicates. |
| `rules.md` | v1 rules. Superseded; kept for the record. |
| `packets/r32-*.md` | Anonymized judging packets, one per bracket. All four (Fence, Dog, Moat, UFO) have been judged. |
| `verdicts/r32-*.md` | Raw panel verdicts. The reasoning behind every score. |
| `r32-draw-map.json` | The draw, A/B assignment, and the seed (99) that produced the flips. |
| `r32-results.json` | Machine-readable tally output. |
| `tally.py` | Verdict parser and aggregator. |
| `test_tally.py` | Regression coverage for live evidence, draw integrity, panel configuration and R32 compatibility. |
| `box-score.html` | Rendered box score, published as an Artifact. Favicon 🛸 — keep it stable across redeploys. |
| `build_box_score.py` | Regenerates the box score's DATA blob from `r32-results.json`. |

---

## Working notes for whoever picks this up

**The owner is the commissioner and enjoys the role.** Bring them contested games with
enough context to rule in one screen — sixteen rows, contested flagged, dig into three.
Do not resolve genuine disagreements on their behalf to keep things moving.

**Print overrides as overrides.** Every commissioner decision is recorded with its reason,
never folded into a panel's verdict. Visible rigging is honest.

**The owner pushes back well and is usually right.** Three of five reactions to the v1 run
identified the same flaw — I had optimized for a tidy narrative over an honest result.
When they say something feels subjective or over-merged, it probably is.

**Efficiency is explicitly not the goal; exploration is.** But usage limits are real, and
they will pause. Design each round to be a clean stopping point.

**Do not let the panels see prior results.** Seed-blind, region-blind, authorship-blind,
and blind to each other. Isolation is why the convergences mean anything — when Builder
and Ecologist independently produced near-identical merged sentences for the Binding Map
without seeing each other, that was evidence, not agreement.

**Do not begin with a scrimmage in a cold session.** First verify that documentation and
contracts are committed, issue #20 is present in all 24 profiles, Ruling 11's carried flags
are present in the five contracts, and the roster/knowledge commit is frozen. The next action
after this preparation pass is a readiness review, then the unscored scrimmages. Ruling 12
requires the random bracket draw to wait until any scrimmage amendments are frozen.
