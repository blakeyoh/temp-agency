---
name: temp-agency-review
description: >-
  Use with /temp-agency-review to staff a diff, PR, branch, file, or artifact:
  a LEAD applies the domain quality bar and a contrasting LENS finds what it ignores.
---

# Temp Agency Review

Staff a **diff, PR, branch, file, or artifact** for review. This skill builds on
the shared dispatcher in `../../SKILL.md`; use that file for roster browsing,
lead/lens selection, isolation, source priority, and synthesis rules. Do not
duplicate the shared roster-selection prose here.

## Input

Accept a diff, PR number, branch name, file path, or pasted artifact. If the
target is ambiguous, ask for the artifact or exact review target before staffing.

## Selection Protocol

Use the shared Staffing Logic in `../../SKILL.md` with this review-specific
shape:

1. Scan `../../roster/` and only select specialists whose `.md` files exist.
2. Propose 2-3 contextual **LEAD** candidates for the artifact's domain.
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
  - the review artifact
- **LENS subagent** gets only:
  - `../../roster/<lens>.md`
  - `../../knowledge/<lens>/` if it exists
  - the review artifact

Do not give either subagent the other's draft. Isolation is the point: it keeps
the lens from anchoring to the lead.

### Lead Prompt

Review this artifact through your profile's domain quality bar. Evaluate whether
it satisfies the real job, not just the stated request. Find concrete risks,
missed requirements, weak evidence, regressions, or implementation gaps.

Return:

- Verdict
- Domain-quality findings
- Required fixes before sign-off
- Questions that block confidence

### Lens Prompt

Attack what this artifact ignores from your profile's angle. Look for excluded
stakeholders, hidden incentives, second-order effects, review criteria that are
too narrow, or the cost of solving the wrong problem well.

Return:

- What the artifact ignores
- Most serious hidden failure mode
- What should be changed, rejected, or explicitly accepted
- What the review target makes harder to see

## Inline Fallback Path: No Subagents

Use this path in Codex or plain chat when isolated subagents are not available.

1. Load only the lead profile and any lead knowledge pack. Run the Lead Prompt
   above against the artifact. Set the output aside.
2. Load only the lens profile and any lens knowledge pack. Run the Lens Prompt
   above against the same artifact with this explicit instruction: **do not
   affirm the lead pass; challenge the artifact's premise and search for what a
   competent domain review would still miss.**
3. Synthesize the two passes as a diff. Make disagreement visible; do not average
   the outputs into a single consensus review.

## Synthesis Output

The main thread performs synthesis; do not dispatch a third subagent for it.

Use this shape:

1. **Staffing** — name the lead and lens, plus one sentence explaining the
   contrast.
2. **Lead Read** — the lead's domain-quality verdict.
3. **Lens Attack** — what the lens says the artifact ignores.
4. **Where the [lead] and [lens] diverge...** — explicit disagreement, including
   any incompatible recommendations.
5. **Review decision** — required fixes, optional improvements, and accepted
   risks.
6. **Reflection** — `Did the [lens] angle add anything, or was it noise this time?`
