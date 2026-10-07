# Codex GMod Gap-Closure Packet — 2026-10-07

Purpose: finish only the remaining evidence required to unlock O02/O03/O04. Do not repeat the broad GMod investigation already merged to `main` at commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`.

Read first:
- all `context/GMOD_2026-10-07/*` reports on main;
- `manifests/gmod_2026-10-07/unresolved_dependencies.json`;
- C01/C02/C03 handoff definitions;
- current failure knowledge and Opus readiness board.

Use IDA Pro 6.8 only where native evidence is required.

## Gap set A — close C01
Resolve:
1. native +menu/-menu/+menu_context/-menu_context registration and dispatch;
2. native command → GM:OnSpawnMenuOpen/Close relationship where observable;
3. exact ModelImage/SpawnIcon native cache/render service boundary;
4. spawnlist native path/precedence behavior;
5. search.GetResults aggregation/ranking dependencies;
6. IconEditor/property dependencies required for the supported local feature set;
7. classify DHTML/Workshop-only features as required, optional or deliberately unsupported;
8. record exact host API contract for each remaining boundary.

Output should amend or produce a C01 evidence package that can truthfully satisfy the original C01 stop condition.

## Gap set B — close C02
Resolve:
1. Toolgun.Single sound-event wave closure;
2. ToolTracer implementation and native/effect dispatch;
3. RenderScreen caller / render-target update semantics;
4. util.GetPlayerTrace native range/filter binding;
5. SWEP base prediction/input interfaces;
6. exact prediction/realm rule needed for one mutation per action;
7. Duplicator host representation requirements for the explicitly supported entity/constraint subset;
8. supported stool dependency closure for at least Remover + Duplicator plus any tools required by the user's initial final scope.

Do not broaden into every possible community stool.

## Gap set C — close C03
Resolve:
1. exact current first-person Physgun presentation/provenance;
2. acquisition trace range/filter rules;
3. hold controller tuning/state transitions;
4. rotation/distance-adjust/freeze/unfreeze/reacquire;
5. release/drop versus punt/launch semantics;
6. held-beam sound start/loop/stop;
7. beam/halo renderer callsite/state and color relation;
8. actor/ragdoll target-state semantics;
9. cleanup on switch/destroy/load/cell/death;
10. direct delta against current FNV short-range/audio/player-target bugs.

## Required result format

For each C01/C02/C03 state:
- COMPLETE or still PARTIAL;
- exact newly proven facts;
- source paths / addresses / function names;
- remaining unresolved items;
- Opus adapter contract delta;
- confidence;
- commit SHA.

Do not implement Fallout runtime code. Stop when the evidence gate is genuinely complete or when the remaining blocker is proven impossible/unavailable and explicitly scoped for Opus adaptation.
