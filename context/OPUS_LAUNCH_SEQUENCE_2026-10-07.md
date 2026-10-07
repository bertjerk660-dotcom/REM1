# Opus Launch Sequence — 2026-10-07

Purpose: define exactly what Claude Opus may start, what must wait, and what evidence must be handed over first.

## Global rule

Claude Opus is the sole substantive implementation/integration owner.
Codex investigates/reverse-engineers and later runtime-validates/debugs.
Normal GPT coordinates, reconciles, documents and prepares packets.

Do not ask Opus to rediscover original-game behavior that Codex should map first.

## Phase 0 — mandatory preflight before any Opus implementation

1. Read AGENTS.md, BOOTSTRAP, GOAL, ARCHITECTURE, CURRENT_STATE, DECISIONS, FAILURE_KNOWLEDGE.
2. Read AGENT_OWNERSHIP, DOCUMENTATION_AUTHORITY_MAP, OPUS_READINESS_BOARD and this launch sequence.
3. Identify exact implementation branch.
4. Record parent commit.
5. Re-check current local source/staged hashes for the selected package.
6. Confirm protected runtime files/hashes before modification.
7. Confirm no quarantined v84-v92 candidate is being promoted merely because it is newer.
8. Read package-specific failure entries and preserved-working-behavior list.
9. Confirm the post-implementation Codex runtime test pack is already defined.
10. Freeze an implementation manifest before runtime validation.

## Phase 1 — work Opus may begin immediately

### O00 — Golden Source bench conversion proof
Status: READY FOR OPUS.

Purpose:
- prove Source→FNV mesh/material/collision conversion in an isolated sidecar before weapon conversion;
- validate shader/material mapping, scale/axis handling and Havok collision mapping;
- stop weapon conversion if the pipeline fails.

Packet:
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`

### O01 — Toolgun view/world presentation
Status: READY AFTER O00 PASS.

Prerequisite:
- O00 human/runtime PASS.

Inputs:
- existing c_toolgun / w_toolgun source packets;
- material dependency closure;
- existing staged GMod/HL weapon audit;
- current FNV attachment/presentation conventions;
- acceptance rows for held/world presentation.

Boundary:
- visual/model/material/attachment implementation only;
- do not invent final Q-menu or Toolgun behavior before C01/C02;
- preserve real GMod source assets and exact provenance.

### O08 — selected model/asset visual integration
Status: PARTIAL / PACKAGE-SPECIFIC.

Allowed only where:
- original asset provenance is strong;
- no unresolved subsystem behavior is required;
- implementation can be isolated and reverted;
- package-specific Codex evidence is not a prerequisite.

Golden-bench style conversion/visual-pipeline work is suitable when current local packet hashes pass.

## Phase 2 — GMod system packages after Codex evidence

### O02 — real Q-menu renderer / compatibility
Unlock: reviewed C01.

Required packet must contain:
- spawnmenu lifecycle/function map;
- VGUI/Derma dependency map;
- content/search/icon registration;
- Q input/focus/cursor semantics;
- host adapter contract;
- preserved Fallout UI/input behavior;
- R02 runtime pack.

### O03 — Toolgun Q-state + Duplicator/Remover
Unlock: reviewed C01 + C02.

Required packet:
- selected tool-state ownership;
- gmod_tool/stool dispatch;
- LeftClick/RightClick/Reload semantics;
- traces;
- Duplicator and Remover dependencies;
- undo/cleanup/notification behavior;
- Q -> selected tool -> Toolgun contract.

### O04 — Physgun parity
Unlock: reviewed C03.

Required packet:
- exact first-person provenance or explicit proven resolution;
- range/acquire/hold/rotate/freeze/drop/launch semantics;
- beam/highlight/audio map;
- actor targeting rules;
- known F009 failure deltas;
- R03 validation pack.

## Phase 3 — THUG2 core packages after Codex evidence

### O05 — master skate movement/state/physics
Unlock: C04 + C08.

Must receive:
- state machine;
- state transitions;
- ground/air/collision semantics;
- velocity/acceleration/friction/turning;
- ollie/landing;
- grind/manual/lip/wall/revert/trick dependencies;
- host collision adapter;
- unified action abstraction.

### O05b — THUG2 camera
Unlock: C05.

Must receive:
- camera function map;
- constants/state map;
- state coupling;
- user input semantics;
- collision/clipping behavior;
- safe Fallout camera adapter contract;
- historical F008 crash constraints.

### O06 — animations + board attachment
Unlock: C06.

Must receive:
- animation IDs/families;
- state-to-animation selection;
- source skeleton/bone map;
- board attachment transforms/state changes;
- blend/timing behavior;
- hand -> feet -> break/recovery -> exit contract;
- F004/F011 regression constraints.

### O07 — HUD/UI/scoring
Unlock: C07 + C04 event interfaces.

Must receive:
- renderer/surface inventory;
- score/combo/SPECIAL/balance state;
- event bindings;
- popups/messages;
- scaling/resolution rules;
- Fallout-HUD suppression/restore contract.

### O07b — THUG2 audio
Unlock: C04/C06/C07 audio evidence or a reviewed narrow Codex audio addendum.

Must receive:
- event -> source sound map;
- loop start/stop ownership;
- transition cleanup;
- bail/trick/grind/push/roll/UI/SPECIAL coverage.

## Phase 4 — integrated candidate

After subsystem implementation:
1. freeze branch/commit;
2. record DLL/ESP/assets hashes;
3. record source hash;
4. record load order;
5. record test save/location/inventory;
6. run static/build validators;
7. hand exact candidate to Codex.

## Phase 5 — Codex validation / Opus fix loop

Codex executes R01-R09 as applicable.
Any failure produces:
- deterministic reproduction;
- exact candidate identity;
- logs/crash evidence;
- expected vs observed behavior;
- suspected subsystem boundary;
- no speculative implementation patch unless the task is investigation/debug evidence.

Opus then fixes the candidate.
Codex regresses the exact fixed build.

## Preserved working behavior that every Opus packet must explicitly protect

At minimum where applicable:
- persistent ESP-owned skateboard identity;
- correct held skateboard model;
- LMB skate activation;
- holster skate exit;
- no grenade/type regression;
- no unsafe player-node assumptions;
- no raw stale camera pointers;
- current Fallout baseline boot/load/Pip-Boy/save behavior;
- Q-menu/weapon state must never create stuck input/cursor ownership;
- support/runtime candidates remain isolated until deliberately promoted.

## Stop rule

Do not start a blocked Opus package because an old handoff says “ready.”
The current OPUS_READINESS_BOARD and reviewed Codex evidence determine unlock state.
