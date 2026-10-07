# Codex C04 — THUG2 master skate state machine and movement/physics investigation

## Objective
Recover and document the source-faithful THUG2 free-roam skating state machine, movement and physics needed for **Claude Opus** to implement THUG2 gameplay inside the Fallout world.

Codex investigates; Opus implements; Codex later validates the live result after Opus implementation.

## Scope
Focus on ordinary free-roam skating systems, not THUG2 maps, missions, story, dialogue, NPC population or campaign progression.

Use the staged THUG2 source/decompilation evidence first. Use IDA Pro 6.8 only for behavior not sufficiently exposed by existing decompiled/script/data evidence.

## Required behavior map
Trace at minimum:
- master skater state machine;
- ground, air, crouch, ollie/pop, landing;
- acceleration, momentum, friction, drag, speed caps and braking;
- turning/carving/heading/board orientation;
- slope/ground-normal handling;
- push/coast logic;
- manual entry/loop/exit/fail conditions;
- grind detection, valid geometry/contact, acquisition/snap/alignment, loop, balance and exit;
- lip state;
- wallride/wallplant state;
- revert;
- bail/fall-off/recovery where part of free-roam;
- board break/recovery state if reachable in normal skating;
- transitions into/out of walking if the selected runtime uses it;
- collision/world queries required from the host;
- all state variables shared with animation, camera, audio, scoring and HUD.

## Questions
1. What are the primary state enums/classes/functions and transition conditions?
2. Which inputs are sampled in each state?
3. Which world/collision queries determine ground, wall, edge, rail and landing eligibility?
4. What units/scales/timesteps are assumed?
5. Which state variables control speed, heading, balance, airborne time and board orientation?
6. Which transitions are physics-driven versus input-triggered?
7. Why is the current FNV behavior allowing G to grind anywhere, and what original eligibility chain is missing?
8. Which parts can be host-adapted without altering THUG2 semantics?
9. What exact interface must Opus receive from the Fallout world/collision layer?
10. Which functions/state variables must later feed the camera, animation and HUD investigations?

## Required outputs
Create:
- context/CODEX/THUG2_C04_SKATE_STATE_PHYSICS_EVIDENCE_2026-10-07.md
- build/evidence/thug2_c04/master_state_machine.json
- build/evidence/thug2_c04/movement_physics_map.json
- build/evidence/thug2_c04/collision_query_contract.json
- build/evidence/thug2_c04/grind_manual_lip_eligibility.json
- build/evidence/thug2_c04/opus_world_adapter_contract.json

For each state/transition record source file/function/address where available, inputs, preconditions, outputs, dependent state, animation/camera/HUD hooks and confidence.

## Stop condition
Stop when Opus can implement the core free-roam movement/state layer without inventing trick/grind eligibility or substituting Fallout movement logic.

Do not perform final FNV implementation or runtime validation.
