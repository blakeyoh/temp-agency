# Tournament Hub — Design

Commissioner-facing front end for The 99th Idea Bracket. Read `HANDOFF.md` first. This
document assumes it.

**Status:** design approved 2026-09-13. No implementation plan, no code.

---

## 1. Purpose

The commissioner needs four things during a live round:

1. Watch the sixteen official runs progress.
2. Compare two entrants' outputs inside a matchup.
3. Read what each panel said, unmerged.
4. Rule on contested games.

`box-score.html` is a results document for a finished round. This is a live surface for a
round in progress. The two coexist. The hub does not replace the box score.

---

## 2. Decisions

| Decision | Choice |
|---|---|
| Coverage | One hub with phases — run floor, then sealed Pass 1, then mechanism |
| Build | Python generator to a published Artifact, stdlib only |
| Ruling | Composes ruling text in `commissioner-rulings.md` format, never writes to the repo |
| Register | Broadcast chrome, editorial core |
| Tail | Ideas 17–24 at full text, 1–16 collapsed to an onset spine |

**Rejected approaches.** A local server adds a web framework to a repo that is markdown plus
stdlib Python, and cannot be published. A static shell fetching JSON collapses into the same
thing, because the Artifact content security policy blocks fetch and so does `file://`.

---

## 3. Contamination model

Read this section before writing any code.

The tournament's results mean something because the panels are isolated. `HANDOFF.md:407`
requires them to be seed-blind, region-blind, authorship-blind and blind to each other.
`build_s16_packets.py` refuses to write two phases in one call so that a mechanism packet
cannot reach disk before Pass 1 seals.

A hub data file works against all of that. It aggregates, into one greppable file, exactly
what the packet system spends effort separating.

| What the data file would hold | Contract it breaks |
|---|---|
| Entrant codes mapped to names | `HANDOFF.md:180` — packets carry no codes, no region labels, no authorship |
| A/B positions and the flip seed | `HANDOFF.md:407` — seed-blind and region-blind |
| Prior-round results | `verdict-template-s16.md:26` — panel attests it inspected no prior-round verdicts |
| Other panels' verdicts, and the tally | `verdict-template-s16.md:26` — same attestation |
| Every matchup | `official-runs/official-run-template.md:20` — entrant receives no opponent information |

The published artifact is **not** the vector. Panels are isolated subagents that read repo
files, and they will not open a URL. The vector is the generated file sitting in the working
tree where an agent can read it.

`box-score.html` is committed with its data blob inline, but it was built after the Round of
32 finished. The same move during a live round is unsafe.

### Guards

1. **The data file never enters the working tree while the round is live.** `build_hub.py`
   writes to an out-directory outside the repo. Default `~/.cache/temp-agency/hub/`, matching
   where the repo already puts its durable runtime. Pass `--out <session scratchpad>` when
   publishing, because the Artifact tool reads sources only from the working directory or the
   scratchpad. Both locations are outside the tree, which is the property that matters.
2. **The artifact is the only distribution channel during the round.** The hub commits into
   the repo after the Sweet 16 seals, the way `box-score.html` did for the Round of 32.
3. **The phase gate works by omission**, not by hiding. See § 6.
4. **The dispatching agent composes packets from `build_s16_packets.py` only**, never from hub
   data. That agent is the one actor with legitimate access to both, so the rule is written
   down rather than assumed.

Belt and braces: add `docs/tournament/hub/*-data.js` to `.gitignore`, so a generator run that
defaults into the repo still cannot be committed.

**Property worth preserving:** the committed shell carries no evidence. `index.html`, the
stylesheet and the view scripts are inert without a data file. Anyone who reads them in the
tree learns nothing about the field.

### Not adopted

`verdict-template-s16.md:26` lists what a panel attests it did not inspect. The hub is not on
that list and will not be added.

Guard 1 already makes the hub unreachable from inside the repo. Adding a line to the
attestation would tell every panel that a hub exists, which is information they do not
currently have. Guarding by absence beats guarding by instruction.

Changing that attestation is a change to a judging contract. If a future session wants it, it
needs a commissioner ruling, not a quiet edit.

---

## 4. Data model

