# Master Project Map — 2026-10-07

Status vocabulary: NOT STARTED, INVESTIGATION IN PROGRESS, INVESTIGATION COMPLETE, READY FOR IMPLEMENTATION, IMPLEMENTATION IN PROGRESS, READY FOR RUNTIME TEST, FAILED TEST, FIX IN PROGRESS, VALIDATED, BLOCKED.

Authority: `main` is the canonical baseline; divergent branches are tracked separately in `context/BRANCH_RECONCILIATION_2026-10-07.md`.

## Fallout New Vegas host

| Subsystem | State | Evidence/current fact | Dependencies / blockers | Owner / next action | Validation / completion |
|---|---|---|---|---|---|
| runtime/plugin layer | BLOCKED | Main has a mapped active source and passing preflight, but CURRENT_STATE still records v81/v82-era deployed state while divergent branches contain v84-v92 candidates. | Branch/runtime reconciliation before promotion. | GPT-5.5 documents; Opus changes implementation; Codex validates candidates. | Exact branch/commit/source/DLL/ESP hashes + boot/playtest gates. |
| inventory integration | READY FOR RUNTIME TEST (partial) | Skateboard held presentation is human-verified; historical GMod inventory integration exists. | Representative drop/pickup/container/trade/save-load still needs current testing. | Codex runtime test packet after candidate chosen. | Identity, names/icons, drop/pickup, world models, save/load. |
| weapon activation | VALIDATED (transition only) | Skateboard LMB enter + holster exit were human-verified on 2026-10-06. | Must survive later THUG2 replacement. | Preserve as Opus regression invariant; Codex retests. | Repeated enter/exit with no crash/state leak. |
| Pip-Boy integration | IMPLEMENTATION IN PROGRESS / evidence mixed | Imported weapons are intended to behave as ordinary inventory items; branch support audits exist. | Main lacks one consolidated current test result. | GPT-5.5 prepare inventory acceptance packet; Codex validates. | Correct names/icons/drop/use/world presentation. |
| actor/NPC systems | FAILED TEST | Physgun actor grab can affect PlayerCharacter instead of target. | Correct acquired-target identity and actor handling. | Codex trace -> Opus fix -> Codex runtime test. | NPC/ragdoll target only; player never incorrectly affected. |
| world spawning | READY FOR IMPLEMENTATION | Curated prop catalogs and content adapter are prepared; current visible menu is placeholder. | Real Q-menu compatibility/renderer + spawn bridge. | Codex Q-menu trace; Opus integration. | Correct model/material/scale/collision and stable spawn. |
| camera | FAILED TEST / incomplete | Skate mode transition works, but source-faithful THUG2 camera is not established; historical camera crash knowledge exists. | THUG2 camera evidence + host-safe adapter. | Codex map; Opus integrate; Codex runtime validation. | Source-faithful follow/rotation/transitions; exit restores Fallout; zoom stable. |
| input | BLOCKED | Multiple systems need exclusive input ownership; branch-only control matrices exist. | Canonical unified matrix + original THUG2/GMod behavior mapping. | GPT-5.5 matrix; Codex evidence; Opus implementation. | No double-consumption/stuck cursor; M&K + Xbox parity. |
| HUD | FAILED TEST for skate mode | Fallout HUD/top-left alerts remain during skate mode. | THUG2 UI renderer/state binding. | Codex UI trace -> Opus -> Codex runtime validation. | Fallout HUD hidden only during THUG2; restored on exit. |
| save/load | NOT CURRENTLY VERIFIED | Historical runtime-form failures make persistence a hard gate. | Final candidate/state serialization policy. | GPT-5.5 test packet; Codex executes. | No identity corruption/crash; chosen active-mode load policy works. |
| audio | FAILED TEST / partial | THUG2 audio appears promising; Physgun held-loop audio is wrong. | Per-state event mapping. | Codex source mapping; Opus implementation; Codex runtime state coverage. | Correct loops/events/start-stop/exit cleanup. |
| physics interfaces | FAILED TEST / incomplete | Physgun range/target handling wrong; grind eligibility wrong; THUG2 free-roam physics incomplete. | Source behavior and collision adapters. | Codex investigate; Opus integrate; Codex validate. | Source-faithful behavior, stable world interaction, cleanup. |
| animation interfaces | FAILED TEST | Held board works; board-to-feet and THUG2 animation set do not. | Skeleton/retarget/attachment/state evidence. | Codex map -> Opus animation integration -> Codex visual/runtime validation. | Full state-family coverage without Fallout animation leakage. |

