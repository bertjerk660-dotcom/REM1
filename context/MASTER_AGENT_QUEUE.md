# Master Agent Queue — 2026-10-07

This queue remaps the existing technical backlog into the current agent-ownership model. Before dispatching a task, re-check for a newer report/commit so completed investigations are not duplicated.

## CODEX NEXT

1. **C01 — GMod Q-menu dependency trace** — NOT STARTED IN CANONICAL MAIN. Trace actual installed spawnmenu/Q-menu lifecycle, VGUI/Derma classes, content registration, search/icon-grid behavior, Q bind, cursor/focus/input ownership, close/restore behavior and required native interfaces. Output evidence only; no final Fallout implementation.
   - Prerequisite: staged 105 Lua / 46 VGUI / 29 UI-material inventory.
   - Unlocks: Opus real Q-menu renderer/compatibility bridge.

2. **C02 — Toolgun dispatch and tool-state trace** — NOT STARTED IN CANONICAL MAIN. Map gmod_tool, stool lifecycle, selected mode, LeftClick/RightClick/Reload, DoToolTrace, Duplicator, Remover, notification and undo/cleanup dependencies.
   - Prerequisite: C01 menu/tool-state boundary.
   - Unlocks: Opus Toolgun integration driven directly from Q.

3. **C03 — Physgun remaining provenance/native trace** — PARTIAL INVESTIGATION COMPLETE. Verify the exact current first-person presentation path for Source-declared `models/weapons/v_physics.*` and close any remaining native range/hold/audio/actor-target semantics not already proven by the IDA 6.8 evidence package.
   - Unlocks: Opus Physgun parity fix.

4. **C04 — THUG2 master skate state machine + movement/physics** — INVESTIGATION REQUIRED. Produce state transitions, ground/air integration, acceleration/friction/momentum, turning, ollie/landing, collision/ground normals, grind/manual/lip/wall/revert/bail rules.
   - Unlocks: Opus core skate runtime.

5. **C05 — THUG2 camera map** — INVESTIGATION REQUIRED. Trace camera ownership, follow/yaw/pitch/smoothing, speed/air/landing coupling and transitions.
   - Unlocks: Opus camera implementation.

6. **C06 — THUG2 animation/board/skeleton map** — INVESTIGATION REQUIRED. Map all required animation IDs/families, selection/blending/timing, skeleton/bone requirements and board hand/feet/break/recovery attachments.
   - Unlocks: Opus animation/retarget/attachment implementation.

7. **C07 — THUG2 HUD/UI/scoring event map** — INVESTIGATION REQUIRED. Trace score, trick/combo text, multiplier, SPECIAL, balance meters, popups, menu/pause surfaces, event binding, scaling and renderer dependencies.
   - Unlocks: Opus THUG2 UI.

8. **C08 — Unified source input map** — INVESTIGATION REQUIRED. Map THUG2 M&K/Xbox actions, GMod Q/Toolgun/Physgun semantics and mode-specific conflicts that must be adapted at the FNV host boundary.
   - Unlocks: Opus unified input integration.

## OPUS READY / WAITING

- **O01 Toolgun view/world presentation** — READY FOR IMPLEMENTATION from existing staged packages, subject to fresh branch/hash check.
- **O02 Real Q-menu compatibility/renderer** — WAITING FOR C01; then READY.
- **O03 Toolgun Q-state + Duplicator/Remover integration** — WAITING FOR C01/C02.
- **O04 Physgun parity implementation** — WAITING FOR C03 exact provenance closure; existing IDA 6.8 evidence should be reused.
- **O05 THUG2 full free-roam runtime** — WAITING FOR C04-C08 evidence completeness. Preserve verified held-board and enter/exit behavior.
- **O06 THUG2 animation/board-to-feet integration** — WAITING FOR C06.
- **O07 THUG2 HUD/UI** — WAITING FOR C07.
- **O08 final model/asset placement and visual matching** — Opus-owned; consume curated/staged assets and provenance.

## ASTRA READY

- **A01 deterministic baseline regression** — READY whenever a specific candidate branch/build is assigned.
- **A02 GMod candidate runtime validation** — WAIT for Opus GMod candidate; run Q/Toolgun/Physgun acceptance + cleanup/save-load.
- **A03 THUG2 candidate runtime validation** — WAIT for Opus candidate; run transition, movement, camera, animations, trick families, HUD, audio, save/load and Xbox/M&K matrices.
- **A04 crash/failure diagnosis** — CONDITIONAL on an observed runtime failure; preserve exact build hashes/logs/steps.
- **Legacy branch note:** `runtime/astra-phase1-input92` contains branch-only runtime work and must be reconciled before being treated as a current candidate.

## GPT-5.5 SUPPORT

1. **S01 branch reconciliation ledger** — COMPLETE initial pass in `context/BRANCH_RECONCILIATION_2026-10-07.md`.
2. **S02 master project map + owner split** — COMPLETE initial pass in this coordination branch.
3. **S03 evidence index** — NEXT: one record per important discovery with source/agent/date/subsystem/location/confidence/verified/implemented/runtime-tested.
4. **S04 work-package conversion** — Convert C01-C08 and O01-O08 into small objective/evidence/dependency/success/risk packets.
5. **S05 acceptance matrix** — Expand existing regression specs so every subsystem has observable completion gates.
6. **S06 input ownership matrix** — Canonical matrix for NORMAL_FALLOUT / GMOD_MENU / GMOD_TOOL_ACTIVE / THUG2_SKATE_MODE / THUG2_WALK_MODE.
7. **S07 provenance reconciliation** — Bring only vetted manifests/hashes from large support branches into a current index; do not redistribute proprietary assets.
8. **S08 stale-reference cleanup plan** — Resolve main handoffs that point to files present only on diverged branches.
9. **S09 failure-history normalization** — Map each known failure to build, action, evidence, owner, fix/retest state.
10. **S10 milestone/readiness rollup** — Keep Evidence / Assets / GMod / THUG2 / Stability / Polish milestones updated without inventing percentages.

## BLOCKED

- **B01 canonical runtime version reconciliation:** main v81/v82-era verified state vs branch-only v84-v92 candidates.
- **B02 main handoff completeness:** readiness document references GMod handoffs absent from main but present on diverged support branches.
- **B03 Physics Gun first-person provenance:** `v_physics.mdl/.vvd/.dx90.vtx` triplet unresolved on main.
- **B04 THUG2 deep evidence:** current overlay contract is strong but not yet a complete Codex-grade state/function/dependency map for all free-roam systems.
- **B05 final cross-system validation:** cannot begin until Opus implementation candidates exist and are frozen by hash.

## DOWNSTREAM RULE

A task becomes implementation-ready only when its required Codex evidence is in the repository and reviewed. A feature becomes complete only after Opus implementation and Astra runtime/regression validation satisfy the applicable acceptance gates.
