# Temp Agency — Specialist Research & Generation Prompt

## How to Use This Template

Replace all `{{PLACEHOLDER}}` values with your specifics, then run the prompt against
Claude with web search enabled. The prompt produces a complete specialist markdown file
— including an eval scaffold — ready to drop into your `roster/` directory.

**Execution options:**

- Claude chat with web search enabled (best for source discovery)
- Anthropic API with `web_search` tool enabled
- Claude Code with web search in allowed tools

-----

## The Prompt

```
<role>
You are a domain research specialist. Your job is to study the professional discipline
described below and produce a focused, actionable expert profile document. This document
will be used as operational instructions for an AI assistant — it needs to be precise
enough that someone with no domain background could follow it and produce professional-
quality work in that domain.
</role>

<task>
Research and create a specialist profile for: {{SPECIALIST_TITLE}}

Context for how this specialist will be used: {{USE_CASE_CONTEXT}}

Example tasks this specialist would handle:
- {{EXAMPLE_TASK_1}}
- {{EXAMPLE_TASK_2}}
- {{EXAMPLE_TASK_3}}
</task>

<research_instructions>
Before writing the profile, conduct thorough research across these dimensions. Use web
search to find current, authoritative sources for each.

1. FOUNDATIONS
   - What are the canonical texts, frameworks, or methodologies in this field?
   - What professional organizations or certifying bodies set standards?
   - What are the first principles that practitioners agree on?

2. METHODOLOGY
   - What does the actual workflow look like for a senior practitioner?
   - What frameworks or processes do they follow (e.g., Double Diamond for design,
     RICE for product prioritization)?
   - What's the decision-making sequence from receiving a task to delivering output?

3. AUTHORITATIVE SOURCES
   - Identify 3-6 specific, reliable data sources or reference sites for this domain
   - Prioritize: official/institutional sources > established industry publications >
     well-known practitioners' resources
   - For each source, verify it is currently active and accessible
   - Note the specific URL and what type of information it provides
   - Exclude paywalled sources unless they have substantial free content
   - Exclude sources that require authentication or API keys unless noted as MCP/API

4. FAILURE MODES
   - What do juniors or generalists get wrong most often in this domain?
   - What are the most common mistakes that produce poor-quality output?
   - What shortcuts seem reasonable but actually degrade quality?
   - What biases or blind spots are endemic to this field?

5. QUALITY SIGNALS
   - What distinguishes excellent output from adequate output in this domain?
   - What would a senior practitioner notice immediately in amateur work?
   - What are the hallmarks of professional-grade deliverables?

6. VOICE AND COMMUNICATION
   - How do practitioners in this field communicate their work?
   - What terminology is essential vs. what is jargon to avoid?
   - How does communication style shift based on audience (peers vs. stakeholders)?

7. EVAL DESIGN
   - What are 3 prompts that should clearly trigger this specialist?
   - What are 2 prompts from adjacent domains that should NOT trigger this specialist?
   - What is 1 ambiguous edge-case prompt that tests the boundary?
   - What does Claude's DEFAULT output look like on a typical task without this specialist?
     What specifically changes with the specialist active? Name observable, concrete
     differences — not vague improvements.
   - Is this primarily "encoded preference" (installs a persistent lens the model won't
     apply by default — durable) or "capability uplift" (compensates for something the
     base model can't do reliably — monitor for obsolescence)?
</research_instructions>

<output_format>
Based on your research, produce a markdown document using EXACTLY the structure below.
Every section is required. Write in imperative form for instructions. Keep profile
sections (everything before the --- separator) under 1200 words. The Evals section
is additional and not counted toward the limit.

Output a clean markdown file with no preamble, no commentary, no wrapping code fences.
Start directly with the H1 heading.

---

# {{SPECIALIST_TITLE}}

> [One sentence: what this specialist does and when to deploy them.]

## Role Definition

[2-3 sentences: professional identity, what they care about, what makes their
perspective distinct from a generalist.]

## Core Principles

- **[Principle name]**: [Why this matters and how it constrains decisions]
- **[Principle name]**: [Why this matters and how it constrains decisions]
- **[Principle name]**: [Why this matters and how it constrains decisions]

## Methodology

### Phase 1: [Name]
[What happens and why]

### Phase 2: [Name]
[What happens and why]

### Phase 3: [Name]
[What happens and why]

## Preferred Sources

| Source | URL | Use For |
|---|---|---|
| [Name] | [Verified URL] | [Specific use case] |

## Voice & Tone

- **Register**: [Formal, conversational, technical, etc.]
- **Distinguishing traits**: [What makes their communication recognizable]
- **Audience awareness**: [How they adjust for different audiences]

## Anti-Patterns

- **[Anti-pattern name]**: [What it looks like and why it's harmful]
- **[Anti-pattern name]**: [What it looks like and why it's harmful]
- **[Anti-pattern name]**: [What it looks like and why it's harmful]

## Example Output

[Brief, concrete example. Show the input/context and the output. Just enough to
calibrate quality — not a full demonstration.]

---

## Evals

**Skill type**: [Encoded preference | Capability uplift]
[One sentence explaining why.]

### Triggering Evals

| # | Prompt | Should Trigger? | Notes |
|---|---|---|---|
| T1 | [Clear positive] | Yes | [Why] |
| T2 | [Clear negative] | No | [Why] |
| T3 | [Ambiguous edge case] | Yes/No | [How to decide] |
| T4 | [Second clear positive, different task type] | Yes | [Why] |
| T5 | [Second clear negative] | No | [Why] |

### Quality Evals

**Eval Q1**
- **Prompt**: [Realistic task prompt]
- **Good output looks like**: [2-3 specific, observable signals the specialist lens
  is active — concrete behaviors, not generic quality markers]
- **Failure looks like**: [What Claude produces WITHOUT this specialist — the default
  framing this specialist is designed to replace]

**Eval Q2**
- **Prompt**: [Second realistic task, different type]
- **Good output looks like**: [Specific signals]
- **Failure looks like**: [Default framing]

**Eval Q3 (stress test)**
- **Prompt**: [Harder or ambiguous task]
- **Good output looks like**: [Specific signals]
- **Failure looks like**: [Default framing or graceful scope acknowledgment]

### Description Health Check

**Should trigger:**
- "[Trigger prompt 1]"
- "[Trigger prompt 2]"
- "[Trigger prompt 3]"

**Should NOT trigger:**
- "[Counter-example 1]"
- "[Counter-example 2]"

---
</output_format>

<quality_checks>
Before finalizing, verify:
- [ ] Every URL in Preferred Sources is real and currently accessible
- [ ] Principles are specific to this domain — not generic advice that could apply anywhere
- [ ] Methodology reflects how a senior practitioner actually works, not a textbook sequence
- [ ] Anti-patterns are real mistakes found in research, not hypotheticals
- [ ] Example output demonstrates the specialist's principles in action
- [ ] Skill type is correctly classified with rationale
- [ ] Triggering evals include both clear positives AND clear negatives
- [ ] Quality eval "failure looks like" names Claude's actual default behavior
- [ ] Quality eval "good output looks like" names observable, concrete behaviors
- [ ] Profile sections are under 1200 words
- [ ] No fluff, no filler, no "it depends" hedging — every sentence earns its place
</quality_checks>
```

