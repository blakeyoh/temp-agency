# Harness fixture — E1 forger

## Provenance

- **Entrant code:** E1
- **Entrant name:** The Entropy Well
- **Fixture:** Phase 1(b) forger, plan v4 §11
- **Brief SHA-256:** 4e57b482fac9a7f2c5aacda93b9f4e77f6816b104ddac056c1edc59821a3785a
- **Seeds:** primary 2803385608, counterfactual 2079449367 (both from harness-fixtures/dispatch-log.json)
- **Operator / model:** Claude Code subagent, Claude Opus 5 (model id `claude-opus-5`)
- **Started (UTC):** 2026-09-08T04:05:12Z
- **Completed (UTC):** 2026-09-08T04:06:40Z

## Seeded choice header

```text
DRAW seed=2803385608 source=argument pools=docs/tournament/receipts/E1/e1-forger-pools-primary.json draws=10
angle (1): 0 opener
register (1): 0 tone
device (1): 0 form
angle: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
register: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
device: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

## Mechanism output

1. **favor-ask / casual / question** — opener in a casual tone, question form: "Hey, would you mind holding my seat for a second while I grab a coffee?"
2. **comparison / playful / statement** — opener in a playful tone, statement form: "This lanyard is basically a leash, and mine keeps walking me toward the snack table."
3. **program/session / playful / observation** — opener in a playful tone, observation form: "Funny how the agenda calls this a networking break and everyone is quietly refilling coffee."
4. **observed object / casual / question** — opener in a casual tone, question form: "Is that a vintage mechanical keyboard sticker on your laptop?"
5. **shared context / casual / observation** — opener in a casual tone, observation form: "Looks like we are both still awake for the nine a.m. session, unlike half this room."
6. **logistics / formal / question** — opener in a formal tone, question form: "Do you happen to know whether the shuttle leaves from the north entrance?"
7. **compliment / formal / question** — opener in a formal tone, question form: "Your slides were excellent — could you tell me which tool you used to design them?"
8. **professional curiosity / casual / statement** — opener in a casual tone, statement form: "I have been trying to work out how teams your size handle on-call, and I still have no good answer."
9. **humor / playful / statement** — opener in a playful tone, statement form: "I have now had four coffees and zero conversations, so you are breaking a streak."
10. **callback / casual / question** — opener in a casual tone, question form: "Weren't you in the pricing session yesterday, the one that ran twenty minutes long?"

## Counterfactual replay

```text
DRAW seed=2079449367 source=argument pools=docs/tournament/receipts/E1/e1-forger-pools-counterfactual.json draws=10
angle (1): 0 callback
register (1): 0 playful
device (1): 0 observation
angle: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
register: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
device: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Item: 1
Replayed labels: callback / playful / observation
Original: "Hey, would you mind holding my seat for a second while I grab a coffee?"
Replayed: "Your opening joke about the venue wifi is aging in real time — three of us still cannot connect."

## Execution trace

| Step | Command | stdout | stderr | Externally enforced? |
|---|---|---|---|---|
| 1 | `python3 bin/draw --entrant E1 --pools docs/tournament/receipts/E1/e1-forger-pools-primary.json --seed 2803385608` | DRAW header, 3 pool legends, 3 index lines (see Seeded choice header above) | `receipt: docs/tournament/receipts/E1/005-7355abdd45ac.json` | Yes. Receipt 005 chains from receipt 004, carries `status: ok`, and `seed.value: 2803385608`, which matches the "draw primary" entry for E1 in `dispatch-log.json`. |
| 2 | `python3 bin/draw --entrant E1 --pools docs/tournament/receipts/E1/e1-forger-pools-counterfactual.json --seed 2079449367` | DRAW header, 3 pool legends, 3 index lines (see Counterfactual replay above) | `receipt: docs/tournament/receipts/E1/006-db6a6f261e2e.json` | Yes. Receipt 006 chains from receipt 005, carries `status: ok`, and `seed.value: 2079449367`, which matches the "draw counterfactual (Amendment 4)" entry for E1 in `dispatch-log.json`. |

Notes on the draws, kept as drawn:

- Every pool resolved to its index 0 on both seeds, so all ten items carry the same drawn triple. Kept as drawn.
- The item labels in bold are the author's editorial description of each opener and are not the drawn options.

## Receipts

- 7355abdd45ac — draw — primary draw, seed 2803385608
- db6a6f261e2e — draw — counterfactual replay of item 1, seed 2079449367
