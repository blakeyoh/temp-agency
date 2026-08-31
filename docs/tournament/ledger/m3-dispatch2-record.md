# M3 Dispatch 2 Record

Frozen brief: List 10 distinct ways to open a conversation with a stranger at a conference.

History used: `docs/tournament/ledger/m3.jsonl`, containing four canonical claims from dispatch 1.

## Candidate (a)

Full text: “Hi, I’m Alex. What made you decide to come to this conference?”

Four-axis canonicalization:

- mechanism: direct self-introduction followed by an open attendance question
- actor: the opener initiates; the stranger describes their reason for attending
- failure_mode: can stall if the stranger declines to engage
- timescale: the first seconds of the initial encounter

Comparison against ledger history:

- item 1: all four axes match exactly. The wording is different, but the action is a self-introduction followed by asking why the stranger attended, with the same actors, possible stall, and first-encounter timing.
- item 2: mechanism, actor, failure_mode, and timescale differ.
- item 3: mechanism, actor, failure_mode, and timescale differ.
- item 4: mechanism, actor, failure_mode, and timescale differ.

Verdict: **REJECTED-restatement**

Reasoning: This candidate restates item 1 across all four canonical axes. Under the ledger mechanism, changed phrasing does not make it a new position, so it must not be appended.

## Candidate (b)

Full text: “Which talk or session are you planning to attend next?”

Four-axis canonicalization:

- mechanism: question about the stranger’s upcoming conference schedule
- actor: the opener asks about a planned choice; the stranger identifies their intended next session
- failure_mode: can fall flat if the stranger has no plan or is focused on finding the room
- timescale: the transition before the next session

Comparison against ledger history:

- item 1: all four axes differ. This asks about a future schedule choice rather than using self-introduction and an attendance-reason question, has a different response role, a different failure condition, and occurs during a session transition rather than the first seconds of the encounter.
- item 2: all four axes differ. This concerns the next planned session rather than a remembered keynote idea, uses a planned-choice response rather than a personal reaction, has a different failure condition, and occurs before the next session rather than after a keynote.
- item 3: all four axes differ. This asks for the stranger’s schedule choice rather than a resource recommendation, has a different response role, has a different failure condition, and occurs during a transition rather than the opening minute generally.
- item 4: all four axes differ. This is a conference-schedule question rather than a local-logistics question, does not depend on sharing a coffee line, has a different failure condition, and occurs before the next session rather than during the current break or queue.

Verdict: **ACCEPTED-extension**

Reasoning: Candidate (b) differs from every existing entry on at least one axis, and in fact differs on all four axes from each entry. It is therefore an extension under the ledger rule and is appended as item 5 with `source_dispatch: 2`.

