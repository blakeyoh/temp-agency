# Temp Agency

**Staff your AI's decision points with two experts who disagree.**

Temp Agency is a specialist dispatcher for agentic coding harnesses (Claude Code, Codex).
When you're about to lock in a plan or sign off on a review, it staffs the work with a
**LEAD** — a domain expert who drives — and a **LENS** — a contrasting expert chosen for
friction, who attacks the premise the lead takes for granted. You get structured
disagreement at the moment it's cheapest to act on, instead of one confident, smoothed
answer.

The roster is markdown profiles, each encoding a *way of seeing* — principles,
methodology, failure modes, voice — grounded in a lineage of named frameworks and
thinkers. A systems thinker traces feedback loops; an investigative journalist treats
every claim as a tip to verify; a Franciscan monk asks whether the feature should exist
at all.

## Does it actually help?

Yes — measured, not asserted. Before building anything we ran an evidence gate: three
real tasks from live projects, each done twice (unstaffed baseline vs. staffed LEAD+LENS),
outputs compared side by side. The lens materially changed the decision in **all three**:

- A security fix that would have made cheating *harder to see* rather than harder to do —
  and would have destroyed the game's free social auditing. *(systems-thinker + behavioral-psychologist)*
- A "boot screen" feature request cross-examined down to one boolean and one line of copy,
  because the fix was importing retention mechanics into a contemplative game. *(behavioral-psychologist + franciscan-monk)*
- A review that caught the ticket's acceptance criteria citing a function that **doesn't
  exist**, plus a fix that patched the 4th symptom of a 4-site pattern. *(investigative-journalist + farmer)*

Full write-ups: [`docs/receipts/`](docs/receipts/).

## The two moves

- **`/temp-agency-plan`** — staff a draft plan *before it hardens*. LEAD stress-tests it
  for domain rigor; LENS runs a pre-mortem and hunts the ignored variable.
- **`/temp-agency-review`** — staff a diff, PR, or artifact. LEAD applies the domain
  quality bar; LENS finds what the artifact ignores.

Both select a LEAD by matching the task, then force the LENS from *outside* that shortlist
so the two never point the same direction. Override with `--with <specialist>`.

## Install

**Claude Code (personal skill):**
```bash
git clone https://github.com/blakeyoh/temp-agency ~/.claude/skills/temp-agency
```
Restart Claude Code. The skill auto-discovers; the `/temp-agency-plan` and
`/temp-agency-review` commands become available.

**Codex / other harnesses:** reference this repo's `SKILL.md` from your `AGENTS.md`. The
profiles are plain markdown; only the invocation mechanics differ (see `docs/plan-v2.md`).

## How it's built

```
SKILL.md            Shared dispatch logic (LEAD + LENS selection, isolation, synthesis)
roster/             Specialist profiles — the ways of seeing
knowledge/          Optional per-specialist knowledge packs (cited frameworks, quotes)
references/         Roster index, author guide, research prompt for new profiles
docs/receipts/      Evidence-gate results — baseline vs. staffed, on real tasks
docs/plan-v2.md     The full design and roadmap
```

## Add your own expert

```
/roster-add "pricing strategist"
```
Researches the specialist, writes a profile + cited knowledge pack, updates the index,
and stubs its evals — in one pass. Demand-driven, so the roster only grows when a real
task needs a lens it doesn't have.

## License

Apache 2.0.
