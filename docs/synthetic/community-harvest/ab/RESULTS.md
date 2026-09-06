# A/B: does removing the scale key inflate answers?

**Date:** 2026-09-06 · **Model:** Sonnet · **n = 3 respondents × 26 questions**

## The question

The original prompt told each agent which questions were temperament spectrums
rather than maturity ladders, and instructed it to "choose by temperament, not
aspiration." That suppressed score inflation, but it is a fidelity bug: real
respondents never see a scoring key, so an agent holding one answers *about the
instrument* instead of *about their organization*.

Variant B removes the key entirely, replaces it with respondent-natural wording
("not the one you wish were true, and not automatically the last one"), and adds
a 200–250 word in-character reflection before any question is read.

The worry: without the key, would answers drift upward on the spectrum items?

## Design

Three respondents spanning the org chart — Carmen Cumberland (CEO),
Katie Savoie (director), Dearllean Walker (line manager).

| Run | Prompt |
|---|---|
| **A** | Original — scale key present, no reflection step |
| **B** | Scale key removed, respondent-natural wording, reflection step added |
| **A2** | Identical to A, rerun — establishes the run-to-run noise floor |

A2 is the control that makes the rest interpretable. Without it, any A→B
difference could be the prompt or could be sampling.

## Result

|  | A→A2 (noise) | A→B (the change) |
|---|---:|---:|
| Direction Focus (ladder) | +0.04 | +0.00 |
| Agility Focus (ladder) | +0.25 | +0.21 |
| Sensing vs. Creating Tradeoff (spectrum) | +0.07 | −0.07 |
| Direction vs. Agility Tradeoff (spectrum) | +0.07 | −0.07 |
| **All 26 questions** | **+0.12** | **+0.04** |
| **Spectrum items only** | **+0.07** | **−0.07** |
| Answers that changed | 26 / 78 | 31 / 78 |
| …of which spectrum | 11 / 30 | 12 / 30 |

**Every effect of the prompt change is smaller than or equal to the noise from
rerunning the identical prompt.** Spectrum items moved −0.07 under the change
and +0.07 under a plain rerun — opposite directions, both trivial.

The inflation worry was unfounded. Variant B is adopted: it is materially more
faithful to how a real respondent encounters the instrument, and it costs
nothing measurable in score discipline.

## The more important finding

**About a third of all answers flip on an identical rerun.** 26 of 78 with no
prompt change at all.

Per-respondent means moved this much between identical runs:

| Respondent | rerun (A→A2) | variant B (A→B) |
|---|---:|---:|
| Carmen Cumberland | +0.04 | −0.12 |
| Katie Savoie | −0.04 | −0.08 |
| Dearllean Walker | **+0.35** | **+0.31** |

Walker is unstable under both, by the same amount. That is a property of the
respondent, not the variant — she is the respondent with the least externally
documented position, so the simulation has the most latitude. The fix is a
sharper `{{SHAPE_HINT}}` and a richer biography, not a prompt tweak.

## What this means for reading any panel

This is variance, not error. Each run is a real judgment, and a third of them
landing differently is what thoughtful answering looks like on a 5-point scale.

1. **Individual scores stay in.** They carry the structure underneath the
   aggregate — who dissents, where the org chart splits, who sits alone on a
   question. Group means alone discard most of the panel's value.
2. **A single score is a position, not a measurement.** "Walker is the low
   outlier on frontline voice" holds. "Walker scored exactly 0.75" over-reports
   precision the method does not have.
3. **A pattern counts when it survives ±0.35.** "Every respondent scored
   Direction above Agility" clears that easily. A 0.1 gap between two
   respondents does not.
4. **To rank or threshold respondents, run each 3+ times and take the median.**
   One run is enough for shape; three is enough for order.
5. **Thin biographies produce noisy respondents.** Instability is a signal that
   a respondent needs more source material, not a different prompt.

## Reproducing

```bash
cd docs/synthetic/community-harvest
python3 ab/compare.py --questions questions.json \
  --a ab/variant-a/data.json --b ab/variant-a2/data.json --label-a A --label-b A2
python3 ab/compare.py --questions questions.json \
  --a ab/variant-a/data.json --b ab/variant-b/data.json --label-a A --label-b B
```
