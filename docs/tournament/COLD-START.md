# Cold Start Prompt

Paste the block below into a fresh session to resume the tournament. It bootstraps;
`HANDOFF.md` carries the depth.

---

```
We are resuming a multi-phase project in the temp-agency repo. Work on branch
claude/ai-creativity-randomness-tournament-e609ek — it is current and pushed.

READ FIRST, IN THIS ORDER:
  1. docs/tournament/HANDOFF.md          — state of play, how to run a bracket, what went wrong
  2. docs/tournament/commissioner-rulings.md — SOURCE OF TRUTH for every decision made so far
  3. docs/tournament/rules-v2.md          — absorption standard, scoring, panel design, the draw
  4. docs/tournament/reference-sets.md    — the ruler: five axes, fixed reference points, predicates

Do not re-derive results from the raw verdicts. Read the ledger.

WHAT THIS IS
I believe models are getting harder to steer as they're trained toward consistency —
reliability up, diversity of thought down. This repo staffs tasks with a LEAD and a
contrasting LENS persona; it produces rigor but not strangeness. The tournament is a
structured search for mechanisms that would fix that.

The framing that governs every judgment call: a creative workshop asks for 100 ways to
protect a home. The first ten are a fence, a dog, a camera. The last ten are a moat and a
fleet of UFOs. Reaching idea #99 requires a different generative process than reaching
idea #3. This repo currently stops around #12. Efficiency is explicitly not the goal;
exploration is.

WHERE WE ARE
Round of 32, 8 of 16 games judged. Brackets 1 (Fence) and 2 (Dog) are complete and ruled.
Eight entrants are in the Sweet 16; three are on the wildcard bench. Brackets 3 (Moat,
games 9-12) and 4 (UFO, games 13-16) have anonymized packets written and committed at
docs/tournament/packets/ and have NOT been dispatched.

YOUR IMMEDIATE TASK
Run bracket 3 (Moat, games 9-12), then STOP and bring me the results to rule on.
Do not run bracket 4 in the same turn.

HOW TO RUN IT — the procedure is in HANDOFF.md; the parts that bite:
  - Dispatch THREE panels in parallel, isolated: Builder (nuclear-reactor-operator +
    magician-illusionist, Mechanism bias), Skeptic (investigative-journalist +
    franciscan-monk, Irreducibility bias), Ecologist (systems-thinker + farmer,
    Compounding bias). Each reads its two roster profiles plus knowledge/<slug>/, then
    reference-sets.md, then docs/tournament/packets/r32-moat.md.
  - Have panels RETURN VERDICTS INLINE. Do not have them write files — that variant
    produced nothing last time.
  - Do NOT regenerate the packets. They are blinded (no codes, seeds, regions, or
    authorship marks) and A/B position was flipped from a logged seed. The blinding is
    part of the evidence.
  - Save each verdict to docs/tournament/verdicts/r32-moat-<panel>.md in the exact
    format of the existing files — the parser depends on it. Then run
    python3 docs/tournament/tally.py.
  - Check the filesystem and TaskList before reporting on agent status. Background agents
    have died silently before and elapsed time tells you nothing.

HOW I WANT TO WORK
  - I am the commissioner. The tournament halts after every round and I rule: OVERRULE,
    FORCE/BLOCK ABSORPTION, REVIVE from the bench, RESEED. I enjoy this; it is not an
    interruption of the process, it is the process.
  - Bring me contested games in one screen — rows, contested flagged — so I can ratify
    most and dig into a few.
  - Print every override AS an override, with my reason, never folded into a panel's
    verdict. Visible rigging is honest.
  - Do not resolve genuine panel disagreements on my behalf to keep things moving. Bring
    them to me. If a ruling of mine requires a judgment call you have to make, say so
    explicitly and show your reasoning.
  - Commit and push the reasoning, not just the results. Verdicts, packets, ledger,
    box score. If a session dies, the reasoning must survive it.

TWO OPEN FINDINGS — do not lose these
  1. The tournament eliminated its own mechanism. "Bracket as a Primitive" lost 19-7 in
     round one to blind judges. The Skeptic's charge is unresolved: with refusal-by-default
     absorption, 24 of 32 entrants may contribute nothing. The counter is that the
     ORTHOGONAL list is itself a deliverable. Do not paper over this.
  2. Two panels independently found bin/claims and bin/who-benefits in Persona Toolbelts
     are not tools — "a prompt wearing an executable's name." It advanced with the defect
     noted. Whether entrants may be amended mid-tournament is still an open call of mine.

The box score is published as an Artifact at
https://claude.ai/code/artifact/77543d3d-2a50-40d6-9288-f2bc4f04c4ef
Republish docs/tournament/box-score.html to the same path to update it in place.

Start by reading the four documents, then tell me what you understand the state to be
before you dispatch anything.
```

---

## Why the last line matters

The read-back is a cheap check that the handoff landed. If the incoming agent's summary of
the state is wrong, that is far better discovered before three panels are dispatched than
after.
