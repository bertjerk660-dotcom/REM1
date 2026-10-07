# Opus packet — THUG2 HUD/UI/scoring

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C07 and required C04 gameplay-event outputs.**

Implement source-faithful THUG2 score/trick/combo/multiplier/SPECIAL/balance/popups and required free-roam menu/HUD lifecycle using original assets and renderer behavior adapted only at the Fallout host boundary.

Remove the simple/fallback skate overlay and suppress Fallout HUD/top-left skate feedback while THUG2 owns gameplay. Restore Fallout HUD exactly on exit.

Acceptance follows ACCEPTANCE_MATRIX and Codex R04/R06/R09.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.