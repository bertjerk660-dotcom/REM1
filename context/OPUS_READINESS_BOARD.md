# Opus Readiness Board — 2026-10-07

**Claude Opus is the sole implementation/integration agent.**
This board prevents implementation from starting before the necessary Codex evidence exists.

| Opus package | Required Codex evidence | Current readiness | Start condition |
|---|---|---|---|
| O00 Golden Source bench conversion proof | provenance/current hashes only | READY FOR OPUS | isolated conversion/material/collision proof; must pass before weapon conversion |
| O01 Toolgun view/world presentation | existing staged model provenance; fresh hash check | READY AFTER O00 PASS | source packet is complete; start only after the golden bench proves the conversion pipeline |
| O02 Real GMod Q-menu renderer/compatibility | C01 | WAITING FOR CODEX GAP CLOSURE | broad source architecture is reviewed; native opener/icon/search/editor gaps still require closure |
| O03 Toolgun Q-state + Remover/Duplicator | C01 + C02 | WAITING FOR CODEX GAP CLOSURE | Q/tool architecture is reviewed; trace/prediction/effect/duplicator-host gaps remain |
| O04 Physgun parity | C03 + existing IDA 6.8 evidence | WAITING FOR CODEX GAP CLOSURE | native/build evidence exists, but view-model/acquisition/controller/audio/render/actor gaps remain |
| O05 THUG2 core movement/state/physics/input | C04 + C08 | WAITING FOR CODEX | state/collision/input contracts reviewed |
| O05b THUG2 camera | C05 | WAITING FOR CODEX | camera state/function/host-adapter contract reviewed |
| O06 THUG2 animation/board attachment | C06 | WAITING FOR CODEX | complete animation/skeleton/attachment catalogue reviewed |
| O07 THUG2 HUD/UI | C07 + C04 event interfaces | WAITING FOR CODEX | HUD/state/scoring event bindings and renderer contract reviewed |
| O07b THUG2 audio | C04 + C06 + C07 event/audio evidence or narrow Codex audio addendum | WAITING FOR CODEX | original sound-event names, source assets and loop/transition semantics reviewed |
| O08 final model/asset visual integration | per-asset provenance + corresponding subsystem evidence | PARTIAL / PACKAGE-SPECIFIC | source provenance current; no unresolved dependency relevant to selected asset |
| O09 cross-system fixes/polish | Codex runtime failure reports | NOT READY | subsystem candidates exist and Codex has produced deterministic failures/regressions |

## What Opus must receive for each package

1. objective and player-visible behavior;
2. Codex source-evidence report;
3. function/state/dependency maps;
4. asset/model/UI/animation provenance;
5. exact host interfaces/adapters;
6. relevant failure-history entries;
7. implementation boundaries;
8. acceptance matrix rows;
9. Codex runtime test pack to be run after implementation;
10. explicit list of preserved working behavior.

## What Opus must not receive as authority

- an old `GPT6_OPUS` owner field;
- an `ASTRA_*` filename interpreted as current ownership;
- a newer branch version number without hash/runtime evidence;
- placeholder UI appearance as proof of final implementation;
- static conversion success as proof of runtime correctness;
- an unresolved Physgun view-model substitute.

## Handoff lifecycle

Codex evidence complete
-> GPT-5.5 reviews/composes Opus packet
-> Opus implements on traceable branch
-> candidate frozen by hashes
-> Codex runs deterministic validation
-> on failure, GPT-5.5 converts Codex evidence into Opus fix packet
-> Opus fixes
-> Codex regresses
-> GPT-5.5 records VALIDATED only after gates pass.


## Preparation control documents

Before starting any Opus package, use:
- `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md` — reproducible overall preparation score and remaining gap;
- `context/OPUS_LAUNCH_SEQUENCE_2026-10-07.md` — exact allowed launch order and package dependencies;
- `context/OPUS_PACKAGE_INTAKE_CHECKLIST_2026-10-07.md` — evidence review, packet assembly, candidate freeze and promotion checklist.
- `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md` — current local hashes and stale-feed-bundle warning.

Current preparation score after the 2026-10-07 workflow finalization pass: **80/100**.

This percentage measures preparation/handoff readiness only. Package unlock state in the table above remains authoritative: most core systems are still waiting for Codex evidence.


## O01 ready packet
O01 Toolgun presentation is now **READY AFTER O00 PASS** after current-local hash verification of:
- c_toolgun required MDL/VVD/DX90;
- c_toolgun QC/reference SMD;
- w_toolgun required MDL/VVD/DX90;
- 13 Toolgun material/texture inputs.

Use:
- `context/HANDOFFS/OPUS_O01_TOOLGUN_PRESENTATION_2026-10-07.md`
- `build/prepared/opus_o01_toolgun_presentation_20261007.json`

This unlocks visual/presentation work only. O02/O03 behavior remains gated on Codex C01/C02.


## GMod C01-C03 evidence intake

Reviewed source commit:
`19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`

Current evidence status:
- C01 Q-menu — SUBSTANTIAL PARTIAL;
- C02 Toolgun — SUBSTANTIAL PARTIAL;
- C03 Physgun — PARTIAL.

Use:
- `context/GMOD_CODEX_EVIDENCE_INTAKE_REVIEW_2026-10-07.md`
- `build/prepared/gmod_codex_evidence_intake_20261007.json`
- `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

Preassembled Opus packets:
- `context/HANDOFFS/OPUS_O02_QMENU_PREASSEMBLY_2026-10-07.md`
- `context/HANDOFFS/OPUS_O03_TOOLGUN_BEHAVIOR_PREASSEMBLY_2026-10-07.md`
- `context/HANDOFFS/OPUS_O04_PHYSGUN_PREASSEMBLY_2026-10-07.md`

Do not repeat the broad GMod investigation; close only the enumerated gaps.


## O00 golden conversion gate

O00 is the first Opus implementation task:
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`
- `build/prepared/opus_o00_golden_bench_20261007.json`

Its source MDL/VVD/DX90/PHY, QC/reference/physics SMDs and VMT/VTF/mask were re-hashed on the current machine and match recorded provenance.

O00 must pass isolated human/runtime visual + collision acceptance before O01 weapon conversion begins. This restores the original safe pipeline ordering and prevents a converter/material/collision defect from being multiplied across weapon packages.