One generator, `build_hub.py`, beside the existing `build_box_score.py`. Stdlib only, so it
runs on `~/.cache/temp-agency/harness-py313`. Five reads, one write.

| Source | What the hub takes from it |
|---|---|
| `s16-results.json` (written by `tally.py --round s16`) | Axis rows, raw signed sums, `splits`, `contested`, the `yield` block with per-panel Pass 1 evidence, `enactment`, `sacrifice`, `collision`, `absorb`, `decided` |
| `s16-draw-map.json` | The eight games, A/B positions, both seeds and their disclosure, the three panel records, the Ruling 22 substitution |
| `official-runs/s16-<code>.md` | The 24-idea proposal, provenance, dispatch boundary, execution trace, cited receipts |
| `field-of-32.md` and `evidence-contracts-s16.md` | Definition, the "not native" claim, R32 record, amendments, defect flags, evidence state |
| `dispatch-log.json`, `receipts/`, `bin/verify` | Run-floor state — which records are frozen, committed and gated |

**The hub never parses a verdict file.** `tally.py` already computes every disagreement worth
showing, and names each one: `OVERALL`, `AGGREGATE-VS-PANEL`, `YIELD-VS-AGGREGATE`,
`YIELD-VS-PANEL`, `ENACTMENT-SPLIT`, `ENACTMENT-INCOMPLETE`, `ENACTMENT-LIMIT`
(`tally.py:608-625`).

Two consequences:

- The hub cannot disagree with the tally. A game is contested because `tally.py` said so.
- Run-floor state is the only thing the hub derives itself, because no tally exists before
  judging. It reads file presence and the dispatch log, and labels that state as observed
  rather than ruled.

Output is a single `hub-data.js` assigning one global. The shell, stylesheet and view scripts
are authored by hand.

---

## 5. Views

Broadcast chrome carries navigation and status. Editorial typography carries the three
surfaces where judgment happens: the tail, the panel feedback, the desk.

**1. The Bracket** — home. Eight game cards with category color, both entrants, and state:
awaiting output, panels 1–3 in, Pass 1 sealed, tallied. Each card carries its headline flag,
so a contested game announces itself from the home screen.

**2. The Run Floor** — the live view, and the only one usable before judging. Sixteen rows
tracking the pipeline in `HANDOFF.md` step 3: inputs frozen, dispatch entry committed, tool
run, generated, record written, gate passed. Header counter reads "6 of 16 records gated."

**3. The Tail Reader** — the marquee view. Two columns of ideas 17–24 at full text, the band
Pass 1 judges. Ideas 1–16 collapse to a spine carrying only the repetition-onset marker, and
open on demand.

Panel evidence pins to the idea it cites. `STRONGEST` marks its idea, `RETURN PATH` annotates
it, `REPETITION ONSET` draws a rule across the column. Three panels means three annotation
sets, toggled one at a time and never merged, because the isolation is the evidence.

1–16 stays reachable for one reason: onset can land below 17
(`verdict-template-s16.md:39`), and `STRONGEST` may cite any of the 24.

**4. The Split Decision** — per game. Pass 1 yield vote beside the Pass 2 mechanism result.
Five axes at raw signed sums across −9…+9, three panel columns, no averaging. The `splits`
array renders as named badges.

**5. Panel Feedback, unmerged** — per panel: `DECIDED BY`, the five axis predicates, the
absorption disposition, and the **Sacrifice Receipt**. That last one — honored, sacrificed,
accepted cost, validation — appears nowhere in the current box score.

**6. The Entrant Card** — reachable from any entrant code anywhere. Definition, "not native"
claim, R32 result, amendment history, defect flags, evidence state
(`RUNNABLE` / `MANUAL PROTOTYPE` / `PROMISE`), enactment status, receipt count.

**7. The Commissioner's Desk** — contested games queued, each ruleable on one screen. The
split named, both sides' evidence, all three panel positions, the ruling draft composer, and
the Collision Residue candidates. Residue sits here because those third mechanisms need a
decision about whether they reach `parallel-track.md`.

### Matchup switcher

Persistent in the chrome. It changes the subject, not the view — switching from Game 4 to
Game 5 inside the Tail Reader keeps you in the Tail Reader.