## Garry's Mod

| Subsystem | State | Evidence/current fact | Dependencies / blockers | Owner / next action | Completion gate |
|---|---|---|---|---|---|
| Q menu / spawn menu / prop browser | READY FOR INVESTIGATION REVIEW | 105 Lua files, 46 VGUI classes and 29/29 direct UI/material refs inventoried; current in-game menu is explicitly a placeholder. | Exact lifecycle, input/focus, content registration, search/grid and host-render bridge need evidence-grade map. | Codex next; then Opus. | Real/source-faithful menu over Fallout world; Q only; no flashing/missing icons; input restores. |
| Toolgun | READY FOR INVESTIGATION REVIEW | Real gmod_tool/stool sources and 40 stool files inventoried; Source models/assets staged. | Dispatch/lifecycle/dependency map and Q-selected mode bridge. | Codex -> Opus. | Q selection drives Toolgun; Duplicator/Remover work; no Fallout selector. |
| Physgun | INVESTIGATION COMPLETE (partial) / FAILED TEST | IDA 6.8 behavior evidence package exists; current runtime has short range, wrong loop audio and target-identity bug. | Exact first-person v_physics provenance still unresolved on main. | Codex closes provenance/native trace; Opus fixes; Codex validates. | Beam/highlight/range/hold/rotate/freeze/drop/launch/actor/audio all pass. |
| GMod notifications | NOT STARTED / evidence incomplete | Requirement defined; no canonical proof of source-faithful runtime notifications. | Notification Lua/VGUI lifecycle and assets. | Codex investigate -> Opus implement. | Correct stack/type/icon/timing/fade; no Fallout substitute alerts. |
| prop assets/catalog | READY FOR IMPLEMENTATION | Main readiness records 290 curated entries (170 FNV + 120 GMod/Source), thumbnails audited. | Runtime Q/spawn bridge and per-prop collision/scale validation. | Opus integrates; Codex tests samples. | Fast usable catalog, correct icons, spawn/collision/scale. |
| weapon/model assets | READY FOR IMPLEMENTATION with gap | Toolgun packages staged; w_physics staged; broader weapon mappings prepared. | Physgun exact view-model provenance; final FNV attachment/scale. | Codex provenance -> Opus model integration. | First-person, third-person, world/drop models all correct. |
| sounds | READY FOR IMPLEMENTATION / partial | Toolgun/Physgun events inventoried; Physgun hold loop currently wrong. | State/event binding. | Codex confirm events; Opus wire; Codex validate. | Correct event/loop semantics. |
| controller adaptation | BLOCKED | Required by product; not canonically runtime-validated. | Unified mode/input matrix. | GPT-5.5 + Codex evidence -> Opus -> Codex runtime validation. | Xbox/M&K mapped without conflicts. |

## THUG2

