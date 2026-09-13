# E6 committed oblique deck

`cards.json` contains thirty imperatives in original generation order for each of the
sixteen real `knowledge/*/positions.md` packs. The first ten of each pack are retained
for audit but **ineligible for every draw**. Twenty per pack remain: 320 eligible cards
across the full corpus. These are model-authored creative distillations, not quotations
or newly adopted project instructions.

The host read all 480 cards and all sixteen source packs. No cards were edited or
reordered after generation. Every pack pins its source's SHA-256. The complete model
response and exact request manifest are retained here; usage and request metadata are
also logged in `../harness-delegations.json`. GLM-5.3 through Z.AI produced the draft in
91.075 seconds for $0.04025084. Host code handles validation and selection.

`bin/oblique --entrant E6 --seed N` counts the real positions files at invocation,
requires an exact sorted deck/corpus match and unchanged source hashes, samples two
packs without replacement from the whole corpus, then draws one card uniformly from
their forty eligible cards. `--pack-count` may choose another positive count within
the corpus; it cannot name preferred packs. `--deck` names a committed alternative
only if it covers the same complete current corpus and obeys the same 30-minus-10 schema.
A corpus addition, removal, stale source or missing pack fails closed.

The receipt pins the deck and every source pack, exposes the corpus count, pack indices,
card index and original card number, and replays from its git archive. The binding checks
the complete draw output in Execution trace and the literal card in Mechanism output.
It does **not** prove the final prose literally obeys the imperative; this is the weak
binding explicitly accepted in the build plan. Human/model contract review remains.

No official dispatch or entrant-standing change is authorized by this deck.
