# GMOD original-system investigation and staging — 2026-10-07

This package investigates the user's installed Garry's Mod and prepares original dependencies for the existing Fallout New Vegas + GMOD + THUG2 project. It is an evidence/staging pass. It does not claim that original GMOD Lua/VGUI or native Physgun behavior now executes inside Fallout.

Canonical project repository: `bertjerk660-dotcom/REM1`. The main baseline inspected at session start was `3610b370d62fb0daa86b10f819b7704ab096809b`; related preparation/runtime branches were reconciled rather than assumed merged. This work is isolated on `prep/gmod-dependency-evidence-20261007`.

Original source installation: `C:\Program Files (x86)\Steam\steamapps\common\GarrysMod`. `garrysmod.ver` reports `260917`, `1920`, `prerelease`; `steam.inf` reports `PatchVersion=2026.04.29`. Both identifiers are retained. The local engineering folder is `C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2`; its lack of a Git checkout is documented rather than assigning it an invented current branch.

## Read the evidence

| Deliverable | Authored report / machine-readable evidence |
| --- | --- |
| Repository reconciliation and prior-work audit | [REPOSITORY_RECONCILIATION.md](REPOSITORY_RECONCILIATION.md) |
| Combined original-system architecture and flow diagram | [ARCHITECTURE_REPORT.md](ARCHITECTURE_REPORT.md) |
| GMOD architecture: Q input through panels/assets to spawn | [QMENU_ARCHITECTURE.md](QMENU_ARCHITECTURE.md) |
| Tool Gun and real Q-selected mode/registry/callback chain | [TOOLGUN_ARCHITECTURE.md](TOOLGUN_ARCHITECTURE.md) |
| Physics Gun native behavior, original visuals/audio/model paths | [PHYSGUN_ARCHITECTURE.md](PHYSGUN_ARCHITECTURE.md) |
| Notifications, hints, kill feed, fonts and HUD interfaces | [OTHER_OVERLAY_SYSTEMS.md](OTHER_OVERLAY_SYSTEMS.md) |
| GMOD / adaptation / Fallout boundary | [INTEGRATION_BOUNDARY.md](INTEGRATION_BOUNDARY.md), [COMPATIBILITY_MATRIX.md](COMPATIBILITY_MATRIX.md) |
| Existing integration classification and regression hypotheses | [EXISTING_IMPLEMENTATION_AUDIT.md](EXISTING_IMPLEMENTATION_AUDIT.md) |
| IDA Pro 6.8 build/function investigation | [IDA68_NATIVE_REPORT.md](IDA68_NATIVE_REPORT.md) |
| Inventory, actual staging, reuse, validation and remaining gaps | [STAGING_SUMMARY.md](STAGING_SUMMARY.md) |
| Required fourteen-subsystem dependency graph | [dependency_graph.json](../../manifests/gmod_2026-10-07/dependency_graph.json) |
| Every selected original resource's provenance | [asset_provenance.json](../../manifests/gmod_2026-10-07/asset_provenance.json) |
| Explicit unresolved dependencies / next evidence | [unresolved_dependencies.json](../../manifests/gmod_2026-10-07/unresolved_dependencies.json) |

Subsystem manifests, native-function records, compatibility metadata and validation reports live under `manifests/gmod_2026-10-07/`. Authored inventory/staging and metadata-validation tools live under `research/`. Windows local staging retains original internal paths and proprietary payloads; GitHub contains reports, tooling, graph/manifest data and hashes only.

## Conclusions to preserve

1. The original spawnmenu is a persistent GMOD panel hierarchy. Loading original icons into the current Fallout-authored menu does not preserve that hierarchy, behavior or native model-icon service.
2. Original Q/tool selection must set the actual original tool mode and reach `gmod_tool` lifecycle/dispatch without a Fallout function-selection popup.
3. Physgun native behavior requires build-specific controller/input/render evidence. Original Lua hooks and assets expose useful boundaries; symbols/strings alone must not be promoted into exact behavioral proof. The project's requested launch action must be distinguished from original input semantics.
4. Original GMOD transient UI has its own panels, materials, fonts, timers, animation and callers. Fallout top-left messages do not satisfy that presentation contract.
5. The necessary bridge is an API/runtime contract: GMOD Lua dialect and original registries/panels/tool logic on one side; stable Fallout refs, Havok, graphics/audio, input ownership and world state on the other. The unresolved native/icon/model/actor boundaries remain explicit.

## Local and Git boundaries

This pass does not deploy a DLL/ESP, edit the source game, convert or invent assets, rewrite the active runtime, start a gameplay test, or change unrelated THUG2 work. Source/deployed hashes and evidence limits are recorded in the implementation audit and staging validation. Working runtime components remain integration-owner inputs, not targets for speculative replacement.

The repository's existing Opus ownership handoff is honored by keeping this pass within evidence, manifests, selective staging, validation tooling and documentation. No additional approval gate was invented for authorized support work.

Existing canonical preparation JSON with appended device-output footers is historical evidence, but is not strict machine-readable JSON. New manifest validation rejects that format and preserves the older files unchanged.
