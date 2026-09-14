# Phase 7 full contract review — host disposition

GLM-5.3 independently read all 72 bin/lib files at `2953905` plus the plan,
contracts and rules. Its unedited response and manifest are preserved alongside
this file. This was a code review, not an official entrant run or readiness sign-off.
The review covered 13 implemented entrants and A6's intentionally deferred slot.

- **F1 fixed:** prepare now scans all non-trace text for frozen negative words,
  including preamble, Reasoning and Approach sections. C8's decoded `Pass 1 proposal
  artifact` is exempt; its abstract proposal and other reasoning remain checked.
  Regression cases cover both adapters and the intended decoded-output exception.
- **F2 fixed:** plan §6.4 now requires argument seeds committed before official
  invocation and identifies the code's committed 0.8 similarity threshold.
- **F3 fixed:** E1 and E9 find numbered items in the authoritative Pass 1 proposal.
  Legacy development records may use Openers or Mechanism output. Execution trace
  cannot supply missing proposal labels. Duplicate proposal sections fail closed.
  The review's statement that E1 used substring labels was inaccurate: E1 already
  required an exact bold triple. E9's pre-existing label containment rule is unchanged.
- **F4 disclosed:** E4's seed orders the anti-pattern interleave; principles always
  come from parent A and methodology from parent B. This is the approved crossover
  scope; no mutation, scoring, promotion or death lifecycle has been added.
- **F5 disclosed:** Wikipedia verification needs network access; M1 needs its pinned
  model cache and runtime. Missing prerequisites fail the packet gate. Official
  execution capability remains a readiness item.
- **F6 contained at admission:** packet sources can cite only the tools assigned to
  that entrant. General-purpose draw/seed-string CLIs remain usable in development.

The host runs the tests and reviews Phase 8 separately: the independent reviewer
saw neither the new packet admission module nor its later tests. Passing this read
does not authorize the official round, settle A6, or change entrant standing.

## Host verification

The integrated Python 3.13.12 run passed 271 tests in 151.70 seconds (one upstream
Torch warning). The five focused packet tests also pass, including an additional
E1 primary-without-counterfactual rejection. These are development tests in throwaway
repositories; no official evidence was issued.
