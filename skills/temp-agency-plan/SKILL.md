---
name: temp-agency-plan
description: >-
  Use with /temp-agency-plan to staff a draft plan before it hardens: a LEAD
  reviews domain rigor and a contrasting LENS runs a pre-mortem.
---

# Temp Agency Plan

Staff a **draft plan** before finalization. This skill builds on the shared
dispatcher in `../../SKILL.md`; use that file for roster browsing, lead/lens
selection, isolation, source priority, and synthesis rules. Do not duplicate the
shared roster-selection prose here.

## Input

Accept a plan as a file path, pasted text, or the current plan-mode plan. If the
artifact is ambiguous, ask for the plan text or path before staffing.

## Selection Protocol

Use the shared Staffing Logic in `../../SKILL.md` with this plan-specific shape:

1. Scan `../../roster/` and only select specialists whose `.md` files exist.
2. Propose 2-3 contextual **LEAD** candidates for the plan's domain.
3. Pick one lead.
4. Force the **LENS** from outside that shortlist using
   `../../references/roster.md`'s High-Contrast Lens Pairings table.
5. Support `--with <slug>` as an override for either role; when the user pins one
   specialist, select the other role to preserve contrast.
6. Never pair two same-direction lenses.

## Claude Code Path: Parallel Isolated Subagents

Use this path when subagents are available.

Dispatch two parallel isolated Sonnet-tier subagents:

- **LEAD subagent** gets only:
  - `../../roster/<lead>.md`
  - `../../knowledge/<lead>/` if it exists
  - the draft plan artifact
- **LENS subagent** gets only:
  - `../../roster/<lens>.md`
  - `../../knowledge/<lens>/` if it exists
  - the draft plan artifact

Do not give either subagent the other's draft. Isolation is the point: it keeps
the lens from anchoring to the lead.

### Lead Prompt

Review this draft plan for domain rigor through your profile's methodology.
Identify what is strong, what is under-specified, what will fail under real
conditions, and what must change before the plan hardens.

Return:

- Verdict
- Methodology-based critique
- Highest-leverage changes
- Open questions or missing evidence

### Lens Prompt

Attack this draft plan from your profile's angle. Run a pre-mortem: assume the
plan failed, then explain why. Hunt the ignored variable, hidden stakeholder,
unpriced cost, or premise the lead-friendly reading would miss.

Return:

- Pre-mortem failure story
- Ignored variable
- What the plan should change or explicitly accept
- What you disagree with in the plan's framing

## Inline Fallback Path: No Subagents

Use this path in Codex or plain chat when isolated subagents are not available.

1. Load only the lead profile and any lead knowledge pack. Run the Lead Prompt
   above against the plan. Set the output aside.
2. Load only the lens profile and any lens knowledge pack. Run the Lens Prompt
   above against the same plan with this explicit instruction: **do not affirm
   the lead pass; challenge the plan's premise and search for what a competent
   lead would still miss.**
3. Synthesize the two passes as a diff. Make disagreement visible; do not average
   the outputs into a single consensus plan.

## Synthesis Output

The main thread performs synthesis; do not dispatch a third subagent for it.

Use this shape:

1. **Staffing** — name the lead and lens, plus one sentence explaining the
   contrast.
2. **Lead Read** — the lead's domain-quality verdict.
3. **Lens Attack** — the lens's pre-mortem and ignored variable.
4. **Where the [lead] and [lens] diverge...** — explicit disagreement, including
   any incompatible recommendations.
5. **Plan changes before finalization** — concrete edits or decisions.
6. **Reflection** — `Did the [lens] angle add anything, or was it noise this time?`
