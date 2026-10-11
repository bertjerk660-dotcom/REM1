# REM Dream — MW2 Rust mashup + LibertyCraft evidence review
Date: 2026-10-11
Track: independent REM1 Bevy successor + planned Fallout 3/GTA IV/TBoGT REM Dream expansion
Status: STATIC SOURCE REVIEW ONLY — no binary reverse engineering, IDA execution, build, import, runtime test, or source integration conducted in this pass
Owner: normal ChatGPT research/workflow lane; Codex investigates/tests and verifies game mechanics with IDA Pro 6.8; Opus implements and integrates

## Source identities and scope

- MW2 + Skate 3 + Minecraft Rust mashup: https://github.com/chasmlol/2010-rust-rewrite-mashup at main SHA `f608f85e407ff1b7689d54a9aafdd16e95711ac4` (reviewed 2026-10-11).
- LibertyCraft: https://github.com/mrborghini/libertycraft at main SHA `18ccef417a93e29332abb5dfcf8005b2f8928376` (reviewed 2026-10-11).
- REM1 Bevy reviewed on `implementation/bevy-slice-chat-20261010` SHA `3a7878ceb0db8ee676176569278c55460b91e863`. Its current B001 report is `bevy/docs/CURRENT_STATE.md`. This research branch is based on that ref, not main. Do not change legacy runtime or claim this branch is merged.
- The MW2 project uses IW4L Rust, including Bevy 0.19 ECS systems/resources. Its local Skate 3 adaptation also uses Bevy 0.19. REM1 B001 pins Bevy 0.20, so direct source drop-in is not promised.
- LibertyCraft's on-screen host is *running GTA IV 1.0.8.0* and its physics/input state owner is an independently running Minecraft process; this is not a source port of GTA IV to Rust.

## Findings from MW2 Rust (evidence -> architectural lesson)

### M01: Bevy ECS integration and isolated movement authority — VERIFIED BY CODE REVIEW

Source: [crates/render_anim/src/skate.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/render_anim/src/skate.rs).

- `register` installs Bevy resources `SkateMode`, `Host` and the `update` system with explicit schedule ordering.
- Worker protocol is `Job::{Activate(epoch, spawn, yaw, aspect), Step(epoch, dt, input, aspect), Suspend}` and `Reply::{Ready, Activated, Pose, Error}`.
- The mode adapter sets external-motion authority only after an activation reply; when stopping, it returns authority to baseline movement via `set_external_motion(..., false)`, clears mode camera/bones/status, and suspends the retained worker.
- `epoch` is incremented on stop/activation; pose/activation replies with old epochs are rejected. Worker disconnect/error triggers stop and attempts a fresh session rather than permanently stranding the player in skate mode.
- Per-map session is preloaded and retained; exiting skate mode does not destroy animation banks/graphs/collision. It checks map changes and player death before presenting.
- The simulation `collect` + `advance` uses a bounded accumulator (0.15s cap) and the session's `period()`. Avoid equating this with REM1's fixed 60Hz Rapier step without studying the actual skate runtime period.
- Same active physical gamepad used for base movement is converted into XInput-like `InputFrame`; gameplay input is suspended if blocked.

**REM application:** use Bevy action input and explicit one-owner motor/camera/animation state, versioned transition requests, late-response protection, fail-safe restoration and session caching. Do **not** copy Skate 3 physics as a substitute for THUG2 or Niko behavior.

### M02: collision is independent of rendered geometry — VERIFIED BY CODE REVIEW

Sources: [skate/collision.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/render_anim/src/skate/collision.rs), [skate/rails.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/render_anim/src/skate/rails.rs), [skate.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/render_anim/src/skate.rs).

- `extract` gathers playable collision from clip triangles, brushes, and static-model collision, rejecting degenerate/non-finite triangles and duplicate faces.
- It explicitly uses collision, not visible meshes: invisible clips and solid props still block the changed movement controller.
- Coordinate contract `to_skate(p) = (p.x, p.z, -p.y) * 0.0254`; inverse restores IW4 space; a unit round-trip check exists. This **specific** mapping is IW4/Skate-specific and not a Fallout/GTA-to-Bevy transform.
- `rails::find` examines upward-facing collision faces, samples the outside of candidate edges for a ground drop and absence of a wall, merges collinear surviving edges, and chains runs into polylines. This avoids universal grinding.
- Minecraft collision is gathered around the skater and rebuilt in another thread when blocks change nearby or the skater moves outside the prepared region. A new collision batch is installed from the result.

