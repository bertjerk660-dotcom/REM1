# Regression Packs

## Fallout baseline regression
Owner: support.

Preconditions:
- No support sidecar enabled unless specifically required
- Installed runtime hash matches recorded v85 or assigned candidate

Steps:
- Boot to main menu
- Load known-safe save
- Move/aim/fire normal Fallout weapon
- Open/close Pip-Boy
- Create new save
- Reload the new save
- Travel/enter another area if practical

Pass:
- No crash
- Normal Fallout controls remain functional
- Save/load succeeds
- No new high-severity plugin/Application errors

## GMod weapon inventory/drop/pickup
Owner: support.

Preconditions:
- Main ESP enabled
- Presentation-fix sidecar only if testing RPG override

Steps:
- Inspect GMod weapon name/icon in Pip-Boy
- Drop weapon
- Inspect dropped world model/name
- Pick weapon back up
- Move to/from container
- Trade where base game permits
- Repeat on representative Tool Gun/Physgun/RPG

Pass:
- Correct origin icon/name
- No invisible or wildly scaled world model
- Pickup/container/trade work normally

## Skateboard item baseline
Owner: support+Astra.

Preconditions:
- Use exact build assigned for test

Steps:
- Inspect THUG2 origin icon/name
- Equip outside skate mode
- Verify held board visibility
- Drop/pickup/container test
- Activate skate mode only on assigned Astra candidate
- Exit skate mode

Pass:
- Inventory behavior normal
- Board visible in required states
- Exit restores Fallout cleanly

Note: Physics/animation/tricks/camera fidelity is Astra-owned and needs a separate deep pack.

## Curated prop representative sample
Owner: support.

Preconditions:
- Enable only REM_GModProps_Catalog.esp for custom GMod sidecar portion

Steps:
- Spawn one rail/fence
- Spawn one bench/table
- Spawn one plank/beam
- Spawn one crate/pallet
- Spawn one barrel/canister
- Spawn one street prop
- Spawn one furniture prop
- Spawn one playground/misc prop
- Approach/touch each
- Check texture/scale/collision
- Manipulate only where mobility is intended

Pass:
- No crash
- Texture resolves
- Plausible scale
- Collision is usable
- No unexpected map-sized geometry

## Combine Soldier armor isolated test
Owner: support.

Preconditions:
- Enable only REM_CombineArmor_Test.esp
- Use disposable save

Steps:
- Add/equip test armor
- Inspect idle/walk/run/crouch/jump
- Inspect common weapon poses
- Inspect first person
- Inspect third person
- Drop and inspect world model
- Equip on NPC
- Save with armor equipped
- Reload
- Unequip

Pass:
- No catastrophic clipping/deformation
- No slot/body disappearance issue
- World model visible
- NPC equip works
- Save/load persists

Note: Do not replace Enclave/Remnants visuals until this passes.

## Real GMod Q-menu integration
Owner: Astra.

Preconditions:
- Astra source-faithful Q-menu candidate installed intentionally

Steps:
- Press Q
- Browse categories
- Search
- Spawn representative prop
- Select Remover
- Use Tool Gun
- Select Duplicator
- Use Tool Gun
- Close/reopen Q
- Confirm selected tool state
- Return to Fallout input

Pass:
- No flashing/missing icons
- Real/ported GMod UI behavior
- Tool selection controlled by Q
- No Fallout prompt substitute
- Input restores cleanly

## Release candidate smoke pack
Owner: joint.

Preconditions:
- Static validator zero errors
- Exact release hashes recorded

Steps:
- Run baseline_fnv
- Run inventory_gmod
- Run skateboard_item
- Run prop_sample
- Run combine_armor if included
- Run Astra skate deep pack
- Run qmenu_future
- Save/load after using imported systems

Pass:
- All included packs pass
- No new high-severity errors
- No progression/save regression
