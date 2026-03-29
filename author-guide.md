# Temp Agency — Author Guide

Reference for adding specialists, managing knowledge files, running evals, and
maintaining the roster over time. Read this when building or updating the system,
not when executing tasks.

-----

## Adding a New Specialist

1. Run the RESEARCH-PROMPT.md generation workflow (see below) to produce a draft profile
1. Save to `roster/[specialist-slug].md`
1. Add the specialist to `references/roster.md` in the appropriate tier and cluster
1. If a personal knowledge source is needed, create `knowledge/[specialist-slug]/`
1. Run triggering evals from the profile’s `## Evals` section to verify firing
1. Use skill-creator’s description optimizer if triggering evals fail

The best profiles come from dedicated research sessions. Personal knowledge files
sharpen *perspective* — build the methodology first, then layer the lens.

-----

## Specialist Profile Structure

Each profile in `roster/` follows the TEMPLATE.md format:

- **Role Definition** — professional identity and what makes the perspective distinct
- **Core Principles** — 3-5 non-negotiable beliefs that act as constraints
- **Methodology** — 3-4 phases; adaptable, not a rigid checklist
- **Preferred Sources** — verified URLs and MCP endpoints
- **Voice & Tone** — register, distinguishing traits, audience awareness
- **Anti-Patterns** — real mistakes, not hypotheticals
- **Example Output** — calibrates quality expectations
- **Evals** — triggering tests, quality benchmarks, description health check

Keep profiles under 1200 words. Sharp briefings, not textbooks.

-----

## Personal Knowledge Sources

Use when a specialist’s domain has significant internal variation and you have a
specific position within it, or when a particular thinker’s framework is foundational
to how you want the specialist to operate.

**When to use:**

- The field has meaningful internal variation and generic knowledge would produce the
  wrong result (e.g., missiology spans colonial extraction to Newbigin’s reciprocal
  witness — which one are you?)
- A specific thinker’s lens is so core that generated output without it feels
  technically correct but *off*

**When not to use:**

- To lock in current views against future refinement — stay open to the specialist
  surprising you
- To compensate for an underdeveloped profile — fix the profile first
- To over-specify everything — most specialists work better with generative latitude

### Knowledge file format

Files live in `knowledge/[specialist-slug]/`:

|Type             |Filename        |Contents                                                                                          |
|-----------------|----------------|--------------------------------------------------------------------------------------------------|
|Thinker profile  |`[name].md`     |Core ideas, key frameworks, distinctive vocabulary, what this thinker would notice or push back on|
|Tradition profile|`[tradition].md`|Theological, philosophical, or methodological commitments                                         |
|Personal canon   |`canon.md`      |Curated sources with notes on what each contributes                                               |
|Worked examples  |`examples.md`   |Annotated samples showing the lens applied to real tasks                                          |

Keep knowledge files under 800 words. They are lenses, not encyclopedias.

-----

## Generating Profiles (RESEARCH-PROMPT Workflow)

Use `RESEARCH-PROMPT.md` to generate new specialist profiles via Claude with web
search enabled. The prompt researches foundations, methodology, authoritative sources,
failure modes, quality signals, voice, and eval design — then outputs a complete
profile including the Evals section.

**Execution options:**

- Claude chat with web search enabled (best for source discovery)
- Anthropic API with `web_search` tool enabled
- Claude Code with web search in allowed tools

**Model choice:**

- Sonnet for batch generation (quality + cost balance)
- Opus for specialists where nuance matters — methodology and anti-patterns sharper

-----

## Evals and Maintenance

Each profile’s `## Evals` section contains:

- **Skill type** — encoded preference (durable; installs a lens) or capability uplift
  (monitors for model obsolescence; run periodically to check if base model now passes)
- **Triggering evals** — 5 rows: 3 positive, 2 negative. Verify with skill-creator
- **Quality evals** — 3 evals each with prompt / good output looks like / failure looks like
- **Description health check** — paste into skill-creator’s description optimizer if
  triggering evals fail

**The “failure looks like” field is the most important.** If you can’t describe what
Claude produces without the specialist, the specialist’s value proposition isn’t clear.

### Maintenance schedule

- **On model update**: Run triggering evals for all Tier 1 specialists; spot-check Tier 2
- **On profile edit**: Re-run the edited specialist’s full eval set before committing
- **Quarterly**: Run skill-creator’s benchmark mode across the full roster
- **Retirement trigger**: A capability-uplift specialist whose quality evals now pass
  *without* the skill loaded can be retired — the model has caught up

### A/B comparison

When iterating on a profile, use skill-creator’s comparator agents for blind A/B
comparison between versions. Judges evaluate without knowing which version is which.
This prevents the trap of editing toward what *sounds* better rather than what
*performs* better.

-----

## Roster Health

**Most temp-agency specialists are encoded preference skills.** They install a lens
the model won’t apply by default. These are durable — models improving doesn’t make
them obsolete, because the *perspective* is the value, not the *capability*.

**Signs a specialist needs work:**

- The “failure looks like” description sounds a lot like the “good output looks like”
- Triggering evals show false positives (fires when it shouldn’t)
- Output feels generically competent but not distinctively *this* perspective

**Signs a specialist can be retired:**

- Capability-uplift skill whose quality evals pass without it loaded
- Domain has shifted enough that the preferred sources are no longer authoritative
- A better specialist has been added that makes this one redundant
