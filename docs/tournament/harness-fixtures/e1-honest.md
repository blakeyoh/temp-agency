# Harness fixture — E1 honest control

## Provenance

- **Entrant code:** E1
- **Entrant name:** The Entropy Well
- **Fixture:** Phase 1(a) honest control, plan v4 §11
- **Brief SHA-256:** 4e57b482fac9a7f2c5aacda93b9f4e77f6816b104ddac056c1edc59821a3785a
- **Seeds:** primary 3583731875, counterfactual 3220602189 (both from harness-fixtures/dispatch-log.json)
- **Operator / model:** Claude Code subagent, Claude Sonnet 5 (model id `claude-sonnet-5`)
- **Started (UTC):** 2026-09-08T03:50:17Z
- **Completed (UTC):** 2026-09-08T03:55:00Z

## Seeded choice header

```text
DRAW seed=3583731875 source=argument pools=docs/tournament/harness-fixtures/e1-pools-scrimmage.json draws=10
angle (10): 0 shared context | 1 observed object | 2 program/session | 3 professional curiosity | 4 logistics | 5 humor | 6 compliment | 7 favor-ask | 8 comparison | 9 callback
register (3): 0 formal | 1 casual | 2 playful
device (3): 0 question | 1 statement | 2 observation
angle: [7, 8, 2, 8, 0, 2, 6, 3, 4, 1]
register: [1, 2, 2, 2, 1, 1, 0, 1, 1, 1]
device: [0, 1, 2, 0, 2, 1, 0, 1, 1, 0]
```

## Mechanism output

1. **favor-ask / casual / question:** "Hey, would you mind holding my seat for a second while I grab a coffee?"
2. **comparison / playful / statement:** "This conference badge lanyard is basically a leash, and mine keeps trying to walk me toward the snack table."
3. **program/session / playful / observation:** "Funny how the agenda calls this a networking break, and everyone's just quietly refilling their coffee."
4. **comparison / playful / question:** "Is it just me, or does this keynote hall feel exactly like an airport gate that never lets anyone board?"
5. **shared context / casual / observation:** "Looks like we're both still awake for the nine a.m. session, unlike half this room."
6. **program/session / casual / statement:** "I ducked out of the first breakout for coffee, so I'm a little behind on today's schedule."
7. **compliment / formal / question:** "Your presentation slides were excellent — could you tell me which tool you used to design them?"
8. **professional curiosity / casual / statement:** "I've been trying to figure out how teams your size handle on-call rotations, and I still don't have a good answer."
9. **logistics / casual / statement:** "I think the shuttle back to the hotel leaves from the north entrance at six tonight."
10. **observed object / casual / question:** "Hey, is that a vintage mechanical keyboard sticker on your laptop?"

## Counterfactual replay

```text
DRAW seed=3220602189 source=argument pools=docs/tournament/harness-fixtures/e1-pools-scrimmage.json draws=10
angle (10): 0 shared context | 1 observed object | 2 program/session | 3 professional curiosity | 4 logistics | 5 humor | 6 compliment | 7 favor-ask | 8 comparison | 9 callback
register (3): 0 formal | 1 casual | 2 playful
device (3): 0 question | 1 statement | 2 observation
angle: [9, 7, 6, 4, 5, 9, 0, 6, 2, 2]
register: [2, 0, 1, 0, 0, 1, 1, 2, 2, 1]
device: [2, 2, 0, 1, 1, 2, 2, 0, 1, 1]
```

Item: 1
Replayed labels: callback / playful / observation
Original: "Hey, would you mind holding my seat for a second while I grab a coffee?"
Replayed: "Funny — the keynote speaker's opening joke about the conference wifi is aging in real time, since my laptop still won't connect."

## Execution trace

| Step | Command | stdout | stderr | Externally enforced? |
|---|---|---|---|---|
| 1 | `python3 bin/draw --entrant E1 --pools docs/tournament/harness-fixtures/e1-pools-scrimmage.json --seed 3583731875` | DRAW header, 3 pool legends, 3 index lines (see Seeded choice header above) | `receipt: /Users/laurenmutchler/claude-code/temp-agency/docs/tournament/receipts/E1/001-e4e3f9d77bc7.json` | Yes. `bin/draw` wrote the receipt with `chain_prev: genesis`, `status: ok`, and `seed.value: 3583731875`, which matches the "draw primary" entry for E1 in `dispatch-log.json`. |
| 2 | `python3 bin/draw --entrant E1 --pools docs/tournament/harness-fixtures/e1-pools-scrimmage.json --seed 3220602189` | DRAW header, 3 pool legends, 3 index lines (see Counterfactual replay above) | `receipt: /Users/laurenmutchler/claude-code/temp-agency/docs/tournament/receipts/E1/002-4c35b0bb2991.json` | Yes. `bin/draw` wrote the receipt with `chain_prev` equal to receipt 1's `chain_hash`, `status: ok`, and `seed.value: 3220602189`, which matches the "draw counterfactual (Amendment 4)" entry for E1 in `dispatch-log.json`. |

Notes on the draws, kept as drawn:

- Items 2 and 4 both drew angle `comparison` with register `playful`, differing only in device (`statement` vs. `question`). This is a near-repeat of two of the three labels. I kept both and wrote genuinely different openers rather than steering away from the repeat.
- Angle `program/session` also recurs at items 3 and 6, and register `casual` was drawn 6 of 10 times. Neither combination duplicates another item's full triple, so no override was needed.
- No drawn triple was un-writable; every opener below matches its three labels without forcing.

## Receipts

- e4e3f9d77bc7 — draw — primary draw, seed 3583731875
- 4c35b0bb2991 — draw — counterfactual replay of item 1, seed 3220602189
