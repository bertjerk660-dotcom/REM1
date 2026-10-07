# Opus packet — unified input layer

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C01/C02/C03/C04/C08.**

Implement one explicit mode-owned action layer for NORMAL_FALLOUT, GMOD_MENU, GMOD_TOOL_ACTIVE, THUG2_SKATE_MODE and THUG2_WALK_MODE if C04 confirms it.

Use INPUT_OWNERSHIP_MATRIX as host policy and C08 as source evidence. Keyboard/mouse and Xbox must express the same gameplay actions/state semantics.

Acceptance: no double consumption, no stuck cursor/focus, Q cleanly captures/restores, Toolgun/Physgun semantics source-faithful, THUG2 controls source-faithful, protected skate exit, deterministic Pip-Boy/pause/console compatibility. Codex runs R08/R09.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.