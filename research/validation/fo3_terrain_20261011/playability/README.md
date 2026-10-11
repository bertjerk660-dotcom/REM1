# REM Dream / Fallout 3 Wasteland two-cell reproducibility suite

Status: **Independent, isolated research validation only. Not merged into the game, and not a complete playable Fallout 3 world.** Date 2026-10-11.

The suite uses data from the owner's legitimately installed Fallout 3 GOTY at `D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\`, and Bevy 0.20 / Rapier 0.36.

## Strict provenance

- Required `Fallout3.esm` SHA256: `D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06`.
- Tested Wasteland worldspace `0000003C`, exterior cell coordinates `(6,7)`/`(7,7)`, corresponding `CELL` IDs `000017A1`/`000017A0`.
- Generated terrain-only GLB (local only): SHA256 `3F9C66437A0F2951816E80DE6B768BF0DAE8D1B242C978F9B2706C08FD3908A2`.
- Generated terrain+NIF world scene GLB (local only): SHA256 `3422008AD5A0C4E2563200B9562B581554564DE3D01B8002BFEA5AF562CC282C`.
- The native model source is `Fallout - Meshes.bsa`, from which 34/34 referenced NIF files were extracted successfully locally. No third-party game meshes, record tables, textures or proprietary executable bytes are committed.

## Reproduce on owner's Windows machine

Scripts in order (Python 3 with local PyFFI 2.2.3):
1. `python fo3_terrain_probe.py` -> inventory original ESM LAND and source record counts.
2. `python fo3_two_cell_mesh_probe.py` -> original LAND heightfield GLB and seam audit.
3. `python fo3_placed_objects_probe.py` -> original REFR/ACRE world placements (local JSON only).
4. `python fo3_base_model_probe.py` -> base records, original NIF model references and bounding boxes (local JSON only).
5. `python fo3_bsa_extract_models.py` -> extract referenced NIF source models locally from original BSA.
6. `python fo3_nif_geometry_inventory.py` -> NIF geometry/Havok collision census.
7. `python fo3_native_scene_export.py` -> untextured native NIF visual scene GLB including original REFR locations.

The local PyFFI installation is old on Python 3.13 and requires `time.clock=time.perf_counter` before importing; the authoring scripts contain this compatibility shim.

Run Rapier test in `rapier/`:
```powershell
$env:REM_FO3_TERRAIN_GLB='D:\REM_Dream_validation_20261011\fo3_original_two_cells_6_7_7_7.glb'
$env:REM_TERRAIN_VALIDATION_DIR='D:\REM_Dream_validation_20261011'
$env:CARGO_TARGET_DIR='D:\rem1_bevy_target_chat'
cargo test --offline -- --nocapture
```
The reproducible source unit tests expect 251 original static placement proxies from original `OBND` data. These are **bounding-box proxies**, not the game's Havok colliders, and tests must not be marked native collision parity.

For Bevy scene load or Bevy fixed-step traversal on a **disposable, isolated clone** of `implementation/bevy-slice-chat-20261010`, copy `fo3_scene_load_gate.rs` / `fo3_playable_bevy_gate.rs` into `bevy/src/bin`, place the local `fo3_two_cell_original_nif_scene.glb` in that clone's `bevy/assets/fo3_wasteland.glb` (not Git), then `cargo run --bin fo3_scene_load_gate` or `cargo run --bin fo3_playable_bevy_gate`, with cargo target on D: drive. Those test binaries create hidden windows to avoid interrupting active GTA IV sessions.

## Verified by independent execution, with limitations

- The ESM parser scanned 718,952 records, identifying 40,256 LAND records, 40,084 valid VHGT grids, and no format errors in the scan.
- Two original LAND cells generated 2,178 vertices and 4,096 triangles with a continuous 33-vertex join (zero difference).
- Original placed objects: 252 references = 251 statics/vegetation/movable statics and one `ACRE` spawn; 37/37 resolved base records.
- Source NIFs: 34/34 found in the owner's original BSA, 34/34 parsed, 50,143 native visual triangles; 28 models have Havok collision blocks (7,516 unique native collision triangles identified but **not** converted to Rapier).
- The original NIF GLB contains 35 unique meshes (34 source models plus LAND) and 239 original NIF instances; 12 SpeedTree/vegetation `.spt` placements and one creature are not rendered by this importer.
- Rapier 0.36 test suite: five tests PASS, including real mesh raycast/grounding, original ref proxy registration, seam continuity, and automated player-controller traversal from x=416.0 to x=461.1565 across x=448 seam in 660 physics frames. Grounded 645/660, no measured below-ground penetration, lateral change -0.7352m. The <1m lateral tolerance is calibrated to native terrain/contact adjustment in this test, not measured original Fallout movement parity.
- The Bevy 0.20 glTF scene loader succeeded using `WorldAssetRoot`/`WorldAsset`: `REM_TERRAIN_SCENE_LOADED=true FRAME=3`; executable exit code 0. Uses invisible window and GPU wgpu/Vulkan.
- Note a ReShade Vulkan API layer produced a warning, but it did not prevent Bevy scene-load success.

## Genuine closure requirements

**Do not declare the whole playable-terrain gate closed** until all are satisfied:
- Original Havok collision blocks are mapped and compared against Rapier triangles/scale/rotation; proxies alone do not prove world-object contact.
- All 12 SpeedTree vegetation instances and the actor spawn are handled with appropriate assets/behaviours.
- Original object transforms, materials/textures and terrain unit scale/height are compared against source-game positions using a source-grounded calibration fixture.
- Bevy end-to-end gameplay mode (not just automated fixed-step harness) provides mouse/keyboard and Xbox input, camera, player rig, save/load, and actor interactions on real imported terrain.
- At least a controlled manual playtest plus automatic regression suite including terrain/objects/roads/structures, collision streaming/LOD, cutscene/quest travel and fall recovery.

This repository contains only authored conversion/test logic and non-proprietary derived metadata; all original asset data is private and remains local. No changes have been made to the protected FNV v85 DLL/ESP or active Bevy B001 implementation.

## Additional native Havok collision reproduction

After extracting source NIFs, execute `python fo3_native_havok_export.py` from the script directory (the script currently uses an absolute test-workspace source root). It generates a *local-only* `fo3_original_havok_static_collisions.bin` plus metadata. Source target is exactly 149 HAVOK-backed placements, 17,214 vertices and 24,754 triangles; hash `F9D79006752BE0C2AB7763004470841AFCF30A7EF0F3DDE5C0F9BA5E8B24F2BF`. Re-run `cargo test` in the `rapier` subdirectory to execute the additional two native-Havok tests. Their PASS does **not** validate actual Havok material/collision-group semantics or all world objects.

`fo3_playable_native_havok_gate.rs` runs the **combined Bevy** version with those 149 native Havok shapes plus 102 fallback bounding-box proxies in an isolated copy of REM1 B001. It requires the local native binary and full (unredacted) local `fo3_havok_collider_export_manifest.json`, which contains source base-form IDs; these remain on the owner's machine and are not committed. The script uses only local files and a hidden test window; it is not the production game binary.