# Codex runtime validation packet template

Use this after **Claude Opus** creates an implementation candidate. GPT-6/Astra is not used.

## Candidate identity
Record:
- subsystem;
- Opus branch;
- commit SHA;
- parent/baseline;
- source hash;
- DLL hash;
- ESP hash;
- asset-manifest hash/version;
- exact enabled plugins/load order relevant to the test.

Do not test an unidentified or drifting candidate.

## Preconditions
- run static/preflight validation;
- confirm candidate hashes match the handoff;
- use disposable/known-good saves where appropriate;
- capture current failure-knowledge entries relevant to the subsystem;
- define exact location/inventory/state needed.

## Deterministic test case format
For every test record:
1. setup;
2. exact steps;
3. expected result;
4. observed result;
5. PASS/FAIL;
6. screenshot/video/log/crash evidence;
7. cleanup/restore result;
8. regression impact.

## Failure handoff to Opus
On failure, report:
- first failing step;
- exact build/hashes;
- last known-good comparison;
- logs/crash exception;
- state immediately before failure;
- likely subsystem boundary;
- evidence-backed suspicion only, clearly distinguished from fact;
- minimal reproduction;
- regression tests that must be rerun after the fix.

Codex should not silently patch Opus implementation as part of validation. Return a precise failure packet to Opus.

## Completion rule
A candidate is not VALIDATED until all applicable acceptance gates pass, cleanup and save/load are verified where relevant, regressions pass, and required human-visible behavior has been confirmed.
