# O02 Preassembled Opus Packet — Real GMod Q-menu renderer/compatibility

**Status: WAITING FOR CODEX GAP CLOSURE**

Evidence already available:
- main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`;
- `context/GMOD_2026-10-07/QMENU_ARCHITECTURE.md`;
- `INTEGRATION_BOUNDARY.md`;
- `COMPATIBILITY_MATRIX.md`;
- qmenu/dependency/native manifests.

Already established for Opus:
- persistent original menu lifecycle;
- panel hierarchy and layout;
- content/search/tool browser structure;
- SpawnIcon click path;
- original input/focus/HangOpen rules;
- original tool-click selection semantics;
- explicit FNV bridge responsibilities;
- current placeholder behaviors that must be replaced.

Still blocking final packet:
- native opener dispatch;
- ModelImage/icon native service;
- spawnlist/search/editor closure;
- exact remaining native interface contract.

When those close, convert this shell to READY FOR OPUS and attach the final C01 commit.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.