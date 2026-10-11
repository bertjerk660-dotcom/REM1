# REM Dream independent bridge validation — 2026-10-11

Status: **Source-level executable validation completed; original-game and full-system integration validation NOT completed**.
Branch: `research/mw2-libertycraft-bevy-20261011`.
Validation host: owner's Windows desktop `DESKTOP-6PTSS3D`, executed in **isolated** `D:\REM_Dream_validation_20261011`. No Fallout NV/REM1 Legacy runtime DLL/ESP, IDA database, game asset archive, or existing Bevy B001 implementation source was modified.

## Source identity

| Repository | Checked-out SHA |
|---|---|
| LibertyCraft `mrborghini/libertycraft` | `18ccef417a93e29332abb5dfcf8005b2f8928376` |
| MW2/Skate 3/Minecraft Rust mashup `chasmlol/2010-rust-rewrite-mashup` | `f608f85e407ff1b7689d54a9aafdd16e95711ac4` |

Relevant upstream source hashes, SHA256:
- `LibertyCraft/asi/src/DriveLogic.h`: `16B73025F6B6DB3507102D3D3161E39EE0F73E657BB8AD2597D73FE30227A81E`.
- `RustMashup/crates/render_anim/src/skate/rails.rs`: `B33D1070B69CC0B998C0EC1157C038FEF0CE454A6C0E8C934FC902A1212DD215`.

## V01 LibertyCraft portable C++ suites — PASSED with specified exception

Used the installed Microsoft Visual Studio 18 BuildTools MSVC compiler in a developer-command environment; `cl /nologo /std:c++17 /EHsc /W3` and upstream `asi/tests/` sources. Directly launched the compiled test executables on Windows.

| Test executable | Source provenance / purpose | Verdict |
|---|---|---|
| `drive_test.cpp` | Original `DriveLogic.h` pure movement/vehicle/cutscene/ragdoll handoff tests | **PASS**, exit 0, `drive_test: all passed` |
| `scene_test.cpp` | Scripted scene control | **PASS**, exit 0 |
| `combat_test.cpp` | Portable hit and damage math | **PASS**, exit 0 |
| `body_test.cpp` | Body/attachment math | **PASS**, exit 0 |
| `hazard_test.cpp` | Hazards | **PASS**, exit 0 |
| `overlay_test.cpp` | Overlay logic | **PASS**, exit 0 |
| `render_test.cpp` | Portable rendering math | **PASS**, exit 0 |
| `collision_test.cpp` unchanged | Original geometry implementation under this MSVC version | **BUILD BLOCKED**: `Geometry.h` lines 914/915, C3493 local constexpr `G` cannot be implicitly captured by `[]` lambdas |
| `collision_test.cpp` with isolated two-line test-only compatibility patch | Replace *only* `auto clampLo = [](float v)` and `auto clampHi = [](float v)` with `[=]` captures. Rebuild and execute original collision fixtures | **PASS**, exit 0, `collision_test: all checks passed` |

The patched collision test printed synthetic examples for spawn/building, overpass, stairs, object probes for lamp post/bench/bin, doors, and material classes; these exercise source collision geometry and sampling, not running GTA world collision.
**Important:** Collision success is conditional on the two-line compiler adaptation, *not* an unmodified-upstream compiler pass. The header was restored after the test. Clone tracked state returned clean after compiler-created `.obj` files were removed.

The `link_test.cpp` suite was not compiled or executed (its original `LinkCore.h` requires Clang/GCC `__atomic` builtins; user requested single-process Bevy, so protocol test is not prerequisite for the target architecture).

`drive_test.cpp` covers default mode, manual toggle, vehicle requests, retry/timeout, paused timers, scripted vehicle entry, post-vehicle handback, cutscene/loading, death, ragdoll recovery and synthetic bumper/prop-hit classes. **Those are LibertyCraft policy tests**; they do not prove the original GTA IV game-state fields or all native call conditions.

## V02 MW2 skating rail detector with REM1-compatible maths — PASSED

Compiled unmodified `crates/render_anim/src/skate/rails.rs` by source path in a tiny authored Rust crate. Its `bevy::math::Vec3` is provided through `bevy_math = 0.20.0` (target REM1 B001 uses Bevy 0.20) without compiling the entire IW4L runtime. Rust/Cargo stable 1.99.0; Cargo used `--offline`. No game assets required.

Six unit fixtures executed against the **original upstream rail-detection function**, all PASSED with exit code 0:
1. Empty triangle world -> no rails.
2. Vertical wall -> no walkable lip/rail.
3. Small platform (below rail-length threshold) -> no completed rail.
4. Large horizontal platform -> usable edge rails, and the interior triangulation diagonal is not treated as a grind lip.
5. Reversed/downward winding -> rejected.
6. Generated endpoint coordinates are finite.

Verbatim result: `test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s`.

Harness (permissible authored test code only) is committed under `research/validation/bridges_20261011/`; the upstream rail file is **not committed**. Reproduction instructions there fetch the exact pinned upstream source and place it locally as an ignored fixture.

