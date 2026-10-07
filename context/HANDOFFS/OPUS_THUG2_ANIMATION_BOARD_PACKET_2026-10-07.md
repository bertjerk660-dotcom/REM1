# Opus packet — THUG2 animation, skeleton and board attachment

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C06.**

## Objective
Integrate the complete source animation catalogue and board attachment transitions onto the Fallout player rig without changing intended THUG2 motion/timing.

## Required evidence
C06 animation catalogue/state binding/skeleton-bone contract/board attachment state machine/retarget contract plus current source hashes.

## Safety invariants
No stale bone pointer caches across 3D/root rebuilds. Preserve root/type validation. Do not regress held-board presentation.

## Acceptance
All catalogue families pass selection, timing, blend and visual checks; board hand -> feet -> trick/bail/break/recovery -> exit states are correct; no Fallout animation leakage or retarget crash. Codex runs R07 plus repeated mode transitions.
