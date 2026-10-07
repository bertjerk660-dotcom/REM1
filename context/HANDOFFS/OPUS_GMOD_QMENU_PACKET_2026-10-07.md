# Opus packet — GMod Q menu

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C01.**

## Objective
Replace the temporary Fallout-authored/placeholder menu path with a source-faithful GMod Q/spawn-menu compatibility and rendering integration over the Fallout world.

## Required evidence before start
- context/CODEX/GMOD_QMENU_C01_EVIDENCE_2026-10-07.md
- build/evidence/gmod_qmenu_c01/function_map.json
- dependency_manifest.json
- ui_state_machine.json
- opus_interface_contract.json
- installed GMod provenance from PROVENANCE_INDEX.md

If C01 does not exist and pass review, do not claim this packet READY.

## Preserve
- Fallout remains host/world.
- curated content adapter remains data input, not replacement UI.
- Q is the intended menu control.
- Tool selection must flow into real Toolgun state.

## Replace/remove
- placeholder menu as final path;
- Fallout prompt/tool selectors;
- any duplicated E-open behavior;
- Fallout notification substitutes for GMod-owned feedback.

## Implementation boundaries
Opus owns renderer/compatibility code, UI hosting, final asset integration and host adapters. Do not alter original GMod behavior without documenting the unavoidable host-boundary adaptation.

## Acceptance
Use ACCEPTANCE_MATRIX Q-menu row plus Codex R02. Candidate must be frozen by branch/commit/DLL/ESP/assets before Codex validation.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.