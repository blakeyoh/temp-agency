# Receipt 03 — mycelium #82 + #83: spec-vs-implementation review (review task)

**Task type:** code/spec review (not planning)
**Source:** [blakeyoh/mycelium#82](https://github.com/blakeyoh/mycelium/issues/82) (Classic rank ignores identity-dedup rule) + [#83](https://github.com/blakeyoh/mycelium/issues/83) (Daily "already played" CTAs lack documented 3-tier prominence).
**Staffing:** LEAD = investigative-journalist · LENS = farmer · vs unstaffed baseline
**Protocol:** three isolated subagents (Sonnet), identical inputs, no cross-visibility. 2026-07-02.

## Baseline (no persona)

Accurate review: confirmed both issues against the code with file:line evidence (noting minor line drift), located `dedupeScoresByIdentity` reuse as the #82 stopgap, recommended two CSS modifier classes for #83, correctly flagged the `expectDailyPathConnections` 8px geometry test as the regression risk. Good, correct, complete-seeming.

## LEAD — investigative-journalist

Treated the issue reports as *tips, not facts* and verified against primary sources — which surfaced defects the baseline accepted at face value:
- **Caught a broken citation in #82's acceptance criteria:** it names `submitClassicScoreWithRank`, a function that **does not exist** — actual function is `submitScore` (line 4472). "The kind of error that wastes an implementer's first ten minutes."
- **Mechanically verified** (not just asserted) the per-device duplicate accumulation: `playerUUID` is a stable const reused on every `.add()`, so multi-doc accumulation under one identity is guaranteed, not speculative.
- **Found a gap the issue AND baseline missed:** `fetchLeaderboard` dedup only operates on the top-200 raw docs (`.limit(200)`), while `fetchClassicRankContext` counts are unbounded — "dedupe the rank counter like the leaderboard does" still diverges past 200 submissions.
- **Systematic line-drift** in citations (3–9 lines optimistic throughout) — suggests they were computed loosely, not re-grepped at filing; habit fix.
- Confirmed #83's "opacity" claim is a minor overreach (opacity is unset, not a divergence point).

## LENS — farmer

Refused to treat the two issues as equal-weight spec drift:
- **#82 is a recurring weed, not a new bug:** #45 dedup'd the leaderboard in April; the same disease reappeared in an adjacent row because dedup was hand-applied to 3 of 4 call sites and forgotten on the fourth. Fix worth doing is **extract one shared deduped-identity query every consumer calls** — patch the counter and you'll read a #84 about a fifth call site next quarter.
- **Named the true root neither review touched:** `writeClassicScore`'s always-`.add()` is the seed; read-side dedup is a workaround for a write path that never stopped sowing duplicates.
- **#83 is correctly left fallow** — a spec written before the visual language was decided. Don't let queue-clearing pressure pick an arbitrary opacity just to close it; a guessed hierarchy that ships becomes the baseline everyone designs around.
- **The real field to till is the broken verification loop (#67, no Playwright):** both fixes touch a live scoring surface but can't verify themselves — "planting blind."
- **Named a process smell to the owner:** an automated filing cadence (Canopy) with no matching harvest cadence "isn't a garden, it's compost" — walk the queue, explicitly cut what won't be planted.

## Diff — what staffing changed

| | Baseline | Staffed |
|---|---|---|
| #82 fix | reuse `dedupeScoresByIdentity` in rank calc | + extract ONE shared deduped query (4 call sites drift); + fix `writeClassicScore` always-`.add()` root; + 200-doc-window gap breaks the naive fix at scale |
| Issue quality | accepted as accurate | + acceptance criteria cite a nonexistent function; + systematic citation drift |
| #83 | add two CSS classes | leave fallow — unmade design decision, don't guess opacity |
| Meta | — | + fix #67 verification loop first; + filing-without-triage process smell |

**What the lens caught that baseline missed (one line):** the baseline would have implemented a fix against acceptance criteria referencing a function that doesn't exist, patched the fourth symptom of a four-site pattern without touching the duplicate-writing root, and shipped it against a test suite that can't run.

## Verdict

**Lens added value: YES — materially changed both the fix and the confidence in the ticket.** Journalist's verification caught a ticket defect that would have derailed implementation and a scaling gap in the obvious fix; farmer reframed #82 from "patch a counter" to "extract a shared query + fix the write root" and defended leaving #83 fallow against close-the-ticket pressure. Both moved the work meaningfully off the baseline.
