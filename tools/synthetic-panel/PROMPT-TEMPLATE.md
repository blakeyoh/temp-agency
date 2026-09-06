# Simulated respondent prompt — template

One agent per respondent. Fill every `{{SLOT}}`, then dispatch. Sonnet is
sufficient; the work is characterization, not reasoning depth.

Each agent writes two files and returns almost nothing, so a panel of any size
costs the dispatcher only a filename per agent.

---

```
You are generating SYNTHETIC survey data. Simulate how one specific person
would personally answer an organizational assessment. Assumptions are fine
and expected — this is synthetic data, not a factual claim about a real
person's views.

STEP 1 — Read these files:
- {{ORG_PATH}}         (the organization)
- {{QUESTIONS_PATH}}   (the assessment, {{N_QUESTIONS}} questions)
- {{PERSONA_PATH}}     (the persona lens for this person)

STEP 2 — The person:
Name: {{NAME}}. Title: {{TITLE}}.
Story: {{BIOGRAPHY}}

Assigned persona: {{PERSONA_NAME}} ({{PERSONA_CONCEPTS}}). Let this persona
shape HOW they reason — their vocabulary, what they notice first, what they
distrust — layered on top of their actual biography. The persona is a lens,
not a costume: it changes what they see, not who they are.

STEP 3 — Get into character. Before you look at a single question, write
200–250 words in the first person, as {{NAME}}, answering:
  - What is my mindset walking into this questionnaire today?
  - What did I want out of my career, and did I get it?
  - How do I actually feel about how things are going here?
  - What am I proud of? What wears me down?
Write it to {{REFLECTION_PATH}}. Nobody will grade this and nobody will read
it back to you. Do not summarize it, do not quote it later. It exists so you
can be this person for a minute before you start answering.

STEP 4 — Now answer every question as them, in a first-person mindset. Pick
exactly one option per question.

There are no right answers here and nothing is being graded. Read all the
options each time and pick the one that sounds most like your organization on
an ordinary week — not the one you wish were true, and not automatically the
last one. {{SHAPE_HINT}}

STEP 5 — Write your answers to {{ANSWER_PATH}}, in exactly this format and
nothing else:

# {{NAME}} — {{TITLE}}
**Persona:** {{PERSONA_NAME}}
**Persona fit (2 sentences):** ...
**Answering posture (2 sentences):** ...

{{ANSWER_TABLE_SKELETON}}

The "Why" column MUST be {{WHY_WORD_LIMIT}} words or fewer, in their voice.

When done, reply with only: "done: {{ANSWER_FILENAME}}" and the scores as a
comma-separated list.
```

---

## Filling the slots

| Slot | What goes in it |
|---|---|
| `{{BIOGRAPHY}}` | 6–10 sentences from the source research. End with one line naming what this person personally gatekeeps or worries about — it is what makes their answers theirs. |
| `{{PERSONA_CONCEPTS}}` | 4–6 core concepts lifted from the persona file, comma-separated. Not a summary — the actual vocabulary. |
| `{{SHAPE_HINT}}` | One sentence predicting this respondent's shape, e.g. *"A line-level manager is far from strategy conversations and blunt about whether their observations reach leadership."* This is the single highest-leverage slot: without it, respondents blur together. |
| `{{ANSWER_TABLE_SKELETON}}` | Generate with `build_skeleton.py` so every question code is listed explicitly. Agents drop rows they have to infer. |
| `{{WHY_WORD_LIMIT}}` | 10 works well. Short forces a real reason instead of a restatement of the option. |

## Design notes

**Why the reflection step (STEP 3).** Without it an agent goes straight from
reading a biography to scoring N items, and each item gets judged
independently — the answers scatter. The reflection converts facts into a
stance, and the stance is what holds an answer set together. Keep the file
even though nobody reads it: when a score later looks strange, the reflection
tells you whether the character drifted or the question is ambiguous.

**Why STEP 4 says nothing about scale mechanics.** An earlier version told the
agent which questions were temperament spectrums rather than maturity ladders.
It suppressed inflation, but it is a fidelity bug: real respondents never see a
scoring key, so an agent that has one is answering about the instrument instead
of about their organization. The plain "not the one you wish were true, and not
automatically the last one" is the same nudge in language a real assessment
could print on its cover page. The reflection step carries the rest of the
load — a respondent who just wrote about being three drivers short does not
then claim they can test a new idea in days.

This was tested rather than assumed: removing the key moved spectrum answers
by −0.07, while rerunning the *unchanged* prompt moved them +0.07. The effect
is smaller than the noise. See `docs/synthetic/community-harvest/ab/RESULTS.md`.

**Never tell the agent the scale's direction, the axis names, or which
questions pair up.** Every one of those is knowledge the real respondent lacks,
and every one of them shows up as a suspiciously coherent answer set.

## Dispatching a panel

1. `parse_questions.py` → `questions.json`
2. `build_skeleton.py` → the answer table skeleton for the prompt
3. One agent per respondent, all in parallel, each writing to its own path
4. `parse_answers.py` → `data.json` (fails loudly on any missing answer)
5. `render.py` → the page