**REM application:** create ONE collision-world reference containing Fallout terrain, statics, dynamics, actor bodies, vehicles and prop colliders. Build the grind-eligibility/rail index from stable collision or curated authored rails, with explicit validation that rails are real and not arbitrary geometry. Use dynamic-collider invalidation for moved/destroyed props. Collision read access must never allow a separate skate motor to contradict the authoritative world.

### M03: skeleton, attachment and source-owned assets — VERIFIED BY CODE REVIEW

Sources: [skate/rig.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/render_anim/src/skate/rig.rs), [docs/SKATE.md](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/docs/SKATE.md), [launcher/first_run.rs](https://github.com/chasmlol/2010-rust-rewrite-mashup/blob/main/crates/launcher/src/first_run.rs).

- `rig::pose` maps named skating joints to a soldier skeleton using a reference bind rig and source pose; unrepresented helper/equipment bones are inherited via mapped parent attachments.
- `rig::board` separately transforms the skateboard mesh from the source rig. There is a documented issue with invisible skateboards on some maps, so treat attachment as a failure-sensitive integration point, not solved in general.
- First-run setup searches owned MW2 data and optionally extracts Skate 3 materials from the user's own `default.xex` and adjacent `data/` using a converter; no proprietary game data needs to be in the public source repository.

**REM application:** define Niko rig/profile, Fallout NPC rig/profile, THUG2 skater rig/profile and prop attachment points separately. Validate visual pose, root motion and board hand-to-feet transfer independently. Use local, owner-supplied game assets, deterministic extraction manifests and hashes; do not commit proprietary game assets.

## Findings from LibertyCraft (evidence -> architectural lesson)

### L01: explicit authority handoff and recovery state machine — VERIFIED BY CODE REVIEW

Sources: [asi/src/DriveLogic.h](https://github.com/mrborghini/libertycraft/blob/main/asi/src/DriveLogic.h), [asi/src/HostDrive.cpp](https://github.com/mrborghini/libertycraft/blob/main/asi/src/HostDrive.cpp), [asi/tests/drive_test.cpp](https://github.com/mrborghini/libertycraft/blob/main/asi/tests/drive_test.cpp).

- The *pure* `drive::Logic` module decides whether Minecraft or GTA IV owns the on-foot player. It separates `Mode::{kMinecraft,kNiko}` from host-reason `Why::{kNone,kNikoMode,kVehicle,kCutscene,kRagdoll,kScript}`.
- Input captures loading/death/paused, vehicle entry, scripted scenes, whether the host reads controls, self-motion, ragdoll and upright checks. Output explicitly reports `hostDrives`, `inVehicle`, `resync`, control presses and recovery conditions.
- Vehicle entry gives control back to GTA for actual door/carjacking logic; its code waits for standing readiness and retries button edges when needed. Vehicle exit/bail/knockdowns retain GTA ownership until a stable upright/on-foot period, with timeout safety caps. GTA-to-Minecraft resynchronization is done when returning ownership.
- These are *LibertyCraft bridge policy timings*, NOT canonical GTA IV physics constants. Reuse the state categories and tested invariants; reproduce exact Niko mechanics only after GTA IV/TBoGT IDA 6.8 evidence.
- `asi/tests/drive_test.cpp` tests the pure transition logic with synthetic frame sequences, including toggles, scripted vehicle entry, and resync.

**REM application:** one `ControlAuthority` state in Bevy (DefaultExploration, GTAOnFoot, GTAVehicle, Skate, ScriptedScene, RagdollRecovery, MenuPause). Only one motor can write the player root each simulation step. Enter/exit includes snapshot/restore for camera, HUD, input map, inventory/equipment and physics flags. Resume only from a valid settled pose; save/load and death forcibly resolve ownership.

### L02: coordinate contract covers axes AND rotation — VERIFIED BY CODE REVIEW

Source: [asi/src/Coords.h](https://github.com/mrborghini/libertycraft/blob/main/asi/src/Coords.h).

- GTA IV to Minecraft uses `(x,z,-y)` and inverse `(x,-z,y)` at 1 metre:1 block, in that project's conventions.
- The module also translates heading/yaw with `h = 180 - yaw`, pitch signs and camera basis; angle conversion is as critical as positions.

**REM application:** establish a *new* Fallout3/GTAIV/THUG2/Bevy reference-frame specification with unit scales, handedness, yaw/pitch convention, forward/up axes, bone-space transforms and ground-height origin. Test round trips for vectors, orientations, velocities, normals, rays, physics impulse and camera forward; do not import LibertyCraft's transforms unchanged.

### L03: streaming collision and dynamic objects — VERIFIED BY CODE REVIEW

Sources: [asi/src/Collision.cpp](https://github.com/mrborghini/libertycraft/blob/main/asi/src/Collision.cpp), [asi/src/collision](https://github.com/mrborghini/libertycraft/tree/main/asi/src/collision), [protocol header](https://github.com/mrborghini/libertycraft/blob/main/protocol/libertycraft_protocol.h).

- GTA terrain collision is sampled in player-centred regions, pre-requested before probing, generated off thread and pushed to the movement owner. Columns have stale/empty retry states, epochs and invalidation.
- Nearby dynamic world objects and moving props are tracked independently, because a static terrain cache is insufficient for interaction. Water is a separate sampled region.
- The protocol header has explicit collision rings, actor table and event messages.

**REM application:** Bevy should use one physics authority (B001 already wraps Rapier3D), not two games exchanging triangles. Preserve *concepts* of streamed world-cell loading, collision readiness, dynamic prop refresh, content masks and versioned jobs. Prefer preconverted Fallout 3 collision and directly registered Rapier shapes over per-frame GTA-ray scraping.

### L04: combat, mission scripts and damage have their own ownership rules — VERIFIED BY CODE REVIEW

Sources: [asi/src/Combat.cpp](https://github.com/mrborghini/libertycraft/blob/main/asi/src/Combat.cpp), [asi/src/Missions.cpp](https://github.com/mrborghini/libertycraft/blob/main/asi/src/Missions.cpp), [asi/tests](https://github.com/mrborghini/libertycraft/tree/main/asi/tests).

- LibertyCraft bridges GTA peds/vehicles into records/events so Minecraft attacks can hit GTA actors and GTA-caused damage can affect the Minecraft player.
- It explicitly observes scripted scenes and distinguishes mission actors from ambient actors to avoid corrupting story mechanics.
- It has unit tests for combat, collision, scene and link logic as well as drive logic.

**REM application:** make Bevy damage and AI state authoritative. GTA guns must use a shared attack/damage/event interface so hits reach Fallout enemies, armor and quests; avoid separate GTA and Fallout health values. Quest/dialogue/trade scenes should temporarily own player input/camera and resume GTA movement cleanly.

### L05: the shared-memory protocol is mostly NOT a Bevy target — VERIFIED BY CODE REVIEW

Sources: [protocol/libertycraft_protocol.h](https://github.com/mrborghini/libertycraft/blob/main/protocol/libertycraft_protocol.h), [asi/src/LinkCore.h](https://github.com/mrborghini/libertycraft/blob/main/asi/src/LinkCore.h).

- Current LibertyCraft needs shared memory, per-side monotonic timestamps, seqlocks, SPSC event/collision rings, heartbeats and overlay frame buffers because Minecraft and GTA IV are separate processes.
- REM Bevy runs all systems in a single process with one ECS world. It does *not* need the bridge file, 191MiB mapping, per-engine heartbeat or overlay pixel copying.
- The transferable idea is explicit data contracts, freshness/epoch validation and bounded producers/consumers for heavy background work.

## Mapping to current REM1 B001 (what exists vs what is proposed)

B001 documented and reviewed at [bevy/docs/CURRENT_STATE.md](https://github.com/bertjerk660-dotcom/REM1/blob/implementation/bevy-slice-chat-20261010/bevy/docs/CURRENT_STATE.md), [bevy/src/input.rs](https://github.com/bertjerk660-dotcom/REM1/blob/implementation/bevy-slice-chat-20261010/bevy/src/input.rs), [bevy/src/physics.rs](https://github.com/bertjerk660-dotcom/REM1/blob/implementation/bevy-slice-chat-20261010/bevy/src/physics.rs).

| Requirement | Existing verified/documented | Next proposed interface |
|---|---|---|
| Movement authority | B001 simple kinematic movement and `ControlOwner::{Gameplay,Menu}` | Separate gameplay motor authority from UI input ownership; one active movement writer |
| Fixed simulation | B001 Rapier 60 Hz wrapper | Explicit fixed-step order: actions -> authority transition -> controller -> collision -> animation/camera -> HUD |
| Collision | B001 arena and props | Authored/imported Fallout 3 collision chunks, dynamic object invalidation, rail/contact eligibility |
| Device mapping | Actions from keyboard/controller; scripted injection | GTA movement, car controls, THUG2 trick actions, GMod tools with mode-specific contexts; *physical Xbox pad testing pending* |
| Asset system | Placeholder primitive meshes | Import provenanced Niko/FO3/THUG2 rigs and animations via local converter |
| Runtime validation | B001 scripted 8/8 pass documented; no human playtest | Cross-mode and Xbox regression pack; full world/quest/vehicle/animation gates |
| World | Test arena only | Fallout 3 region and core exploration/quest behaviour; TBoGT and GTA IV weapon/vehicle content only after scope/content validation |

**Important:** B001's report is the existing branch's claim based on its run artifacts (local D:), not a new build performed in this research pass. The REM1 main branch is older. Do not infer any integration of GTA, Fallout 3, MW2, Skate 3 or LibertyCraft source into B001.

## Proposed Bevy system contracts for Opus (design, not implemented)

1. **Authority/mode:** `PlayerMode` + `TransitionRequest` + `TransitionEpoch` and `PlayerSnapshot`; distinct `ControlOwner` for gameplay vs menu; reject stale asynchronous state; cancel on death/level load/unload.
2. **Motion:** `MotorProfile` with default Fallout movement, source-evidenced GTA IV/Niko on foot, THUG2 skating, vehicle seat/driver, ragdoll recovery. Only active motor writes root pose. No host executable runs beside Bevy.
3. **Transforms:** `CoordinateProfile` maps input-source file conventions to Bevy Y-up for vertices, normals, poses, velocities, forward/right/up, camera, collision and bone bind-space, with reversible tests.
4. **Physics:** Rapier is authoritative. `CollisionLayer` and `WorldCellCollision`, `DynamicPropCollider`, `VehicleCollider`, `RailSegment`, `GrindEligibility`; no automatic grind on keypress without valid spatial contact.
5. **Visuals:** Skater/niko animation graph and rig adapter, root-motion arbitration and attach/detach slots (hands/feet/weapons/vehicle seat). Visible board in hand and under feet separately validated.
6. **Combat:** `DamageEvent`, `HitTarget`, faction/armor/resistance rules, impulse/ragdoll events; Fallout AI/quest consequences use the same pipeline for GTA/TBoGT and Fallout arms.
7. **World:** region streaming with stable entity IDs, deterministic asset provenance, collision/navmesh/water content, and save/load restoration of state.

## Priority evidence tasks for Codex (NOT implementations)

- **C-BRIDGE-01:** review pinned `skate.rs` and `skate/collision.rs` thoroughly; produce sequence diagram of activation->motor handoff->pose publication->stop/error, with tick/epoch ordering and failure cases. Identify what's generic and what's tied to IW4L/Skate 3. Source citations with commit SHA + path + lines.
- **C-BRIDGE-02:** reconstruct `DriveLogic.h` pure state machine and `drive_test.cpp` assertions into a transition matrix: walk->vehicle->bail->ragdoll->walk, scripted scene and exit, pause, death, save/load. Distinguish bridge policy constants from source GTA IV behaviour.
- **C-BRIDGE-03:** reconcile external collision transform conventions with REM Bevy Y-up and actual Fallout 3 and GTA IV data axes. Derive reversible transform matrices; prove with reference positions/orientations and collision ray fixtures.
- **C-BRIDGE-04:** in local IDA Pro 6.8 investigate exact Niko walk/run/sprint, vehicle entry/exit, damage, ragdoll and GTA IV/TBoGT weapon hit behaviour. Record binary versions/hashes, game fields, caller predicates, function evidence and negative cases. No guess becomes a proven GTA mechanic.
- **C-BRIDGE-05:** test a pure Bevy authority prototype in an isolated branch, compare against approved fixtures, and hand failures to Opus. Codex owns validation; Opus implements.
- **C-BRIDGE-06:** review licensing/provenance and installation/data availability. Never commit proprietary game content or a copied GPL module without explicit license review.

## Proposed regression/acceptance scenarios (not yet run)

- R01 Normal walk -> GTA/Niko on-foot movement -> normal with position/velocity/camera/input restored; no two controllers moving the same entity.
- R02 In Niko mode enter car -> drive -> exit; verify collision, seat transform, weapon/UI/animation and control handback.
- R03 Bail from moving car -> ragdoll -> full stand -> Niko movement; no instant reactivation mid-ragdoll.
- R04 GTA weapon hits Fallout NPC, resistance and quest hooks update once (not twice); NPC attacks Niko and damage/knockback is coherent.
- R05 Quest dialogue/trade pauses the movement motor, uses Fallout menu input, then returns Niko movement/voice/camera without stuck key.
- R06 Skateboard equip/hand display -> LMB THUG2 skate -> grind ONLY on confirmed rail/contact -> holster restores default; original THUG2 behaviour requires separate IDA validation.
- R07 Worker failure, map unload, save/load, death, pause during transition -> no stale pose, permanent external motor, invisible board, duplicated input or lost inventory.
- R08 Transform roundtrip for vectors/quaternions/matrices/collision normals, forward axes, scale and root motion.
- R09 Controller, keyboard/mouse, switch devices mid-vehicle/mid-skate; same actions, no menu-input leak.
- R10 Collision stream enters/leaves world cell; no falling through not-ready terrain; moving prop, destroyed prop and dynamic rail invalidate correctly.
- R11 Distinct source game installation and asset provenance manifests; no proprietary binary/asset committed to GitHub.

## Licensing, evidence levels and exclusions

- MW2 mashup top-level workspace indicates Apache-2.0; bundled Skate subsystem and assets include other dependency/ownership considerations. It embeds source-evidenced and reverse-engineering-informed work. Verify subtree license and compatibility before copying any source.
- LibertyCraft root `LICENSE` is MIT, but `asi/LICENSE` is GPL-3.0, and the README explicitly calls out the IV-SDK component. Do not assume all source is MIT or copy ASI into the Bevy binary without license review.
- Original game data is proprietary. Private, legitimately sourced originals may be used for authorized analysis and local import; rights to distribute the completed game are a separate question.
- No IDA Pro 6.8 was opened by this source-review pass. No executable, files or game data were downloaded to the user's Windows PC and no Rust build or game behaviour was personally tested. Findings labelled VERIFIED mean *observed in public repository source*, not validated against original GTA IV, Skate 3, MW2 or THUG2 runtime.
- Preserve the distinction: **Skate 3 is not THUG2**; **LibertyCraft's host GTA IV is not independently recreated GTA IV code**; **a successful MW2 Bevy subsystem does not imply direct compatibility with Bevy 0.20 or REM1 physics**.

## References / follow-up indexes

- MW2 skating: `crates/render_anim/src/skate.rs`, `skate/collision.rs`, `skate/rails.rs`, `skate/rig.rs`, `docs/SKATE.md`, `crates/launcher/src/first_run.rs`.
- LibertyCraft: `asi/src/DriveLogic.h`, `HostDrive.cpp`, `Coords.h`, `Collision.cpp`, `Combat.cpp`, `Missions.cpp`, `LinkCore.h`, `protocol/libertycraft_protocol.h`, `asi/tests/drive_test.cpp`.
- REM1 Bevy: `context/BEVY_PARALLEL_TRACK_DECISION_2026-10-10.md`, `bevy/README.md`, `bevy/docs/CURRENT_STATE.md`, `bevy/docs/DECISIONS_AND_FAILURES.md`.
