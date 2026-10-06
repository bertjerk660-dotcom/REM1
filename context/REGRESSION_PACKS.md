# Regression Test Packs

Run preflight before and postflight after every gameplay test. Static validation is not a substitute for these packs.

## Baseline Fallout regression
ID: baseline_fallout
Astra-owned: False

Steps
1. Run support_playtest_preflight.ps1 with label baseline_fallout.
2. Boot Fallout New Vegas to main menu.
3. Load a disposable known-good save.
4. Move, aim, attack, open/close Pip-Boy and change normal Fallout equipment.
5. Create a new test save, return to menu, reload it.
6. Exit normally and run support_playtest_postflight.ps1.

Pass gates
- No new crash
- Normal Fallout controls/inventory work
- Save and reload work
- No unexpected plugin/DLL/ESP hash change

## GMod/THUG2 inventory presentation
ID: inventory_presentation
Astra-owned: False

Steps
1. Run preflight with label inventory_presentation.
2. Inspect representative GMod weapons and THUG2 Skateboard in Pip-Boy.
3. Verify names and GMod/THUG2 origin icons.
4. Drop, inspect world model, pick up, container-transfer and trade representative items.
5. Exit and capture postflight.

Pass gates
- Correct source-origin icons
- Representative items drop/pick up normally
- No invisible world item in tested set
- No new crash

## RPG presentation sidecar
ID: rpg_presentation_fix
Astra-owned: False

Steps
1. Enable only REM_WeaponPresentation_Fixes.esp after baseline succeeds.
2. Run preflight with label rpg_presentation_fix.
3. Inspect GMod RPG Pip-Boy icon and equipped/dropped world presentation.
4. Drop and pick up the RPG.
5. Exit, postflight, then disable the sidecar.

Pass gates
- GMod origin icon appears
- Prepared rocket-launcher world model appears
- Drop/pickup remains functional
- No new crash

## Curated GMod prop sidecar
ID: gmod_prop_catalog
Astra-owned: False

Steps
1. Enable only REM_GModProps_Catalog.esp after baseline succeeds.
2. Run preflight with label gmod_prop_catalog.
3. Spawn a small sample from every prepared category, not all records at once.
4. Inspect scale, materials, collision and stability on approach/contact.
5. For authored movable examples, check ordinary physical response.
6. Exit, capture postflight, disable sidecar.

Pass gates
- Sample records resolve
- Textures/materials display
- Collision is present
- Scale is plausible
- No crash on spawn/contact

## Combine Soldier armor sidecar
ID: combine_armor
Astra-owned: False

Steps
1. Enable only REM_CombineArmor_Test.esp after baseline succeeds.
2. Run preflight with label combine_armor.
3. Equip on player; inspect front/back/side in idle, walk, run, crouch and jump.
4. Check common weapon poses, first person and third person.
5. Drop armor and inspect world model.
6. Equip on one test NPC.
7. Save with armor equipped, reload, then unequip.
8. Exit, postflight, disable sidecar.

Pass gates
- No severe clipping/body disappearance
- World model works
- NPC equip works
- Save/load persists
- Unequip restores normal body

## Skateboard non-runtime presentation baseline
ID: skateboard_baseline
Astra-owned: False

Steps
1. Run preflight with label skateboard_baseline.
2. Equip THUG2 Skateboard without entering skate mode.
3. Inspect held/world visibility, origin icon, drop and pickup.
4. Do not use this pack to claim skate-mode mechanics correctness.
5. Exit and capture postflight.

Pass gates
- Board is visible in tested inventory/world states
- Drop/pickup works
- Normal Fallout remains functional before skate-mode activation

## Astra skate activation gate
ID: astra_skate_activation
Astra-owned: True

Steps
1. Run only on the explicitly assigned Astra build/branch.
2. Capture preflight and exact DLL/ESP hashes.
3. Enter skate mode, remain active beyond retarget delay, move/turn/jump, then exit.
4. Capture plugin log and Windows events immediately after.
5. Repeat enter/exit at least three times only after first pass survives.

Pass gates
- No activation crash
- No delayed retarget crash
- Exit restores Fallout
- Repeated transition survives

## Astra GMod runtime gate
ID: astra_qmenu_tool_physgun
Astra-owned: True

Steps
1. Run only after real GMod Q-menu compatibility runtime is integrated.
2. Open Q, browse/search curated catalog, select Remover/Duplicator.
3. Confirm selected Q-menu tool drives Tool Gun with no Fallout selection prompts.
4. Check GMod notification feedback.
5. Test Physgun target/hold/rotate/freeze/drop/launch behavior against source semantics.
6. Exit Q and verify normal Fallout input restores.

Pass gates
- Real Q-menu flow works
- No Fallout tool-selection prompts
- Tool Gun follows selected tool
- Physgun core behavior stable
- Input restores
