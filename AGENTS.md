# Temp Agency Adapter for Codex and Other Harnesses

Temp Agency profiles are plain markdown. Claude Code and Codex differ in invocation
mechanics, not in the dispatch model: load the shared dispatcher, choose a LEAD
and contrasting LENS, run their passes, and surface disagreement instead of smoothing
it into one voice.

## Point Codex at this repo

Clone Temp Agency somewhere stable:

```bash
git clone https://github.com/blakeyoh/temp-agency ~/temp-agency
```

Then reference it from the project-level `AGENTS.md` where you want to use it:

```markdown
## Temp Agency

For decision-point staffing, use the Temp Agency repo at `~/temp-agency`.
Read `~/temp-agency/SKILL.md` for shared dispatch logic. For focused flows,
read `~/temp-agency/skills/temp-agency-plan/SKILL.md` or
`~/temp-agency/skills/temp-agency-review/SKILL.md`.
```

Use `/temp-agency-plan` semantics before a plan hardens and `/temp-agency-review`
semantics for a diff, PR, branch, file, or artifact.

## Inline Fallback Flow

When isolated subagents are unavailable, run the flow inline:

1. Read `SKILL.md` for the shared dispatch logic.
2. Browse `roster/` or `references/roster.md`.
3. Pick 2-3 contextual LEAD candidates, choose one, then choose a LENS from
   outside that shortlist using the high-contrast pairing rule.
4. Load `roster/<lead>.md` and any files under `knowledge/<lead>/`.
5. Run the lead pass against the plan or review target.
6. Set that output aside. Load `roster/<lens>.md` and any files under
   `knowledge/<lens>/`.
7. Run the lens pass against the same artifact with an explicit instruction to
   challenge the premise and hunt what a competent lead would still miss.
8. Synthesize as a diff: lead read, lens attack, where they diverge, and concrete
   changes or review decisions. Surface disagreement plainly.

Honor `--with <slug>` as a user override for either role, then choose the other
role to preserve contrast. Only select specialists whose `roster/<slug>.md` file
exists.

## `/roster-add` Equivalent

In Codex, treat "add X to roster" as the `roster-add` skill:

1. Read `skills/roster-add/SKILL.md`.
2. Read `docs/plan-v2.md` Phase 4, `roster/TEMPLATE.md`,
   `references/RESEARCH-PROMPT.md`, `references/roster.md`, and `CLAUDE.md`.
3. Research the requested specialist with web search enabled.
4. Draft the whole package before writing: `roster/<slug>.md`,
   `knowledge/<slug>/frameworks.md`, `knowledge/<slug>/canon.md`,
   `knowledge/<slug>/positions.md`, and the `references/roster.md` update.
5. Write only when the complete set is ready. Do not leave a partial profile,
   partial knowledge pack, or index-only change.
6. Run the self-verification checklist in `skills/roster-add/SKILL.md`.

If source URLs, lineage, or the index update cannot be verified, stop and report
the blocker rather than creating roster debt.
