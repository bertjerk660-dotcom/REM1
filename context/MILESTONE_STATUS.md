# Milestone Status — 2026-10-07

Do not use percentages unless supported by an explicit task-count method. These statuses describe readiness, not effort remaining.

## Milestone A — Evidence complete
**Status: IN PROGRESS**

Ready/strong:
- GMod/Toolgun/Q-menu source inventory.
- Physgun partial native evidence package.
- THUG2 staged source, board animation and HUD/input evidence.
- current product/overlay contracts.

Still required:
- Codex C01 Q-menu dependency trace.
- C02 Toolgun dispatch trace.
- C03 Physgun provenance closure.
- C04 THUG2 master state/physics.
- C05 camera.
- C06 animation/board/skeleton.
- C07 HUD/UI/scoring.
- C08 unified source input.

Exit gate: all required evidence packages reviewed with unresolved gaps explicitly classified.

## Milestone B — Assets staged
**Status: SUBSTANTIAL PREPARATION COMPLETE / NOT CLOSED**

Strong:
- 71/71 concrete GMod/HL weapon model refs staged in branch evidence.
- Toolgun source assets prepared.
- Physgun world/beam assets prepared.
- curated 290-entry prop catalog prepared.
- skateboard held/world assets and 20 animation resources recorded.
- THUG2 executable and FNV skeleton provenance recorded.

Open:
- exact Physgun first-person provenance.
- final Opus conversion/attachment/model integration.
- selective canonical reconciliation of branch-only staging manifests.
- runtime presentation validation.

## Milestone C — GMod foundation
**Status: NOT VALIDATED**

Placeholder menu exists visually but does not count.
Physgun has known runtime failures.
Real Q-menu + direct Toolgun bridge + source-faithful Physgun are still required.

## Milestone D — THUG2 foundation
**Status: PARTIAL TRANSITION ONLY**

Verified positive:
- held board presentation;
- enter skate mode;
- exit to Fallout.

Not validated:
- source-faithful movement/physics;
- camera;
- board-to-feet;
- animation;
- HUD;
- grind eligibility;
- unified controls.

## Milestone E — THUG2 full gameplay
**Status: NOT COMPLETE**

Requires complete trick/state families, combos, balance, specials, grinds/manuals/lips/walls, bail/recovery/board break, audio, HUD and animations.

## Milestone F — Cross-system stability
**Status: NOT COMPLETE**

Requires frozen Opus candidates and Codex regression across Fallout/GMod/THUG2 transitions, save/load and input ownership.

## Milestone G — Regression and polish
**Status: NOT STARTED AS FINAL GATE**

Begins only after core systems are implemented and pass their subsystem acceptance gates.

## Current critical path

C01/C02/C03 -> Opus GMod implementation -> Codex GMod runtime validation

C04/C05/C06/C07/C08 -> Opus THUG2 implementation -> Codex THUG2 runtime validation

then cross-system stability -> regression/polish.


## Quantified Opus preparation readiness

A percentage is now permitted for **Opus preparation readiness** because an explicit weighted rubric exists in `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md`.

- before the current workflow-finalization pass: **58/100**;
- after the pass: **80/100**;
- improvement: **+22 percentage points**.

This is not game-completion percentage. The principal remaining readiness deficit is Codex C01-C08 implementation-grade evidence; normal GPT cannot legitimately award those missing evidence points.


## O01 preparation milestone
O01 Toolgun presentation preflight is now complete and **READY FOR OPUS**. Required Source model companions, QC/reference geometry and all Toolgun material/texture inputs were re-hashed on the current machine and match the recorded source packets. This does not unlock Toolgun behavior; O02/O03 still wait for Codex C01/C02.


## Authenticated GMod evidence milestone
Main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0` added a validated GMod evidence bundle. Normal-GPT intake classifies C01/C02 as substantial partial and C03 as partial. The broad investigation is now reusable and should not be repeated; only the narrow gap-closure packet remains before O02/O03/O04 can unlock.
