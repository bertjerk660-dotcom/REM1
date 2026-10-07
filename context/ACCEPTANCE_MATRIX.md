# Acceptance Matrix — 2026-10-07

Rule: compile/deploy is never completion. Final completion requires source/evidence confidence, Opus implementation, and Astra runtime validation where applicable.

| Feature | Evidence gate | Opus implementation gate | Astra runtime gate | Completion state today |
|---|---|---|---|---|
| Q menu | Codex traces lifecycle, VGUI/Derma, content registration, search, input/focus, tool-state bridge | real/source-faithful menu hosted in FNV; placeholder disabled | Q opens/closes repeatedly; no flashing; icons/search/categories work; input restores | NOT COMPLETE |
| Toolgun | Codex maps gmod_tool/stool dispatch, Duplicator/Remover, trace/actions | Q-selected tool directly drives Toolgun; source assets/effects/sounds | select tools in Q; use them; no Fallout selector; save/load/tool-state regression | NOT COMPLETE |
| Physgun | Codex closes view-model provenance + native semantics | correct model/beam/highlight/range/hold/rotate/freeze/drop/launch/actor/audio | deterministic prop + actor tests, cleanup, save/load, repeated use | FAILED / INCOMPLETE |
| GMod notifications | Codex maps notification creation/type/icon/stack/fade dependencies | original-style notification path used for GMod-owned feedback | correct visuals/timing; no Fallout top-left substitution | NOT COMPLETE |
| curated props | provenance/catalog/collision/thumbnail evidence complete per entry/sample | integrated into real Q content adapter | spawn category samples; verify model/material/scale/collision/stability | READY FOR IMPLEMENTATION / TESTING DEPENDS ON Q |
| skateboard held item | source asset + persistent WEAP identity documented | preserve current correct held model and inventory semantics | equip/drop/pickup/save-load; no grenade/type regression | PARTIALLY VALIDATED |
| skate entry/exit | source/host transition rules documented | transition activates/deactivates full THUG2 stack while preserving Fallout | repeat entry/exit; HUD/camera/input/audio restore; no crash | TRANSITION ONLY VALIDATED |
| THUG2 movement | Codex complete movement/physics/state map | source-faithful movement adapter against Fallout world | push/coast/turn/brake/ollie/air/land across varied surfaces | BLOCKED ON EVIDENCE |
| grind/manual/lip/wall | Codex eligibility/state/balance/collision map | implement source rules and meters/state transitions | invalid surface reject; valid rail/manual/lip/wall tests; fail/exit rules | FAILED / BLOCKED |
| tricks/combos/SPECIAL | Codex trick recognition/state/scoring map | source-faithful trick/combo/scoring runtime | flip/grab/manual/grind chain, multiplier, score, SPECIAL lifecycle | BLOCKED |
| THUG2 camera | Codex camera function/state/coupling map | source camera behavior via host-safe adapter | yaw/pitch/follow/smoothing/speed/air/landing; clean exit; zoom stable | BLOCKED |
| THUG2 animations | Codex IDs/state/selection/blend/skeleton map | Opus retarget/attachment integration for all required families | visual/runtime pass for every animation family | FAILED / BLOCKED |
| board attachment | Codex hand/feet/break/recovery attachment map | state-correct board transforms/attachments | hand->feet->break/recovery->exit transitions | FAILED |
| THUG2 HUD/UI | Codex renderer/assets/event-binding/scaling map | score/combo/SPECIAL/balance/popups/menu implementation; Fallout HUD suppression | all UI surfaces update correctly; no Fallout alerts; clean restore | FAILED |
| THUG2 audio | Codex maps state/event loops where needed | correct assets and event/loop bindings | state-by-state start/stop; mode-exit cleanup | PARTIAL |
| unified input | Codex original control semantics + workflow conflict matrix | single mode-owner implementation for M&K and Xbox | no double input/stuck focus; semantic parity across devices | BLOCKED |
| save/load | serialization/persistence policy documented | no unsafe transient pointers/forms; stable state cleanup/restore | save/load in baseline, GMod, before/after THUG2; inventory identity intact | NOT CURRENTLY VERIFIED |
| cross-system stability | all subsystem evidence complete | all isolated candidates integrated without ownership leaks | full regression suite + human playability | NOT STARTED FINAL GATE |

## Global pass rules

A feature cannot be marked VALIDATED unless:
1. required original-game evidence is in the repository;
2. Opus implementation is tied to a traceable branch/commit/build;
3. build/assets/references pass;
4. feature is reachable;
5. behavior matches acceptance criteria;
6. cleanup/exit behavior passes;
7. save/load passes if state persists;
8. regression tests pass;
9. Astra or required human runtime validation has been recorded;
10. no critical unresolved failure entry contradicts completion.
