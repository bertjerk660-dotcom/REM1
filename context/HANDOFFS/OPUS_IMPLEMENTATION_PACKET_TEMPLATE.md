# Opus Implementation Packet Template

Use this only for **Claude Opus**. Do not group another agent with Opus.

## Package identity
- Package ID:
- Feature:
- Prepared by normal GPT:
- Reviewed Codex evidence commit(s):
- Implementation owner: Claude Opus
- Runtime validation owner: Codex

## Player-visible objective
Describe exactly what the player should experience.

## Existing verified behavior to preserve
List every currently working behavior that must not regress.

## Source-faithful behavior
Summarize the original-game behavior proven by Codex. Do not fill gaps by assumption.

## Codex evidence
For each evidence item record:
- repository path;
- branch;
- commit;
- source game/build;
- function/address if applicable;
- confidence;
- unresolved points.

## Provenance / required source and assets
For each:
- source game;
- original path/package;
- source hash;
- staged/converted path;
- dependencies;
- intended Fallout destination;
- current-local hash verification status.

## Host adapter contract
Define:
- inputs;
- outputs;
- ownership boundaries;
- lifetime;
- error/cleanup behavior;
- serialization policy;
- input/UI/camera ownership where relevant.

## Implementation boundaries
State exactly what Opus owns in this package.

## Explicit non-goals
List what must not be implemented, approximated or guessed here.

## Failure knowledge
Link all relevant FAILURE_KNOWLEDGE / FAILURE_LEDGER entries and the prevention rule for each.

## Acceptance criteria
Reference exact ACCEPTANCE_MATRIX rows and package-specific checks.

## Required outputs
- source changes;
- build outputs;
- asset outputs;
- manifest;
- hashes;
- rollback artifacts.

## Candidate freeze
Before Codex receives the build, record:
- implementation branch;
- commit;
- parent;
- source hash;
- DLL/ESP hashes;
- changed asset hashes;
- load order;
- test save/location;
- required inventory/state;
- known issues.

Use `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`.

## Codex validation
Point to the exact R-test pack(s) and any feature-specific steps.

## Promotion rule
No CURRENT_STATE success claim until the exact frozen candidate passes required Codex runtime/regression gates and any required human playability check.
