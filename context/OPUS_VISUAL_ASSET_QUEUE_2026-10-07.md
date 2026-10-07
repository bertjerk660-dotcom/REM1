# Current Opus Visual / Asset Queue — 2026-10-07

This supersedes the execution meaning of older `GPT6_OPUS`/Astra visual queues while preserving their historical evidence.

## Order

| Order | Package | State | Why |
|---:|---|---|---|
| 1 | O00 Golden Source bench | READY FOR OPUS | prove Source→FNV geometry/material/collision pipeline |
| 2 | O01 Toolgun presentation | READY AFTER O00 PASS | complete source/model/material packet; behavior excluded |
| 3 | O08a Crowbar presentation | READY AFTER O00 PASS | first/world models directly archive-verified; behavior excluded |
| 4 | O08b Pistol presentation | READY AFTER O00 PASS | c/w models and full VMT/VTF closure archive-verified; behavior excluded |
| 5 | O08c SMG1 presentation | READY AFTER O00 PASS | c/w models archive-verified; material closure repaired with exact original specular mask |
| 6 | O04 Physgun visual/parity | BLOCKED | first-person `v_physics` provenance and C03 native behavior gaps remain |
| 7 | THUG2 board/animation visual integration | WAITING FOR C06 | attachment/skeleton/animation behavior must be evidence-backed |
| 8 | THUG2 prop visual wave | REVIEW/PACKAGE-SPECIFIC | 20 reviewed candidates remain unpromoted; use only after O00 pipeline proof and per-prop visual/collision evidence |

## Rules

- O00 is a pipeline gate, not optional polish.
- Weapon visual packages may proceed after O00 only when their source provenance is complete.
- Visual readiness never authorizes gameplay mechanics.
- Do not use `c_superphyscannon` as proof/substitute for missing declared `v_physics`.
- Do not retarget THUG2 animation/board attachment without C06.
- Do not batch-promote THUG2 props merely because conversion candidates exist.
- Every Opus candidate uses `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`.
- Codex validates the frozen candidate after Opus implementation.


## Current unified source validation
`build/validation/opus_visual_source_validation_20261007.json`:
- O00 PASS;
- O01 PASS;
- O08a PASS;
- O08b PASS;
- O08c PASS;
- 87 files checked;
- 0 errors.

Re-run `research/validate_opus_visual_source_packets.py` before Opus starts or after any staging change.
