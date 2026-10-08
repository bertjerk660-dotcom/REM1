# Support Playtest Checklist

This checklist is for staged/support features and regression evidence. It does not authorize support-lane changes to Astra's v88 runtime candidate.

## Before any test
- Run `research/support_playtest_preflight.ps1` with a descriptive label.
- Confirm the installed runtime DLL is still v85 unless a separate Astra test explicitly says otherwise.
- Confirm the v88 candidate hash is unchanged and v88 is not accidentally deployed.
- Confirm only the sidecar plugin required for the specific test is enabled.
- Do not enable `REM_CombineArmor_Test.esp`, `REM_GModProps_Catalog.esp`, or `REM_WeaponPresentation_Fixes.esp` together unless the test explicitly requires them.
- Record the save used for the test. Prefer a disposable/non-critical save.

## Baseline Fallout regression
- Game reaches the main menu without a new error.
- Existing save loads.
- Player can move, aim, attack and open/close Pip-Boy normally.
- Normal inventory browsing works.
- A new save can be created.
- Save can be reloaded.
- No unexpected new high-severity entries appear in the plugin log or Windows Application events.

## Inventory / weapon presentation
- GMod weapons show their expected names.
- GMod weapons show the GMod Pip-Boy origin icon.
- THUG2 Skateboard shows the THUG2 Pip-Boy origin icon.
- Each tested GMod weapon can be dropped.
- Dropped item uses the intended world model.
- Item can be picked back up.
- Item can be transferred to/from a container.
- Item can be transferred in normal trade where the base game allows it.
- RPG presentation-fix sidecar, when specifically enabled, shows the prepared GMod RPG world model and GMod icon.
- Camera/view-only exceptions are documented instead of silently replaced.

## THUG2 Skateboard baseline
- Equipping the board outside skate mode does not alter normal Fallout gameplay unexpectedly.
- Held board is visible in the intended state.
- Dropped board is visible and can be reacquired.
- Left-click skate activation is tested only on the branch/build assigned by Astra.
- Exiting skate mode restores normal Fallout HUD/input/state.
- Do not use this support checklist as evidence that THUG2 physics/animations are complete; Astra owns those validation gates.

## Curated prop catalog
- Enable only `REM_GModProps_Catalog.esp` for the isolated catalog test.
- Verify representative records from every prepared category can be resolved by the game.
- Spawn a small representative sample first rather than all 120 records.
- Verify model appears at plausible scale.
- Verify textures resolve.
- Verify collision works.
- Verify object does not crash the game when approached or touched.
- For mass-authored/movable candidates, verify normal physical behavior.
- For fixed obstacles, verify they behave as stable skate/environment pieces.
- Later Physgun tests must distinguish a natively movable object from one that requires an Astra runtime wrapper.
- Disable the sidecar again after the isolated test.

## Combine Soldier armor
- Enable only `REM_CombineArmor_Test.esp` for the armor test.
- Equip on player and inspect front/back/side.
- Check idle, walk, run, crouch and jump.
- Check common weapon poses.
- Check head/helmet and hand clipping.
- Check first-person view for unexpected body obstruction.
- Check third-person view.
- Drop the armor and inspect the world model.
- Equip on an NPC and inspect movement/weapon poses.
- Save with the armor equipped, reload, and confirm state persists.
- Unequip and confirm the normal body/slots restore correctly.
- Do not replace Enclave/Remnants equipment until these gates pass.

## GMod Q-menu / Tool Gun / Physgun future integration
- Support-lane content manifests and thumbnails may be used as data inputs.
- Final menu behavior must come from the real GMod Q-menu port.
- Tool selection must happen in the real/ported Q menu, not Fallout prompts.
- GMod notification bubbles/feedback replace Fallout top-left tool prompts.
- Tool Gun and Physgun mechanics remain Astra/native-runtime validation tasks.

## After any test
- Run `research/support_playtest_postflight.ps1 -SessionDir <preflight session dir>`.
- Preserve the postflight plugin log and Application event capture.
- Write the human observation into the session folder or build manifest.
- Compare pre/post hashes and investigate any unexpected file change.
- Update CURRENT_STATE only with observed facts; do not promote a staged feature to verified without the relevant gameplay checks.
