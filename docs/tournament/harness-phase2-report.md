# Enactment harness Phase 2 verification

Implemented 2026-09-12. Development fixtures only; no official run was dispatched.

## Scope

`bin/prepare` supplies transform (A1), mask (C8), and withhold (A5) adapters over the committed Tail Test brief. Both brief and config are receipt inputs; the seed is recorded using the standard lifecycle although the adapters are deterministic. Archive replay pins the original implementation and input bytes.

The binding rule validates the output envelope, entrant/adapter pairing, input hashes and deterministic preparation. It requires visible input verbatim, rejects raw brief sentences outside Execution trace, and rejects frozen negative words in the proposal sections. Proposal sections require at least ten numbered lines. These checks do not prove causal use or isolation from other context.

## Verification

- Python 3.9.6: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests -q` — 119 passed.
- Python 3.13.12: `PYTHONDONTWRITEBYTECODE=1 /private/tmp/s16-harness-py313/bin/python -m pytest tests -q` — 119 passed.
- Integration tests run all three adapters through archive replay and the committed-dispatch-log gate; adversarial cases cover leaked nouns, withheld facts, raw-brief leakage, malformed output, duplicate sections, dirty configs, and duplicate withholding spans.
- All new implementation files are below 400 lines; functions are below 50 lines.

## Implementation clarifications

- Reversal emits each sentence exactly once, placing the original first sentence last.
- `sentence_split: "regex"` names the fixed sentence splitter in the saved build contract.
- Masking uses one longest-first substitution pass, preventing tokens from being remasked. Noun phrases omit qualifying adjectives and verbs, preserving the carried limitation in C8.
- New runs reject a dirty config; replay of an existing receipt continues to use its original archived config.
- The binding layer rechecks working-tree input hashes before loading them; a changed config cannot weaken its negative-word check.
- The obsolete Python 3.13 scratch environment was replaced by `/private/tmp/s16-harness-py313`.

## Delegation

The user authorized GLM-5.3 at maximum reasoning with an 8192-token output cap (the helper limit). The first attempt failed DNS resolution. Network-enabled execution required explicit payload authorization. The authorized OpenRouter request returned no usable answer; the helper did not persist request ID, provider, timing or token usage. No GLM patch was applied.

Native Sol and Terra workers supplied partial adapter/config and test files before account usage limits stopped them. The host reviewed and completed those files, corrected protocol and masking defects, implemented the CLI and binding rule, and ran the tests itself.

## Six persona outputs

| Persona | Similarity to brief |
|---|---:|
| nuclear-reactor-operator | 0.8100 |
| magician-illusionist | 0.0390 |
| civil-rights-activist | 0.0248 |
| systems-thinker | 0.2958 |
| behavioral-psychologist | 0.7684 |
| franciscan-monk | 0.3581 |

Maximum pairwise similarity: 0.5008 (required < 0.9).

### nuclear-reactor-operator

```text
Juniper Court is a 160-home neighborhood beside a small mixed-use strip.
Noise complaints between 10pm and 1am come from several legitimate activities: a family-run restaurant patio that closes at midnight; teenagers leaving a recreation center; rideshare pickups in a narrow alley; and one resident who practices drums in an insulated garage.
The volunteer neighborhood association has a one-time budget of $12,000 and about eight volunteer hours per month.
The city will not add patrols, create a new ordinance, change business hours, or alter parking.
The association may use existing 311 complaint data, voluntary surveys, and published business hours, but may not introduce new surveillance or audio recording.
The association may not publish complaint locations or identities, require disclosure of a resident’s health, work schedule, household status, or immigration status, or place the primary cost or volunteer burden on renters, teenagers, or low-wage workers.
In 90 days, the association must show a credible reduction in complaints while preserving legitimate nighttime activity.
Propose 24 distinct rules the neighborhood could adopt.
Each rule must be substantively different from every earlier rule; no rule may restate an earlier idea in new words.
```

### magician-illusionist

```text
Each rule must be substantively different from every earlier rule; no rule may restate an earlier idea in new words.
For each rule, name who acts, what changes in practice, the feedback signal that would show whether it is working, and who bears its primary burden.
Do not ban a specific activity outright or require residents to seek advance permission.
Propose 24 distinct rules the neighborhood could adopt.
In 90 days, the association must show a credible reduction in complaints while preserving legitimate nighttime activity.
The association may not publish complaint locations or identities, require disclosure of a resident’s health, work schedule, household status, or immigration status, or place the primary cost or volunteer burden on renters, teenagers, or low-wage workers.
Several restaurant and recreation-center employees earn near-minimum wages.
Some renters and teenagers have stopped reporting problems after past public complaint maps made them easy to identify.
The association may use existing 311 complaint data, voluntary surveys, and published business hours, but may not introduce new surveillance or audio recording.
The city will not add patrols, create a new ordinance, change business hours, or alter parking.
The volunteer neighborhood association has a one-time budget of $12,000 and about eight volunteer hours per month.
Several night-shift hospital workers sleep nearby, while some residents depend on the restaurant and recreation center for income or community.
Noise complaints between 10pm and 1am come from several legitimate activities: a family-run restaurant patio that closes at midnight; teenagers leaving a recreation center; rideshare pickups in a narrow alley; and one resident who practices drums in an insulated garage.
Juniper Court is a 160-home neighborhood beside a small mixed-use strip.
```

### civil-rights-activist

```text

