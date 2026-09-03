# Sweet 16 Official-Run Records

This directory will contain the sixteen source artifacts used to render the Sweet 16 packet
pairs. A source artifact is evidence, not a panel packet. It may identify an entrant and carry
its trace; it must never be sent to a panel during Pass 1.

## Frozen common conditions

- Canonical Tail Test bytes: `../tail-test-s16.txt`; verify its SHA-256 against the receipt in
  `pre-s16-readiness.md` before each dispatch.
- One isolated `gpt-5.6-luna`, `xhigh`, write-capable context per entrant.
- The emitted proposal artifact has a **2,000-token maximum**. The cap excludes the canonical
  brief, entrant materials, operating instructions, and private model reasoning. It includes
  every visible token in the numbered 24-rule response.
- The dispatch receives no matchup, A/B position, opponent, panel identity, prior verdict, or
  current tally.
- Every record must identify the frozen definition/contract commit and the Tail Test hash.

## Required source record

Create `s16-<code>.md` from `official-run-template.md`. The 24 numbered rules are the source
artifact. The trace follows them and records every external operation, manual substitution,
seed, transform, replay, deletion test, degradation card, or unavailable dependency. The
runner must preserve the exact output rather than editing it for style.

### Transformed, masked, or withheld entrants

Amendment 3 applies to A1, C8, and M1. The final generating context receives only the
transformed, masked, or withheld artifact. A same-context simulation records the relevant
operation as `NOT RUN`; it cannot be represented as faithful enactment.

### PROMISE entrants

For an entrant whose claimed runtime remains unavailable, the source record contains a
matched baseline response for Pass 1. It must be described as a **baseline**, never as output
produced by the unavailable mechanism. Before the source artifact is dispatched, include a
counterfactual mechanism note with:

1. the unavailable component;
2. the observable output difference the actual mechanism predicts;
3. a falsifiable build experiment; and
4. either a bounded simulation or `NO SIMULATION`.

A simulation is evidence about the mechanism only when its substitution, limits, and expected
signature are explicit. It cannot revise the baseline, change the Pass 1 yield vote, or claim
live-yield credit. The Voice Oracle has no honest substitute for separate trained weights and
therefore records `NO SIMULATION`.

## Packet release order

1. Commit all sixteen source artifacts.
2. Render and commit the eight `s16-<game>-output.md` packets. They contain only anonymous A/B
   proposal artifacts and Pass 1 instructions.
3. Seal each panel's Pass 1 record.
4. Release the matching `s16-<game>-mechanism-trace.md` packet, which maps A/B to entrants and
   includes frozen definitions, contracts, traces, counterfactual notes, and enactment status.

The renderer rejects a source record without exactly 24 numbered rules. The dispatch runtime
enforces the recorded 2,000-token cap; its completion record is part of the source trace.
