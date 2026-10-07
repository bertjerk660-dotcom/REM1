# Opus packet — THUG2 skate camera

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C05.**

Implement the source-grounded THUG2 camera through the host-safe adapter defined by C05. Do not imitate it with arbitrary Fallout offsets and do not revive direct unsafe playerNode/camera transform assumptions.

Acceptance: source-faithful follow/yaw/pitch/distance/smoothing/speed/air/landing/state coupling; no clipping regression beyond defined source/host behavior; repeated entry/exit restores Fallout camera; zoom/transition stable. Codex runs R04/R05 plus camera regressions.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.