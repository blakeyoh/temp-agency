---
name: roster-add
description: >-
  Use with /roster-add to add one Temp Agency v2 specialist in a guarded single
  pass: research the role, write the roster profile, create the knowledge pack,
  update the roster index, and self-verify that no partial profile was created.
---

# Roster Add

Add exactly one Temp Agency specialist from a user request such as
`/roster-add pricing strategist`. This is an authoring pipeline, not a runtime
staffing flow. It implements Phase 4 of `../../docs/plan-v2.md` and GitHub
issue #6.

The output must be complete in one invocation:

1. `roster/<slug>.md` - v2 profile conforming to `../../roster/TEMPLATE.md`
2. `knowledge/<slug>/frameworks.md`
3. `knowledge/<slug>/canon.md`
4. `knowledge/<slug>/positions.md`
5. `../../references/roster.md` updated so the index matches the filesystem

If any artifact cannot be completed, stop and report the blocker. Do not write a
partial profile, partial knowledge pack, or index-only change.

## Input

Accept the specialist title from the slash-command arguments. If the title is
missing or ambiguous, ask for the exact specialist title before doing research.

Normalize the title into a slug:

- lowercase
- ASCII when possible
- words separated by single hyphens
- no leading or trailing hyphen

Examples:

- `pricing strategist` -> `pricing-strategist`
- `Soccer Referee (European football)` -> `soccer-referee`
- `Magician / Illusionist` -> `magician-illusionist`

Before researching, check:

- `../../roster/<slug>.md` does not already exist.
- `../../knowledge/<slug>/` does not already contain unrelated files.
- `../../references/roster.md` does not already mark the slug as built.

If any check fails, stop and report the exact conflict.

## Required Source Files

Read these files before writing:

- `../../docs/plan-v2.md` Phase 4 for the feature contract
- `../../roster/TEMPLATE.md` for the required v2 profile structure
- `../../references/RESEARCH-PROMPT.md` for the research and output contract
- `../../references/roster.md` for the index structure and existing clusters
- `../../CLAUDE.md` for project context

Do not copy the research prompt blindly. Use it as the contract for this single
specialist package.

## One-Pass Guardrail

This command must not create debt. Work in this order:

1. **Research first** with web search enabled.
2. **Draft all artifacts in memory**: profile, three knowledge files, and roster
   index update.
3. **Verify the draft set is complete** against the checklist below.
4. **Write all files and the index update only after the complete set passes.**
5. **Run final self-verification** against the filesystem.

If web search is unavailable, source URLs cannot be verified, the lineage cannot
be grounded in named frameworks, or the correct index update is uncertain, stop
and report. Do not write any artifact.

## Research Requirements

Follow `../../references/RESEARCH-PROMPT.md` v2. Use web search. Prefer primary,
institutional, professional, or canonical sources.

Research must establish:

- 2-4 named lineage frameworks, thinkers, schools, institutions, or canonical
  sources
- 5-10 canon sources with resolvable URLs or precise book citations
- 4-8 short quote snippets only when the wording is verified
- concrete positions the persona holds as a lead or lens
- methodology phases that a senior practitioner would actually use
- failure modes a generalist or junior practitioner would miss
- eval prompts T1-T5 and quality evals Q1-Q3

Do not fabricate quotes. If wording cannot be verified from a resolvable URL or
a book citation with page number, paraphrase the idea and cite the source work
instead. Every quote snippet in `frameworks.md` must include a source. Prefer
paraphrase plus citation over a weak or unverifiable quote.

Keep the persona archetypal. Real people and institutions are cited as lineage
or sources; the specialist must not impersonate a living person.

## Artifact Requirements

### `roster/<slug>.md`

Create a v2 profile that follows `../../roster/TEMPLATE.md`.

Required structure:

- H1 specialist title
- one-line summary blockquote
- `**Lineage**:` line naming actual frameworks and thinkers/sources
- `**Knowledge pack**:` line pointing to `knowledge/<slug>/`
- `## Role Definition`
- `## Core Principles`
- `## Methodology`
- `## Voice & Tone`
- `## Anti-Patterns`
- `## Example Output`
- `## Preferred Sources` — omit only when no profile-specific preferred
  sources exist (rare for a source-heavy `/roster-add` build; prefer including it)
