# Combine Solider Goodsprings rampage encounter — 2026-10-06

## Requested behavior
A Raider-derived NPC named exactly **Combine Solider** is staged in exterior Goodsprings wearing the current torso-lowered Combine armor. It has 100,000 HP, a 200 movement-speed multiplier, a Minigun, 10,000,000 standard 5mm rounds, and Frenzied/Foolhardy AI intended to attack any detected actor rather than preserve Raider faction allies.

## Artifact
- Plugin: `Data\REM_CombineSolider_GoodspringsRampage.esp`
- SHA256: `A15C94CB5F677F8A53DE6EAA50E7FF8FA105C15DFAFAE10AA87ED3161A51F0CB`
- Generator: `third_party\tools\xEdit-4.1.5f\Edit Scripts\REM_CreateCombineGoodspringsRampage.pas`
- Structured manifest: `build\combine_armor\goodsprings_rampage_manifest.json`

## Exact records
- Raider donor: `Raider3GunHMNV [NPC_:000CEAB3]`
- Minigun: `WeapMinigun [WEAP:0000433F]`
- Standard 5mm: `Ammo5mm [AMMO:0006B53D]`
- Armor master record: `REMCombineSoldierFullBodyTest` from `REM_CombineArmor_Test_TorsoLowered.esp`
- Goodsprings exterior cell: `Goodsprings [CELL:000DAEBB]`
- New NPC local record: `02000800`
- New placed actor local record: `02000801`

## NPC validation
- FULL: `Combine Solider`
- Base Health: `100000`
- Speed Multiplier: `200`
- Aggression: `Frenzied`
- Confidence: `Foolhardy`
- Template record removed; template flags are 0.
- Faction list removed so inherited Raider allegiances cannot suppress the rampage.
- Inventory contains exactly:
  - 1 current Combine armor
  - 1 Minigun
  - 10,000,000 standard 5mm rounds

## Placement
The ACHR is correctly nested under the Goodsprings exterior cell temporary-children hierarchy and placed at:
`X=-71300, Y=1800, Z=8352`.

## Next-launch load order
1. `FalloutNV.esm`
2. `REM_GModTHUG2.esp`
3. `REM_CombineArmor_Test_TorsoLowered.esp`
4. `REM_CombineSolider_GoodspringsRampage.esp`

## Validation status
Binary/plugin validation passes. FalloutNV.exe was not running when the plugin was enabled. Human runtime validation is still pending; do not mark the encounter as runtime-verified until the player confirms the actor appears, wears the armor, uses the Minigun, moves at the intended speed, and attacks the player/nearby actors.
