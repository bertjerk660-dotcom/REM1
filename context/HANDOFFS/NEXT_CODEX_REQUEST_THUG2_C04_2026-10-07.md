# NEXT CODEX REQUEST — THUG2 C04 Master Skate State / Movement / Physics Evidence

Use this as the **next THUG2 Codex investigation request** for the Fallout New Vegas + Garry's Mod + THUG2 project.

## Role boundary — mandatory

You are **Codex**, the investigation / reverse-engineering / evidence agent.

You are **NOT** the implementation agent.

**Claude Opus is the sole implementation/integration owner.**

Do **not**:
- write or modify the final Fallout/xNVSE gameplay implementation;
- port THUG2 gameplay code into Fallout;
- implement the skate state machine;
- implement physics/collision adapters;
- retarget or integrate animations;
- move the board to the feet;
- build or render the THUG2 HUD;
- create/recreate visual assets;
- convert models for final use;
- write final camera code;
- alter the deployed DLL/ESP;
- deploy or promote a runtime candidate;
- fix the current grind bug in Fallout directly.

Your job is to recover and document enough original THUG2 behavior that **Opus can implement it without guessing**.

You may create investigation scripts, evidence manifests, function maps, call graphs and documentation needed to prove the source behavior.

Where native reverse engineering is required, use **IDA Pro 6.8 only**.

## Canonical repository / branch

Repository:
`bertjerk660-dotcom/REM1`

Use canonical `main` for durable project truth and read the latest preparation branch:
`prep/opus-ready-20261007`

Before investigation, read:
- `AGENTS.md`
- `context/BOOTSTRAP.md`
- `context/GOAL.md`
- `context/ARCHITECTURE.md`
- `context/CURRENT_STATE.md`
- `context/DECISIONS.md`
- `context/FAILURE_KNOWLEDGE.md`
- `context/AGENT_OWNERSHIP.md`
- `context/OPUS_READINESS_BOARD.md`
- `context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md`
- `context/HANDOFFS/CODEX_C04_THUG2_STATE_PHYSICS_2026-10-07.md`
- existing THUG2 staging/evidence manifests already in the repository.

Inspect the actual local THUG2 files/executable/decompiled evidence before trusting old notes. Record exact hashes for the analyzed executable/data where practical.

Create a traceable evidence branch such as:
`codex/thug2-c04-state-physics-20261007`

Do not merge runtime candidates.

## Why C04 is next

C04 is the state-vocabulary dependency hub for:
- C05 camera;
- C06 animation and board attachment;
- C07 HUD/scoring;
- C08 unified input;
- Opus package O05 THUG2 core movement/state/physics.

Current Fallout integration has a human-verified failure where pressing **G can grind anywhere**. This must be explained by identifying the original THUG2 eligibility chain, not by patching the Fallout implementation in this task.

## Investigation objective

Recover the **source-faithful THUG2 free-roam skating state machine, movement/physics rules, collision/eligibility queries and cross-system state outputs** needed for Opus to implement THUG2 skating inside the Fallout world.

Do not investigate THUG2 campaign/story/mission/NPC progression except where a free-roam skating function cannot be understood without a small dependency.

## Required state-machine evidence

Trace the master free-roam skater state machine and, at minimum, identify the actual states/substates/transitions for:

- skate idle;
- push;
- coast;
- ground movement;
- turn/carve;
- crouch;
- ollie/pop;
- air/fall;
- landing;
- braking/deceleration;
- manual entry/loop/exit/fail;
- grind detection/eligibility/acquisition/snap/alignment/loop/balance/exit;
- lip eligibility/state;
- wallride/wallplant eligibility/state;
- revert;
- bail/fall-off;
- recovery/get-up where part of free-roam;
- board break/recovery if reachable in ordinary skating;
- walking/board-carry/mount/dismount states if the original free-roam controller uses them.

For each state/transition, capture:
- source file/module and function/class when available;
- IDA 6.8 address/signature when native;
- caller/callee relationship;
- entry preconditions;
- sampled inputs/actions;
- collision/world-query preconditions;
- important state variables;
- calculations/constants;
- outputs/state mutations;
- transition condition;
- animation event/state emitted;
- camera event/state emitted;
- HUD/scoring/audio event/state emitted;
- cleanup/exit behavior;
- confidence;
- unresolved ambiguity.

## Required movement / physics evidence

