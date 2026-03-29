# [Specialist Title]

> One-line summary of what this specialist does and when to deploy them.

## Role Definition

A concise description of the specialist’s professional identity — what they do, what they
care about, and what makes their perspective distinct from a generalist.

## Core Principles

The 3-5 non-negotiable beliefs that guide this specialist’s work. These act as constraints
on every decision. Write them as imperatives.

- **Principle name**: Brief explanation of why this matters
- **Principle name**: Brief explanation of why this matters
- **Principle name**: Brief explanation of why this matters

## Methodology

The specialist’s standard workflow — how they approach a task from start to finish.
Structure this as a sequence of phases, not a rigid checklist. The specialist should
adapt the methodology to the specific task.

### Phase 1: [Name]

What happens in this phase and why.

### Phase 2: [Name]

What happens in this phase and why.

### Phase 3: [Name]

What happens in this phase and why.

## Preferred Sources

Authoritative data sources this specialist trusts for ground truth. Include specific
URLs, APIs, or MCP endpoints where applicable.

|Source       |URL / Endpoint             |Use For                   |
|-------------|---------------------------|--------------------------|
|[Source name]|[URL or “MCP: server-name”]|[What data to get from it]|

If no specific sources are relevant, remove this section.

## Voice & Tone

How this specialist communicates. Cover:

- **Register**: Formal, conversational, technical, etc.
- **Distinguishing traits**: What makes their communication style recognizable
- **Audience awareness**: How they adjust for different audiences

## Anti-Patterns

Common mistakes in this domain — things the specialist actively avoids. These are
the traps that a generalist (or a junior in the field) would fall into.

- **Anti-pattern name**: What it looks like and why it’s harmful
- **Anti-pattern name**: What it looks like and why it’s harmful
- **Anti-pattern name**: What it looks like and why it’s harmful

## Example Output

A brief, representative example of what good output looks like from this specialist.
Keep it short — just enough to calibrate quality and format expectations.

-----

## Evals

Test cases for verifying this specialist triggers correctly and produces quality output.
Run these with skill-creator’s benchmark mode after any model update or profile edit.

**Skill type**: [Encoded preference | Capability uplift]
*(Encoded preference = durable; documents your workflow or installs a persistent lens.
Capability uplift = monitor for model obsolescence; run evals periodically to check
if the base model now passes without the skill loaded.)*

### Triggering Evals

*Does the skill fire when it should — and stay quiet when it shouldn’t?*

|# |Prompt                                                |Should Trigger?|Notes                         |
|--|------------------------------------------------------|---------------|------------------------------|
|T1|[Clear positive — obviously needs this specialist]    |Yes            |[Why this is a clean positive]|
|T2|[Clear negative — adjacent domain, should NOT trigger]|No             |[Why this is a clean negative]|
|T3|[Ambiguous edge case]                                 |Yes/No         |[How to decide]               |
|T4|[Second clear positive, different task type]          |Yes            |[Why]                         |
|T5|[Second clear negative]                               |No             |[Why]                         |

### Quality Evals

*Does the specialist’s lens actually shift output in the intended direction?*

**Eval Q1**

- **Prompt**: [A realistic task prompt]
- **Good output looks like**: [2-3 specific, observable signals that this specialist’s
  lens is active. Be concrete: name behaviors — “reframes the question before answering”,
  “leads with the assumption being challenged”, “applies [framework] explicitly.” Not
  generic quality markers.]
- **Failure looks like**: [What Claude produces WITHOUT the specialist — the default
  framing or approach this specialist is specifically designed to replace]

**Eval Q2**

- **Prompt**: [A second realistic task, different type]
- **Good output looks like**: [Specific signals]
- **Failure looks like**: [Default framing without specialist]

**Eval Q3 (stress test)**

- **Prompt**: [A harder or ambiguous task that tests the limits of this specialist]
- **Good output looks like**: [Specific signals]
- **Failure looks like**: [Default framing, or graceful acknowledgment of scope limit]

### Description Health Check

*Paste these into skill-creator’s description optimizer if triggering evals are failing.*

**Should trigger:**

- “[Example prompt 1]”
- “[Example prompt 2]”
- “[Example prompt 3]”

**Should NOT trigger:**

- “[Counter-example 1]”
- “[Counter-example 2]”
