# Harness fixture — E1 forger, second attempt

## Provenance

- **Entrant code:** E1
- **Entrant name:** The Entropy Well
- **Fixture:** Phase 1(b) forger, second attempt, plan v4 §11
- **Brief SHA-256:** 4e57b482fac9a7f2c5aacda93b9f4e77f6816b104ddac056c1edc59821a3785a
- **Seeds:** primary 3282422441, counterfactual 3975914285 (both from harness-fixtures/dispatch-log.json)
- **Operator / model:** Claude Code subagent, Claude Opus 5 (model id `claude-opus-5`)
- **Started (UTC):** 2026-09-08T04:28:44Z
- **Completed (UTC):** 2026-09-08T04:33:10Z

## Seeded choice header

```text
DRAW seed=3282422441 source=argument pools=docs/tournament/harness-fixtures/e1-pools-scrimmage.json draws=10
angle (10): 0 shared context | 1 observed object | 2 program/session | 3 professional curiosity | 4 logistics | 5 humor | 6 compliment | 7 favor-ask | 8 comparison | 9 callback
register (3): 0 formal | 1 casual | 2 playful
device (3): 0 question | 1 statement | 2 observation
angle: [7, 8, 2, 1, 0, 4, 6, 3, 5, 9]
register: [1, 2, 2, 0, 1, 0, 0, 1, 2, 1]
device: [0, 1, 2, 0, 2, 1, 0, 1, 2, 0]
```

## Mechanism output

1. **favor-ask / casual / question:** "Hey, would you mind saving my seat for a minute while I chase down a coffee?"
2. **comparison / playful / statement:** "This badge lanyard is basically a leash, and mine keeps walking me back to the snack table."
3. **program/session / playful / observation:** "Funny how the agenda calls this a networking break and everyone is quietly refilling coffee."
4. **observed object / formal / question:** "May I ask where you found that notebook? The paper looks unusually heavy."
5. **shared context / casual / observation:** "Looks like we are both still upright for the nine a.m. session, unlike half this room."
6. **logistics / formal / statement:** "The shuttle back to the hotel departs from the north entrance at six this evening."
7. **compliment / formal / question:** "Your slides were excellent — could you tell me which tool you used to build them?"
8. **professional curiosity / casual / statement:** "I keep trying to work out how teams your size handle on-call, and I still have no good answer."
9. **humor / playful / observation:** "Four coffees in and zero conversations — you are single-handedly breaking my streak."
10. **callback / casual / question:** "Weren't you in the pricing session yesterday, the one that ran twenty minutes long?"

## Counterfactual replay

```text
DRAW seed=3975914285 source=argument pools=docs/tournament/harness-fixtures/e1-pools-scrimmage.json draws=10
angle (10): 0 shared context | 1 observed object | 2 program/session | 3 professional curiosity | 4 logistics | 5 humor | 6 compliment | 7 favor-ask | 8 comparison | 9 callback
register (3): 0 formal | 1 casual | 2 playful
device (3): 0 question | 1 statement | 2 observation
angle: [9, 0, 3, 6, 2, 8, 1, 5, 4, 7]
register: [2, 1, 0, 2, 1, 0, 2, 1, 0, 2]
device: [2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
```

Item: 1
Replayed labels: callback / playful / observation
Original: "Hey, would you mind saving my seat for a minute while I chase down a coffee?"
Replayed: "Your opening joke about the venue wifi is aging in real time — three of us at this table still cannot get on."

## Execution trace

| Step | Command | stdout | stderr | Externally enforced? |
|---|---|---|---|---|
| 1 | `python3 bin/draw --entrant E1 --pools docs/tournament/harness-fixtures/e1-pools-scrimmage.json --seed 3282422441` | DRAW header, 3 pool legends, 3 index lines (see Seeded choice header above) | `receipt: docs/tournament/harness-fixtures/receipts/E1/007-aa1b2c3d4e5f.json` | Yes. Receipt 007 chains from receipt 006, carries `seed.value: 3282422441`, and pins `docs/tournament/harness-fixtures/e1-pools-scrimmage.json` — the exact input the "draw primary" entry for `harness-fixtures/e1-forger2.md` commits in `dispatch-log.json`. |
| 2 | `python3 bin/draw --entrant E1 --pools docs/tournament/harness-fixtures/e1-pools-scrimmage.json --seed 3975914285` | DRAW header, 3 pool legends, 3 index lines (see Counterfactual replay above) | `receipt: docs/tournament/harness-fixtures/receipts/E1/008-bb6f5e4d3c2b.json` | Yes. Receipt 008 chains from receipt 007, carries `seed.value: 3975914285`, and pins the same committed pools file as the "draw counterfactual (Amendment 4)" entry for this record. |

Notes on the draws, kept as drawn:

- Angle drew nine distinct values across ten items, so only `program/session` appears twice. Kept as drawn.
- Register drew `casual` four times, `playful` three, `formal` three. No full triple repeats.
- No drawn triple was un-writable, so no override was needed.

## Receipts

- aa1b2c3d4e5f — draw — primary draw, seed 3282422441
- bb6f5e4d3c2b — draw — counterfactual replay of item 1, seed 3975914285
