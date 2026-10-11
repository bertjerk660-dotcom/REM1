# REM Dream: Fallout 3 playable-terrain gate — independent validation
Date: 2026-10-11
Owner lane: independent evidence collection/testing; implementation remains Claude Opus; Codex must independently trace original game mechanics in IDA Pro 6.8.
Status: **AUTOMATED TWO-CELL BEVY VERTICAL SLICE PASSED; FULL PLAYABLE-TERRAIN GATE REMAINS OPEN.**
Branch: `research/four-gates-20261011`. Original-game data, binaries and generated meshes remain exclusively on owner's local machine.

## Source and test build fingerprints

- Source `D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm`; SHA256 `D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06`.
- Wasteland worldspace `0000003C`; exterior cell `000017A1` at (6,7), cell `000017A0` at (7,7).
- Two-cell LAND-only GLB SHA256 `3F9C66437A0F2951816E80DE6B768BF0DAE8D1B242C978F9B2706C08FD3908A2` (local file only).
- Two-cell LAND + original NIF-scene GLB SHA256 `3422008AD5A0C4E2563200B9562B581554564DE3D01B8002BFEA5AF562CC282C` (local file only).
- Engine used: Bevy `=0.20.0`, rapier3d `=0.36.0`, Rust 1.99.0. Existing independent B001 source pinned branch `implementation/bevy-slice-chat-20261010` at `3a7878ceb0db8ee676176569278c55460b91e863`; cloned to **isolated** `D:\REM_Dream_validation_20261011\REM_Bevy_Terrain_Test`.
- Existing FNV Legacy v85 and REM1 B001 working directories untouched. Windows DESKTOP-6PTSS3D, Nvidia RTX 4060 with Vulkan. GTA IV process was left running, and Bevy test used a hidden window.

## Original game content extraction — PASS, narrowly scoped

| Finding | Observed |
|---|---|
| ESM `LAND` records across Fallout3.esm | 40,256 |
| `LAND` records with valid `VHGT` grid | 40,084 |
| Target cells | 2 adjacent exterior Wasteland cells |
| Terrain vertices/triangles | 2,178 / 4,096 |
| Shared 33-vertex cell-edge difference | 0 (exact decoded height matching) |
| In-cell entities | 252 (`REFR` 251 + `ACRE` 1) |
| Referenced base forms resolved | 37 of 37 |
| Original source NIFs extracted from `Fallout - Meshes.bsa` | 34 of 34 |
| Source NIFs parsed with local PyFFI | 34 of 34 |
| Source NIF visual triangles | 50,143 across 103 NiTriStrips |
| Original NIF models with Havok collision blocks | 28; 7,516 unique source collision triangles |
| Instances of authentic NIF geometry in scene GLB | 239 |
| Original SpeedTree `.spt` instances not converted | 12 |
| Creature `ACRE` not yet visually or behaviorally instantiated | 1 |

No game assets are included in GitHub; repository contains scripts and aggregate non-proprietary provenance/test manifests only. Local extraction workspace is `D:\REM_Dream_validation_20261011`.

## Physics collision alignment — PASS for original LAND, partial for static assets

The real decoded `LAND` mesh was accepted by Rapier trimesh and hit by downwards rays at expected heights. The kinematic capsule settled onto real terrain. A prior failed test was **a harness initialization bug** (query pipeline before the first `world.step()`), and was resolved by stepping physics before testing.

On the original LAND seam at x=448, z=-506, adjacent raycasts at x=447.98 and 448.02 both returned `height=232.125`; no discontinuity.

The original game placed 251 non-creature refs, and their real REFR positions, scale, original NIF references and source `OBND` bounding boxes were extracted. The first physics suite registered 251 test-only OBND box proxies; an **additional independent native Havok suite** subsequently loaded 149 authentic source-object Havok instances as Rapier triangles. The 102 other object references require source-specific collision/no-collision classification or fallback proxies. Source scale /64 and placement rotation conventions remain unverified against the live game; entire world-object collision fidelity remains open. Source model geometry is real, untextured, and loaded into the Bevy visual scene.

Additional original NIF Havok scale census of 28 collision-bearing models: converting Havok vertices by factor `7` brought collider and source visual AABB size medians near 1.0 (x 1.0001363, y 1.0001363, z 0.9943011). This is strong static geometric evidence for a candidate Havok-to-NIF scale of 7. Rapier successfully loaded and raycast the converted Havok triangles in a separate executable test, **but this is not original-game Havok contact parity**; outliers up to approx 0.61 in some axes reflect simplified native collision shapes.

## Direct Rapier physics tests — five PASS

Independent original mesh, plus source derived world-reference bounding proxy fixtures:
1. Imported LAND mesh builds and surface rays match known height samples.
2. Player capsule grounds properly on the mesh.
3. 251 source-placed static proxy colliders registered; source reference base definitions 37/37.
4. Seam raycast matches near x=448.
5. Fixed controller runs 660 frames at 60Hz and crosses x=448 with 251 proxies in world; final x=461.1565, z=-506.7352, grounded 645/660 frames, maximum sink 0.0, maximum vertical offset above contact 0.4928894. Passed bounded lateral deflection tolerance 1.0m and max lift 1.5m.

Result: `test result: ok. 5 passed; 0 failed`, exit 0.

## Bevy 0.20 scene loader — PASS

