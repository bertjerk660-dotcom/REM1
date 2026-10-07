# THUG2 Codex → Opus Packet Assembly Matrix — 2026-10-07

Purpose: define exactly how reviewed Codex evidence will be assembled into Claude Opus implementation packets without asking Opus to rediscover source behavior.

This is a coordination matrix only. It does not implement THUG2.

| Opus package | Codex gate(s) | Exact evidence slots | Known failures/preservation | Runtime validation |
|---|---|---|---|---|
| O05 core skate state/movement/physics | C04 + C08 | C04 master_state_machine, movement_physics_map, collision_query_contract, grind_manual_lip_eligibility, opus_world_adapter_contract + C08 source/input/conflict/adapter maps | preserve persistent board identity, held-board presentation, LMB entry, holster exit, normal Fallout outside skate mode; fix F010 only through source eligibility semantics | R04, R05, R06, R08, R09 |
| O05b camera | C05 | camera_function_map, camera_state_map, state_coupling_matrix, opus_camera_adapter_contract | avoid F002 unsafe player node access, F005 transition crash history and any raw stale camera-pointer path | R04, R05, R09 |
| O06 animation / skeleton / board | C06 + C04 state vocabulary | animation_catalog, animation_state_binding, skeleton_bone_contract, board_attachment_state_machine, opus_retarget_contract | preserve F004 held board; prevent F003 stale bone caching and F011 board-to-feet/animation failure | R04, R06, R07, R09 |
| O07 HUD/UI/scoring | C07 + C04 gameplay events | hud_surface_manifest, gameplay_event_binding, ui_asset_font_manifest, scaling_layout_contract, opus_ui_adapter_contract | replace F008 fallback text/Fallout top-left alerts; suppress Fallout HUD only during THUG2 ownership and restore on exit | R04, R06, R09 |
| O07b audio | reviewed C04/C06/C07 audio event evidence or narrow addendum | event→sound map, source provenance, one-shot/loop rules, stop/interrupt ownership, mode-exit cleanup | preserve only audio whose original identity is proven; no stuck loops or Fallout substitutes | R04, R05, R06, R09 |
| unified mode-owned input layer | C01+C02+C03+C04+C08 | GMod menu/tool/physgun source input semantics + THUG2 source action maps + conflict matrix + Opus adapter contract | one owner per conflicting input; protected skate exit; no Q/Pip-Boy cursor conflict; no double consumption | R02, R03, R04, R08, R09 |

## Assembly rule

A packet changes from WAITING/PREASSEMBLED to READY FOR OPUS only when:
1. every required Codex gate is reviewed COMPLETE;
2. exact evidence paths and commit SHA are inserted;
3. direct evidence vs inference is classified;
4. relevant failure-knowledge entries are attached;
5. preserved-working behavior is explicit;
6. implementation boundary is explicit;
7. post-implementation Codex runtime pack is linked;
8. candidate manifest template is attached.

## C04 handoff into later investigations

When C04 completes, normal GPT must extract and freeze a shared source vocabulary containing:
- original state IDs/names;
- state transitions;
- speed/heading/board orientation variables;
- air/ground/landing flags;
- grind/manual/lip states;
- collision-query result names;
- gameplay events exposed to animation/camera/HUD/audio/input.

C05/C06/C07 must use that vocabulary rather than creating parallel guessed names.

## No-crossing rule

Codex evidence outputs may describe what an adapter must do.
They must not contain the final Fallout implementation.

Opus packets may consume reviewed evidence.
They must not treat unresolved Codex fields as permission to approximate original THUG2 behavior.
