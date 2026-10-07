# O03 Preassembled Opus Packet — Q-selected Toolgun + Remover/Duplicator

**Status: WAITING FOR CODEX GAP CLOSURE**

Evidence already available:
- main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`;
- `context/GMOD_2026-10-07/TOOLGUN_ARCHITECTURE.md`;
- dependency/provenance/native manifests;
- O01 Toolgun presentation packet is independently READY FOR OPUS.

Already established for Opus:
- string-mode tool registry/selection;
- Q selection → Toolgun state contract;
- LeftClick/RightClick/Reload dispatch model;
- Remover semantics;
- Duplicator graph-copy/paste semantics;
- undo/cleanup ownership;
- entity/trace/constraint host boundaries;
- current hover-index/R-selector paths are temporary and must be removed from final behavior.

Still blocking final packet:
- trace range/native binding;
- prediction/realm semantics;
- ToolTracer/RenderScreen/audio closure;
- Duplicator supported host constraint representation;
- final supported-stool dependency closure.

Do not implement until C01 + C02 are reviewed COMPLETE.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.