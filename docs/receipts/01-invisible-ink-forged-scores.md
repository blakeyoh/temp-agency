# Receipt 01 — invisible-ink #141: client-forged classification scores (plan task)

**Task type:** implementation planning (security fix)
**Source:** [blakeyoh/invisible-ink#141](https://github.com/blakeyoh/invisible-ink/issues/141) — client-controlled `classification` field lets any player forge an unbounded round score.
**Staffing:** LEAD = systems-thinker · LENS = behavioral-psychologist · vs unstaffed baseline
**Protocol:** three isolated subagents (Sonnet), identical inputs (issue body + repo access), no visibility into each other's output. 2026-07-02.

## Baseline (no persona)

Competent two-tier plan:
1. **Now:** Firebase rules backstop — restore missing `$drawingId` key-scoping sub-rule, `.validate` clamp `claudeScore` to [0,100], boolean-validate `hasSpeedBonus`, immutability guard on written classifications.
2. **Later:** move classification authority server-side — `classify.js` writes the score via Firebase Admin SDK; rules deny client writes to `classification` entirely.

Also independently discovered the live `firebase-rules.json` is *more* permissive than the issue quotes (no `$drawingId` sub-rule exists at all). Solid verification plan (rules-simulator tests, exploit replay, legit-play regression).

## LEAD — systems-thinker

Same two technical tiers, but reframed in ways that change the plan:

- **Named the recurrence archetype with repo evidence:** this is *Shifting the Burden* — issue #125 previously patched `players/$uid/score` writes (symptomatic fix on the output), and the exploit migrated one hop upstream to `classification` (the input). Shipping the clamp with the structural fix "left as a design decision" repeats the exact move that caused this ticket.
- **The clamp alone makes things worse, not better:** attackers move from `999999999` to exactly `100` every round — unbounded forgery is an anomaly-monitoring gift; always-max forgery inside the valid range is invisible to the same monitoring. Symptom disappears, forcing function for the real fix dies.
- **Predicted the next ticket:** `hasSpeedBonus` has the same client-authored shape; sweep it into the structural fix now rather than waiting for it to earn its own issue.
- **Deploy-risk catch:** repo rules don't match issue-quoted rules — confirm which rules file is actually live before shipping any `.validate`; "a structurally correct fix deployed to the wrong file is not a fix."
- **Sharpened the server-side option:** `classify.js` must derive `playerId`/`drawingId` from a server-verified ID token, not client parameters — otherwise the forgery vector just moves to "which submission do I attach my call to."

## LENS — behavioral-psychologist

Constraints no technical pass surfaced:

- **Two attacker populations, only one addressed:** the *griefer* (wants visible absurdity — the clamp stops them) vs the *quiet inflator* (writes a plausible 97 — the clamp does nothing, and they're the one who actually corrodes the room's trust).
- **The reveal screen is the game's existing fraud detector:** drawings shown next to scores make forgery socially falsifiable in real time — free moderation. Any server-side fix that reorders the flow so scores lock before reveal trades a technical vulnerability for a trust vulnerability. *Constraint on Tier 2 design that neither technical pass imposed.*
- **Post-fix accusation toxicity:** once players learn the exploit existed, honest high scores get accused. Ship a legibility fix (visible score-source signal) alongside the security fix.
- **Host-authoritative scoring moves the attack surface** to whoever hosts — not neutral in stranger rooms.
- **Proportionality:** anti-fraud-banking UX in a party game reads as ridiculous and gets mocked.

## Diff — what staffing changed

| | Baseline | Staffed |
|---|---|---|
| Fix content | clamp now + Admin SDK later | same tiers, but clamp **must** ship paired with tracked structural fix (archetype evidence), `hasSpeedBonus` swept in, token-derived identity required |
| Risk model | unbounded forgery | + in-range forgery becoming *less* detectable post-clamp; + rules-file drift as deploy risk |
| Constraints | technical only | + preserve reveal-before-score-lock sequencing; + score legibility to prevent accusation toxicity; + host-trust displacement |

**What the lens caught that baseline missed (one line):** the fix as planned would have made cheating harder to *see* rather than harder to *do*, and could have silently destroyed the reveal-screen social auditing that currently moderates the game for free.

## Verdict

**Lens added value: YES — materially changed the decision.** Baseline's plan was correct but incomplete in ways that would have shipped: no pairing/forcing function for the structural fix (the exact failure mode that produced this issue, per #125), no protection for the reveal-flow social contract, no awareness that the stopgap degrades detectability. LEAD's archetype framing + LENS's social-contract constraints both alter what gets built and in what order.