- Reads `GAME 4 OF 8 · E1 vs A5` with a caret.
- Opens to all eight with state and flag, so it navigates rather than only selects.
- Arrow keys step between games without opening it.
- Inert on the Bracket and Run Floor, which have no single subject.

---

## 6. Phase gate

`build_hub.py --phase runfloor | output | mechanism`, mirroring `build_s16_packets.py`.

Each phase emits a strict subset of the next. Nothing outside a phase's column is read.

| Data | `runfloor` | `output` | `mechanism` |
|---|---|---|---|
| Field, draw, entrant cards, run-floor state | yes | yes | yes |
| 24-idea proposals and Pass 1 yield evidence | no | yes | yes |
| Axis scores, absorption, sacrifice, collision, tally | no | no | yes |

Views follow the data. At `runfloor` only the Bracket, Run Floor and Entrant Card render. The
Tail Reader joins at `output`. The Split Decision, Panel Feedback and Desk join at
`mechanism`.

**The gate works by omission.** At `--phase output`, mechanism fields are never read and never
emitted. They are absent from the data file, not hidden with CSS. A field that is not in the
bytes cannot leak.

The generator refuses `--phase mechanism` until every panel record carries
`PASS 1 SEALED (UTC)`. It reuses `tally.py`'s existing seal and chronology check
(`tally.py:468`) rather than inventing a second one that could drift.

Failure is closed. An unreadable source, a missing seal or an unknown phase aborts the build
and writes nothing.

---

## 7. Ruling draft composer

On a contested game the commissioner picks a disposition — `RATIFY`, `OVERRULE`, `AMEND` or
`DEFER` — and writes a reason. The hub composes markdown matching
`commissioner-rulings.md:600-623`:

```
### Ruling 26 — Game 4 · E1 v A5 — OVERRULE
**Sourced from:** S16 G4. Tally B by 4 (A 18, B 22). Splits:
YIELD-VS-AGGREGATE. Panels: Builder B, Advocate A, Architect A.
**Ruling:** ...
**Reason:** <commissioner text>
```

Three constraints:

- **It never writes.** The commissioner copies and commits, so the ledger stays
  hand-committed.
- **The ruling number is a suggestion.** The generator reads the highest existing number and
  offers the next, labeled as a suggestion, because rulings can land between builds.
- **An unfinished draft survives a reload** via browser storage, and never leaves the
  commissioner's machine.

Evidence is pre-filled from the tally. The reason stays empty until the commissioner writes
it.

---

## 8. File layout

```
docs/tournament/build_hub.py        # generator, stdlib only
docs/tournament/hub/                # authored, committed, inert without data
  index.html
  hub.css
  chrome.js                         # matchup switcher, phase banner, navigation
  views/bracket.js
  views/runfloor.js
  views/tail.js
  views/split.js
  views/panels.js
  views/entrant.js
  views/desk.js

<out-dir>/hub-data.js               # generated, outside the working tree
```

Files stay under 400 lines each, per the workspace coding standard. Published as a multi-file
Artifact. Scripts load in order and namespace their exports, rather than using ES modules,
because same-origin module resolution inside an Artifact is unverified.

---

## 9. Out of scope

- Replacing `box-score.html`. The Round of 32 record stays where it is.
- Writing to any repo file, including `commissioner-rulings.md`.
- Rounds beyond the Sweet 16. The data model is round-prefixed, so an Elite 8 build follows
  the same pattern with its own prefix, but no Elite 8 work happens here.
- Any change to a judging contract, a template or a dispatch prompt.

---

## 10. Known gaps at design time

- **Views 3 through 7 render as scaffolding until the round runs.** No
  `official-runs/s16-*.md` record exists yet. The Bracket and Run Floor work immediately.
- **`dispatch-log.json` holds `{"entries": []}`.** The Run Floor shows sixteen untouched rows
  on first build. That is correct.
- **`s16-results.json` does not exist yet.** It appears after `tally.py --round s16` runs.

---

## 11. Shipped

- **Plan 1 (run floor)** — `build_hub.py` at `--phase runfloor`, plus the Bracket, Run Floor
  and Entrant Card views. See `hub-plan-1-runfloor.md`.
