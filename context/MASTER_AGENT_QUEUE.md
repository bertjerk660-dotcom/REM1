# Master Agent Queue — 2026-10-07

Current rule: **GPT-6/Astra is unused. Codex owns investigation plus runtime testing/debugging/validation. Opus alone owns implementation.**

Before dispatching any item, check current repository evidence and recent commits to prevent duplicate work.

## CODEX — INVESTIGATION NEXT

1. **C01 — GMod Q-menu dependency trace** — SUBSTANTIAL PARTIAL. Authenticated broad evidence is on canonical main; only narrow native/icon/search/editor gap closure remains.
   Trace installed spawnmenu/Q-menu lifecycle, VGUI/Derma classes, content registration, search/icon-grid behavior, Q bind, cursor/focus/input ownership, close/restore behavior and native interfaces.
   - Unlocks: O02 real Q-menu implementation.

2. **C02 — Toolgun dispatch and tool-state trace** — SUBSTANTIAL PARTIAL. Original registry/selection/Remover/Duplicator architecture is traced; narrow trace/prediction/effect/audio/host-representation closure remains.
   Map gmod_tool, stool lifecycle, selected mode, LeftClick/RightClick/Reload, DoToolTrace, Duplicator, Remover, notification and undo/cleanup dependencies.
   - Depends on: C01 menu/tool-state boundary.
   - Unlocks: O03 Toolgun integration.

3. **C03 — Physgun remaining provenance/native trace** — PARTIAL. Build/native boundaries are documented; first-person provenance, acquisition/controller/audio/render/actor-state closure remains.
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

- **O00 Golden Source bench conversion proof** — READY FOR IMPLEMENTATION and must pass first.
- **O01 Toolgun view/world presentation** — READY AFTER O00 PASS; 87-file unified visual-source validator currently passes.
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
11. **S11 selective branch reconciliation** — SUBSTANTIAL PASS COMPLETE. Q-menu/weapon staging and phase-4 prop/catalog provenance are indexed; v85/v88/v92 candidates remain quarantined. Future reconciliation is package-triggered with fresh local hash checks rather than broad branch merging.
12. **S12 documentation authority map** — COMPLETE in `context/DOCUMENTATION_AUTHORITY_MAP.md`; use it for future conflict resolution.
13. **S13 runtime packet hardening** — COMPLETE initial pass; all Codex test packs now require exact candidate/save/location/inventory/hashes and evidence capture.
14. **S14 THUG2 audio implementation packet** — COMPLETE as a gated Opus packet; remains WAITING FOR CODEX evidence.
15. **S15 Opus readiness scorecard** — COMPLETE with explicit weighted rubric in `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md`; current preparation score is 81/100 on the clean main-descended Opus-ready branch.
16. **S16 Opus launch sequence** — COMPLETE in `context/OPUS_LAUNCH_SEQUENCE_2026-10-07.md`; distinguishes immediate O01/O08 work from Codex-gated packages.
17. **S17 Opus evidence/package intake gate** — COMPLETE in `context/OPUS_PACKAGE_INTAKE_CHECKLIST_2026-10-07.md`; use after every Codex evidence or runtime report.
18. **S18 current-local Opus preflight identity** — COMPLETE; GMod appmanifest/VPK, THUG2 executable and FNV skeleton were re-hashed on the local machine and the stale old feed-bundle source hash is explicitly flagged.
19. **S19 Opus candidate/fix templates** — COMPLETE; implementation manifest, implementation packet and Codex-failure fix packet templates are ready.
20. **S20 normal-GPT pre-Opus backlog** — COMPLETE in `context/NORMAL_GPT_PRE_OPUS_BACKLOG_2026-10-07.md`; future workflow work is now package-triggered and Codex-result-driven.

## BLOCKED

