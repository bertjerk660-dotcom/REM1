# Claude Opus — Session 1 Start Here — 2026-10-07

This is the current implementation entrypoint for Claude Opus.

## Canonical project
Repository:
`bertjerk660-dotcom/REM1`

Preparation branch:
`prep/opus-readiness-finalization-20261007`

Current preparation readiness:
**80/100**

This is preparation readiness, not game-completion percentage.

## Ownership
- Claude Opus: implementation, visual/model/animation/UI integration.
- Codex: investigation/reverse engineering and later runtime validation/debugging.
- Normal GPT: coordination, evidence intake, manifests, provenance, handoff/fix packets.
- Historical Astra/GPT6 ownership text is not current authority.

## Read first
1. `AGENTS.md`
2. `context/BOOTSTRAP.md`
3. `context/GOAL.md`
4. `context/ARCHITECTURE.md`
5. `context/CURRENT_STATE.md`
6. `context/DECISIONS.md`
7. `context/FAILURE_KNOWLEDGE.md`
8. `context/AGENT_OWNERSHIP.md`
9. `context/OPUS_READINESS_BOARD.md`
10. `context/OPUS_LAUNCH_SEQUENCE_2026-10-07.md`
11. `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`

## First implementation package

### O00 — Golden Source Bench conversion proof
**READY FOR OPUS**

Read:
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`
- `build/prepared/opus_o00_golden_bench_20261007.json`
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`

O00 exists to prove the Source→FNV model/material/collision pipeline in an isolated sidecar. Do not start weapon conversion until O00 passes its human/runtime gate.

### O01 — Toolgun presentation
**READY AFTER O00 PASS**

Read:
- `context/HANDOFFS/OPUS_O01_TOOLGUN_PRESENTATION_2026-10-07.md`
- `build/prepared/opus_o01_toolgun_presentation_20261007.json`
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`

After O00 passes, O01 authorizes:
- authentic GMod c_toolgun first-person visual conversion/adaptation;
- authentic w_toolgun third-person/world visual conversion/adaptation;
- material/texture conversion;
- scale/orientation/attachment;
- Fallout-compatible visual hierarchy;
- isolated presentation records/assets where needed.

O01 does **not** authorize:
- final Q-menu;
- Toolgun behavior/tool dispatch;
- Duplicator/Remover logic;
- final GMod notifications;
- Physgun behavior;
- THUG2 runtime systems.

Those remain evidence-gated.

## GMod behavior packages

A large authenticated GMod evidence bundle is now imported from main commit:
`19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`

Read:
- `context/GMOD_CODEX_EVIDENCE_INTAKE_REVIEW_2026-10-07.md`
- `context/GMOD_2026-10-07/*`
- `manifests/gmod_2026-10-07/unresolved_dependencies.json`

Current status:
- C01 Q-menu = SUBSTANTIAL PARTIAL;
- C02 Toolgun = SUBSTANTIAL PARTIAL;
- C03 Physgun = PARTIAL.

Therefore:
- O02 = WAITING FOR CODEX GAP CLOSURE;
- O03 = WAITING FOR CODEX GAP CLOSURE;
- O04 = WAITING FOR CODEX GAP CLOSURE.

Preassembled packet shells already exist. Do not implement these behavior packages until normal GPT marks the corresponding evidence COMPLETE.

## THUG2 packages
Current major THUG2 implementation packages remain gated:
- O05 movement/state/physics/input — waits C04+C08;
- O05b camera — waits C05;
- O06 animation/board attachment — waits C06;
- O07 HUD/UI — waits C07+C04 interfaces;
- O07b audio — waits relevant C04/C06/C07 evidence.

Do not replace these evidence requirements with approximation.

## Mandatory implementation preflight

Before editing:
1. create/select a traceable implementation branch;
2. record its parent commit;
3. hash the exact current source file(s);
4. decide whether unrelated support sidecars are disabled or explicitly included;
5. record current DLL/ESP/load order;
6. preserve rollback copies/commits;
7. copy `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json` into the candidate build folder and fill it as work proceeds.

Important:
the old 2026-10-06 feed-bundle `main.cpp` hash is stale.
Use the current baseline selected at implementation time.

## Current support sidecars
The local preflight snapshot records support sidecars currently enabled on the test machine. They are not automatically part of an O01 candidate.

For clean O01 validation, either:
- disable unrelated support sidecars; or
- explicitly include them in the candidate manifest and explain why.

Do not silently change the test environment.

## O01 acceptance
Opus should not claim final success from conversion/build alone.

Freeze:
- implementation branch/commit;
- source hashes;
- output NIF/texture hashes;
- changed ESP/DLL hashes;
- load order;
- test save/location;
- known issues.

Then hand the exact candidate to Codex for:
- first-person Toolgun presentation;
- third-person/world Toolgun presentation;
- scale/orientation/attachment;
- material resolution;
- repeated holster/equip;
- inventory/Pip-Boy switching;
- drop/pickup where current record supports it;
- save/load regression;
- no unrelated Q/Toolgun behavior changes;
- no skateboard/Physgun regression.

## Stop rule
Implement only packages explicitly marked READY FOR OPUS or package-specific O08 work with proven provenance.

If a required fact is missing, record it and stop that package rather than inventing original-game behavior.