Compiled isolated binary `fo3_scene_load_gate`. Used the actual **Bevy 0.20 `WorldAssetRoot` and `WorldAsset`** interface; older Bevy examples using `SceneRoot`/`Scene` are incompatible (Bevy 0.20 has a `Scene` trait instead).
Source local GLB `fo3_two_cell_original_nif_scene.glb` (35 meshes, 239 original NIF instances, exact original terrain).
Result:
`REM_TERRAIN_SCENE_LOADED=true FRAME=3 handle_loaded=true`
Exit code 0.
An injected ReShade Vulkan layer logged error 1114 loading `ReShade64.dll` but rendering adapter succeeded. This error did not prevent the scene loading.

## INTEGRATED automated Bevy gameplay-traversal test — PASS

Compiled and executed isolated `fo3_playable_bevy_gate` binary, using full Bevy 0.20 asset/render/ECS graph, Rapier 0.36 real LAND collision, a spawned visual capsule player, 251 reference-derived box proxy colliders and scripted movement on `FixedUpdate` 60Hz.

Exact result:
```text
FO3_BEVY_GATE_BOOTSTRAP objects=251 initial_x=416 land_cells=2
FO3_BEVY_TRAVERSE_COMPLETE passed=true x=461.156 z=-506.735 grounded=645 ticks=660 sink=0.00000 lift=0.49289 objects=251
FO3_BEVY_GATE_RESULT passed=true scene_loaded=true gltf_meshes=35 gltf_nodes=240 named_entities=241 world_instances=239 land_triangles=4096
```
Exit code 0. Full test execution consumed a hidden-window renderer; existing GTA IV session was not stopped or manipulated.

**Interpretation:** This test actually ran a Bevy 0.20 program with the 2-cell original landscape, authored conversion from 34 original NIF model geometries, registered original object location proxies, and 11 seconds of simulated character traversal across the source cell seam. It is stronger than merely parsing a file or running a physics-only isolated algorithm.

## Additional authentic Havok static-object collision validation — PASS (independent physics test)

Local extractor script: `research/validation/fo3_terrain_20261011/playability/fo3_native_havok_export.py`. It reads **source NIF hkPackedNiTriStrips collision geometry**, applies candidate 7x Havok/NIF scale, original extracted placements and *provisional* ZYX rotation order, and produces a local-only aggregate collider binary. No proprietary Havok vertex/triangle data has been committed.

- **28** distinct source NIF collision models; **149** source object placements with a Havok collision shape; **102** additional non-creature placements without directly imported Havok collision.
- **17,214** placed Havok vertices, **24,754** collision triangles across 149 native instances.
- Local binary SHA256 `F9D79006752BE0C2AB7763004470841AFCF30A7EF0F3DDE5C0F9BA5E8B24F2BF`; file `D:\REM_Dream_validation_20261011\fo3_original_havok_static_collisions.bin` is not distributed.
- Rust test `rapier/src/native_havok.rs` constructed Rapier trimesh colliders from those vertices, confirmed collision raycast, and walked the same original LAND region using **original Havok static collision** rather than only box proxies. The native test moved to `x=461.5104, z=-506.72736`, grounded **645/660**, max terrain penetration **0**.
- Extended independent Rapier suite verdict: **7 passed, 0 failed, exit 0**.

This establishes *physical compatibility of converted native geometry*, NOT source engine equivalence. Surface collision characteristics of Havok shapes (materials, motion systems, group masks, MOPP flags), original-game transform fidelity, and all 102 uncovered objects remain open. The prior integrated Bevy executable originally used proxy boxes; a separate upgraded native+fallback Bevy test has its own verdict below.
## Remains to close the FULL playable-terrain gate

- [x] Extract and physically test native per-model Havok triangles for 149 placed objects / 28 NIFs in isolated Rapier; [ ] integrate their original collision semantics and verify remaining 102 objects (including 12 SpeedTrees) and actual rotation against original-game state.
- [ ] Extract/convert source SpeedTree `.spt` meshes for 12 instances; NPC/creature spawn, AI and interactions not implemented yet.
- [ ] Reconstruct original materials/textures, terrain normals/LOD/water/navmesh and collision semantics. No source texture/visual parity has been playtested.
- [ ] Validate 1 Bevy unit = 1m, source /64 and Havok x7 against actual Fallout3.exe 1.7.0.4 game measurements with IDA Pro 6.8 support; current values are coherent conversion assumptions only.
- [ ] Build keyboard/mouse and physical Xbox user-control path on this imported terrain and conduct **human playtest** (real input, camera, collide with objects, interact with NPCs, save/load, death and falling).
- [ ] Cover full Fallout 3 world outside two selected cells, interior/exterior transitions, scripted quests/prologue, collision streaming and persistent save entity state. This two-cell test is not the complete Fallout game.

## Reproducibility / ownership

Testing scripts: `research/validation/fo3_terrain_20261011/playability/`; directions and hashes in its README. Local source ESM, BSA, 34 NIF and two generated GLB files must **not** be committed. Keep original game owners' assets local. Opus-only implementation and Codex-only original-game reverse engineering with IDA Pro 6.8 remain unchanged. Existing Bevy prototype source was not modified.

**Final verdict as of this evidence:** Automated source-terrain Bevy vertical-slice acceptance **PASS**; full playable world fidelity **NOT YET CLEARED**.