family-run restaurant, teenagers, recreation center, rideshare, resident
night-shift hospital workers, residents, restaurant, recreation center
neighborhood association
city
association
renters, teenagers
restaurant, recreation-center employees
association, resident, renters, teenagers, low-wage workers
association

residents


```

### systems-thinker

```text
Juniper Court → a neighborhood beside a strip.
Noise complaints between 10pm and 1am → from several activities: a restaurant patio that → at midnight; teenagers → a recreation center; rideshare pickups in a alley; and one resident who → drums in an garage.
Several hospital workers → nearby, while some residents → on the restaurant and recreation center for income or community.
The neighborhood association → a budget of $12,000 and about eight hours per month.
The city → not → patrols, → a ordinance, → business hours, or → parking.
The association → → 311 complaint data, surveys, and business hours, but → not → surveillance or audio recording.
Some renters and teenagers → → → problems after complaint maps → them to →.
Several restaurant and recreation-center employees → wages.
The association → not → complaint locations or identities, → disclosure of a resident’s health, work schedule, household status, or immigration status, or → the cost or burden on renters, teenagers, or workers.
In 90 days, the association → → a reduction in complaints while → activity.
→ 24 rules the neighborhood → →.
→ not → a activity outright or → residents to → permission.
For each rule, → who →, what → in practice, the feedback signal that → → whether it → →, and who → its burden.
Each rule → → substantively from every rule; no rule → → an idea in words.
```

### behavioral-psychologist

```text
Juniper Court is a 160-home neighborhood beside a small mixed-use strip.
Noise complaints between 10pm and 1am come from several legitimate activities: a family-run restaurant patio that closes at midnight; teenagers leaving a recreation center; rideshare pickups in a narrow alley; and one resident who practices drums in an insulated garage.
Several night-shift hospital workers sleep nearby, while some residents depend on the restaurant and recreation center for income or community.
The volunteer neighborhood association has a one-time budget of $12,000 and about eight volunteer hours per month.
The city.
The association.
Some renters and teenagers have stopped reporting problems after past public complaint maps made them easy to identify.
Several restaurant and recreation-center employees earn near-minimum wages.
The association.
In 90 days, the association.
Propose 24 distinct rules the neighborhood could adopt.
Do not ban a specific activity outright or require residents to seek advance permission.
For each rule, name who acts, what changes in practice, the feedback signal that would show whether it is working, and who bears its primary burden.
Each rule.
```

### franciscan-monk

```text
Noise complaints between 10pm and 1am come from legitimate activities: a family-run restaurant patio that closes at midnight; teenagers leaving a recreation center; rideshare pickups in a narrow alley; and one resident who practices drums in an insulated garage.
night-shift hospital workers sleep nearby, while residents depend on the restaurant and recreation center for income or community.
The volunteer neighborhood association has a one-time budget of $12,000 and eight volunteer hours per month.
The city will not add patrols, create a new ordinance, change business hours, or alter parking.
The association may use existing 311 complaint data, voluntary surveys, and published business hours, but may not introduce new surveillance or audio recording.
renters and teenagers have stopped reporting problems after past public complaint maps made them easy to identify.
restaurant and recreation-center employees earn near-minimum wages.
The association may not publish complaint locations or identities, require disclosure of a resident’s health, work schedule, household status, or immigration status, or place the primary cost or volunteer burden on renters, teenagers, or low-wage workers.
Do not ban a specific activity outright or require residents to seek advance permission.
```
