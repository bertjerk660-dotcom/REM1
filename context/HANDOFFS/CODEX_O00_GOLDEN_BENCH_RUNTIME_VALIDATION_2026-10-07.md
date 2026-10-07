# Codex O00 Golden Bench Runtime Validation — 2026-10-07

Run only after Claude Opus freezes an O00 candidate.

Codex is the validation/debug evidence owner, not the implementation owner.

## Required candidate identity

Record before launch:
- Opus branch;
- Opus commit SHA;
- parent commit;
- O00 candidate manifest path/hash;
- sidecar ESP path/SHA256;
- bench NIF path/SHA256;
- all generated texture path/SHA256 values;
- enabled plugin/load order;
- test save;
- test location/cell;
- relevant source-validation report identity.

If any expected identity is missing or drifted, stop and return CANDIDATE_IDENTITY_FAIL.

## Isolation checks

Before testing:
1. verify main `REM_GModTHUG2.esp` hash matches the pre-O00 baseline unless explicitly declared changed;
2. verify main NVSE DLL hash matches pre-O00 baseline unless explicitly declared changed;
3. verify only the intended O00 sidecar is newly enabled for this test;
4. verify no quarantined v84-v92 runtime candidate was activated;
5. verify O00 candidate paths are isolated under the declared namespace.

Failure here is FAIL; do not continue and normalize an unidentified environment.

## Static/runtime test O00-R1 — boot/load

Steps:
1. start a fresh FalloutNV process;
2. load the declared known-good/disposable save;
3. verify baseline player control and HUD;
4. enter the declared O00 test area.

PASS:
- no startup/load crash;
- no unexpected imported-mode activation;
- baseline player control intact.

## O00-R2 — visibility/material

Observe the candidate bench from multiple angles and distances.

Verify:
- bench visible;
- geometry complete;
- no missing-purple/black/placeholder material;
- original material grouping preserved;
- mask/detail/specular intent visibly plausible for the mapped Fallout shader;
- normals are not inverted;
- no obvious z-fighting caused by conversion.

Capture screenshots.

## O00-R3 — scale/orientation/placement

Verify:
- bench orientation is correct;
- dimensions are credible relative to Fallout player/world props;
- no 90°/180° axis error;
- no obvious floating or sinking;
- origin/pivot produces stable placement.

Record any measurable or visual mismatch.

## O00-R4 — collision

Test from all practical sides:
- walk into bench;
- move around legs/seat/back;
- jump/contact where useful;
- confirm player cannot pass through expected solid regions;
- confirm collision is not a gross oversized invisible box;
- confirm collision does not trap the player unexpectedly.

Verify the candidate uses the documented justified Fallout Havok material rather than the historical silent wood→metal fallback.

## O00-R5 — sidecar/world behavior

Verify:
- only intended test record(s) exist/are exposed by the sidecar;
- disable/re-enable or unload/reload as applicable without corrupting baseline state;
- no unrelated inventory/menu/runtime behavior changes.

## O00-R6 — save/load

With the candidate active:
1. save to a disposable slot;
2. return to menu;
3. reload;
4. revisit/re-observe the bench.

PASS:
- no crash;
- bench state/presentation remains sane;
- no save corruption symptom.

## O00-R7 — Fallout baseline regression

Re-run representative R01 checks:
- move/look/attack/interact;
- Pip-Boy open/close;
- equipment change;
- save/reload.

PASS:
- no regression attributable to O00.

## Final verdict

Use exactly one:
- PASS
- FAIL
- BLOCKED_BY_CANDIDATE_IDENTITY
- BLOCKED_BY_ENVIRONMENT

A PASS requires O00-R1 through O00-R7 to pass.

On FAIL return:
- first failing test;
- expected vs observed;
- exact candidate identity;
- screenshots/video/logs;
- minimal reproduction;
- passing gates that must remain protected;
- suspected boundary clearly labeled as evidence-backed or speculative.

Do not patch the candidate during this validation task.

## Unlock effect

Only a reviewed O00 PASS allows normal GPT to change:
- O01 → READY FOR OPUS;
- O08a → READY FOR OPUS;
- O08b → READY FOR OPUS;
- O08c → READY FOR OPUS.

O00 PASS does not validate those packages themselves.
