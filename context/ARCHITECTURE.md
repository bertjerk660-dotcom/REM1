# Architecture

This document records intended architecture; implementation must be checked against source before being treated as current fact.

## Integration boundaries
Fallout: New Vegas remains the host game/runtime and baseline gameplay state.

Imported systems should be isolated behind explicit integration layers where practical:
- skateboard item/state transition layer;
- THUG2 skating movement/camera/animation integration;
- GMod Tool Gun tool-selection and action integration;
- GMod Physics Gun interaction/rendering integration;
- inventory/drop/pickup/world-presentation integration.

## State transitions
Normal Fallout gameplay is the default state. Skate mode is entered deliberately through the skateboard item/action and exited deliberately back to normal Fallout behavior.

## Reproducibility
Reverse-engineering discoveries should be captured as documented offsets/signatures/behavioral notes or tooling rather than existing only inside an IDA database or chat. Build transformations should be scripted where practical and recorded in manifests.


## 2026-10-09 Bevy successor architectural boundary (new edition)

**The architecture above is authoritative for the legacy Fallout/NVSE edition only.** For the future primary standalone Bevy/Rust edition (D-012), avoid the NVSE host runtime dependency entirely. Use a new Bevy Cargo workspace and edition-isolated executable, asset conversion/import process, data schemas, persistent entity IDs, physics/collision and rigging layers, ECS systems/plugins, GMod tool/Q UI bridges, THUG2 skater/board mode, default Fallout-like world/gameplay loop, unified KBM/Xbox input, and separate save/load and validation. Maintain provenance and per-subsystem behavior mappings from local FNV/GMod/THUG2 research. Do not treat the installed Rust/Bevy dependency probe as an engine implementation. The Opus handoff contains the initial architecture/validation plan, to be refined and recorded by Opus in a dedicated Bevy architecture ADR before substantive coding.
