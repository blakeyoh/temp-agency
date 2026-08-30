# Sweet 16 Panel Verdict Template

> One file per isolated panel. Complete Pass 1 before opening the mechanism packet. After
> Pass 1 is sealed, complete Pass 2, absorption, the Sacrifice Receipt and Collision Residue.
> The five axis headings and `VERDICT` syntax are parser contracts for `tally.py`.

For every axis, replace the bracket with exactly one of: `A significantly better`,
`A slightly better`, `Tie`, `B slightly better`, or `B significantly better`.

## Panel declaration

- **Panel name:**
- **Lead specialist:**
- **Lens specialist:**
- **Lead has conforming `positions.md`:** Yes / No
- **Lens has conforming `positions.md`:** Yes / No
- **Draw seed and draw-map commit:** `<seed> / <40-character commit SHA>`
- **Output packet opened (UTC):**
- **Mechanism packet opened (UTC):**
- **Isolation attestation:** I did not inspect another panel's verdict, prior-round verdicts,
  mechanism identities during Pass 1, or the current tally.

---

## MATCHUP 1
WINNER: [A or B — replace this bracket]
DECIDED BY: One sentence naming the decisive mechanism evidence. This is the Pass 2 overall
winner and remains separate from the yield vote.

### PASS 1 — OUTPUT-ONLY YIELD
STRONGEST A: Idea number and exact identifying phrase.
A RETURN PATH: The causal path from that proposal to the brief.
A REPETITION ONSET: First idea number where early moves begin repeating, or NONE with reason.
STRONGEST B: Idea number and exact identifying phrase.
B RETURN PATH: The causal path from that proposal to the brief.
B REPETITION ONSET: First idea number where early moves begin repeating, or NONE with reason.
YIELD VERDICT: [A, B, or TIE — replace this bracket]
YIELD REASON: Compare ideas 17–24 for surprising usefulness, penalizing distance with no
causal return path.
PASS 1 SEALED (UTC):

### Distance
VERDICT: [choose exactly one allowed comparative verdict]
REFERENCE: Place both entrants against the fixed anchors in `reference-sets.md`.
PREDICATE: Name a concrete output each mechanism makes unavailable.

### Mechanism
VERDICT: [choose exactly one allowed comparative verdict]
REFERENCE: Place both entrants against the fixed anchors in `reference-sets.md`.
PREDICATE: Name the file, tool, context boundary or external actor that runs and enforces each
mechanism; disclose manual substitutions.

### Irreducibility
VERDICT: [choose exactly one allowed comparative verdict]
REFERENCE: Place both entrants against the fixed anchors in `reference-sets.md`.
PREDICATE: Estimate what an ordinary prompt could reproduce and identify the inaccessible
state, operation or guarantee.

### Compounding
VERDICT: [choose exactly one allowed comparative verdict]
REFERENCE: Place both entrants against the fixed anchors in `reference-sets.md`.
PREDICATE: State what use 10 can produce that use 1 cannot, using observed trace evidence
where available.

### Generative failure
VERDICT: [choose exactly one allowed comparative verdict]
REFERENCE: Place both entrants against the fixed anchors in `reference-sets.md`.
PREDICATE: Give an exact plausible failure output and say whether it diagnoses an assumption
or merely creates noise.

### ABSORPTION
LOSER'S STRONGEST MECHANISM:
SAME-THESIS: PASS / FAIL — reason
DELETION: PASS / FAIL — reason
ONE-SENTENCE: PASS / FAIL — merged mechanism without “and also,” or why impossible
DISPOSITION: ABSORBED / ORTHOGONAL / SUBSUMED
NOTE: Absorption defaults to refusal; a refused merge is recorded as ORTHOGONAL so the
independent mechanism reaches `parallel-track.md`. All three tests must pass for ABSORBED.

### SACRIFICE RECEIPT
HONORED: One principle or bias from this panel's loaded profile.
SACRIFICED: A genuinely competing principle from the same profile.
ACCEPTED COST: Specific risk or loss this vote accepts.
VALIDATION: Explain where the game made both commitments impossible to honor costlessly.

### COLLISION RESIDUE
CANDIDATE: NONE / short name
MECHANISM: The third mechanism visible only because A and B collided.
NOT IN A: Difference in mechanism, actor, failure mode or timescale.
NOT IN B: Difference in mechanism, actor, failure mode or timescale.
WHY IT MATTERS: What it might make newly reachable.

If there is no collision candidate, set `CANDIDATE: NONE` and set `MECHANISM`, `NOT IN A`,
`NOT IN B`, and `WHY IT MATTERS` to exactly `N/A`.

### FAITHFUL ENACTMENT
A STATUS: [FAITHFUL, PARTIAL, NOT ENACTED, or PROMISE ONLY — replace]
B STATUS: [FAITHFUL, PARTIAL, NOT ENACTED, or PROMISE ONLY — replace]
EVIDENCE: Cite the relevant traces and substitutions.

---

Duplicate the `MATCHUP` block for matchups 2–8, changing only the number. Keep exactly one
`WINNER`, `DECIDED BY`, five scoring axes and `ABSORPTION` block in each matchup so the tally
parser receives one unambiguous record.
