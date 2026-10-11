# REM Dream four-gate validation: evidence and exact unresolved blockers
Date: 2026-10-11
Status: **PARTIAL VALIDATION ONLY. NONE of the four requested complete-integration gates is fully cleared.**
Research execution lane: isolated read-only original-game source audit, IDA Pro 6.8 database preparation, synthetic Rust/Rapier tests, Fallout 3 ESM landscape extraction. No production Bevy gameplay code, source-game install, or protected legacy runtime modified.

## Branch, environment and provenance
- Research branch: `research/four-gates-20261011` (forked from `research/mw2-libertycraft-bevy-20261011`).
- Local isolated workspace: `D:\REM_Dream_validation_20261011` on `DESKTOP-6PTSS3D`.
- Native IDA executable: `C:\Program Files (x86)\IDA 6.8\idaw.exe`, invoked in isolated automatic/batch mode from a copy of the GTA IV executable; other pre-existing IDA sessions remained untouched.
- GTA IV running executable: `D:\SteamLibrary\steamapps\common\Grand Theft Auto IV\GTAIV.exe`; **1.2.0.59**, length 17,425,752 bytes, SHA256 `08759A5516F9837920EA504436236BBAB89D0826A8E4D04FF106345177B5345D`.
- GTA DLC directories **TBoGT** and **TLAD** present in the same root. TBoGT script/animation/config exists; this pass did not boot TBoGT or measure flight live.
- Fallout 3 source executable: `D:\SteamLibrary\steamapps\common\Fallout 3 goty\Fallout3.exe`, version **1.7.0.4**.
- Fallout 3 main ESM: `D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm`, 288,771,262 bytes, SHA256 `D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06`.
- REM Bevy baseline: `implementation/bevy-slice-chat-20261010` SHA `3a7878ceb0db8ee676176569278c55460b91e863`, B001 only; current documentation notes no imported Fallout/GTA/skate gameplay.
- LibertyCraft 1.0.8.0 native addresses **not automatically applicable** to installed GTA IV 1.2.0.59.

## GATE 1: Exact GTA IV/TBoGT native mechanics — **NOT CLEARED**

**Actually performed:**
- Copied GTAIV.exe to isolated `GTAIV_1.2.0.59.exe`, re-hashed copy equal to installed SHA.
- Ran IDA Pro **6.8** automatic analysis with authored IDC report script. `Wait()` completed, database saved at `D:\REM_Dream_validation_20261011\GTAIV_1.2.0.59.idb` (152,491,922 bytes) and log `gta_1260_ida68.log`.
- Script reported `FUNCTION_COUNT=38802`, segments and sample function entrypoints, but the majority are unnamed `sub_...` candidates. The PDB was unavailable. No valid claim of knowing what these functions do can follow solely from identification counts.
- Located original TBoGT `common/data/handling.dat`, `moveblend.dat`, `WeaponInfo.xml`, and `effects/weaponFx.dat`.
- Source hashes:
  - `TBoGT/common/data/handling.dat`: `68B8BD6AC555F739953DD417C65433E5CB7BE0D3FBC00BCA9B10F14822660AA0`.
  - `TBoGT/common/data/moveblend.dat`: `67E7CB206A6A631989B092701F82580AEF7CA601810A570F6CE5D75DE9259303`.
  - `TBoGT/common/data/WeaponInfo.xml`: `D0662BFB082EC5B4D484EFE120C1BF519695B667A340BA75DABBB48871A55336`.
  - `TBoGT/common/data/effects/weaponFx.dat`: `2B54DA1CE4779EF4BB8169C1FE26AD1CB0AE1BD83356E40D25EE089B99045916`.
  - `common/data/handling.dat`: `A6FA49CA549DCC5A19B3432E546AFC3C536A49E9C38DC3FABCD054156914DC8D`.
- Found two original `BUZZARD` handling entries: base line with nominal mass 3800.0, drag 10.0 (as encoded) and a second prefixed `$ BUZZARD` helicopter-specific line beginning `0.58 0.035 0.4 -1.35...`. Both lines are needed as evidence of parameters, not proof of the flight equations.

**Still required for clearance:** IDA 6.8 function trace of Niko walk/run/sprint state fields and caller guards, step timing/acceleration/friction, vehicle enter/exit/fall/ragdoll and control return, TBoGT Buzzard live handling and flight laws, weapon effect/damage paths. Each evidence record must have binary SHA, image base, RVA, caller/callee graph, inputs/conditions, test fixture and live measurement. Do not label names from GTA III/SA or LibertyCraft downgraded 1.0.8.0 as confirmed 1.2.0.59 functions.

## GATE 2: Original-game physics parity — **NOT CLEARED**

**Actually performed:** Read TBoGT handling + weapon configuration hashes/entries, reviewed B001's `bevy/src/physics.rs` which uses Rapier3D 0.36.0 and a fixed 60Hz step. B001 has a simple kinematic player and no source-evidenced GTA on-foot motor, vehicle controller, Buzzard simulation, original-game collision solver, or original GTA damage model. There is therefore no like-for-like game/Bevy physics output to compare. No GTA IV/TBoGT live timed measurement was collected in this pass.

**Required clearance tests:** run controlled source-game trace for time/distance during walk/run/sprint and turn, stop/accelerate/airborne and ragdoll conditions; controlled vehicle drive/steer/brake/collision/suspension tests; controlled TBoGT Buzzard hover/acceleration/turn/descent/damage; compare identical initial states at matching input rates, positions, velocities, camera yaw and collision impulses against Bevy with explicit tolerances and measured error. Do not assume Rapier engine default behaviour is GTA IV physics parity.

