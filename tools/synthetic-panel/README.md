# Synthetic panel

Generate a panel of simulated respondents who answer an organizational
assessment in character, then render their answers as a single page.

Built for stress-testing an assessment instrument: you get plausible,
differentiated respondents at every level of an org chart, in minutes,
without recruiting anyone.

**Everything produced here is fabricated.** It is useful precisely because it
is not real data, and it is dangerous the moment anyone forgets that. Every
rendered page carries a notice saying so.

## The pipeline

```
source .docx  ──parse_questions.py──▶  questions.json ──┐
                                              │         │
                                    build_skeleton.py   │
                                              │         │
   ORG.md + persona files + biographies       │         │
                    │                         ▼         │
                    └────────▶  one agent per respondent│
                                              │         │
                                    answers/*.md        │
                                              │         │
                               parse_answers.py ◀───────┘
                                              │
                                        data.json
                                              │
                                        render.py
                                              │
                                        panel.html
```

Nothing downstream hardcodes a question code, a scale, or a grouping. Swap the
source documents, re-run, and the page adapts.

## Running one

```bash
RUN=docs/synthetic/my-org
mkdir -p $RUN/answers $RUN/reflections

# 1. Questions -> manifest. One --docx per instrument.
python3 tools/synthetic-panel/parse_questions.py \
  --docx check.docx:check --docx full.docx:full \
  -o $RUN/questions.json

# 2. Table skeleton to paste into each agent prompt.
python3 tools/synthetic-panel/build_skeleton.py --questions $RUN/questions.json

# 3. Write $RUN/ORG.md by hand (see below), then dispatch one agent per
#    respondent using PROMPT-TEMPLATE.md. Run them in parallel.

# 4. Collect and validate. Fails loudly on any missing answer.
python3 tools/synthetic-panel/parse_answers.py \
  --questions $RUN/questions.json --answers $RUN/answers -o $RUN/data.json

# 5. Render.
python3 tools/synthetic-panel/render.py \
  --questions $RUN/questions.json --data $RUN/data.json \
  --config $RUN/panel.json -o $RUN/panel.html
```

## Writing ORG.md

This is the highest-leverage file in the pipeline and the one part that is not
automated. Write it by hand from your source research. Around 40 lines.

| Section | Why |
|---|---|
| Scale | Hard numbers, so respondents anchor on real constraints |
| Programs / products | Named things, so answers use the real vocabulary |
| Known strengths | What they would score themselves high on |
| **Known weaknesses** | What caps their scores — the most important section |
| Opportunities / threats | External pressure they would cite |
| Culture note | One blunt line about how decisions actually get made |

Weaknesses do the heavy lifting. A briefing that lists only strengths produces
a panel that scores itself uniformly high, which tells you nothing.

## Source document format

`parse_questions.py` expects each question as:

```
DS1 · Direction Focus in a Sensing Context
Prompt: When it comes to understanding what our customers actually need…
0 · We rely on what we've historically offered
1 · We gather feedback but mostly to refine existing offerings
…
```

Two things are derived from the axis label, not configured:

- **group** — the label with context suffixes stripped
  (`Direction Focus in a Sensing Context` → `Direction Focus`)
- **kind** — `spectrum` if the label contains "tradeoff", else `ladder`

Both can be overridden per code with `--overrides`:

```json
{ "TC2": { "kind": "ladder", "group": "Portfolio discipline" } }
```

## Files

| File | Does |
|---|---|
| `parse_questions.py` | .docx/.txt → `questions.json` (the source of truth) |
| `build_skeleton.py` | `questions.json` → answer table for the prompt |
| `parse_answers.py` | `answers/*.md` → `data.json`, with hard validation |
| `render.py` | → standalone `panel.html`, light and dark |
| `PROMPT-TEMPLATE.md` | The respondent prompt, with slot-filling notes |

## Reading the output

Two scale kinds are colored differently and must not be averaged together:

- **Ladder** questions are maturity — higher is genuinely stronger, and a group
  mean is meaningful.
- **Spectrum** questions are temperament — a low score sits at the other end,
  not lower down. Averaging these produces a number that means nothing.

`render.py` only computes group means for ladder groups, for this reason.
