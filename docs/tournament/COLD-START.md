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
  3. docs/tournament/commissioner-rulings.md — THE SOURCE OF TRUTH for every decision
  4. docs/tournament/reference-sets.md   — the ruler the panels judge against

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
ROUND OF 32 IS COMPLETE - all 16 games judged by blind panels and ruled. 10 commissioner
rulings, 4 absorptions kept, 6 ideas on the wildcard bench. The next round is the SWEET 16,
8 games, and the bracket has NOT been drawn yet.

Five of the sixteen survivors carry a known defect into the next round - see "Open items
carried into the Sweet 16" in commissioner-rulings.md. Do not seed the bracket without
reading that section.

YOUR NEXT ACTION
Confirm you've read the four documents and tell me the current Sweet 16 field and the
wildcard bench back to me in a short table, so I know the handoff landed. Then ask how I want the Sweet 16 seeded. Do not draw or dispatch until I say so — I watch usage
limits and I want to rule between rounds.

HOW TO RUN A BRACKET (full detail in HANDOFF.md)
Three panels, isolated, in parallel, each reading its two persona profiles plus
knowledge/<slug>/, then reference-sets.md, then its packet:
  Builder    = nuclear-reactor-operator + magician-illusionist   (bias: Mechanism)
  Skeptic    = investigative-journalist + franciscan-monk        (bias: Irreducibility)
  Ecologist  = systems-thinker + farmer                          (bias: Compounding)
Have them RETURN RESULTS INLINE — do not have them write files, that variant failed.
Save each verdict to docs/tournament/verdicts/r32-<bracket>-<panel>.md in the exact
existing format, then run python3 docs/tournament/tally.py. Then STOP and bring me the
bracket.

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

TWO ISSUES ARE FILED AND OPEN - work them independently of the bracket
#20 - every roster profile resolves its own principles into non-conflict; 0 of 24 name an
internal tension. This is plausibly a direct cause of the homogeneity the tournament
exists to fight. Highest-value item in the repo right now.
#21 - the knowledge packs total 22,004 words across all 18. Too small to train a voice,
and 8 of 24 specialists have no pack at all including the contrarian, which SKILL.md
designates the default lens. Phase 1 needs no ML.

FIVE DEFECTS THE PANELS FOUND IN THE FIELD - see HANDOFF.md
Two entrants cite things that do not exist (fake tools in Persona Toolbelts; a fault line
in Stochastic Persona Fracture that is not in the monk's profile). One overstates its
mechanism. The Blind Auditor carries an unresolved objection: it cannot tell "median
because unimaginative" from "median because correct." Do not let these get lost.

TWO OPEN FINDINGS I DO NOT WANT LOST
1. The tournament eliminated its own mechanism. "Bracket as a Primitive" lost 19-7 in
   round one to blind judges. The Skeptic's charge is unresolved: with refusal-by-default
   absorption, 24 of 32 entrants may contribute nothing. The counter is that the
   ORTHOGONAL list is itself a deliverable.
2. Run 1 was badly mis-scored by a single model using absolute 1-10 scores. It put "The
   Wrong Expert on Purpose" dead last at 25/50; three blind panels then ranked it top of
   its bracket on Distance. Do not trust solo absolute scoring.
```

---

## Why the prompt is shaped this way

**It asks for a read-back before any work.** The first action is not "run bracket 3" —
it is "tell me the Sweet 16 and the bench." A wrong read-back is cheap to catch; a
bracket judged from a misremembered state is not.

**It names the failure modes rather than the successes.** A cold agent will infer the
successes from the ledger. It will not infer that background agents die silently on
interrupt, that the file-write variant failed, or that solo absolute scoring produced a
tidy narrative and a wrong answer.

**It withholds permission to dispatch.** The single most expensive mistake available to a
fresh agent here is firing twelve subagents before the commissioner has ruled.
