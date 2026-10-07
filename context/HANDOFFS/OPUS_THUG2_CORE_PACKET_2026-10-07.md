# Opus packet — THUG2 core movement/state/physics

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C04 + C08.**

## Objective
Replace incomplete/approximate skate behavior with source-faithful THUG2 free-roam movement/state/physics operating against the Fallout world.

## Preserve
- persistent ESP-owned skateboard identity;
- verified held-board presentation;
- verified deliberate enter and exit gateway;
- normal Fallout outside skate mode.

## Required evidence
C04 master state machine, movement/physics map, collision contract, grind/manual/lip eligibility and world-adapter contract; C08 source action/conflict maps.

## Known failure
Current grind can trigger without valid geometry/contact.

## Acceptance
Push/coast/turn/brake/crouch/ollie/air/land, slopes, manuals, valid-only grind, lips/walls/revert, bail/recovery/board break where source behavior requires, no Fallout movement leakage. Codex runs R04-R06 and R08.
