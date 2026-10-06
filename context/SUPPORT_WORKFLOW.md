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

## Near-term support sequence
1. Audit existing ESP/base-form coverage for the 290 ready prop candidates so duplicate forms are not created.
2. Audit thumbnail/icon coverage and prepare missing thumbnails as data assets only.
3. Build a disabled sidecar catalog only for genuinely missing custom/GMod prop forms.
4. Expand asset/reference/sidecar validators and promotion checklists.
5. Continue importing reusable project-authored support tooling and manifests into GitHub.
6. Keep the Astra handoff current without editing/deploying its runtime candidate.
