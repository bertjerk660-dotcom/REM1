# Codex Runtime Test Packs — 2026-10-07

Run only against an identified Opus candidate. Use `CODEX_RUNTIME_VALIDATION_TEMPLATE_2026-10-07.md` for evidence capture.

## R01 Fallout baseline
- Boot game.
- Load known-good disposable save.
- Move/look/attack/interact.
- Open/close Pip-Boy.
- Change normal equipment.
- Save, return to menu, reload.
Pass: no crash, no imported-mode leakage, save/load works.

## R02 GMod Q / Toolgun
- Open Q repeatedly.
- Browse categories; search; scroll; select props/tools.
- Confirm no flashing/missing icons/stuck cursor.
- Select Remover; close Q; use Toolgun.
- Select Duplicator; close Q; use Toolgun.
- Open/close Pip-Boy before and after.
Pass: selected tool state persists correctly; no Fallout selector; input restores.

## R03 Physgun
- Acquire near and far valid props to establish range.
- Hold/move target; adjust distance; rotate.
- Freeze/unfreeze/reacquire.
- Release normally.
- Launch/punt.
- Acquire actor/NPC and verify only target receives intended actor effect.
- Verify beam/highlight and held-loop audio start/stop.
- Weapon switch/cell transition/save-load cleanup.
Pass: all source/project semantics correct; no player-target confusion.

## R04 THUG2 entry/exit
- Equip board in Fallout.
- Verify held presentation.
- Activate once.
- Confirm Fallout HUD suppression, THUG2 ownership and board-to-feet transition.
- Exit.
- Repeat three times.
Pass: exact state cleanup/restoration, no crash or residual HUD/camera/input/audio.

## R05 THUG2 movement/camera
- Push/coast.
- Turn/carve/brake.
- Crouch/ollie/air/land.
- Use slopes and varied terrain.
- Observe camera through speed/air/landing transitions.
Pass: source-faithful state behavior and camera coupling; no Fallout movement/camera leakage.

## R06 THUG2 trick/state systems
- flip;
- grab;
- manual;
- valid grind;
- invalid grind attempt;
- lip;
- wallride/wallplant;
- revert;
- combo chain;
- SPECIAL;
- bail/recovery;
- board break/recovery where applicable.
Pass: eligibility, animation, scoring, HUD, audio and state transitions agree.

## R07 Animation/board matrix
Check every catalogue family:
idle, push, coast, turn, crouch, ollie, air, land, flips, grabs, manual, grind entry/loop/exit, wall, lip, revert, special, bail, recovery, walk/carry, pickup, mount, dismount, break, recovery.
Pass: correct pose/timing/blend/board attachment and no Fallout animation leakage.

## R08 Keyboard/mouse and Xbox
Repeat representative GMod and THUG2 paths under each input profile.
Pass: same gameplay-action semantics, no stuck input/focus, no double consumption.

## R09 Cross-system/save-load
Sequence:
Fallout -> Q -> Toolgun -> Physgun -> Fallout -> skateboard -> THUG2 -> Fallout -> save -> reload -> repeat.
Pass: no ownership leakage, inventory identity corruption, crash or persistence failure.
