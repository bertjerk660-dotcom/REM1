# Support Workflow

This file defines the parallel support lane requested by the project owner. It is intended to keep time-consuming preparation and validation moving while Astra concentrates on the complex runtime/mechanics work.

## Astra lane
Primary branch: `feature/thug2-native-ui-g6`.

Astra owns work where correctness depends on deep reverse engineering, engine ABI work or high-risk runtime behavior:
- THUG2 skating state machine, movement, physics, collision, tricks, balance and scoring;
- THUG2 camera behavior and animation selection/blending/retargeting;
- board attachment behavior when it depends on animation/rig/runtime state;
- original THUG2 HUD/QB runtime behavior and menu runtime integration;
- real GMod Q-menu runtime port;
- Tool Gun and Physics Gun core behavior/native integration;
- complex model rigging or skeleton work that cannot be handled by a proven repeatable conversion pipeline.

Support work must not overwrite or deploy Astra candidates.

## Support lane
Primary branch: `prep/support-workflow`.

The support lane should keep the project moving through lower-risk but time-consuming work:
- source-asset inventories and dependency maps;
- extraction/conversion scripts already understood by the pipeline;
- xEdit record creation and isolated sidecar plugins;
- Pip-Boy icons and inventory presentation;
- texture/path/reference validation;
- prop curation, collision/scale audits and thumbnail preparation;
- GMod/HL weapon/prop staging;
- manifests, hashes and provenance;
- regression scripts and smoke-test checklists;
- build/package organization;
- GitHub project memory and handoff notes.

## Coordination rules
1. Before modifying anything, re-check actual local hashes/mtimes and the relevant GitHub branch.
2. Never use support tasks to quietly change `src/plugin/main.cpp` or Astra's candidate directories.
3. Prefer isolated output directories and sidecar ESPs.
4. Proprietary game binaries/assets stay local; GitHub receives scripts, mappings, hashes, manifests and reproduction notes.
5. Static validation is not a playtest. A staged feature stays staged until human gameplay checks pass.
6. When a support task uncovers a mechanics/ABI/rig problem, record evidence and hand it to Astra rather than applying speculative runtime patches.

## Current support checkpoint
- Combine Soldier armor staging and its isolated test gate are prepared.
- Pip-Boy origin-icon tooling is preserved.
- GMod/HL concrete weapon-model staging has 100% model-reference coverage.
- The curated FNV pool has a 278-item static-clean shortlist.
- The curated GMod/Source pool contains 120 conversion/collision/material-clean candidates.
- The real GMod Q-menu/Tool Gun/notification dependency stack is inventoried and hashed for Astra.
- THUG2 has 106 named embedded-prop extraction targets, not yet standalone props.
- The compact ready-content handoff currently contains 290 candidates: 170 FNV + 120 GMod/Source.

## Support preparation completion state
The requested broad non-Astra preparation pass is complete. Current durable outputs include:
- validated Combine armor staging and origin-icon tooling;
- 100% concrete GMod/HL weapon-model reference coverage plus view/world/sound dependency handoff;
- 290-entry final prop catalog with form bindings and 290/290 support previews;
- disabled validated GMod prop and RPG presentation sidecars;
- real GMod Q-menu/Tool Gun/notification source/dependency inventory;
- 106 THUG2 embedded-prop per-level handoffs;
- THUG2 skateboard source/animation metadata handoff;
- THUG2 HUD/font/controller/audio source handoff;
- unified static validator and preflight/postflight playtest evidence tooling.

## Next support sequence
1. Do not make further runtime changes merely to keep busy; the remaining support-critical evidence is human gameplay validation.
2. Use the prepared checklist and evidence capture scripts for isolated sidecar/inventory/armor/prop tests.
3. Record any observed failure with exact artifact hash/log/event evidence and convert repeated manual diagnosis into validation tooling.
4. Keep support manifests synchronized when Astra/Claude changes the canonical runtime.
5. Hand mechanics/ABI/rig/runtime faults to Astra rather than applying speculative support patches.

## Completion snapshot C
- Unified support validator: 94 checks / zero errors.
- Final catalog: 290 ready entries, all form-bound, all with clean fallback thumbnails.
- GMod/HL weapon source model staging: 71/71 concrete references; 48 view + 48 world candidates.
- Source weapon sound events: 15/15 definitions recovered from original installed Source/GMod sound scripts; 14/15 have every referenced payload confirmed.
- Tool Gun/Physgun asset audit: 33/36 exact paths resolve; only the source-declared v_Physics view-model triplet is absent and remains an explicit dependency discrepancy.
- THUG2 prop queue: 106 classified = 85 spatial geometry candidates + 14 semantic/gap identifiers + 7 unresolved named targets.
- THUG2 input handoff: 22 source-backed control entries derived from 17 decompiled evidence files.
- Release/install ledger, eight regression packs, historical artifact registry and nine Astra subsystem handoffs are prepared.
- Human playtesting and Astra/Opus runtime/model integration are now the primary remaining gates.
