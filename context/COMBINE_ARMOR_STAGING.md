# Combine Soldier Armor Staging

Status: static validation PASS; runtime playtest NOT RUN.

## Goal
Prepare a separate full-body Combine Soldier armor item for later testing before any Enclave/Remnants replacement is attempted.

## Source/provenance
- Visible geometry/materials come from the user's installed Garry's Mod / Source Combine Soldier asset pipeline.
- Fallout Remnants Power Armor is used only as the FNV ARMO/container donor and humanoid skeleton compatibility target.
- Proprietary NIF/DDS assets are local and are not committed to GitHub.

## Current local artifacts
- Wearable NIF: `Data\meshes\rem\gmod\armor\CombineSoldierFullBody.nif`
  - SHA256 `90A836EEF689C50994ED6E5BECC7B37CEFA0B32DA6E20D88C34DC193837B6728`
  - 3,535 vertices / 4,682 triangles
  - `NiSkinInstance`
  - 41 Fallout humanoid bones
  - no uncovered vertices
  - max 3 influences per vertex
  - max weight-sum error 4.47e-08
- World NIF: `Data\meshes\rem\gmod\Combine_Soldier.nif`
  - SHA256 `1878E5E9E776F70897504EBC31A4B9E13CDF0C496384974453FDF4601D68D3A5`
- Test sidecar: `Data\REM_CombineArmor_Test.esp`
  - SHA256 `52B06C9D1FA087B32BD2F83120603903893D24781BC9490D89C3D9EEE105979E`
  - EDID `REMCombineSoldierFullBodyTest`
  - display name `Combine Soldier Full-Body Armor (Test)`
  - currently disabled in `plugins.txt`

## Validation completed
- wearable/world NIFs exist;
- expected topology present;
- skin instance present;
- all vertices have valid skin weights;
- weights normalize to 1 within tolerance;
- core Fallout humanoid bones present;
- referenced Combine diffuse/normal textures resolve;
- sidecar contains expected EDID/model/icon strings;
- live installed v85 DLL hash remains unchanged;
- local v88 HUD candidate hash remains unchanged.

## Required later playtest
Enable the sidecar only for an isolated armor test, then check:
- male and female player display/fallback behavior;
- idle/walk/run/crouch/jump and weapon poses;
- hand/head/helmet clipping;
- third person and first person;
- dropped world model;
- NPC equip/unequip;
- save/load;
- no body-part disappearance or slot conflicts.

Only after those gates pass should the project consider replacing Enclave/Remnants visuals or NPC equipment.
