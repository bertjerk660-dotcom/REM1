# Opus Readiness Board — 2026-10-07

**Claude Opus is the sole implementation/integration agent.**
This board prevents implementation from starting before the necessary Codex evidence exists.

| Opus package | Required Codex evidence | Current readiness | Start condition |
|---|---|---|---|
| O01 Toolgun view/world presentation | existing staged model provenance; fresh hash check | READY WITH PREFLIGHT | verify source/staged package hashes immediately before Opus work |
| O02 Real GMod Q-menu renderer/compatibility | C01 | WAITING FOR CODEX | C01 evidence/function/dependency/interface package reviewed |
| O03 Toolgun Q-state + Remover/Duplicator | C01 + C02 | WAITING FOR CODEX | C01/C02 reviewed and Q-selected tool-state contract stable |
| O04 Physgun parity | C03 + existing IDA 6.8 evidence | WAITING FOR CODEX | exact view-model provenance/source path resolved or explicitly proven; behavior delta ready |
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

Current preparation score after the 2026-10-07 workflow finalization pass: **71/100**.

This percentage measures preparation/handoff readiness only. Package unlock state in the table above remains authoritative: most core systems are still waiting for Codex evidence.
