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

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.