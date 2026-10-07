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

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.