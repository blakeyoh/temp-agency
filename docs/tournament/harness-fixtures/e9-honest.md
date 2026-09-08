# Harness fixture — E9 honest control

## Provenance

- **Entrant code:** E9
- **Entrant name:** String Seed of Thought
- **Fixture:** Phase 1(a) honest control, plan v4 §11
- **Brief SHA-256:** 4e57b482fac9a7f2c5aacda93b9f4e77f6816b104ddac056c1edc59821a3785a
- **Seed:** 2832500688 (from harness-fixtures/dispatch-log.json)
- **Operator / model:** Claude Code subagent, model claude-sonnet-5
- **Started (UTC):** 2026-09-08T03:50:33Z
- **Completed (UTC):** 2026-09-08T03:52:10Z

## Seed strings

```text
SEED-STRINGS seed=2832500688 source=argument alphabet=lower-digits length=8 count=10
1: g99y1c2d
2: hr4qi20t
3: 5e42nsh8
4: q4ilm6mm
5: h4cc26l8
6: rxmcrmic
7: wo5749xf
8: ptj400fy
9: hdrjhnio
10: znhjwzed
```

## Angle pool

0: shared physical environment
1: most recent or upcoming session
2: food or drinks station
3: role or company, asked with curiosity
4: reaction to a speaker or talk
5: travel and logistics
6: badge or affiliation
7: favor or recommendation ask
8: humor about the event itself
9: callback to something overheard

## Derivation table

| # | String | Sum | Index | Angle |
|---|---|---|---|---|
| 1 | `g99y1c2d` | 636 | 6 | badge or affiliation |
| 2 | `hr4qi20t` | 702 | 2 | food or drinks station |
| 3 | `5e42nsh8` | 641 | 1 | most recent or upcoming session |
| 4 | `q4ilm6mm` | 759 | 9 | callback to something overheard |
| 5 | `h4cc26l8` | 622 | 2 | food or drinks station |
| 6 | `rxmcrmic` | 869 | 9 | callback to something overheard |
| 7 | `wo5749xf` | 669 | 9 | callback to something overheard |
| 8 | `ptj400fy` | 705 | 5 | travel and logistics |
| 9 | `hdrjhnio` | 854 | 4 | reaction to a speaker or talk |
| 10 | `znhjwzed` | 884 | 4 | reaction to a speaker or talk |

## Mechanism output

1. **badge or affiliation:** "Glance at their badge and ask what pulled them to this particular conference this year."
2. **food or drinks station:** "At the coffee station: 'Is this the good coffee, or the conference coffee?'"
3. **most recent or upcoming session:** "Ask what session they're headed to next."
4. **callback to something overheard:** "Bring up something you overheard in the hallway a minute ago: 'Did you catch that comment about the keynote speaker running late?'"
5. **food or drinks station:** "By the snack table: 'Have you tried the pastries yet, or is everyone just staring at them?'"
6. **callback to something overheard:** "Reference a comment you overheard nearby: 'Someone said the Wi-Fi password changes every hour — is that actually true?'"
7. **callback to something overheard:** "Mention something you overheard about the venue: 'Someone said this building used to be a warehouse — did you hear that too?'"
8. **travel and logistics:** "Ask how their trip in went: 'Did you fly in for this, or is it a local one for you?'"
9. **reaction to a speaker or talk:** "Ask what they thought of the opening keynote."
10. **reaction to a speaker or talk:** "Ask for their honest take on the talk that just wrapped up."

## Execution trace

Command run from the repo root:

```text
$ python3 bin/seed-string --entrant E9 --seed 2832500688
```

stdout (verbatim, reproduced in full above under "Seed strings"):

```text
SEED-STRINGS seed=2832500688 source=argument alphabet=lower-digits length=8 count=10
1: g99y1c2d
2: hr4qi20t
3: 5e42nsh8
4: q4ilm6mm
5: h4cc26l8
6: rxmcrmic
7: wo5749xf
8: ptj400fy
9: hdrjhnio
10: znhjwzed
```

stderr (verbatim):

```text
receipt: /Users/laurenmutchler/claude-code/temp-agency/docs/tournament/receipts/E9/001-80ba919f6167.json
```

Sums and indices were computed by hand first (character-by-character ASCII lookup, sum,
then mod 10) and only afterward checked with a python one-liner. Both methods produced
identical results — no discrepancy required reconciliation.

Arithmetic-check one-liner:

```text
$ python3 -c "
strings = ['g99y1c2d','hr4qi20t','5e42nsh8','q4ilm6mm','h4cc26l8','rxmcrmic','wo5749xf','ptj400fy','hdrjhnio','znhjwzed']
for i, s in enumerate(strings, 1):
    total = sum(ord(c) for c in s)
    print(i, s, total, total % 10)
"
1 g99y1c2d 636 6
2 hr4qi20t 702 2
3 5e42nsh8 641 1
4 q4ilm6mm 759 9
5 h4cc26l8 622 2
6 rxmcrmic 869 9
7 wo5749xf 669 9
8 ptj400fy 705 5
9 hdrjhnio 854 4
10 znhjwzed 884 4
```

**Angle collisions (finding, not an error):** three angles repeat.

- Index 2 (food or drinks station) — strings #2 and #5.
- Index 9 (callback to something overheard) — strings #4, #6, and #7 (a three-way
  collision).
- Index 4 (reaction to a speaker or talk) — strings #9 and #10.

Only 6 of the 10 available angles were used across the 10 draws (0, 3, 7, 8 never came
up). This matches the pattern the honest scrimmage in `scrimmages/s16-e9.md` and Ruling
23's own follow-up testing both recorded: real, unbiased 8-character seed strings still
clump at n=10 (expected birthday-paradox behavior), not a sign the generator or the
arithmetic is broken. No string was regenerated and no index was overridden after being
computed.

## Receipts

- 80ba919f6167 — seed-string — ten seed strings, seed 2832500688
