# Opus Fix Packet Template

Use only after Codex reports a deterministic failure against a frozen implementation candidate.

## Failed candidate identity
- Package:
- Branch:
- Commit:
- Parent:
- Source SHA256:
- DLL/ESP hashes:
- changed asset hashes:
- Load order:
- Save:
- Location:
- Required inventory/state:

## Codex failure
- Runtime test pack:
- Exact failing step:
- Expected:
- Observed:
- Reproduction frequency:
- Logs/crash evidence:
- Screenshots/video evidence if applicable:
- Suspected subsystem boundary:
- Confidence:

## Protected behavior
List all passing behavior that must remain unchanged.

## Failure-knowledge match
- existing failure ID/title:
- same root cause / related / new:
- proven prior fixes that must not be undone:

## Opus fix scope
Define the smallest implementation area Opus should modify.

## Do not change
List unrelated systems, assets, serialization, input ownership, camera ownership or working paths that should remain untouched.

## Required post-fix artifacts
- fix branch/commit;
- source hash;
- DLL/ESP/asset hashes;
- updated candidate manifest;
- actual root-cause explanation;
- rollback path.

## Return to Codex
Re-run the originally failing step first, then the affected subsystem pack, then any cross-system pack required by ACCEPTANCE_MATRIX.

Do not mark fixed from compilation/static validation alone.
