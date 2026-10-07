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
