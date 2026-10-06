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

## Near-term support sequence
1. Finish Combine Soldier armor staging and prepare its isolated playtest gate.
2. Preserve the Pip-Boy origin-icon pipeline and verify all assigned weapon records.
3. Import remaining project-authored conversion/validation tooling into GitHub.
4. Continue GMod/HL weapon and curated prop staging plus dependency/collision reports.
5. Prepare GMod Q-menu source inventories/dependency graphs for Astra without implementing the runtime port.
6. Expand automated asset/reference/build/regression checks.
7. Keep CURRENT_STATE, OPEN_WORK, manifests and failure knowledge synchronized after each support iteration.
