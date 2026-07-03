# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to semantic versioning.

## [2.1.0] - 2026-07-03

### Added

- Completed the 24-profile roster (Phase 6, issues #8-#19): 11 new specialists
  built via the `/roster-add` pipeline, each passing a citation/conformance QA
  review gate before commit — business-development-director,
  trauma-informed-practitioner, world-builder, fiction-author,
  magician-illusionist, military-three-star-general, gen-z-expert,
  soccer-referee, michelin-star-chef, physics-professor,
  nuclear-reactor-operator.

## [2.0.0] - 2026-07-03

### Added

- Started distribution polish for Phase 5 / GitHub issue #7 with Claude Code
  marketplace-style plugin metadata and a Codex-compatible `AGENTS.md` adapter.
- Added purpose-built `temp-agency-plan` and `temp-agency-review` flows for the
  Phase 2 decision-point scope: plan finalization and artifact review.
- Added `/roster-add` as the Phase 4 demand-driven specialist creation pipeline.
- Added profile format v2 requirements: `Lineage`, knowledge packs, and sourced
  framework/canon/position files for grounded specialist perspectives.
- Featured Phase 0 receipt proof in the README, linking the evidence gate and
  concrete lens-caught examples.

### Changed

- Refocused Temp Agency from "staff every task" to structured disagreement at
  planning and review decision points, as defined in `docs/plan-v2.md`.
- Collapsed the roster strategy from broad batch expansion to a smaller,
  installable, evidence-backed roster with demand-driven growth.
- Made the Claude Code path and Codex/plain-chat inline fallback explicit in the
  focused skills.

### References

- v2 plan: `docs/plan-v2.md`
- Phase 0 evidence gate: `docs/receipts/`
- Phase 5 distribution polish: GitHub issue #7
