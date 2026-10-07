# Opus packet — cross-system state transitions and fixes

**Implementer: Claude Opus only.**
**Readiness: NOT READY until subsystem candidates exist and Codex has runtime evidence.**

This packet is for integration fixes after Q/Toolgun/Physgun/THUG2 subsystem candidates exist. It must consume Codex failure reports rather than guessing.

Required transition sequence: Fallout baseline -> Q -> Toolgun -> Physgun -> Fallout -> skateboard -> THUG2 -> Fallout -> save/load -> repeat.

Success requires no HUD/camera/input/audio/animation ownership leakage, no inventory identity corruption, no crash, and all applicable acceptance/save-load/regression gates. Codex runs R09 and targeted failing tests after every Opus fix.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.