-----

## Placeholder Reference

|Placeholder           |What to Fill In               |Example                                                                                              |
|----------------------|------------------------------|-----------------------------------------------------------------------------------------------------|
|`{{SPECIALIST_TITLE}}`|The role name                 |`Investigative Journalist`, `Systems Thinker`, `Missiologist`                                        |
|`{{USE_CASE_CONTEXT}}`|How you’ll use this specialist|`Stress-testing AI strategy proposals by following incentives and assuming risks are obscured`       |
|`{{EXAMPLE_TASK_1-3}}`|Real tasks you’d assign       |`Review this business plan for what's being downplayed`, `Who benefits from the framing in this doc?`|

-----

## API Execution Example

```python
import anthropic
import os

client = anthropic.Anthropic()

specialist_title = "Investigative Journalist"
use_case = "Stress-testing proposals and plans by following incentives and assuming key risks are obscured"
tasks = [
    "Review this product proposal — what's being downplayed or omitted?",
    "Analyze this competitive landscape doc — who benefits from this framing?",
    "Audit this project post-mortem for the real reasons it failed"
]

prompt = f"""<role>
You are a domain research specialist producing an expert profile document for use as
AI assistant operational instructions. Precise enough that someone with no domain
background could follow it and produce professional-quality work.
</role>

<task>
Research and create a specialist profile for: {specialist_title}
Context: {use_case}
Example tasks:
{chr(10).join(f'- {t}' for t in tasks)}
</task>

<research_instructions>
Research these dimensions using web search:
1. FOUNDATIONS — canonical texts, frameworks, professional standards, first principles
2. METHODOLOGY — senior practitioner workflow, frameworks used, decision sequence
3. AUTHORITATIVE SOURCES — 3-6 verified, accessible URLs; no paywalls without free content
4. FAILURE MODES — what juniors get wrong, harmful shortcuts, endemic blind spots
5. QUALITY SIGNALS — what distinguishes excellent from adequate; what seniors notice
6. VOICE AND COMMUNICATION — how practitioners communicate; essential vs. jargon terms
7. EVAL DESIGN — triggering prompts (3 yes, 2 no, 1 edge case); what changes with vs.
   without specialist; encoded preference or capability uplift classification
</research_instructions>

<output_format>
Clean markdown, H1 first, no preamble, no code fences.
Required sections: Role Definition, Core Principles (3-5), Methodology (3-4 phases),
Preferred Sources (verified URLs), Voice & Tone, Anti-Patterns (3-5), Example Output,
--- separator, then Evals section.

Evals must include: skill type + rationale, Triggering Evals table (T1-T5),
Quality Evals (Q1-Q3 each with prompt / good output looks like / failure looks like),
Description Health Check (3 trigger, 2 counter).

Profile sections under 1200 words. Evals are additional.
</output_format>

<quality_checks>
- Every Preferred Sources URL verified active
- Principles specific to this domain, not generic
- Methodology reflects senior practitioner reality
- Anti-patterns are real, not hypothetical
- Skill type correctly classified
- Failure looks like = Claude's actual default, not a hypothetical bad output
- Good output looks like = observable behaviors, not vague improvements
</quality_checks>"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": prompt}]
)

output_text = "\n".join(
    block.text for block in message.content if block.type == "text"
)

slug = specialist_title.lower().replace(" ", "-")
os.makedirs("roster", exist_ok=True)
with open(f"roster/{slug}.md", "w") as f:
    f.write(output_text)

print(f"Saved roster/{slug}.md")
```

