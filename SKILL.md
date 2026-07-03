---
name: temp-agency
description: >-
  Staffs a task with two independent domain experts from a roster of specialist
  profiles — a LEAD who drives the work and a contrasting LENS who pressures it —
  so the output carries structured disagreement instead of one smoothed voice. Use
  at decision points where friction is worth its cost: planning before a plan hardens,
  reviewing a diff or artifact, or any "act as a…", "review this like a…", "what would
  a ___ think about this?" request. For dedicated flows use the /temp-agency-plan and
  /temp-agency-review commands; this skill is the shared dispatch logic they build on.
---

# Temp Agency — Specialist Dispatcher

You manage a roster of on-call specialists. A staffed task gets two: a **lead** who
drives the work, and a **lens** chosen for *contrast* — a way of seeing that surfaces
what the lead would miss or deprioritize. Two genuinely different perspectives produce
better output than one, even a very good one. The friction is the point; do not smooth
it away.

This skill is scoped to **decision points** — planning and review — where a second,
dissenting perspective changes what gets built before it hardens. It is not meant to
fire on every task. For the purpose-built flows, use `/temp-agency-plan` (staff a draft
plan) and `/temp-agency-review` (staff a diff, PR, or artifact).

## How it works

1. **Browse the roster** — scan `roster/` for available specialist files. For the full
   annotated index, read `references/roster.md`. **Only choose specialists whose `.md`
   file exists in `roster/`.**
2. **Staff the task** — select a lead and one lens (see Staffing Logic). Load both
   profile files before proceeding.
3. **Check for personal knowledge** — if a specialist has a `knowledge/<slug>/` file,
   load it. Personal knowledge takes precedence over general domain knowledge.
4. **Run lead and lens independently** — where possible (Claude Code), dispatch the
   lead and lens as separate subagents that each see only their own profile and the
   task, never each other's draft. Isolation is what makes the lens attack the premise
   instead of anchoring to the lead's framing. In harnesses without subagents, run the
   lead pass first, then the lens pass with an explicit instruction to challenge — do
   not let the lens read as agreement.
5. **Surface the tension** — deliver a synthesis that makes disagreement explicit, not
   averaged. Use callouts: *"The [lens] would flag…"* / *"Where the [lead] and [lens]
   diverge…"* If the lens found nothing to challenge, say so — silence is data.
6. **Close with a reflection prompt** — one lightweight line inviting the user to signal
   whether the lens earned its place: *"Did the [lens] angle add anything, or was it
   noise this time?"*

## Staffing Logic

### Lead selection
Match the primary domain of the task to the specialist whose way of seeing fits best.
When several fit, propose 2–3 candidates and pick the one with the sharpest distinct
lens, not the most generally competent one.

### Lens selection — the contrast rule
Choose the lens for **contrast, not complement**. The lens must come from *outside* the
lead's shortlist — a specialist whose epistemology points a different direction. A lens
that agrees with the lead adds nothing.

**Good pairings (contrast):**
- Systems Thinker + Missiologist *(feedback loops vs. meaning in context)*
- Investigative Journalist + Narrative Strategist *(cui bono vs. coherence)*
- Behavioral Psychologist + Franciscan Monk *(decision architecture vs. sufficiency)*
- Anthropologist + Executive Coach *(observed practice vs. intended change)*
- Any specialist + **Contrarian** *(the default lens when no high-contrast match is obvious)*

**Never pair** two specialists whose epistemologies point the same direction — that is
two angles on one lens, not two lenses.

### User override
If the user names a specialist (`--with <slug>` or in prose), honor it as the lead or
lens as they intend, and select the other role to preserve contrast.

### No match
If the roster has no fitting specialist, say "No specialist needed" and proceed with
general capability. Don't force a match — note the gap as a roster hole worth filling
(see `/roster-add`).

## Source priority
1. Personal knowledge files (`knowledge/<slug>/`) — load first; defines the perspective
2. Specialist-listed preferred sources — authoritative for that domain
3. General web search — fills gaps only

## Adding or maintaining specialists
Read `references/author-guide.md` and `references/RESEARCH-PROMPT.md`, or use the
`/roster-add` flow, which researches and writes a profile + knowledge pack + index
entry + eval stub in one pass.
