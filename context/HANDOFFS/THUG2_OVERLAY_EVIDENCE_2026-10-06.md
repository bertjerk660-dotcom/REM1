# THUG2 overlay / free-roam evidence package — 2026-10-06

Status: preparation/evidence for external Opus 5.5. This is not runtime implementation.

## Product interpretation
Fallout: New Vegas remains the host world and default game. One normal inventory weapon — the THUG2 skateboard — is the singular gateway into a complete THUG2 free-roam gameplay layer.

Before activation, the player is playing Fallout and the board behaves as a normal inventory/equippable/drop/pickup weapon. Left-click/attack with the equipped board activates THUG2 mode. At that boundary the THUG2 gameplay stack should take ownership of player movement, camera, board, animation, trick logic, skating collision/state, skating audio and skating UI/HUD while the Fallout world remains the physical environment. The holster/exit control returns ownership to Fallout.

The intended sensation is not "Fallout with skateboard controls." It is "THUG2 has been switched on inside the Fallout world."

## Durable source/evidence already staged
The canonical readiness audit records:
- 17 decompiled THUG2 Q source files in the skate-runtime handoff.
- Original physics/controller/trick-state evidence.
- 20 parsed board SKA animation assets.
- THUG2 HUD/input handoff indexing 49 files with no missing source files.
- 22/22 HUD/input image previews available.
- Board source/converted geometry and attachment evidence staged.
These are evidence inputs, not proof of runtime parity.

## Verified current runtime facts to preserve
- The held skateboard is now visible and positioned correctly in the player's hand.
- Left-click with the skateboard equipped successfully enters skate mode.
- The configured holster key successfully exits skate mode.
- THUG2 sounds appear to work in the currently tested path, pending exhaustive state-by-state validation.

## Verified current failures
- Board does not transition from hand to feet in skate mode.
- THUG2 skating/idle/trick animation integration is not functioning.
- Grinding can be triggered by pressing G anywhere rather than by valid THUG2 grind contact/eligibility.
- THUG2 HUD/UI/popups are absent/incomplete; a simple overlay/Fallout HUD remains.
- Fallout top-left alerts still leak into the THUG2 presentation path.
- Earlier plugin/load-order testing caused the skateboard to behave like a grenade; weapon identity/type/load-order integrity is therefore a regression gate.

## Single-weapon activation contract

### State A — Fallout / board unequipped
Fallout owns movement, camera, animation, combat, HUD, input and world interaction.
The skateboard remains a normal persistent weapon/inventory object.

### State B — Fallout / board equipped
Still Fallout gameplay. The authentic board presentation is held in the player's hand.
No THUG2 physics/trick/HUD takeover occurs merely because the weapon is equipped.
The player may drop/holster/switch it using the defined Fallout inventory integration.

### Transition B -> C — left-click activation
The attack action is a mode switch, not a grenade throw or ordinary melee strike.
Transition requirements:
1. validate persistent skateboard weapon identity;
2. suppress conflicting Fallout attack/movement/camera paths;
3. switch to THUG2 third-person camera behavior;
4. move/attach the board from hand presentation to the correct feet/skater attachment;
5. bind/activate the recovered THUG2 animation/state system;
6. activate THUG2 movement/physics/controller/trick runtime;
7. suppress Fallout HUD and Fallout-owned skate-status alerts;
8. activate THUG2 HUD/UI/scoring/combo/special/balance presentation;
9. transfer relevant input ownership to THUG2;
10. start the appropriate THUG2 audio state.
The transition should read as one seamless mode change rather than a sequence of Fallout popups.

### State C — THUG2 free-roam overlay
Fallout supplies world geometry, NPC/world context and underlying host runtime. THUG2 owns the player-facing skating game.

THUG2 ownership includes:
- ground/air state;
- acceleration, momentum, friction, speed and braking;
- turning/carving;
- crouch/ollie/pop/air/landing;
- manuals and balance;
- grind detection, eligibility, snap/alignment, balance and exit;
- lips;
- wallrides/wallplants and related wall interactions;
- reverts;
- grabs, flips and specials;
- trick recognition/state and trick/combo chaining;
- score, combo, SPECIAL and balance state;
- bail/fall-off/recovery;
- board-break behavior and its animation/state recovery;
- camera position, follow, rotation, speed coupling and transitions;
- board transforms/attachment;
- animation selection, timing, blending and transitions;
- skating controls/input interpretation;
- THUG2 skating sounds and state transitions;
- THUG2 HUD/UI/popups/menus required for free-roam skating.

Fallout movement/combat animation must not continue underneath and visibly fight the THUG2 state.

### Transition C -> Fallout — holster/exit
The configured exit/holster action must:
1. safely finish/cancel current THUG2 state according to defined exit rules;
2. detach board from feet and restore the correct held/holstered representation;
3. stop THUG2-only looping audio/effects;
4. remove THUG2 HUD/UI/popups;
5. restore Fallout HUD;
6. restore Fallout camera/movement/combat/input ownership;
7. clear temporary skating state without corrupting inventory or save data.
This transition is already functionally reachable in the current build and must remain a regression gate while deeper THUG2 systems are replaced.