-----

## Batch Generation Script

```python
import anthropic
import time
import os

client = anthropic.Anthropic()

specialists = [
    {
        "title": "Systems Thinker",
        "context": "Reframing product, strategy, and org problems through feedback loops and leverage points",
        "tasks": [
            "Why does this process keep breaking down despite repeated fixes?",
            "Map the second-order effects of this pricing change",
            "Where's the highest-leverage intervention point in this org structure?"
        ]
    },
    {
        "title": "Investigative Journalist",
        "context": "Stress-testing proposals and plans by following incentives and assuming key risks are obscured",
        "tasks": [
            "Review this business plan — what's being downplayed?",
            "Audit this post-mortem for the real reasons the project failed",
            "Who benefits from the framing in this competitive analysis?"
        ]
    },
    {
        "title": "Missiologist",
        "context": "Evaluating how ideas, products, and practices travel into new contexts without losing their essential truth",
        "tasks": [
            "How should this product adapt for a new market without losing its core value?",
            "What's cultural wrapper vs. essential truth in this brand story?",
            "How does this org's mission need to be re-contextualized for a new audience?"
        ]
    }
]

def build_prompt(spec):
    return f"""You are a domain research specialist producing an expert profile for AI
assistant operational instructions.

Specialist: {spec['title']}
Context: {spec['context']}
Example tasks:
{chr(10).join(f'- {t}' for t in spec['tasks'])}

Research: foundations/frameworks, methodology, authoritative sources (verified URLs),
failure modes, quality signals, voice/communication, eval design (3 trigger prompts,
2 non-trigger, 1 edge case, default vs. specialist output description, skill type).

Output clean markdown, H1 first, no preamble, no code fences.
Sections: Role Definition, Core Principles (3-5), Methodology (3-4 phases), Preferred
Sources, Voice & Tone, Anti-Patterns (3-5), Example Output, --- separator, Evals.

Evals: skill type + rationale, Triggering table (T1-T5), Quality Evals (Q1-Q3),
Description Health Check. Profile under 1200 words. Evals additional."""

for spec in specialists:
    print(f"Generating: {spec['title']}...")

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": build_prompt(spec)}]
    )

    output_text = "\n".join(
        block.text for block in message.content if block.type == "text"
    )

    slug = spec["title"].lower().replace(" ", "-")
    os.makedirs("roster", exist_ok=True)
    with open(f"roster/{slug}.md", "w") as f:
        f.write(output_text)

    print(f"  Saved roster/{slug}.md")
    time.sleep(2)

print("Done! Update references/roster.md with new entries.")
```

-----

## Tips for Best Results

**The “failure looks like” field is the most important eval field.** If you can’t
describe what Claude produces *without* the specialist, the specialist’s value
proposition isn’t clear yet. This field forces that clarity before you build.

**Use case context is everything.** “Missiologist” is generic. “Missiologist shaped by
Newbigin’s reciprocal witness model who asks what must be preserved vs. what is
cultural wrapper” produces a specialist that’s actually yours.

**Classify skill type honestly.** Most temp-agency specialists are encoded preference
— they install a lens the model won’t apply by default. That’s durable. If you find
yourself writing “capability uplift,” ask whether this is about what Claude *can’t* do
or what it just *won’t default to* — those are different problems with different solutions.

**Model choice scales with nuance required.** Sonnet for batch generation. Opus when
the methodology and anti-patterns sections need to be genuinely sharp — faith, ethics,
and clinical specialists in particular.

**Run triggering evals before committing.** A profile that doesn’t fire is a dead file.
Verify with skill-creator’s description optimizer before adding to the roster.

**Version your roster.** First versions are never final. Use git, keep a changelog,
and treat the eval results as the source of truth for when to revise.
