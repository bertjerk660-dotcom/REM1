# Opus Implementation Packet Template

Use this only for **Claude Opus**. Do not group another agent with Opus.

## Feature objective
Describe one subsystem and the exact player-visible result.

## Original-game behavior
Summarize Codex-confirmed source behavior only. Mark unknowns.

## Codex evidence
List:
- evidence report;
- function/call map;
- state machine;
- dependency manifest;
- asset/UI/animation manifest;
- native interface evidence;
- confidence/unresolved items.

## Required source/assets
For each:
- source game;
- original path/package;
- hash/provenance;
- staged/converted path;
- dependencies;
- intended FNV destination.

## Host integration contract
Define the exact Fallout/xNVSE interfaces Opus must use or expose.

## Preserve
List already-working behavior that must not regress.

## Known failures
Link failure-ledger IDs relevant to this package.

## Implementation boundaries
State exactly what Opus owns and what must remain untouched.

## Acceptance criteria
Copy the applicable rows from `context/ACCEPTANCE_MATRIX.md` and subsystem-specific requirements.

## Codex runtime validation packet
Point to the exact R-test pack and any feature-specific steps.

## Completion evidence expected from Opus
- branch/commit;
- parent;
- source hash;
- DLL/ESP/assets hashes;
- build result;
- changed files;
- known compromises;
- items not tested;
- candidate manifest.

Implementation is not called validated until Codex runtime/regression tests pass.