| Subsystem | State | Evidence/current fact | Dependencies / blockers | Owner / next action | Completion gate |
|---|---|---|---|---|---|
| skateboard weapon | VALIDATED (held state only) | Authentic board is visible/correctly positioned in hand; normal weapon gateway concept established. | Must preserve identity through later work. | Opus preserve; Codex regression. | Equip/drop/pickup/save-load; no grenade/type regression. |
| skate-mode activation / exit | VALIDATED (transition only) | LMB enters; holster exits. | Full subsystem takeover/cleanup not yet complete. | Opus preserve and extend; Codex regression. | Clean repeated transitions with all ownership restored. |
| movement / physics / state machine | BLOCKED | Existing behavior is not accepted as complete THUG2 free roam. | Complete source state-machine/collision/physics map. | Codex investigation -> Opus. | Push/coast/turn/brake/ollie/air/land/etc source-faithful. |
| tricks / combos / specials | BLOCKED | Product scope requires full reachable free-roam trick state. | Source trick recognition/state/scoring mapping. | Codex investigation -> Opus -> Codex runtime validation. | Trick families, chaining, scoring/SPECIAL lifecycle correct. |
| grinding / manuals / lips / wall interactions | FAILED TEST / BLOCKED | Grind can currently trigger anywhere. | THUG2 geometry/contact/eligibility/balance evidence. | Codex trace -> Opus fix -> Astra. | Only valid surfaces/states; correct balance/exit/fail behavior. |
| bail / recovery / board break | NOT STARTED in canonical validated runtime | Required by product/animation catalog. | State/animation/audio evidence. | Codex investigation -> Opus -> Codex runtime validation. | Correct triggers, animations, recovery and board state. |
| walking / board carry | PARTIAL | Held/carry board works in Fallout state; THUG2 walk mode behavior not verified. | THUG2 walking/state transition evidence. | Codex -> Opus. | Correct board carry/walk/mount/dismount flow. |
| skate camera | BLOCKED | Must use recovered THUG2 behavior, not Fallout offset imitation. | Camera function/state map. | Codex investigation -> Opus -> Codex runtime validation. | THUG2-like follow/yaw/pitch/smoothing/state coupling. |
| HUD / menus / popups | FAILED TEST | Simple/Fallout presentation remains; THUG2 HUD absent/incomplete. | UI assets + renderer + gameplay event binding. | Codex investigation -> Opus -> Codex runtime validation. | Score/combo/trick/SPECIAL/balance/popups work; Fallout HUD suppressed. |
| sound system | READY FOR DEEP VALIDATION | Current playtest says THUG2 sounds seem to work. | Exhaustive state/event coverage. | GPT-5.5 creates matrix; Codex validates after Opus candidate. | Correct state-by-state events and loop cleanup. |
| animation states | FAILED TEST | Current THUG2 animation set not functioning; branch-only later evidence exists. | Full source animation IDs, skeleton mapping, retarget/attachment contract. | Codex investigation -> Opus -> Codex runtime validation. | Catalogue below passes visually/runtime. |
| board attachment | FAILED TEST | Board stays in hand instead of moving to feet in skate mode. | Attachment/skeleton/state transitions. | Codex evidence -> Opus. | Hand -> feet -> break/recovery -> hand/holster transitions correct. |
| controller mappings | BLOCKED | Required unified Xbox/M&K behavior. | Original control semantics + host conflict matrix. | Codex + GPT-5.5 -> Opus -> Codex runtime validation. | Same gameplay actions/state semantics across devices. |

## THUG2 animation catalogue

Required families: skating idle, push, coast, turning/carving, crouch, ollie, air/fall, landing, flip tricks, grabs, manuals, grind entry/loop/exit, wallrides/wallplants, lip tricks, specials, bail/fall-off, recovery/get-up, walking/running with board, board pickup/carry, mounting, dismounting, board break, board recovery.

Current canonical status: **held-board presentation verified; remaining source-faithful animation integration is not validated**.

## Critical path

1. Reconcile investigation evidence without promoting divergent runtime branches.
2. Codex closes GMod Q-menu/Toolgun/Physgun evidence gaps.
3. Opus completes GMod foundation in isolated candidates.
4. Codex validates GMod candidates and regressions.
5. Codex completes THUG2 free-roam state/camera/animation/UI/input maps.
6. Opus integrates the THUG2 stack.
7. Codex validates deterministic state-family and transition tests.
8. Cross-system save/load/input/HUD/camera regression.
9. Promotion only after acceptance gates and human playability pass.

## Milestones

- A — Evidence complete: NOT COMPLETE.
- B — Assets staged: SUBSTANTIAL PREPARATION COMPLETE, but provenance/validation gaps remain.
- C — GMod foundation: NOT VALIDATED.
- D — THUG2 foundation: transition partially validated; gameplay foundation NOT VALIDATED.
- E — THUG2 full gameplay: NOT COMPLETE.
- F — Cross-system stability: NOT COMPLETE.
- G — Regression/polish: NOT STARTED as a final-release gate.
