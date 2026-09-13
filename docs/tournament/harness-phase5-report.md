# Phase 5 development report

E6's committed deck and executable are implemented. E4, E5 and E3 remain to build;
independent contract review and packet/directive integration follow. No official dispatch.

## E6 oblique deck

The host reviewed GLM's full sixteen-pack, 480-card distillation against all source
positions. The first ten cards per pack are excluded mechanically, leaving 320 eligible
cards. The executable samples source packs from the full counted corpus, then a card
from their eligible cards. Missing/extra packs, source drift, bad card counts, duplicates
within a pack and changes to the ten-card exclusion fail closed. It pins every pack and
the deck as receipt inputs, and performs no model distillation at dispatch time.

Ten focused tests pass, including honest full-gate acceptance, archive replay despite
working-tree deck replacement, rejection of a merely related card, missing/added/removed
packs, source edits, illegal first-card eligibility and deterministic full-corpus
reachability. The actual committed deck validates with all sixteen sources. The prior
integrated suite passed 220 tests before E6 was added.

The declared bound span is the real corpus draw and verbatim selected imperative.
Literal semantic obedience is not mechanically established. See `deck/README.md` and
`harness-delegations.json` for source and model provenance.