This test confirms **algorithm-level geometry suitability**, not full imported Fallout terrain, dynamic prop streaming, high-speed skater contact, THUG2-specific grind eligibility, source-game runtime or complete Bevy integration.

## V03 MW2 movement authority — SOURCE REVIEW ONLY

Source: `crates/render_anim/src/skate.rs`. Confirmed:
- epoch-tagged `Job::Activate`, `Job::Step`, `Job::Suspend`;
- reply-gated activation and `set_external_motion(..., true)` only after activated response;
- `stop` disables external motion, invalidates pending epoch, sends `Suspend`, clears mode camera/pose state;
- stale epoch replies ignored and disconnected workers stop mode and are eligible for new session preload;
- map change and player death force mode stop.

**Not executable-validated here:** full worker scheduling/thread interleavings, pose publication, live Skate 3 runtime sessions, rendering or gamepad input against real hardware. These source-level invariants need dedicated isolated Bevy/Opus integration tests and Codex verification; do not mark whole MW2 skating physics as passed.

## V04 REM1 B001 compatibility and gaps

Reviewed `implementation/bevy-slice-chat-20261010` (`bevy/README.md`, `bevy/docs/CURRENT_STATE.md`, `bevy/src/input.rs`, `bevy/src/physics.rs`). B001 report records 8/8 scripted run checks, Rapier fixed 60Hz, action input and keyboard/gamepad mappings, but no real game rigs, imported maps, GTA on-foot motor, THUG2 skate motor, or genuine collision data. Its Xbox path lacks real-device verification.

- **Validated by this pass:** isolated `rails.rs` compiles/runs with target Bevy 0.20 maths; LibertyCraft portable handoff tests pass.
- **Not validated:** integration with REM1 B001 ECS and Rapier update ordering, collision masks, Niko rig/transitions, Fallout quest ownership, GTA IV/TBoGT native timing, original THUG2 skating physics, or actual in-game terrain and vehicle interactions.
- **Not conducted:** original GTA executable research in IDA Pro 6.8; no GTA IV/FO3 binaries read. The public LibertyCraft sources are evidence of how *that bridge* was built, not a source-verified mapping of *all GTA IV mechanics*.

## Acceptance gates for implementation

1. Build an independent Bevy authority arbitration test where only one of GTA-on-foot, vehicle, skate, ragdoll recovery and scripted dialogue may write player root/camera per fixed tick, and all mode changes preserve saved gameplay state.
2. Test stale activation responses, worker panic/disconnect, cancellation on death/map transition, and resume after pause. Use real concurrent task/epoch scheduling, not only a fake state machine.
3. Import a **small legitimate owner-supplied Fallout 3 collision region** with source transform metadata; test ground, ledge, curb, railing, staircase, moved prop and destroyed prop with physics and grind classifier.
4. Physically test Xbox controller alongside KBM through enter vehicle -> drive -> bail/ragdoll -> recover -> shoot -> interact with Fallout NPC -> skateboard equip/skate -> exit.
5. Have Codex check GTA IV/TBoGT walk/run/sprint, vehicle entry/exit and ragdoll game-state fields/call predicates with IDA Pro **6.8** on locally hashed binaries. Do not label LibertyCraft constants or its debug flags as GTA IV ground truth.
6. Hand Opus only isolated interface design/test evidence; implementation remains Opus-owned on Bevy branch. Keep all Legacy v85 protected assets and existing B001 code unchanged.

## Evidence retention

Local workspace: `D:\REM_Dream_validation_20261011\`.
- `LibertyCraft/asi/tests` and `RustMashup/crates/render_anim/src/skate` are pinned public Git checkouts.
- `validation_results.txt` retains condensed original process exit codes.
- `*_compile.log` records compiler outputs, including the unpatched collision compile error.
- `rust_target/debug/deps/mw_collision_checks-*.exe` is the isolated Rust test executable, not a distributable game runtime.
- GitHub `research/validation/bridges_20261011` retains an authored standalone reproduction harness. Avoid committing the licensed third-party source copies or proprietary game assets into REM1.

**Verdict:** PASS for the tested portable LibertyCraft handoff/math suites and tested MW2 rail algorithm, with documented MSVC compile adaptation for collision; NOT YET VALIDATED for original GTA IV game parity, runtime Skate 3/THUG2 physics, or native REM1 Bevy gameplay integration.

## V05 Fresh checkout of committed validation harness — PASSED

After committing the authored `research/validation/bridges_20261011/` harness, independently cloned the REM1 **research branch** into the isolated `D:\\REM_Dream_validation_20261011\\RemResearchValidation` folder, sparse-checked out the harness, copied the unchanged upstream `rails.rs` to the ignored `src/rails_external.rs`, and ran `cargo test --offline -- --nocapture` using the isolated `D:` target directory. Result: **six passed, zero failed; exit code 0**. This confirms the precise committed test harness works as documented, not just the initial scratch harness. Compiled dependencies `bevy_math =0.20.0` and `glam =0.33.12` were taken from the Windows cargo cache.
