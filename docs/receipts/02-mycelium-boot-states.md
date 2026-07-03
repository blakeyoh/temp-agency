# Receipt 02 — mycelium #70: first-time vs returning boot screen (plan task)

**Task type:** implementation planning (product/UX)
**Source:** [blakeyoh/mycelium#70](https://github.com/blakeyoh/mycelium/issues/70) — boot screen never distinguishes first-time vs returning players despite PLAN.md's Home State Variants contract.
**Staffing:** LEAD = behavioral-psychologist · LENS = franciscan-monk · vs unstaffed baseline
**Protocol:** three isolated subagents (Sonnet), identical inputs, no cross-visibility. 2026-07-02.

## Baseline (no persona)

Thorough, high-quality plan: pure-function variant selection (`pickHomeVariant`), `mycelium-visited` flag, "played before? skip intro" escape link, Daily-status/streak second line for returning players, `resetOverlaySections()` cleanup to prevent overlay leakage, ~60 lines total. Independently caught the `mycelium-uuid` detection trap (minted on first load — always present, useless as a returning signal). Good verification (truth-table unit tests, manual matrix, deferred Playwright per #67).

## LEAD — behavioral-psychologist

Same architecture, but with behavioral *reasons* that harden the plan:
- Boot screen framed as the **habit cue**: re-showing tutorial copy degrades the cue's signature — mechanism, not preference.
- Skip link reframed as **self-identification device** (reactance avoidance), not a button.
- **Error-direction reasoning**: on storage failure default to first-time — "a veteran skims one line; a novice with no instructions is the expensive error."
- Same uuid trap caught, with the crisper rule: use evidence of *behavior*, not evidence of *visitation*.
- Daily status line justified via implementation intentions + loss-framed streak motivation.
- Explicit anti-pattern list (no tour, no announced personalization, no "welcome back" warmth copy).

## LENS — franciscan-monk

Attacked the premise everyone else accepted:
- **"The plan invokes 'ritual' and then prescribes its opposite. Ritual *is* sameness."** The same eight quiet words on the hundredth morning may be where the welcome lives — the shipped "bug" might be the more contemplative artifact. Burden of proof belongs on the branch, not the sameness.
- **"No one is trapped by a door you never build."** The skip-intro escape exists only because the differentiation trap is being proposed; delete the branch and the escape, heuristics, and test scaffolding vanish with it.
- **localStorage-as-identity misreads the margins**: shared iPad, spouse on the same tab, library computer, storage cleared out of necessity. Branching greets the wrong person warmly; a single humble greeting excludes no one.
- **Refuse boot-screen streak/status outright**: "streak displays do not serve the player's memory; they serve the game's claim on the player" — retention mechanics wearing the clothes of care. *Direct contradiction of both baseline and LEAD, who included it.*
- Minimal version if the contract must be honored: one boolean (`highScore > 0`), one copy swap to "a memory network." No skip link, no status line, no heuristics.

## Diff — what staffing changed

Baseline and LEAD converged on the same build (~60 lines, status line included). The LENS split the decision open:

1. **A product fork neither surfaced:** does a quiet contemplative game want loss-aversion mechanics on its boot screen at all? LEAD argued streak-on-boot *works* (that's the problem, says the monk). This is now an explicit owner decision, not a default.
2. **A scope floor:** monk's minimal version (boolean + copy swap) is a genuine shippable alternative at ~10% of the cost, and three independent agents agreeing the branch is cheap doesn't answer whether it's warranted.
3. **An honest failure mode:** device-residue personalization mis-greeting exactly the players at the margins of device ownership.

**What the lens caught that baseline missed (one line):** that the issue's premise deserved cross-examination — the "fix" imports retention mechanics into a product whose identity is contemplative sameness, and the minimal honest version is one boolean and one line of copy.

## Verdict

**Lens added value: YES — changed the decision space.** Without the lens, the ~60-line variant (streak line included) ships by default. With it, the owner faces a named fork: full behavioral variant vs monk-minimal copy swap, and the boot-screen streak display needs an explicit yes rather than riding in silently. Visible LEAD↔LENS contradiction (streak line: load-bearing feature vs refused outright) is exactly the friction the skill exists to produce.