## GATE 3: Full asynchronous skating integration — **NOT CLEARED**

**Actually performed:** Upstream IW4L `crates/render_anim/src/skate.rs` source audit in prior research; it uses epoch-tagged `Job::{Activate,Step,Suspend}`, `Reply::{Ready,Activated,Pose,Error}`, retained sessions, stale result checks, fail-stop reset, preloading and external motor authority gating. Previous isolated upstream rail tests passed 6/6 (committed harness).
**But:** REM Bevy B001 has **no** skate motor, THUG2 session, async pose pipeline, board-rig animation, skate HUD, or source-faithful camera. Actual worker interleavings, fault recovery and in-engine skate operation were not tested. Skate 3/ IW4L worker source is not equivalent to original THUG2 PS2 skating behaviour.
**Required clearance:** Opus implementation in isolated Bevy branch; Codex validate worker, double-authority prevention, state transition epoch and loaded-world invalidation, crash/panic/disconnect, input ownership, Xbox controller, real THUG2 board rig, collision and score/HUD semantics, save/load/holster restoration. Keep real skater simulation and THUG2 source evidence distinct from mock tests.

## GATE 4: Playable Fallout 3 terrain import — **PARTIALLY VALIDATED, NOT CLEARED**

**Actually performed on original source file:**
- Wrote local-only read-only `fo3_terrain_probe.py` to traverse native TES4 groups, parse records, decompress zlib-flagged `LAND` records and decode original `VHGT` 33×33 signed delta grids (height conversion is a provisional importer and must be checked against the running source game).
- Full ESM scan completed with **718,952 records**, **89,748 groups**, **40,256 LAND records**, **40,084 valid VHGT grids**, **41,989 CELL records with XCLC**, and **zero structural parse errors**. Original `LAND` extraction never modifies game files.
- Selected Wasteland world `0000003C`, cells `(6,7)` and `(7,7)`: LAND FormIDs `00001E60`, `00001E61`; CELL IDs `000017A1`, `000017A0`. Their 33 shared vertices have **height difference exactly 0** in the decoded source data.
- Exported only on local D: `fo3_original_two_cells_6_7_7_7.glb`, mesh of **2,178 vertices and 4,096 triangles**, SHA256 `3F9C66437A0F2951816E80DE6B768BF0DAE8D1B242C978F9B2706C08FD3908A2`. Derived proprietary terrain data is **not** committed or shared.
- The local authored Rust `fo3_physics_probe` loads this GLB in Rapier 0.36.0 (REM Bevy B001's physics version), registers a static triangle-mesh collider, and validates downward raycasts in both cells and grounding of a kinematic player capsule at a source terrain location.
- **Initial test 0/2 FAILED:** collider was inserted but broad-phase/query state not advanced; the query could not detect it. This was a **test setup mistake**, not an importer geometry failure. Corrected with `world.step()` after collider insertion. Re-ran: **2/2 PASS, zero failures, exit 0**.
- Geometry conversion assumes game-space scaling /64 to metre and Z-up->Bevy Y-up mapping; these values must be checked against source-engine reference points before claiming exact spatial fidelity.
- Authored source scripts and harness are under `research/validation/fo3_terrain_20261011`. The original ESM, output GLB and IDA databases remain local only.

**Still required for full clearance:** rendering the imported real terrain in the actual REM Bevy executable, player walking/turning/jumping/landing on it with both KBM and Xbox, physics/visual alignment, collision of original world objects, navmesh and NPC traversal, materials/textures, neighboring cell streaming, saves/loads, travel to interiors/exteriors, and quest/dialogue integration. A collision test in a sandbox is not gameplay acceptance.

## Targeted owner-approved next actions (strict implementation boundary)

1. **Codex / IDA 6.8:** from the hash-pinned GTA IV database, trace the real player motion/task/vehicle/weapon functions and document exact fields and evidence. TBoGT source uses same GTAIV.exe build but episode-specific data/mission records must be tracked distinctly.
2. **Codex:** perform recorded controlled tests in original GTA/TBoGT version 1.2.0.59. Record exact frame timelines and collision/vehicle telemetry for future Bevy comparisons. Do not downgrade or inject scripts into a running game without planned rollback/safety.
3. **Opus:** integrate the authored, source-validated importer into an isolated Bevy scene with proper colliders and collision readiness; do not overwrite B001 or Legacy. Codex independently validates render/physics/gameplay.
4. **Opus:** implement the actual GTA on-foot motor/vehicle sim and source-faithful THUG2 asynchronous skate session; Codex records full state transition, failure injection, controller and parity tests.
5. **Codex:** run a cross-mode integration acceptance suite including player dialogue, Fallout 3 HP and quests, GTA weapon hits/AI, car entry/exit, ragdoll recovery, skate mode and save/load across world-cell transitions.
6. Keep tests and source in GitHub; keep original proprietary inputs/local derived assets (including GLB) in local authorized storage; preserve protected Legacy v85 and B001 baseline.

## Accuracy / non-results

This research work **does not** claim any of the four complete-integration gates fully cleared. It verifies specific source inputs, IDA tool execution, actual LAND decoding, exact two-cell seam and isolated Rapier contact. IDA 6.8 disassembly count alone is not a native mechanics map. Source-original data hashes are real; numerical constants are recorded as source parameters, not independently demonstrated dynamics. Do not promote a sandbox Rapier test to evidence of an interactive, quest-capable Fallout 3 game running on Bevy.
