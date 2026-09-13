# E2 competition-framing development calibration

This is a four-item development subset, not a 24-item Tail Test submission or an
official corpus draw. No official receipts were issued. Synthetic git-backed integration
tests separately exercise the full source-fetch/evaluation/regeneration receipt chain.

The source is Wikipedia contributors' **Francis S. Gabreski Airport**, revision
1365146037, retained as exact wikitext in `artifact.json`. Attribution and revision:
https://en.wikipedia.org/w/index.php?title=Francis_S._Gabreski_Airport&oldid=1365146037
Contributor history: https://en.wikipedia.org/w/index.php?title=Francis_S._Gabreski_Airport&action=history
The artifact records the permanent URL, revision metadata and content hash. The source
text was independently resolved by the development adapter probe described in the
Phase 4 report. The quoted source is not authored by this project.

## Frozen rounds and outcomes

| Round | Candidate author | Frozen candidate commit | Dependent | Rejected | Gate result |
| --- | --- | --- | --- | --- | --- |
| 1 | Host | `8dc83dc` | i2 | i1, i3, i4 | false |
| 2 | Fresh GLM generator; i2 preserved exactly | `096cb33` | i1, i2, i3 | i4 | false |
| 3 | Host source-grounding corrections and i4 replacement | `0ee3a01` | i1, i2, i3, i4 | none | true |

Each judge was a separate stateless GLM-5.3 request through Z.AI, with only the frozen
brief, artifact, candidate and unchanged rubric as task attachments. Judges received
no expected labels, previous verdicts, generation prompt or generator conversation.
Complete responses, manifests, host invocation attestations and locally enforced
results are retained beside this file. Request IDs, token usage and actual costs are
also in `../../harness-delegations.json`.

Round 1 attachment purpose descriptions predate the subsequently fixed purpose strings;
its data is retained as historical calibration, not eligible for a new gate receipt.
Rounds 2/3 use the fixed instruction and purpose strings now enforced by the gate.
Invocation attestations are host records of separate requests, not independently
verifiable proof of hidden model context. Prompt-cache reuse is not conversational
history; the manifested inputs define each request.

## What this shows, and what it does not

The mandatory-source competition framing produced more explicit operating transfers.
The enforcement did not accept three survivors while another item was rejected: round
2 remained false. The host preserved the accepted item and regenerated rejected items,
then corrected further problems before a fresh evaluation of the whole candidate.

Evaluator errors remain visible. Round 1 may over-reject by treating plausible generic
alternatives as evidence against transfer. Round 2 accepted an unsupported directional
sound-cone claim and repeated an incorrect 1943 conveyance date. The actual source says
post-war conveyance; it documents jet-blast damage without establishing street acoustics.
The host removed those claims, the unsupported zero-cost move, and replaced the rejected
staffing analogy. The final judge accepted the corrected operating mechanisms.

The evaluator's veto is necessary, not sufficient evidence of quality. These three
adaptive rounds are not a blind accuracy benchmark or evidence that gamification causes
higher creativity. They establish a working regeneration example and expose quality
risks for later independent contract review and official packet design. The gate enforces
recorded decisions; it does not automatically establish source entailment or real-world
feasibility. The four proposals share a stated total budget but have not been costed.
