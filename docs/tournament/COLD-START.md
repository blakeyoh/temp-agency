# Cold-Start Prompt

Paste the block below into a fresh session on this repo. It is the ignition; the detail
lives in `HANDOFF.md`, which it tells the agent to read first.

---

```
We are mid-tournament on the temp-agency repo, branch
claude/ai-creativity-randomness-tournament-e609ek. I am clearing context, so you are
picking this up cold from a previous session. Everything you need is committed.

READ THESE FIRST, IN THIS ORDER, BEFORE DOING ANYTHING:
  1. docs/tournament/HANDOFF.md          — state of play, procedure, what went wrong
  2. docs/tournament/rules-v2.md         — absorption standard, scoring, panels, my powers
  3. docs/tournament/commissioner-rulings.md — the ledger of every result and override
     (rules-v2.md §4 governs what the rules are; this file governs what happened)
  4. docs/tournament/reference-sets.md   — the ruler the panels judge against
  5. docs/tournament/next-round-protocol.md — approved Sweet 16 and Elite 8 procedure
  6. docs/tournament/evidence-contracts-s16.md — what every survivor owes
  7. docs/tournament/collision-residue.md — new ideas produced by collisions
  8. docs/tournament/parallel-track.md   — ORTHOGONAL architecture
  9. docs/tournament/pre-s16-readiness.md — blockers and execution freeze

Do not re-derive results from the raw verdicts. Read the ledger.

WHAT THIS IS
I believe models are getting harder to steer as they're trained toward consistency —
reliability up, diversity of thought down. This repo staffs tasks with a LEAD and a
contrasting LENS persona, and it produces rigor but not strangeness. The tournament is a
structured search for mechanisms that would push it further: 32 mechanisms, cross-
pollinated into four brackets, judged head to head by three independent blind panels,
with me as commissioner ruling between rounds.

The framing that governs every judgment call: a creative workshop asks for 100 ways to
protect a home. The first ten are a fence, a dog, a camera. The last ten are a moat and a
fleet of UFOs. Reaching idea #99 requires a different generative process than reaching
idea #3, and this repo currently stops around #12.

WHERE WE ARE
ROUND OF 32 IS COMPLETE. The Sweet 16's 16 unscored scrimmages, post-scrimmage rulings,
entrant-definition freeze, M3 ledger bootstrap, random reseed, A/B assignment, and panel draw
are complete. Rulings 20 and 21 amended the Tail Test/PROMISE procedure and corrected the
draw-map schema before any official output dispatch. No panel has been dispatched.

Five of the sixteen survivors carry a known defect into the next round - see "Open items
carried into the Sweet 16" in commissioner-rulings.md. Do not seed the bracket without
reading that section.

YOUR NEXT ACTION
Read `official-runs/README.md`, verify the hash of `tail-test-s16.txt`, then create the sixteen
isolated official source records. Run `python3 build_s16_packets.py --write` only after every
record contains exactly 24 numbered rules. Commit the source artifacts and packet pairs before
dispatching a panel. Do not reveal a mechanism-and-trace packet before that panel seals Pass 1.

HOW THE NEXT ROUNDS DIFFER (full detail in next-round-protocol.md)
Every entrant first receives one unscored scrimmage under its frozen evidence contract.
The commissioner rules on any amendment before the official brief is revealed. The Sweet
16 then uses the Tail Test: 24 proposals, with ideas 17-24 as the primary comparison window.
Panels complete an output-only yield vote before they see mechanism names or traces, then
apply the existing five-axis rubric. A mismatch is CONTESTED. Every verdict includes a
Sacrifice Receipt and, after the vote is sealed, a Collision Residue proposal.

Builder is the Sweet 16 calibration anchor. Two fresh high-contrast panels are drawn only
after outputs are sealed. All 24 profiles remain eligible, but each fresh panel must include
at least one specialist with a conforming positions.md. Have panels RETURN RESULTS INLINE.
Never have a background panel write its own file.

HOW I WANT YOU TO WORK
- I am the commissioner and I enjoy it. Bring me contested games with enough context to
  rule in one screen. Do not resolve genuine panel disagreements on my behalf to keep
  things moving.
- Print overrides as overrides, with my reason attached, never folded into a panel's
  verdict. Visible rigging is honest.
- Absorption defaults to REFUSAL. Three tests, all must pass. ORTHOGONAL is a finding,
  not a failure — I do not want Frankenstein ideas, I want the best version of each
  superior concept.
- Never tell me a background agent is "probably still running." Check the filesystem and
  TaskList before reporting agent status. The last session got this wrong.
- Efficiency is not the goal; exploration is. But usage limits are real, so make every
  round a clean stopping point.
- Commit and push the reasoning, not just the results. If a session dies, the reasoning
  must survive.

TWO ISSUES FOUND BY THE ROUND OF 32
#20 - IMPLEMENTED ON THIS BRANCH. roster/TEMPLATE.md and all 24 profiles now carry at
least two unresolved Internal Tensions. The roster-add skill and research prompt require
them for future profiles. Future verdicts operationalize them through a Sacrifice Receipt.
#21 - DEFERRED AS A ROUND BLOCKER. The knowledge packs remain too small to train the Voice
Oracle, and 8 of 24 specialists lack a conforming positions.md. Do not exclude all eight
from judging; use the mixed-pack panel guardrail above. Voice Oracle remains PROMISE and
Oblique Deck remains defect-flagged.

FIVE CARRIED SURVIVOR DEFECTS OR EVIDENCE GAPS - see commissioner-rulings.md and contracts
Persona Toolbelts has two tools that are prompts in costume. Make the Problem Strange
First overstates noun masking. Blind Auditor's forced/chosen fix is approved but untested.
Adjudicated Ledger has no writer, extractor, ledger, or gate. Oblique Deck's corpus claim
is overstated. Ruling 11 authorizes all five to enter their unscored scrimmages with these
flags visible. Ruling 12 orders a random reseed after any scrimmage amendments are frozen.

TWO OPEN FINDINGS I DO NOT WANT LOST
1. The tournament eliminated its own mechanism. "Bracket as a Primitive" lost 19-7 in
   round one to blind judges. The completed record falsified the Skeptic's predicted waste
   quantity: 5 of 32 contributed nothing recorded, not 24. The cost and attention objection
   survives. `parallel-track.md` now makes the ORTHOGONAL list a real deliverable.
2. Run 1 was badly mis-scored by a single model using absolute 1-10 scores. It put "The
   Wrong Expert on Purpose" dead last at 25/50; three blind panels then ranked it top of
   its bracket on Distance. Do not trust solo absolute scoring.
```

---

## Why the prompt is shaped this way

**It asks for a readiness check before any work.** The first action is to verify the
preparation state and unresolved commissioner calls. A wrong read-back is cheap to catch;
a scrimmage run against an unfrozen contract is not.

**It names the failure modes rather than the successes.** A cold agent will infer the
successes from the ledger. It will not infer that background agents die silently on
interrupt, that the file-write variant failed, or that solo absolute scoring produced a
tidy narrative and a wrong answer.

**It withholds permission to dispatch.** The single most expensive mistake available to a
fresh agent here is beginning sixteen scrimmages or firing panels before the commissioner
has frozen the evidence contracts.
