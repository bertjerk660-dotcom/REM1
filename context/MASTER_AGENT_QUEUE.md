# Master Agent Queue — 2026-10-07

Current rule: **GPT-6/Astra is unused. Codex owns investigation plus runtime testing/debugging/validation. Opus alone owns implementation.**

Before dispatching any item, check current repository evidence and recent commits to prevent duplicate work.

## CODEX — INVESTIGATION NEXT

1. **C01 — GMod Q-menu dependency trace** — NOT STARTED IN CANONICAL MAIN.
   Trace installed spawnmenu/Q-menu lifecycle, VGUI/Derma classes, content registration, search/icon-grid behavior, Q bind, cursor/focus/input ownership, close/restore behavior and native interfaces.
   - Unlocks: O02 real Q-menu implementation.

2. **C02 — Toolgun dispatch and tool-state trace** — NOT STARTED IN CANONICAL MAIN.
   Map gmod_tool, stool lifecycle, selected mode, LeftClick/RightClick/Reload, DoToolTrace, Duplicator, Remover, notification and undo/cleanup dependencies.
   - Depends on: C01 menu/tool-state boundary.
   - Unlocks: O03 Toolgun integration.

3. **C03 — Physgun remaining provenance/native trace** — PARTIAL INVESTIGATION COMPLETE.
   Close exact first-person presentation provenance and any remaining range/hold/audio/actor-target semantics not already proven by the IDA 6.8 evidence package.
   - Unlocks: O04 Physgun parity fix.

4. **C04 — THUG2 master skate state machine + movement/physics** — INVESTIGATION REQUIRED.
   - Unlocks: O05 core skate runtime.

5. **C05 — THUG2 camera map** — INVESTIGATION REQUIRED.
   - Unlocks: O05/O06 camera integration.

6. **C06 — THUG2 animation/board/skeleton map** — INVESTIGATION REQUIRED.
   - Unlocks: O06 animation/attachment integration.

7. **C07 — THUG2 HUD/UI/scoring event map** — INVESTIGATION REQUIRED.
   - Unlocks: O07 THUG2 UI.

8. **C08 — Unified source input map** — INVESTIGATION REQUIRED.
   Map THUG2 keyboard/mouse + Xbox actions and GMod Q/Toolgun/Physgun semantics against Fallout host conflicts.
   - Unlocks: O05/O07 unified input implementation.

## OPUS — IMPLEMENTATION READY / WAITING

- **O01 Toolgun view/world presentation** — READY FOR IMPLEMENTATION from existing staged packages after fresh branch/hash check.
- **O02 Real Q-menu compatibility/renderer** — WAITING FOR C01.
- **O03 Toolgun Q-state + Duplicator/Remover integration** — WAITING FOR C01/C02.
- **O04 Physgun parity implementation** — WAITING FOR C03 evidence closure; reuse existing IDA 6.8 evidence.
- **O05 THUG2 full free-roam runtime** — WAITING FOR C04/C05/C08.
- **O06 THUG2 animation/board-to-feet integration** — WAITING FOR C06.
- **O07 THUG2 HUD/UI** — WAITING FOR C07 and event/state interfaces from C04.
- **O07b THUG2 audio integration** — WAITING FOR C04/C06/C07 audio-event evidence or a narrow Codex audio addendum.
- **O08 final model/asset placement and visual matching** — OPUS ONLY; consume staged assets/provenance.

## CODEX — RUNTIME / VALIDATION QUEUE

These begin only after Opus produces a frozen candidate identified by branch, commit, source hash, DLL/ESP hashes and manifest.

- **R01 deterministic Fallout baseline regression** — boot/load/movement/combat/Pip-Boy/save-load.
- **R02 GMod Q/Toolgun runtime validation** — Q open/close, focus/cursor, icons/search/categories, tool selection, Duplicator/Remover, cleanup/save-load.
- **R03 Physgun runtime validation** — range, acquire, beam/highlight, hold audio, distance, rotate, freeze, drop, launch, NPC target identity, cleanup/save-load.
- **R04 THUG2 transition validation** — held board, activation, HUD ownership, board-to-feet, exit/restore, repeated transitions.
- **R05 THUG2 movement/camera validation** — push/coast/turn/brake/ollie/air/land and camera coupling.
- **R06 THUG2 trick/state validation** — flips, grabs, manuals, grind/lip/wall/revert, combos, SPECIAL, bail/recovery/board break.
- **R07 THUG2 animation/attachment validation** — every required animation family and board attachment transition.
- **R08 unified input validation** — keyboard/mouse + Xbox parity, no double-consumption, no stuck focus/cursor.
- **R09 cross-system/save-load regression** — Fallout -> GMod -> Fallout -> THUG2 -> Fallout, persistence and cleanup.
- **R10 crash diagnosis** — conditional on any failure; capture exact reproduction, logs, exception/crash evidence, hashes and suspected boundary, then hand back to Opus.

Legacy branches such as `runtime/astra-phase1-input92` remain historical candidate evidence only. Codex owns any future runtime validation of that work if it is deliberately reconciled into a test candidate.

## GPT-5.5 SUPPORT

1. **S01 branch reconciliation ledger** — COMPLETE initial pass.
2. **S02 master project map + owner split** — COMPLETE initial pass.
3. **S03 evidence index** — COMPLETE initial index; keep updated.
4. **S04 work-package conversion** — COMPLETE initial pass: C01-C08, Opus work packages and Codex runtime packs are defined.
5. **S05 acceptance matrix** — COMPLETE initial version; expand as evidence arrives.
6. **S06 input ownership matrix** — COMPLETE initial version.
7. **S07 provenance reconciliation** — COMPLETE initial pass in `context/PROVENANCE_INDEX.md`; refresh hashes before implementation.
8. **S08 stale-reference cleanup plan** — COMPLETE initial pass in `context/LEGACY_ROLE_PATH_MAP.md`.
9. **S09 failure-history normalization** — COMPLETE initial pass in `context/FAILURE_LEDGER.md`.
10. **S10 milestone/readiness rollup** — COMPLETE initial rollup in `context/MILESTONE_STATUS.md`; update as evidence lands.
11. **S11 selective branch reconciliation plan** — COMPLETE initial classification in `context/SELECTIVE_BRANCH_RECONCILIATION_2026-10-07.md`; execute promotions only after hash/evidence checks.
12. **S12 documentation authority map** — COMPLETE in `context/DOCUMENTATION_AUTHORITY_MAP.md`; use it for future conflict resolution.
13. **S13 runtime packet hardening** — COMPLETE initial pass; all Codex test packs now require exact candidate/save/location/inventory/hashes and evidence capture.
14. **S14 THUG2 audio implementation packet** — COMPLETE as a gated Opus packet; remains WAITING FOR CODEX evidence.

## BLOCKED

- **B01 canonical runtime version reconciliation:** main v81/v82-era verified state versus branch-only v84-v92 candidates.
- **B02 main handoff completeness:** some readiness references point to files present only on diverged branches.
- **B03 Physics Gun first-person provenance:** `v_physics.mdl/.vvd/.dx90.vtx` unresolved on main.
- **B04 THUG2 deep evidence:** full Codex-grade state/function/dependency maps still required.
- **B05 final cross-system validation:** waits for Opus candidates frozen by hash.

## Downstream rule

A subsystem becomes implementation-ready only after required Codex evidence is reviewed. A feature becomes complete only after Opus implementation and Codex runtime/regression validation satisfy all applicable acceptance gates.
