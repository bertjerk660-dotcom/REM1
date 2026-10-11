# Fallout 3 original LAND -> GLB -> Rapier 0.36 validation harness

Date: 2026-10-11. Authored *test tooling*, not the REM Dream runtime importer. These scripts only READ an authorized local Fallout 3 installation, and write derived data to a separate, local `D:\REM_Dream_validation_20261011` workspace. Original Fallout3.esm, IDA projects, and generated GLB must never be committed to REM1.

## Pinned input

`D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm`

SHA256 `D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06`

Fallout 3 GOTY `Fallout3.exe` version 1.7.0.4.

## Reproduction (on owner's machine)

In PowerShell:

```powershell
python .\scripts\fo3_terrain_probe.py
python .\scripts\fo3_two_cell_mesh_probe.py
$env:REM_FO3_TERRAIN_GLB = "D:\REM_Dream_validation_20261011\fo3_original_two_cells_6_7_7_7.glb"
$env:CARGO_TARGET_DIR = "D:\rem1_bevy_target_chat"
cargo test --offline -- --nocapture
```

The scanner reports count/metadata and first selected data; the converter exports only 2 neighboring Wasteland cells `(6,7)` and `(7,7)` from original LAND records, and checks 33-point seam continuity. It does not include textures, rocks, roads, buildings, navmesh, quests or object instances. The metres-per-FO3-unit assumption in the converter remains *provisional* pending source engine validation.

Expected local derived GLB: 2178 vertex positions, 4096 triangles, 0 maximum original-height seam delta between the 2 cells, sha256 `3F9C66437A0F2951816E80DE6B768BF0DAE8D1B242C978F9B2706C08FD3908A2`.

Rapier: uses `=0.36.0` (the physics version pinned by REM1 B001). Both raycast and kinematic capsule ground checks pass after `world.step()` updates the collision query state. The initial pre-step failure was in the test harness, not a collision geometry fault.

**Passing tests do not mean full Fallout 3 gameplay has been imported into REM1 Bevy.** See [four-gate validation report](../../../bevy/docs/GATE_VALIDATION_GTAIV_ASYNC_SKATE_FO3_2026-10-11.md) and [Bevy B001 current state](../../../bevy/docs/CURRENT_STATE.md).

No direct reuse or redistribution of proprietary Fallout 3 geometry is granted by these tests; local authorized source input is required.
