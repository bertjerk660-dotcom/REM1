# Non-Astra / Non-Opus Code Preservation — Next 20 Steps

Date: 2026-10-06
Lane: support/preparation only
Runtime boundary: do not overwrite or deploy Astra/GPT-6 runtime work.

## Objective
Preserve source-backed discoveries, conversion tooling, interfaces, manifests and reproducible evidence so the high-risk integration agent can consume them without rediscovery. Proprietary game binaries/assets are not committed; GitHub stores tooling, hashes, mappings, manifests and handoff knowledge.

## 20 next steps
1. Freeze a hash inventory of reusable local research/conversion scripts and generated metadata.
2. Classify each preserved artifact by subsystem: THUG2 animation/camera/input/HUD, GMod Q-menu, Tool Gun, Physgun, weapons, props, FNV host/runtime, validation.
3. Mark generated outputs versus authoritative scripts so generated evidence is not mistaken for source.
4. Record tool/runtime dependencies for every reusable script, including IDA Pro 6.8 requirements.
5. Preserve IDA 6.8 automation scripts and their expected inputs/outputs separately from IDB databases.
6. Preserve THUG2 reverse-engineering address/xref/signature evidence needed to reproduce animation/camera/controller findings.
7. Preserve the THUG2 animation manifest, bone map and GLB→FNV conversion tooling with provenance.
8. Build a THUG2 skate-state handoff schema covering states, transitions, controls, animation IDs and unresolved native behavior.
9. Preserve THUG2 HUD/font extraction and decoding tooling plus source hashes and presentation metadata.
10. Preserve GMod Q-menu Lua/Derma dependency inventory and source-file provenance without committing proprietary payloads.
11. Preserve Q-menu adapter contracts: categories, prop entries, search/filter fields, tool selection and icon identifiers.
12. Preserve Tool Gun SWEP/tool definitions as manifests/hashes and map each tool to required host callbacks.
13. Preserve Physics Gun behavior evidence as an interface contract: acquire, hold, rotate, freeze, release/launch, beam/highlight, actor handling.
14. Preserve GMod weapon model/sound mappings and distinguish confirmed payloads, missing payloads and fallback-prohibited gaps.
15. Preserve curated prop catalog generation/validation code and form-binding rules.
16. Build a host integration contract for Pip-Boy item identity, drop/pickup, world names, model attachment and mode activation.
17. Build a runtime ownership map defining which subsystem owns input, camera, HUD, animation and physics in Fallout mode vs skate mode vs Q-menu mode.
18. Consolidate known crash invariants from v73-v85 into machine-checkable preconditions and regression assertions.
19. Add a preservation validator that fails on missing required scripts/manifests, hash drift, stale handoffs or accidental proprietary binaries.
20. Produce a final promotion packet for Astra/GPT-6 containing preserved code/tooling refs, verified hashes, unresolved gaps and exact integration entry points.

## Work started
Step 1 is complete locally: 247 reusable research/code/metadata artifacts were hashed into `builds/code_preservation_inventory_20261006.csv`.
Inventory SHA256: `FABECA179A0196C277E7E1EA01B60F405FC3BC19B0F7739F95419827FFA18113`.

Step 2 is in progress. Existing support work is not repeated: the 290-entry prop catalog, GMod/HL weapon staging, Q-menu dependency inventory, Tool/Physgun inventory, THUG2 HUD/input/prop preparation, regression packs and support validator remain inputs to this lane.

## Safety / concurrency
Before any runtime modification, re-check hashes and mtimes because another engineering session may be changing v88/v89 work. This lane does not deploy runtime DLL/ESP changes unless explicitly promoted after validation.
