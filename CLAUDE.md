# Temp Agency — Project Context for Claude

This repo contains the **temp-agency** skill: a specialist dispatcher that staffs every
task with at least two domain experts, each bringing a distinct epistemological lens.
The goal is not task execution by a generalist — it’s productive tension between
perspectives that wouldn’t naturally share a room.

-----

## What This Project Is

Temp Agency is a Claude Code skill built around a roster of specialist profiles. Each
profile encodes a professional’s way of *seeing* — their principles, methodology, and
failure modes — not just their domain knowledge. When a task is staffed, a **lead**
specialist drives the work and a **lens** specialist reframes or pressures the output
from a contrasting position. The tension is intentional and should be visible, not
smoothed over.

Key design principle: **encoded preference over capability uplift.** These specialists
don’t teach Claude things it can’t do. They install perspectives it won’t apply by
default. That distinction makes the roster durable across model updates.

-----

## File Structure

```
temp-agency/
│
├── SKILL.md                        # Runtime dispatch logic — lean, no author docs
│
├── CLAUDE.md                       # This file — project context for Claude Code sessions
│
├── roster/                         # Specialist profile files
│   ├── TEMPLATE.md                 # Profile template (copy to create new specialists)
│   ├── anthropologist.md           # ✓ Built
│   ├── behavioral-psychologist.md  # ✓ Built
│   ├── chief-of-staff.md           # ✓ Built
│   ├── civil-rights-activist.md    # ✓ Built
│   ├── contrarian.md               # ✓ Built
│   ├── executive-coach.md          # ✓ Built
│   ├── farmer.md                   # ✓ Built
│   ├── franciscan-monk.md          # ✓ Built
│   ├── investigative-journalist.md # ✓ Built
│   ├── left-fielder.md             # ✓ Built
│   ├── missiologist.md             # ✓ Built
│   ├── pediatric-occupational-therapist.md # ✓ Built
│   ├── systems-thinker.md          # ✓ Built
│   └── [slug].md                   # Add new specialists here
│
├── knowledge/                      # Knowledge packs (required per-specialist as of v2)
│   └── [specialist-slug]/
│       ├── frameworks.md           # Sourced framework summaries + quote snippets with citations
│       ├── canon.md                # Curated sources with notes on contribution
│       └── positions.md            # Positions the persona holds
│
└── references/                     # Author documentation — not loaded at runtime
    ├── roster.md                   # Full annotated specialist index (all tiers)
    ├── author-guide.md             # How to add specialists, manage evals, maintain roster
    └── RESEARCH-PROMPT.md          # Prompt template + scripts for generating new profiles
```

-----

## Key Files

|File                           |Purpose                       |Load when…                            |
|-------------------------------|------------------------------|--------------------------------------|
|`SKILL.md`                     |Runtime dispatch logic        |Always (auto-loaded by skill system)  |
|`roster/[slug].md`             |Specialist profile            |Staffing the task                     |
|`knowledge/[slug]/`            |Personal knowledge sources    |Specialist references it              |
|`references/roster.md`         |Full specialist index         |Browsing for lead or lens candidate   |
|`references/author-guide.md`   |Adding/maintaining specialists|Building or updating the roster       |
|`references/RESEARCH-PROMPT.md`|Generating new profiles       |Creating new specialists              |
|`roster/TEMPLATE.md`           |Profile structure             |Creating a new specialist from scratch|

-----

## Workflow: Staffing a Task

1. Read `SKILL.md` for dispatch logic
1. Browse `roster/` (or `references/roster.md` for full annotated index)
1. Select **lead** (primary domain match) and **lens** (high-contrast perspective)
1. Load both specialist `.md` files
1. Check for `knowledge/[slug]/` files — load if referenced, treat as authoritative
1. Execute as lead; apply lens before delivering; make tension visible

**The contrast rule:** The lens specialist should be chosen for friction, not harmony.
A lens that agrees with the lead adds nothing. When no high-contrast match is obvious,
default to the Contrarian.

-----

## Workflow: Adding a New Specialist

1. Use `references/RESEARCH-PROMPT.md` to generate a profile via Claude + web search
1. Save to `roster/[specialist-slug].md`
1. Add entry to `references/roster.md` (correct tier and cluster)
1. Create the required `knowledge/[specialist-slug]/` pack (frameworks.md, canon.md, positions.md) — the research prompt outputs it alongside the profile
1. Run triggering evals from the profile’s `## Evals` section
1. Use skill-creator’s description optimizer if triggering fails

Personal knowledge files sharpen *perspective* after *methodology* is solid.
Fix the profile before adding a knowledge file.

-----

## Roster Status

**Roster complete: 24/24 built** (down from an unbuilt ~94-entry index — see
`docs/plan-v2.md` for the v2 refocus). The final 11 were built via the
`/roster-add` pipeline (Phase 6, 2026-07-03), each passing a citation/conformance
QA review gate before commit: anthropologist, behavioral-psychologist,
business-development-director, chief-of-staff, civil-rights-activist, contrarian,
executive-coach, farmer, fiction-author, franciscan-monk, gen-z-expert,
investigative-journalist, left-fielder, magician-illusionist,
michelin-star-chef, military-three-star-general, missiologist,
nuclear-reactor-operator, pediatric-occupational-therapist, physics-professor,
soccer-referee, systems-thinker, trauma-informed-practitioner, world-builder.
Grow further with `/roster-add` (demand-driven, one pass, all four artifacts).

The scope narrowed from "staff every task" to **structured disagreement at decision
points** (planning + review). See `docs/plan-v2.md` for the full plan and
`docs/receipts/` for the evidence gate that validated the approach (3/3 real tasks,
the lens materially changed the decision).

-----

## Design Decisions Worth Knowing

**Why at least two specialists?** One perspective produces competent output. Two
perspectives that genuinely conflict produce output with personality and surprise.
The friction is the feature.

**Why “contrast over complement”?** A Copywriter + Content Marketer agree on almost
everything. A Copywriter + Behavioral Psychologist see the same problem differently.
The pairing table in `references/roster.md` makes this concrete.

**Why encoded preference, not capability uplift?** Models improve. Capabilities that
required a skill last year may be native today. But a *perspective* — the way a
missiologist or investigative journalist frames a problem — doesn’t become native.
It has to be installed. That’s a durable investment.

**Why personal knowledge files?** Some domains have significant internal variation.
“Missiologist” covers everything from colonial extraction to Newbigin’s reciprocal
witness. A knowledge file specifies *which* missiologist this is. Same for a Seth
Godin-influenced marketer vs. a Byron Sharp-influenced one. The methodology is general;
the perspective is yours.
