# Normal GPT Opus-readiness finalization — 2026-10-07

## Scope
Workflow / documentation / provenance / handoff preparation only. No Codex reverse engineering and no Claude Opus implementation were performed in this pass.

## Readiness result
Using the explicit weighted rubric in `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md`:

- **before:** 58/100 Opus-preparation readiness;
- **after:** 80/100 Opus-preparation readiness;
- **gain:** +22 percentage points.

This measures preparation quality, not game completion or runtime-validation completion.

## Work completed

### Repository / provenance reconciliation
- re-read canonical goal/architecture/current-state/decisions/failure/open-work documents;
- reconciled workflow-coordination branch state;
- selectively mined phase-4 prop/catalog evidence without promoting runtime claims;
- retained v84-v92 runtime candidates in quarantine;
- preserved THUG2 prop candidates at 0-ready/20-blocked rather than falsely promoting them.

### Current-local identity refresh
Remote Desktop Commander re-hashed:
- GMod appmanifest — matches recorded provenance;
- `garrysmod_dir.vpk` — matches;
- THUG2 `SLES_526.21` — matches;
- FNV skeleton extract — matches;
- current local main source, installed main DLL, main ESP and enabled support sidecars.

Important drift discovered:
- old 2026-10-06 feed-bundle `main.cpp` SHA256:
  `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`
- current local `main.cpp` SHA256:
  `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE`

Therefore the old feed bundle is reference/provenance input only and cannot define a new Opus implementation baseline without a fresh freeze.

### New control documents
- `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md`
- `context/OPUS_LAUNCH_SEQUENCE_2026-10-07.md`
- `context/OPUS_PACKAGE_INTAKE_CHECKLIST_2026-10-07.md`
- `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`
- `context/NORMAL_GPT_PRE_OPUS_BACKLOG_2026-10-07.md`

### New/hardened templates
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`
- `context/HANDOFFS/OPUS_IMPLEMENTATION_PACKET_TEMPLATE.md`
- `context/HANDOFFS/OPUS_FIX_PACKET_TEMPLATE.md`

### Existing coordination files updated
- `context/EVIDENCE_INDEX.md`
- `context/PROVENANCE_INDEX.md`
- `context/SELECTIVE_BRANCH_RECONCILIATION_2026-10-07.md`
- `context/MASTER_AGENT_QUEUE.md`
- `context/OPUS_READINESS_BOARD.md`
- `context/MILESTONE_STATUS.md`
- `context/OPEN_WORK.md`

## Current Opus package status
- O00 Golden Source bench conversion proof: **READY FOR OPUS**.
- O01 Toolgun presentation: **READY AFTER O00 PASS**.
- O08 selected visual/model packages: **PARTIAL / PACKAGE-SPECIFIC**.
- O02 Q-menu: waits for C01.
- O03 Toolgun behavior: waits for C01+C02.
- O04 Physgun parity: waits for C03.
- O05 THUG2 movement/state/physics: waits for C04+C08.
- O05b THUG2 camera: waits for C05.
- O06 animation/board attachment: waits for C06.
- O07 HUD/UI: waits for C07+C04 interfaces.
- O07b audio: waits for relevant C04/C06/C07 evidence.
- O09 polish/fix loop: waits for implemented candidates and Codex runtime reports.

## Remaining preparation bottleneck
The remaining 20 readiness points are dominated by missing **Codex implementation-grade evidence**. Normal GPT must not fabricate those points from source inventories.

As each C01-C08 result lands, normal GPT should:
1. ingest/review it;
2. update evidence/provenance indexes;
3. resolve contradictions;
4. compose the unlocked Opus packet;
5. refresh only the package-relevant local hashes;
6. freeze candidate manifest/test requirements;
7. hand implementation to Opus;
8. route the frozen candidate to Codex for runtime validation.

## Local mirror
The new scorecard, launch sequence, intake checklist, preflight snapshot, backlog and Opus packet/fix templates were mirrored into the local project workspace so the build machine and GitHub coordination branch agree.

## Branch policy
Work is on:
`prep/opus-readiness-finalization-20261007`

Do not wholesale merge runtime/specialist branches. Promote coordination artifacts selectively when the long-term integration branch is chosen.


### Additional O01/promotion completion
- O01 Toolgun presentation source geometry/materials were re-hashed on the current machine and match recorded provenance.
- Final packet: `context/HANDOFFS/OPUS_O01_TOOLGUN_PRESENTATION_2026-10-07.md`.
- Machine-readable preflight: `build/prepared/opus_o01_toolgun_presentation_20261007.json`.
- O01 is now READY FOR OPUS for visual/presentation work only.
- Canonical coordination promotion is preplanned in `context/CANONICAL_COORDINATION_PROMOTION_PLAN_2026-10-07.md`; no specialist/runtime branch was merged.


### Authenticated GMod evidence intake
- Canonical main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0` was reviewed and selectively imported.
- C01 Q-menu = SUBSTANTIAL PARTIAL.
- C02 Toolgun = SUBSTANTIAL PARTIAL.
- C03 Physgun = PARTIAL.
- Broad GMod rediscovery is now unnecessary; narrow gap closure is defined in `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`.
- O02/O03/O04 preassembled packets now exist.

### Golden conversion gate
- O00 bench source geometry/collision/material inputs were freshly re-hashed and match provenance.
- O00 is the first Opus implementation task.
- O01 is fully prepared but starts only after O00 passes visual/collision/runtime acceptance.
