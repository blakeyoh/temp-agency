# Temp-Agency v2 — Revamp Plan

> Approved 2026-07-02. This document is the source of truth for the v2 revamp. Each phase has a corresponding GitHub issue with acceptance criteria; issues link back here. Phase 3 and Phase 6 issues are provisional until Phase 0 (evidence gate) results land.

## Context

temp-agency is a markdown "specialist dispatcher": a skill that staffs tasks with a LEAD expert + contrasting LENS persona from a roster of epistemological-lens profiles. The concept is strong; the execution stalled. As of this plan the repo was dormant since 2026-04-01, had 13 built profiles against ~94 promised in the index, and — critically — **was not an installable skill at all**: `skill.md` uses `## name:` markdown headers instead of `---`-fenced YAML frontmatter, files are lowercase (`skill.md`, `Claude.md`), there is no README, no install path, no manifest. There was also zero evidence the lens pass had ever changed a real output — every profile's Evals section is author-predicted, never executed.

This plan was itself staffed per the project's own method: **systems-thinker (LEAD)** and **contrarian (LENS)** ran as independent subagents against the owner's 10 hypotheses. Their findings shaped the verdicts below; the owner resolved the four open forks directly.

**Goal redefinition (systems-thinker's highest-leverage move):** from *"staff every task with two voices"* to **"install structured disagreement at decision points — planning and review — with a closed loop proving it changed the decision."**

## Hypothesis verdicts

| # | Hypothesis | Verdict |
|---|---|---|
| 1 | Scope to planning + review | **ACCEPT** — both specialists agree; highest-leverage change |
| 2 | Two skills; hook vs slash | **ACCEPT, resolved**: slash commands as portable core + opt-in Claude Code hook at plan finalization |
| 3 | Contextual vs random selection | **REPLACE**: contextual shortlist + forced contrasting pick. Model proposes 2-3 candidate leads; lens must come from outside that shortlist. `--with <name>` user override. No random mode (left-fielder profile already covers serendipity) |
| 4 | Personas as subagents | **ACCEPT with fallback**: parallel isolated subagents on Claude Code (lens cannot see lead's draft); inline degradation on Codex/plain chat |
| 5 | Full-person profiles replace lens extraction | **REJECT/REFINE** — both specialists pushed back. Lens spine is falsifiable ("did the contrarian actually pre-mortem?"); full-person is diffuse improv with no nameable failure mode. Keep lens spine as core, deepen the person layer *under* it (the `knowledge/` architecture already exists). "Parachuted in" behavior comes from dispatch prompt framing, not profile dissolution |
| 6 | Real named people on roster | **REPLACE, resolved**: cited frameworks + archetypal composite personas. Knowledge packs quote/cite real thinkers; persona stays role-named with an explicit **lineage line** ("draws on Godin's permission marketing, Sharp's evidence-based marketing"). Framework names > quality adjectives — they give the subagent retrievable anchors |
| 7 | Revamp RESEARCH-PROMPT.md | **ACCEPT** — downstream of 5/6 |
| 8 | `/roster-add` command | **ACCEPT with guardrails**: one pass must produce profile + knowledge pack + index update + eval stub, or it recreates the 13/94 debt faster |
| 9 | Tier 2 partially obsolete | **ACCEPT, harder**: delete all unbuilt index rows; keep built + a short demand-driven gap list |
| 10 | Trivial public install | **ACCEPT — precondition.** Currently broken, fix first |
| — | Kill the project? | **No — shrink and refocus.** Contrarian's verdict: "shrink hard, don't rebuild-and-expand." Reversal condition adopted as Phase 0 |

## Roster decision (final)

**Keep (16):** systems-thinker, investigative-journalist, behavioral-psychologist, executive-coach, chief-of-staff, contrarian, left-fielder, missiologist, anthropologist, farmer, civil-rights-activist, franciscan-monk, pediatric-occupational-therapist (all 13 built) + business-development-director, trauma-informed-practitioner, world-builder (index entries, not yet built).

**Add (8):** fiction-author, magician-illusionist, military-three-star-general, gen-z-expert, soccer-referee (European football), michelin-star-chef, physics-professor, nuclear-reactor-operator.

**Everything else in `references/roster.md` is removed.** Target roster: 24.

## Phases

### Phase -1 — Spec-driven setup (first)
- Commit this plan to the repo so it is versioned and public.
- Create GitHub issues — one per phase (and per-profile issues for Phase 6 builds) — each with intentionally crafted context: goal, verdict rationale, acceptance criteria, file list, and links to this doc, so future models/subagents can execute without re-deriving context.
- Phase 3 and 6 issues are provisional and carry a `blocked-by-phase-0` label; update them with receipt findings before execution.

### Phase 0 — Evidence gate (before any expansion)
Run 3–5 real plan/review tasks twice each: baseline (no staffing) vs staffed (lead + lens as isolated subagents). Capture side-by-side outputs in `docs/receipts/NN-<task>.md` with a one-line "what the lens caught that baseline missed."

**Task sourcing:** prefer real open GitHub issues from the owner's live projects (mycelium, invisible-ink, manifesto), falling back to project-level `TODOS.md` items — authentic plan/review material with real stakes.

**Gate:** ≥1 documented case where the lens materially changed the decision. If zero after 5 tasks, stop — descope to the contrarian's minimum (packaging fix + 4 best lenses + slash commands, nothing else).

Receipts double as README proof/marketing.

### Phase 1 — Repackage as installable skill (fix what's broken)
- `skill.md` → `SKILL.md` with valid `---`-fenced YAML frontmatter (`name`, `description`); `Claude.md` → `CLAUDE.md`.
- New `README.md`: value prop, receipts excerpt, install one-liners (Claude Code: clone into `~/.claude/skills/` or plugin marketplace entry; Codex: referenced from `AGENTS.md`).
- **Deletions**: prune `references/roster.md` to the 24-profile roster decision (tiers collapsed or simplified accordingly); "Plan mode always requires staffing" rule; "Team staffing (3+ specialists)" section; batch-generation Python scripts in RESEARCH-PROMPT.md (they produced the burst-then-abandon pattern).
- Fix `(built)` tags so they match the filesystem exactly.

### Phase 2 — Two purpose-built skills
- **`temp-agency-plan`** (slash): staffs a plan *before finalization*. LEAD reviews the draft plan for domain rigor via its methodology phases; LENS attacks it (pre-mortem, ignored variables). Orchestrator runs a synthesis diff — disagreements surfaced explicitly, not smoothed.
- **`temp-agency-review`** (slash): same topology against a diff/PR/artifact. Review-specific prompt: LEAD applies domain quality bar; LENS hunts for what the artifact ignores.
- **Selection protocol** (shared): model proposes 2-3 contextual LEAD candidates → picks one → LENS forced from outside that shortlist using the high-contrast pairing table. `--with <name>` overrides.
- **Execution:** Claude Code → two parallel subagents (Sonnet, own context, only their profile + the artifact — no visibility into each other); other harnesses → documented inline fallback in the same skill file.
- **Opt-in hook** (separate install step, documented in README): Claude Code `PreToolUse` hook on `ExitPlanMode` that reminds/offers a staffing pass once at plan finalization. Never unconditional; trivially removable.

### Phase 3 — Profile format v2 + knowledge backfill *(provisional until Phase 0)*
- TEMPLATE.md v2: unchanged lens spine (Role, Principles, Methodology, Voice, Anti-Patterns, Evals) + new required **Lineage** line (named frameworks/thinkers) + required companion `knowledge/<slug>/` pack (sourced framework summaries, quote snippets with citations, positions).
- Revamp `references/RESEARCH-PROMPT.md`: outputs profile *and* knowledge pack; research dimensions expanded to source real frameworks/quotes with URLs; drop batch scripts.
- Backfill knowledge packs for the strongest existing profiles (start with the ones Phase 0 receipts showed working) rather than all 13 at once.

### Phase 4 — `/roster-add`
Slash command: user says "add X to roster" → runs the v2 research prompt (web search) → writes profile + knowledge pack + updates roster index + stubs evals, in one pass. Demand-driven growth replaces batch authorship.

### Phase 5 — Distribution polish
Plugin manifest for Claude Code marketplace-style install; `AGENTS.md` adapter snippet for Codex; receipts featured in README; CHANGELOG started.

### Phase 6 — Complete the roster *(provisional until Phase 0)*
Build the remaining 11 profiles (business-development-director, trauma-informed-practitioner, world-builder + the 8 adds) using the Phase 4 `/roster-add` pipeline — dogfooding it — so every profile ships with lineage line, cited knowledge pack, index entry, and eval stub. One issue per profile; updated with Phase 0 learnings before execution.

## Verification
- Phase -1: issues visible on GitHub with acceptance criteria; plan doc renders in repo; Phase 3/6 issues carry blocked-by label.
- **Phase 0 is itself the core verification** — receipts prove/disprove the premise.
- Phase 1: fresh clone into a clean `~/.claude/skills/` (or plugin install), confirm skill auto-discovers and triggers in a new Claude Code session.
- Phase 2: run `/temp-agency-plan` on a real draft plan and `/temp-agency-review` on a real diff; confirm two subagents spawn, outputs disagree visibly, synthesis diff renders. Repeat inline-fallback path in a Codex session.
- Phase 4: `/roster-add "pricing strategist"` produces valid profile + cited knowledge pack + updated index in one pass.
- Each phase commits separately; repo stays public throughout.
