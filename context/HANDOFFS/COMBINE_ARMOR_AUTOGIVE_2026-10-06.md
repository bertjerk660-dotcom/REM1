# Combine armor auto-give support patch — 2026-10-06

Purpose: automatically add the isolated Combine Soldier test armor to the player inventory for the current armor playtest without touching the protected Astra v88 candidate.

## Local runtime state
- Host runtime remains the v85 code line.
- Live plugin: `Data/NVSE/Plugins/FNVGModTHUG2.dll`.
- Deployed SHA256 after this support patch: `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206`.
- `REM_CombineArmor_Test.esp` must be enabled for the armor form to exist.
- Test load order restored to `FalloutNV.esm`, `REM_GModTHUG2.esp`, then `REM_CombineArmor_Test.esp`.
- Legacy `REM_GModTHUG2.pre_v79_persistent_board.esp` and `REM_GModTHUG2_firstperson_patch.esp` remain disabled because both duplicate the THUG2 Skateboard record and caused bad weapon behavior when all plugins were enabled.

## Behavior
After PostLoadGame/NewGame reaches the existing safe form-init window:
1. Find the ARMO record by display name `Combine Soldier Full-Body Armor (Test)`.
2. Read the player's inventory through `InventoryItemsMap`.
3. If the armor is already owned, do nothing.
4. If absent, execute `additem <resolved runtime FormID> 1`.
5. Log either the existing-item or auto-added result with a `[COMBINE]` prefix.

This avoids hard-coding the sidecar load-order prefix and avoids adding duplicate armor on every save load.

## Validation
- Release/Win32 rebuild completed successfully with MSBuild 18.
- Live DLL hash matches the built DLL hash.
- Human runtime playtest still required: fully restart Fallout New Vegas, load a save, and verify one copy appears in Apparel and does not duplicate on a subsequent reload.
- This patch does not automatically grant Power Armor Training.
- Astra v88 candidate was not modified or deployed.

The exact source delta is stored beside this note in `COMBINE_ARMOR_AUTOGIVE_PATCH_2026-10-06.patch`.
