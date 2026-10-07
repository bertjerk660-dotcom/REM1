# GMod Evidence Intake Review — 2026-10-07

Source evidence commit on canonical `main`:
- `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`
- merge message: `Merge authenticated GMOD investigation and local staging evidence`

This review is performed by the normal GPT workflow lane. It does not claim implementation or runtime success.

## Evidence bundle accepted into coordination

Primary reports on `main`:
- `context/GMOD_2026-10-07/QMENU_ARCHITECTURE.md`
- `context/GMOD_2026-10-07/TOOLGUN_ARCHITECTURE.md`
- `context/GMOD_2026-10-07/PHYSGUN_ARCHITECTURE.md`
- `context/GMOD_2026-10-07/IDA68_NATIVE_REPORT.md`
- `context/GMOD_2026-10-07/INTEGRATION_BOUNDARY.md`
- `context/GMOD_2026-10-07/COMPATIBILITY_MATRIX.md`
- `context/GMOD_2026-10-07/EXISTING_IMPLEMENTATION_AUDIT.md`

Machine evidence:
- `manifests/gmod_2026-10-07/dependency_graph.json`
- `manifests/gmod_2026-10-07/qmenu_evidence.json`
- `manifests/gmod_2026-10-07/native_functions.json`
- `manifests/gmod_2026-10-07/native_boundary_client.json`
- `manifests/gmod_2026-10-07/native_boundary_server.json`
- `manifests/gmod_2026-10-07/asset_provenance.json`
- `manifests/gmod_2026-10-07/unresolved_dependencies.json`
- `manifests/gmod_2026-10-07/bundle_validation.json`

Bundle metadata validation:
- pass = true;
- 36,078 checks;
- 0 errors;
- 58 dependency-graph nodes;
- 89 graph edges;
- 14 required roots.

This validation proves metadata/graph/report consistency only, not runtime parity.

## C01 — Q-menu evidence assessment

### Newly strong/proven
- installed Q bind is `+menu`, C bind is `+menu_context`;
- original spawnmenu create/open/close lifecycle and hook order;
- persistent panel semantics rather than recreate-every-open;
- hold/release behavior, optional toggle mode and 0.180-second release guard;
- HangOpen/text-focus behavior;
- CreationMenu / ToolMenu / ContentSidebar / ContentContainer hierarchy;
- original tabs/categories/order;
- original prop browser / SpawnIcon / ModelImage path;
- click-to-`gm_spawn` server chain;
- search trigger behavior and model search indexing;
- tool selection through `spawnmenu.ActivateTool`;
- current FNV hover-selected numeric Toolgun state is source-incompatible;
- explicit host-compatibility surface is documented.

### Still unresolved
- build-specific native `+menu/-menu/+menu_context/-menu_context` registration/dispatch;
- exact native ModelImage/cache/render service;
- exact spawnlist native disk precedence;
- search aggregation/ranking native/library closure;
- IconEditor/property native dependencies;
- HTML/DHTML Dupes/Saves dependency closure where retained;
- exact native interface identifiers/addresses for remaining boundaries.

### Gate decision
**C01 = SUBSTANTIAL PARTIAL, NOT COMPLETE.**

Reason: the source/UI/state architecture is implementation-useful, but the C01 stop condition asked for a complete reviewable interface package. Native opener/icon/search/editor boundaries remain explicitly unresolved and must not be guessed.

O02 therefore remains **WAITING FOR CODEX GAP CLOSURE**, but most of its packet can now be pre-assembled.

## C02 — Toolgun evidence assessment

### Newly strong/proven
- original gmod_tool/stool registry and stable string-mode selection;
- Q click selection → command/state → Toolgun lifecycle relationship;
- LeftClick / RightClick / Reload dispatch architecture;
- Remover exact three-action semantics;
- Duplicator graph-copy/paste model and player-owned current-dupe state;
- undo/cleanup ownership expectations;
- constraints/physics-bone/local-coordinate data requirements;
- distinction between camera stool and camera SWEP;
- host adapter surface for entity handles, trace, constraints, UI and prediction;
- current Fallout hover numeric index/R-as-selector behavior is incompatible with original lifecycle.

### Still unresolved
- exact Toolgun sound-event wave closure;
- ToolTracer implementation/native dispatch;
- RenderScreen caller and RT-screen backend details;
- exact `util.GetPlayerTrace` range/native trace binding;
- SWEP-base prediction/input native interfaces;
- complete transitive dependencies for every supported stool;
- full Duplicator host constraint representation;
- prediction/realm semantics in the single-player bridge;
- converted view/world animations and screen attachment runtime proof.

### Gate decision
**C02 = SUBSTANTIAL PARTIAL, NOT COMPLETE.**

O03 remains **WAITING FOR CODEX GAP CLOSURE**.

## C03 — Physgun evidence assessment

### Newly strong/proven
- existing FNV defects are explicitly mapped against source-evidence requirements;
- native build/base identity and selected native functions/imports are reproducibly recorded;
- Physgun adapter responsibilities are documented;
- actor/target identity is explicitly separated from PlayerCharacter;
- beam/halo/audio/model/input boundaries are named.

### Still unresolved
- exact first-person `v_physics` provenance/current-build presentation;
- acquisition trace and source-faithful range/filter rules;
- native hold controller branch closure/tuning;
- release/freeze/reload/punt branch semantics;
- renderer/callsite/halo traversal closure;
- exact held-beam sound start/loop/stop semantics;
- actual current view-model selection;
- actor/ragdoll bridge runtime proof.

### Gate decision
**C03 = PARTIAL, NOT COMPLETE.**

O04 remains **WAITING FOR CODEX GAP CLOSURE**.

## Durable conclusion

The broad GMod investigation should **not be repeated**. The next Codex work should be a narrow closure pass against the unresolved items listed above.

This evidence materially improves Opus preparation because O02/O03/O04 can now be preassembled around proven original architecture while keeping unresolved native behavior explicit.

No live runtime change is authorized by this review.
