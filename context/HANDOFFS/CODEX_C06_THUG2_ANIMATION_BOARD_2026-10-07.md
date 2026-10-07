# Codex C06 — THUG2 animation, skeleton and board-attachment investigation

## Objective
Produce a complete source-evidence map for THUG2 free-roam animation selection, blending, skeleton requirements and skateboard attachment so **Claude Opus** can perform the actual retargeting/integration. After implementation, **Codex** validates it in runtime.

Codex must not retarget or implement final animations.

## Required animation catalogue
Investigate:
- skating idle;
- push;
- coast;
- turn/carve;
- crouch;
- ollie/pop;
- air/fall;
- landing;
- flip tricks;
- grabs;
- manuals;
- grind entry/loop/exit;
- wallrides/wallplants;
- lip tricks;
- reverts;
- specials;
- bail/fall-off;
- recovery/get-up;
- walking/running with board;
- board pickup/carry;
- mount;
- dismount;
- board break;
- board recovery.

## For every family determine
- original resource/file identifiers;
- lookup tables/checksums/IDs;
- state trigger;
- variant selection;
- duration/timing;
- blend/cancel windows;
- looping rules;
- root-motion assumptions;
- required skeleton/bones;
- board transform/attachment;
- hand/feet/break/recovery transitions;
- event/audio hooks;
- camera/scoring dependencies.

Inspect staged board SKA assets and branch-only later evidence only as candidate evidence; divergent branches are not canonical validation.

## Required outputs
- context/CODEX/THUG2_C06_ANIMATION_BOARD_EVIDENCE_2026-10-07.md
- build/evidence/thug2_c06/animation_catalog.json
- build/evidence/thug2_c06/animation_state_binding.json
- build/evidence/thug2_c06/skeleton_bone_contract.json
- build/evidence/thug2_c06/board_attachment_state_machine.json
- build/evidence/thug2_c06/opus_retarget_contract.json

## Stop condition
Stop when Opus has an implementation-grade catalogue and attachment/skeleton contract for every required animation family.

No final retargeting or board implementation in Codex.
