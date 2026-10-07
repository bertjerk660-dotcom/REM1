# Acceptance Matrix — 2026-10-07

Rule: compile/deploy is never completion. Final completion requires source/evidence confidence, Opus implementation, and Codex runtime validation where applicable.

| Feature | Codex evidence gate | Opus implementation gate | Codex runtime gate | Completion state today |
|---|---|---|---|---|
| Q menu | trace lifecycle, VGUI/Derma, content registration, search, input/focus, tool-state bridge | real/source-faithful menu hosted in FNV; placeholder disabled | repeated open/close; no flashing; icons/search/categories; input restore | NOT COMPLETE |
| Toolgun | map gmod_tool/stool dispatch, Duplicator/Remover, trace/actions | Q-selected tool directly drives Toolgun; source assets/effects/sounds | select/use tools; no Fallout selector; save/load/tool-state regression | NOT COMPLETE |
| Physgun | close view-model provenance + native semantics | correct model/beam/highlight/range/hold/rotate/freeze/drop/launch/actor/audio | deterministic prop + actor tests, cleanup, save/load, repeated use | FAILED / INCOMPLETE |
| GMod notifications | map notification creation/type/icon/stack/fade dependencies | source-faithful notification path for GMod feedback | correct visuals/timing; no Fallout top-left substitute | NOT COMPLETE |
| curated props | provenance/catalog/collision/thumbnail evidence | integrated into real Q content adapter | category sample spawn; model/material/scale/collision/stability | READY FOR IMPLEMENTATION / Q DEPENDENCY |
| skateboard held item | source asset + persistent WEAP identity | preserve correct held model/inventory semantics | equip/drop/pickup/save-load; no grenade/type regression | PARTIALLY VALIDATED |
| skate entry/exit | source/host transition rules | activates/deactivates full THUG2 stack while preserving Fallout | repeat transitions; HUD/camera/input/audio restore; no crash | TRANSITION ONLY VALIDATED |
| THUG2 movement | complete movement/physics/state map | source-faithful movement adapter | push/coast/turn/brake/ollie/air/land across surfaces | BLOCKED ON EVIDENCE |
| grind/manual/lip/wall | eligibility/state/balance/collision map | source rules/meters/transitions | invalid reject; valid rail/manual/lip/wall; fail/exit | FAILED / BLOCKED |
| tricks/combos/SPECIAL | trick recognition/state/scoring map | source-faithful trick/combo/scoring runtime | flip/grab/manual/grind chain, multiplier, score, SPECIAL | BLOCKED |
| THUG2 camera | camera function/state/coupling map | source camera via host-safe adapter | yaw/pitch/follow/smoothing/speed/air/landing; exit; zoom stable | BLOCKED |
| THUG2 animations | IDs/state/selection/blend/skeleton map | Opus retarget/attachment for all required families | visual/runtime pass for every animation family | FAILED / BLOCKED |
| board attachment | hand/feet/break/recovery map | state-correct transforms/attachments | hand->feet->break/recovery->exit | FAILED |
| THUG2 HUD/UI | renderer/assets/event/scaling map | score/combo/SPECIAL/balance/popups; Fallout HUD suppression | all surfaces update; no Fallout alerts; clean restore | FAILED |
| THUG2 audio | state/event/loop map | correct asset/event/loop bindings | state-by-state start/stop and mode-exit cleanup | PARTIAL |
| unified input | original control semantics + conflict matrix | single mode-owner implementation for M&K/Xbox | no double input/stuck focus; semantic parity | BLOCKED |
| save/load | serialization/persistence policy | no unsafe transient pointers/forms; stable cleanup/restore | baseline/GMod/before-after THUG2; inventory identity intact | NOT CURRENTLY VERIFIED |
| cross-system stability | all subsystem evidence complete | isolated candidates integrated without ownership leaks | full regression suite + human playability | NOT STARTED FINAL GATE |

## Global pass rules

A feature cannot be marked VALIDATED unless:
1. required original-game evidence is in the repository;
2. Opus implementation is tied to a traceable branch/commit/build;
3. build/assets/references pass;
4. feature is reachable;
5. behavior matches acceptance criteria;
6. cleanup/exit passes;
7. save/load passes if applicable;
8. regression tests pass;
9. Codex runtime validation and any required human playability evidence are recorded;
10. no critical unresolved failure entry contradicts completion.