Recover and document the real behavior for:
- acceleration;
- push impulse / push cadence;
- momentum retention;
- friction / drag;
- speed caps;
- braking;
- heading;
- turning / carving;
- board orientation;
- ground normal / slope handling;
- gravity / airborne update;
- ollie/pop impulse;
- landing acceptance;
- air-to-ground transition;
- any timestep or frame-rate assumptions;
- any unit/coordinate assumptions that Opus must adapt to Fallout.

Do not substitute Fallout movement values.

## Required collision / world-query evidence

Identify the exact queries and result fields used to determine:
- ground contact;
- surface normal;
- slope validity;
- wall contact;
- ledge/rail/grind candidate;
- grindable geometry;
- grind direction / tangent;
- snap/acquisition distance;
- lip eligibility;
- wallride/wallplant eligibility;
- landing;
- bail/collision response.

For each query, record what the original engine provides and what the Fallout host adapter must provide.

If a native query boundary cannot be fully recovered, define the missing contract precisely instead of inventing the behavior.

## Grind-anywhere failure analysis

Produce a direct evidence-based delta for the current Fallout failure:

**Observed:** pressing G can enter grind state anywhere.

Determine:
1. what THUG2 checks before grind entry;
2. which geometry/contact/state requirements are mandatory;
3. whether grind is input-triggered, contact-triggered or both;
4. how candidate rails/edges are selected;
5. how direction, position and board alignment are established;
6. how invalid attempts are rejected;
7. what exact original chain the current Fallout implementation is missing.

Do **not** modify the Fallout code. Return the evidence and the missing adapter contract for Opus.

## Cross-system outputs

C04 must define stable source-derived vocabulary that later C05/C06/C07/C08 investigations can reuse.

Explicitly list:
- state IDs/names;
- movement variables;
- balance variables;
- airborne/landing variables;
- grind/manual/lip state;
- board orientation;
- speed/heading;
- trick/state events that camera needs;
- animation-selection events;
- HUD/scoring events;
- audio events;
- input-action gates.

Do not invent friendly names without preserving the original identifier/address/reference.

## Required deliverables

Produce exactly these durable outputs:

1. `context/CODEX/THUG2_C04_SKATE_STATE_PHYSICS_EVIDENCE_2026-10-07.md`
2. `build/evidence/thug2_c04/master_state_machine.json`
3. `build/evidence/thug2_c04/movement_physics_map.json`
4. `build/evidence/thug2_c04/collision_query_contract.json`
5. `build/evidence/thug2_c04/grind_manual_lip_eligibility.json`
6. `build/evidence/thug2_c04/opus_world_adapter_contract.json`

Also record:
- analyzed executable/data SHA256 values;
- evidence source paths;
- IDA database/input identity where applicable;
- unresolved dependencies;
- confidence per major finding;
- evidence branch and final commit SHA.

## Opus interface contract requirements

The final `opus_world_adapter_contract.json` must tell Opus what interfaces to implement, not implement them for Opus.

For each host-facing requirement specify:
- purpose;
- THUG2 caller/state;
- required input;
- required output;
- units/coordinate semantics;
- lifetime/state ownership;
- failure/invalid result behavior;
- whether it is required synchronously per frame;
- dependencies on later C05/C06/C07/C08 evidence.

Examples of interface categories:
- ground probe;
- collision sweep/raycast;
- grind candidate query;
- surface-normal/tangent query;
- stable target/reference identity;
- timestep;
- mode-owned action state.

Do not write the FNV adapter implementation.

## Evidence quality rules

A state/function name alone is not sufficient.

Do not mark a behavior proven unless you can tie it to one or more of:
- decompiled source/body;
- caller/callee evidence;
- data tables;
- native disassembly;
- resource/state usage;
- repeatable observed behavior where appropriate.

Separate:
- PROVEN;
- STRONG INFERENCE;
- UNRESOLVED.

Do not turn an inference into an implementation requirement without labeling it.

Do not claim 1:1 behavior merely because the current Fallout implementation looks similar.

## Stop condition

Stop when **Opus can implement the THUG2 core free-roam state/movement/physics layer without inventing movement rules, grind/manual/lip eligibility, collision semantics or state transitions**.

Do not continue into final implementation.

Do not retarget animations.

Do not build the camera.

Do not build the HUD.

Do not deploy Fallout.

At completion, report:

| Gate | Status | Commit | Remaining blocker | Opus package unlocked |
|---|---|---|---|---|
| C04 | COMPLETE or PARTIAL | SHA | exact missing evidence | O05 only if COMPLETE |

If C04 remains PARTIAL, state exactly why and stop. Do not hide missing evidence by implementing an approximation.
