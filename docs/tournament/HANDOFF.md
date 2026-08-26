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
judged by three blind panels and ruled by the commissioner: 10 rulings, 4 absorptions kept,
6 ideas on the wildcard bench. The **Sweet 16 bracket has not been drawn.**

*(This section previously read "12 of 16 games judged" and listed two outstanding Moat
rulings. Both were ruled — G11 ratified 2–1, G12 overruled with the entrant amended — and
bracket 4 has since been dispatched, judged and ruled.)*

The Sweet 16 field and the wildcard bench are in `commissioner-rulings.md`. That file is the
source of truth for every decision. Do not re-derive results from the verdicts — read the
ledger.

**Before seeding, read two things.** `commissioner-rulings.md` → "Open items carried into
the Sweet 16": five of the sixteen survivors carry a known defect. And `field-of-32.md` →
"Going into the Sweet 16": each entrant now carries a Status / Enhancements / Gaps trailer,
and the file's front matter holds a result board, a shared-gap table (which survivors are
waiting on the same missing surface), and a list of collisions the draw should be made
deliberately about rather than discover.

---

## How to run the remaining brackets

Everything needed is committed. The procedure is mechanical.

1. **Packets already exist**: `docs/tournament/packets/r32-moat.md` and `r32-ufo.md`.
   They are anonymized — no codes, no seeds, no region labels, no marking of which
   entries are the owner's — and A/B position was flipped on 10 of 16 games from
   **seed 99**, logged in `r32-draw-map.json`. Do not regenerate them; the blinding and
   the flip are part of the evidence.

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

5. **Run the tally**: `cd docs/tournament && python3 tally.py`. It reads
   `verdicts/r32-*-<panel>.md` relative to its own location. **Run it in place** — a copy
   moved elsewhere silently globs the wrong layout and reports a partial tally as if it
   were complete. That happened once and nearly lost a whole bracket's results. It parses verdicts, sums signed per-axis points across panels, flags
   CONTESTED, and writes `r32-results.json`.

6. **Stop.** Present the bracket to the commissioner and take rulings before proceeding.
   The owner explicitly wants to rig matches; that is a feature of this process, not an
   interruption of it.

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
after two brackets. The Skeptic's charge is sharper and remains **unresolved**: with
refusal-by-default absorption, 24 of 32 entrants may contribute nothing. The counter is
that the ORTHOGONAL list is itself a deliverable. Do not paper over this.

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

Four now. Three are authoring defects in entrants — recorded because a future session will
otherwise re-inherit them silently — and one is about the repo itself.

- **Persona Toolbelts** names two things that are not tools (`bin/claims`,
  `bin/who-benefits`). A model judgment dressed as an executable launders a judgment into
  apparent measurement, which is worse than stating it plainly. Four of six are real.
- **Stochastic Persona Fracture** cites a fault line that does not exist: the Skeptic
  checked `roster/franciscan-monk.md` and found no such tension named. The panel escalated
  this to a finding about the **repo** — every roster file resolves its principles into
  mutual non-conflict, which real practitioners do not do. Worth acting on independently
  of the tournament.
- **Make the Problem Strange First** overstates its mechanism: verbs and adjectives carry
  priors too, so stripping nouns does not strip the prior. Advanced 30–2 anyway.
- **The Blind Auditor** carries an unresolved objection the amendment does not fix: its
  gate cannot tell "median because unimaginative" from "median because correct," so it
  systematically punishes right answers for being reachable. Resolve before it advances.

## Two older defects

- **`bin/claims` and `bin/who-benefits`** in Persona Toolbelts are not tools — *"a prompt
  wearing an executable's name."* Found independently by two panels. Persona Toolbelts
  advanced with the defect noted. Whether entrants may be amended mid-tournament is an
  **open commissioner decision**.
- **v1's absorptions were mostly unjustified.** Applied retroactively, roughly a third
  survive the three tests. The v1 box score is kept as a record of the first method, not
  as a result to build on.

---

## File map

| File | What it is |
|---|---|
| `HANDOFF.md` | This file. Read first. |
| `commissioner-rulings.md` | **Source of truth for every decision.** Overrides, tiebreaks, absorptions, the bench. |
| `field-of-32.md` | All 32 entrants with mechanism and "not native" claim — plus, since the
Round of 32, a per-entrant **Status / Enhancements / Gaps** trailer and a result board,
shared-gap table and collision list for seeding the Sweet 16. Annotated *from*
`commissioner-rulings.md`; the ledger still wins any disagreement. |
| `rules-v2.md` | Absorption standard, scoring anchors, panel design, commissioner powers, cross-pollinated draw. |
| `reference-sets.md` | The ruler — five axes, fixed reference points, required predicates. |
| `rules.md` | v1 rules. Superseded; kept for the record. |
| `packets/r32-*.md` | Anonymized judging packets, one per bracket. Moat and UFO are unrun. |
| `verdicts/r32-*.md` | Raw panel verdicts. The reasoning behind every score. |
| `r32-draw-map.json` | The draw, A/B assignment, and the seed (99) that produced the flips. |
| `r32-results.json` | Machine-readable tally output. |
| `tally.py` | Verdict parser and aggregator. |
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
