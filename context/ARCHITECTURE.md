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