- **B01 canonical runtime version reconciliation:** main v81/v82-era verified state versus quarantined branch-only v84-v92 candidates; candidate identities are preserved but require Codex local/runtime evidence before promotion.
- **B02 main handoff completeness:** some readiness references point to files present only on diverged branches.
- **B03 Physics Gun first-person provenance:** `v_physics.mdl/.vvd/.dx90.vtx` unresolved on main.
- **B04 THUG2 deep evidence:** full Codex-grade state/function/dependency maps still required.
- **B05 final cross-system validation:** waits for Opus candidates frozen by hash.

## Downstream rule

A subsystem becomes implementation-ready only after required Codex evidence is reviewed. A feature becomes complete only after Opus implementation and Codex runtime/regression validation satisfy all applicable acceptance gates.


21. **S21 O01 Toolgun presentation preflight** — COMPLETE. Exact c/w Toolgun source models, QC/reference geometry and 13 materials/textures re-hashed and matched; final visual-only packet is `context/HANDOFFS/OPUS_O01_TOOLGUN_PRESENTATION_2026-10-07.md`. Status: READY AFTER O00 PASS.
22. **S22 canonical coordination promotion plan** — COMPLETE in `context/CANONICAL_COORDINATION_PROMOTION_PLAN_2026-10-07.md`; actual promotion remains deferred until the destination integration branch is selected.


23. **S23 GMod evidence intake review** — COMPLETE. Main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0` reviewed and imported into preparation branch. C01/C02 = SUBSTANTIAL PARTIAL; C03 = PARTIAL; none is falsely marked complete.
24. **S24 GMod narrow gap-closure handoff** — COMPLETE in `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`; broad GMod rediscovery is explicitly forbidden.
25. **S25 O02/O03/O04 preassembly** — COMPLETE. Packet shells exist and list only the unresolved evidence needed before READY FOR OPUS.


26. **S26 O00 golden conversion preflight** — COMPLETE. Bench source geometry/collision/material inputs re-hashed and matched; O00 packet is READY FOR OPUS.
27. **S27 Opus Session 1 bootstrap** — COMPLETE. Current start-here, session input manifest and machine-readable gate matrix now point to O00 first, then O01 after PASS.


28. **S28 O08a Crowbar presentation preflight** — COMPLETE. First-person and world crowbar model packages were directly extracted from installed Source/GMod VPKs and matched current staged hashes; material closure also reverified. Status: READY AFTER O00 PASS.
29. **S29 current Opus visual queue** — COMPLETE in `context/OPUS_VISUAL_ASSET_QUEUE_2026-10-07.md`; old GPT6/Astra visual queues are historical only.


30. **S30 O08b Pistol presentation preflight** — COMPLETE. c/w pistol models were directly extracted from installed GMod archives and matched staged hashes; original VMT/VTF closure verified. Status: READY AFTER O00 PASS.
31. **S31 O08c SMG1 presentation preflight** — COMPLETE. c/w SMG1 models were directly archive-verified; original material closure verified and the missing world-SMG specular mask was repaired with the exact original VPK file. Status: READY AFTER O00 PASS.
32. **S32 unified visual-source validation** — COMPLETE. O00/O01/O08a/O08b/O08c: 87 files checked, 0 errors. Report: `build/validation/opus_visual_source_validation_20261007.json`.
33. **S33 clean main-descended Opus-ready branch** — COMPLETE. `prep/opus-ready-20261007` was created from current main and verified ahead with 0 behind; it is the preferred preparation branch.


34. **S34 next Codex C04 request packet** — COMPLETE. `context/HANDOFFS/NEXT_CODEX_REQUEST_THUG2_C04_2026-10-07.md` is the next new investigation request; it explicitly forbids Opus-owned implementation work.
35. **S35 Codex C04 evidence return** — WAITING FOR CODEX. Review with `context/HANDOFFS/CODEX_C04_REVIEW_CHECKLIST_2026-10-07.md`; award the 3 C04 readiness points only on semantic COMPLETE.