## Movement/gameplay evidence Opus should map
For every recovered THUG2 subsystem, produce a source/evidence -> host adaptation -> validation mapping. At minimum:
1. controller/input sampling and action mapping;
2. skater master state machine and state transitions;
3. ground contact/normal/slope handling;
4. velocity integration, acceleration, friction, drag and speed caps;
5. turning/carving/heading and board orientation;
6. crouch/ollie/pop/air trajectory and landing qualification;
7. grindable-surface detection, rail/edge acquisition, alignment and grind exit;
8. manual/lip/balance meter state and fail conditions;
9. wallride/wallplant/revert transitions;
10. flip/grab/special input recognition and trick state;
11. combo/scoring/SPECIAL lifecycle;
12. bail/fall-off/recovery and board-break lifecycle;
13. camera update/coupling;
14. animation lookup/selection/blend/transition;
15. board transform/hand-feet-break attachment state;
16. sound/event dispatch;
17. HUD/UI event/state binding.
Use extracted/decompiled THUG2 evidence first and IDA Pro 6.8 for native behavior that the available script/data does not expose sufficiently.

## Animation evidence contract
Do not treat "animation works" as a single gate. Validate source-faithful motion/state families independently:
- board equipped idle/carry;
- board-equipped walking/running where applicable;
- mount/enter skate;
- push;
- coast/ride idle;
- turn/carve;
- crouch;
- ollie/pop;
- air/fall;
- landing;
- manual;
- grind families;
- lip;
- wallride/wallplant;
- revert;
- flip tricks;
- grab tricks;
- specials;
- bail/fall-off;
- recovery/get-up;
- board break;
- exit/dismount/return to Fallout.
For each family verify correct skater pose, board transform, timing, state transition, root/motion interaction and no Fallout animation leakage.

## THUG2 UI/HUD overlay contract
During State C the Fallout HUD should be suppressed and the recovered THUG2 free-roam presentation should own skating information.
Required source-faithful surfaces include, where used by the recovered runtime:
- score;
- active trick/combo text and score accumulation;
- SPECIAL meter/state;
- balance/manual/grind/lip meters;
- trick/status popups and messages;
- bail/land/combo resolution presentation;
- any free-roam menu/pause/input surfaces needed by the selected THUG2 runtime.
Do not replace these with Fallout top-left alerts or generic text overlays.
The Fallout world remains visible behind the THUG2 presentation. This is a gameplay/UI overlay, not a THUG2 map import.

## Input ownership
- Fallout owns all ordinary controls before activation.
- Board-equipped Fallout state still uses Fallout controls except the explicit activation action.
- THUG2 owns skating movement/trick/camera controls while State C is active.
- Exit/holster remains a protected transition control.
- Pip-Boy, pause, console and other host-level menus need explicit compatibility rules so Fallout and THUG2 do not consume the same input simultaneously.
- Keyboard/mouse and Xbox mappings must resolve to the same THUG2 gameplay actions/state semantics rather than separate approximations.

## World/collision adaptation
THUG2 logic must operate against Fallout world geometry without importing THUG2 maps. Therefore Opus must define an adaptation layer between recovered THUG2 queries and Fallout collision/world data.
This layer must preserve THUG2 gameplay semantics for ground normals, slopes, ledges, rails, walls, landing surfaces and grind eligibility.
The current "press G to grind anywhere" behavior proves that input-only substitution is unacceptable.

## Camera contract
Once skating is active, use the recovered THUG2 camera behavior rather than Fallout third-person with adjusted offsets. Validate follow distance, heading/yaw behavior, pitch, smoothing, speed response, landing/air transitions and state-specific coupling against THUG2 evidence. Exiting restores Fallout camera state without a jump, stuck zoom or crash.

## Audio contract
Current sounds seem promising but require state coverage. Validate event/loop start-stop behavior for push/roll, ollie/land, grind, manual/balance where applicable, trick/bail/board-break, combo/SPECIAL/UI events and mode exit. THUG2 loops must stop cleanly when returning to Fallout.

## Save/load and persistence
The persistent skateboard WEAP remains the mode gateway. Save/load must not serialize unsafe transient THUG2 pointers/state. Define whether active skate mode is restored or normalized to Fallout on load, then test it. Preserve inventory identity and prevent the historical grenade/type regression.

## Acceptance sequence
1. Equip board in Fallout: correct held model; Fallout remains normal.
2. Left-click: one clean transition into THUG2 ownership.
3. Fallout HUD disappears; THUG2 HUD appears.
4. Board moves to feet; correct ride/push idle animation begins.
5. Push/coast/turn/brake/ollie/land feel source-faithful.
6. Perform flip + grab + manual; state, animation, scoring and UI agree.
7. Approach valid rail/edge: grind engages only when THUG2 eligibility conditions pass; arbitrary G press cannot grind empty ground/air.
8. Grind/manual balance presentation and failure/exit behavior work.
9. Wall/lip/revert states work where valid.
10. Build and resolve a combo; score/SPECIAL/UI update correctly.
11. Trigger bail/fall-off and recovery.
12. Trigger board-break behavior where the recovered game allows it; animation/state recovery works.
13. Camera behaves like THUG2 through ground/air/trick transitions.
14. THUG2 audio follows state and loops terminate correctly.
15. Holster/exit: THUG2 stack shuts down and Fallout HUD/camera/movement/input return cleanly.
16. Drop/pick up board and repeat.
17. Save/load and repeat without weapon identity/type corruption.
18. Repeat using Xbox and keyboard/mouse control profiles.

## Non-goals
- Do not import THUG2 maps, campaign missions, story, dialogue, NPC population or cutscenes.
- Do not make a generic Fallout skateboard mod and skin it with THUG2 assets.
- Do not leave Fallout HUD/alerts active as the primary skating UI.
- Do not implement tricks as isolated key-triggered animations without recovered THUG2 state/physics/eligibility logic.
- Do not treat a successful mode toggle as proof of THUG2 parity.

## Opus ownership
All implementation, reverse-engineered runtime integration, animation/rigging, physics, camera, UI hosting, audio, gameplay code and cross-game asset work described here is exclusively external Opus 5.5 work. This document is evidence/acceptance preparation only.
