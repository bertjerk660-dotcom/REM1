# Codex Runtime Test Packs — 2026-10-07

Run only against an identified Opus candidate. Use `CODEX_RUNTIME_VALIDATION_TEMPLATE_2026-10-07.md` for evidence capture.

## Mandatory header for every executed pack

Before step 1, Codex records:
- exact candidate branch;
- commit SHA;
- parent/baseline commit;
- build/version label;
- active source hash;
- DLL SHA256;
- ESP SHA256;
- asset-manifest hash/version;
- enabled plugin/load-order subset relevant to the test;
- exact disposable/known-good save identifier;
- exact test location/cell;
- starting inventory/equipment;
- starting gameplay mode/state;
- keyboard/mouse or Xbox profile;
- relevant known-failure IDs from `FAILURE_LEDGER.md`.

If any identity field that should exist is unknown, mark it UNKNOWN and do not promote the result to VALIDATED until resolved.

For each pack capture:
- observed result at every meaningful checkpoint;
- plugin/runtime logs;
- Windows crash/application evidence when a crash occurs;
- screenshots for visible UI/model/HUD/beam/highlight/attachment assertions;
- video for timing, camera, animation, movement, transition and intermittent behavior where a still image cannot prove the result;
- exact first failing step and minimal reproduction on failure;
- cleanup/restoration result;
- neighboring regressions rerun after any fix.

A PASS is valid only for the exact recorded candidate identity. A later commit or changed DLL/ESP/asset manifest requires a new result or an explicitly justified unaffected-test determination.

## R01 Fallout baseline
- Boot game.
- Load known-good disposable save.
- Move/look/attack/interact.
- Open/close Pip-Boy.
- Change normal equipment.
- Save, return to menu, reload.
Pass: no crash, no imported-mode leakage, save/load works. Evidence: boot/load/save/reload log checkpoints; screenshot of loaded baseline state; crash/application logs if abnormal.

## R02 GMod Q / Toolgun
- Open Q repeatedly.
- Browse categories; search; scroll; select props/tools.
- Confirm no flashing/missing icons/stuck cursor.
- Select Remover; close Q; use Toolgun.
- Select Duplicator; close Q; use Toolgun.
- Open/close Pip-Boy before and after.
Pass: selected tool state persists correctly; no Fallout selector; input restores. Evidence: video of open/browse/search/select/close/use/reopen; screenshots proving icons/categories; logs for spawn/tool actions and cleanup.

## R03 Physgun
- Acquire near and far valid props to establish range.
- Hold/move target; adjust distance; rotate.
- Freeze/unfreeze/reacquire.
- Release normally.
- Launch/punt.
- Acquire actor/NPC and verify only target receives intended actor effect.
- Verify beam/highlight and held-loop audio start/stop.
- Weapon switch/cell transition/save-load cleanup.
Pass: all source/project semantics correct; no player-target confusion. Evidence: video for acquire/range/hold/rotate/freeze/release/punt; screenshots for beam/highlight; logs identifying acquired target and audio state.

## R04 THUG2 entry/exit
- Equip board in Fallout.
- Verify held presentation.
- Activate once.
- Confirm Fallout HUD suppression, THUG2 ownership and board-to-feet transition.
- Exit.
- Repeat three times.
Pass: exact state cleanup/restoration, no crash or residual HUD/camera/input/audio. Evidence: continuous video of three transitions plus before/during/after HUD/board screenshots and transition logs.

## R05 THUG2 movement/camera
- Push/coast.
- Turn/carve/brake.
- Crouch/ollie/air/land.
- Use slopes and varied terrain.
- Observe camera through speed/air/landing transitions.
Pass: source-faithful state behavior and camera coupling; no Fallout movement/camera leakage. Evidence: continuous video on defined terrain route; logs/state trace where available.

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
Pass: eligibility, animation, scoring, HUD, audio and state transitions agree with the reviewed Codex source map. Evidence: per-state video/screenshots plus scoring/state/audio trace; invalid grind attempt must be visibly rejected.

## R07 Animation/board matrix
Check every catalogue family:
idle, push, coast, turn, crouch, ollie, air, land, flips, grabs, manual, grind entry/loop/exit, wall, lip, revert, special, bail, recovery, walk/carry, pickup, mount, dismount, break, recovery.
Pass: correct pose/timing/blend/board attachment and no Fallout animation leakage. Evidence: catalogue checklist with video clips or timestamped continuous capture and board/skeleton state trace.

## R08 Keyboard/mouse and Xbox
Repeat representative GMod and THUG2 paths under each input profile.
Pass: same gameplay-action semantics, no stuck input/focus, no double consumption. Evidence: separate M&K and Xbox recordings using the same representative action sequence.

## R09 Cross-system/save-load
Sequence:
Fallout -> Q -> Toolgun -> Physgun -> Fallout -> skateboard -> THUG2 -> Fallout -> save -> reload -> repeat.
Pass: no ownership leakage, inventory identity corruption, crash or persistence failure. Evidence: one continuous transition/save/reload recording, before/after inventory screenshots, hashes and logs.
