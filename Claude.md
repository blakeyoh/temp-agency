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
├── knowledge/                      # Personal knowledge sources (optional, per-specialist)
│   └── [specialist-slug]/
│       ├── [thinker-name].md       # Thinker profile: core ideas, frameworks, vocabulary
│       ├── [tradition].md          # Theological/philosophical/methodological commitments
│       ├── canon.md                # Curated sources with notes on contribution
│       └── examples.md             # Annotated samples showing the lens applied
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
1. If a personal knowledge source is needed, create `knowledge/[specialist-slug]/`
1. Run triggering evals from the profile’s `## Evals` section
1. Use skill-creator’s description optimizer if triggering fails

Personal knowledge files sharpen *perspective* after *methodology* is solid.
Fix the profile before adding a knowledge file.

-----

## Roster Status

Thirteen specialists are currently built (Tier 1 core lenses + a few domain specialists).
The full target roster is documented in `references/roster.md` across three tiers:

- **Tier 1** — Core lenses (17 specialists): cross-domain worldviews, strong lens
  candidates for almost any task
- **Tier 2** — Domain specialists (57 specialists): deep professional methodology
  in specific domains
- **Tier 3** — Artifact producers (8 specialists): bounded deliverable outputs

Priority build order: Tier 1 first, starting with the high-contrast lens pairings
table in `references/roster.md`.

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