- `## Evals`

The Evals section must be stubbed with:

- Triggering evals T1-T5
- Quality evals Q1-Q3
- concrete, observable good-output and failure signals
- description health-check examples
- `Skill type` set to either `Encoded preference` or `Capability uplift` with a
  one-sentence rationale

### `knowledge/<slug>/frameworks.md`

Create sourced framework summaries. Include:

- the tradition encoded in the pack
- one section per framework or thinker
- core claim
- when to use it
- how not to misuse it
- quote snippet only if verified, otherwise a cited paraphrase

### `knowledge/<slug>/canon.md`

Create a canon table with 5-10 sources:

- title/source name
- verified URL or book citation
- contribution to the persona

Include source notes for limits, cautions, contested claims, or common misuse.

### `knowledge/<slug>/positions.md`

State the persona's commitments as concrete positions:

- what it prioritizes
- what it rejects
- how it resolves common field tensions
- how those positions change Temp Agency planning or review output

### `references/roster.md`

Update the index so it matches the filesystem exactly:

- If `<slug>` is already in `Planned`, move that row to `Built`.
- If `<slug>` is new, add a row to `Built`.
- Remove any duplicate planned row for the same slug.
- Mark status as `✓ Built`.
- Use a concise epistemological lens description, not generic capability copy.
- Update nearby built/planned counts in headings and intro text when present.
- Do not leave a built profile without a built index row.
- Do not leave an index row marked built without a matching profile file.

Do not edit unrelated rows except for count corrections required by the new
state.

## Write Procedure

After research and draft verification:

0. Snapshot for rollback: record the current content of
   `../../references/roster.md` (restorable via
   `git checkout -- references/roster.md` when the working tree was clean),
   and keep a running list of every file and directory this invocation
   creates.
1. Create `../../knowledge/<slug>/` if needed.
2. Write:
   - `../../roster/<slug>.md`
   - `../../knowledge/<slug>/frameworks.md`
   - `../../knowledge/<slug>/canon.md`
   - `../../knowledge/<slug>/positions.md`
3. Update `../../references/roster.md`.

Use the repo's normal markdown style:

- ASCII punctuation
- tables matching existing alignment where practical
- no wrapping code fences around generated file contents
- no fabricated citations or placeholder URLs

## Self-Verification Checklist

Before final response, verify against the actual filesystem:

- [ ] `roster/<slug>.md` exists.
- [ ] `knowledge/<slug>/frameworks.md` exists.
- [ ] `knowledge/<slug>/canon.md` exists.
- [ ] `knowledge/<slug>/positions.md` exists.
- [ ] `references/roster.md` contains exactly one row for `<slug>`.
- [ ] That row is in the `Built` cluster and marked `✓ Built`.
- [ ] There is no remaining `Planned` row for `<slug>`.
- [ ] The profile contains a `**Lineage**:` line.
- [ ] The profile contains a `**Knowledge pack**:` line for `knowledge/<slug>/`.
- [ ] The profile contains `## Evals`.
- [ ] The Evals section includes T1-T5 and Q1-Q3.
- [ ] The profile keeps the template spine: Role Definition, Core Principles,
      Methodology, Voice & Tone, Anti-Patterns, Evals.
- [ ] Source URLs or book citations are present in the knowledge pack.
- [ ] Every direct quote has a verified citation; unverifiable wording is
      paraphrased instead.
- [ ] Built/planned counts in `references/roster.md` match the rows.

If any checklist item fails after writing, fix it before final response. If it
cannot be fixed without new user input or unavailable web access, ROLL BACK
before reporting: restore `references/roster.md` from the snapshot and delete
every file and directory created by this invocation. The repository must be
left with either the complete four-artifact package or no trace of the
attempt — never a partial profile. Then report the failure and what input is
needed to retry.

## Final Response

Print a file-by-file summary:

- `roster/<slug>.md` - what was created
- `knowledge/<slug>/frameworks.md` - source/framework coverage
- `knowledge/<slug>/canon.md` - canon source count
- `knowledge/<slug>/positions.md` - position coverage
- `references/roster.md` - whether a planned row was moved or a new built row
  was added

Also state that the self-verification checklist passed, or list the exact
unchecked item.
