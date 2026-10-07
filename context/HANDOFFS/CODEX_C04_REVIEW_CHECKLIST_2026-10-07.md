# Normal-GPT Review Checklist — Codex C04 THUG2 State / Physics

Use this only after Codex returns the C04 evidence branch.

## Ownership check
Reject the result if Codex performed substantive Opus work such as:
- editing the final Fallout/xNVSE implementation;
- implementing skate physics/state behavior;
- animation retargeting;
- board attachment integration;
- HUD/camera implementation;
- deploying a gameplay candidate.

Investigation tooling and evidence generation are allowed.

## Required files
All must exist:
- `context/CODEX/THUG2_C04_SKATE_STATE_PHYSICS_EVIDENCE_2026-10-07.md`
- `build/evidence/thug2_c04/master_state_machine.json`
- `build/evidence/thug2_c04/movement_physics_map.json`
- `build/evidence/thug2_c04/collision_query_contract.json`
- `build/evidence/thug2_c04/grind_manual_lip_eligibility.json`
- `build/evidence/thug2_c04/opus_world_adapter_contract.json`

## Semantic pass conditions
C04 earns its 3 readiness points only if the evidence package closes:
- state IDs/transitions;
- movement/physics constants/rules;
- ground/air/landing logic;
- grind/manual/lip eligibility;
- collision-query contract;
- cross-system state/event outputs;
- host adapter inputs/outputs;
- current grind-anywhere failure delta;
- source/function/address/caller evidence;
- confidence/unresolved items.

A list of animation names, controller buttons or asset filenames is not enough.

## On COMPLETE
Normal GPT:
1. raises readiness 81 → 84 unless other gates were simultaneously completed;
2. finalizes O05 core packet using the reviewed C04 contract, but O05 still waits for C08 if unified input evidence is required;
3. updates evidence/provenance indexes;
4. provides C04 state vocabulary to C05/C06/C07;
5. prepares the next Codex request (normally C05 camera or parallel C06/C07 after vocabulary review).

## On PARTIAL
Do not award points.
Create one narrow Codex follow-up containing only the missing evidence.
