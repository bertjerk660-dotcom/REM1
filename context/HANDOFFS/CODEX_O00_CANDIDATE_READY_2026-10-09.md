# O00 candidate ready for Codex runtime validation - 2026-10-09

Status: **FROZEN - WAITING FOR CODEX VALIDATION**. Run the existing test pack
`context/HANDOFFS/CODEX_O00_GOLDEN_BENCH_RUNTIME_VALIDATION_2026-10-07.md` (O00-R1..R7).
Do not patch the candidate. Return one verdict: PASS / FAIL / BLOCKED_BY_CANDIDATE_IDENTITY / BLOCKED_BY_ENVIRONMENT.

## Candidate identity

| Item | Value |
|---|---|
| Branch | `implementation/opus-o00-golden-bench-20261009` |
| Tooling commit | `94206ab77cbb7304d8a2ec32022b91cc92071587` |
| Parent commit | `ba35ebe4402cba7482ff1a735494e3de469aa4ae` (prep/gmod-research-intake-20261009) |
| Manifest | `builds/O00_golden_bench_candidate_20261009.json` (freeze PASS) |
| Static report | `build/candidates/O00_20261009/o00_static_validation.json` (12/12 PASS) |

Deployed files (new paths only; hashes in the manifest `outputs`):
- `Data/REM_GoldenBench_Test.esp`
- `Data/meshes/rem/golden_bench/bench01a.nif`
- `Data/textures/rem/golden_bench/bench01a.dds`, `bench01a_m.dds`, `bench01a_n.dds`

## Test setup

1. Confirm the protected hashes in the manifest `rollback.previous_hashes` still match (DLL, main ESP, main.cpp, skateheldx.nif). Any drift: BLOCKED_BY_CANDIDATE_IDENTITY.
2. Back up `%LOCALAPPDATA%\FalloutNV\plugins.txt`, then append one line: `REM_GoldenBench_Test.esp`. Expected active list: FalloutNV.esm, REM_GModTHUG2.esp, REM_GoldenBench_Test.esp.
3. Copy `Save 22   Glerb  Hidden Valley  00 34 52.fos` to a disposable slot and load the copy only. Verify the original's SHA-256 against the manifest first.
4. Record whether `Data/NVSE/Plugins/REMGoodspringsResponse.dll` is present (it loads regardless of plugins.txt; not changed by O00).
5. In game, open the console and run `player.placeatme 02000800 1`. If the sidecar's load-order index is not 02, use that index instead.
6. Run O00-R1..R7.

## What to look at (from the converter's own evidence)

- Expected size: about 133 x 41 x 69 game units (about 1.9 m long, 1 m tall), seat at about 37 units. Bench faces the direction the player faced when it spawned (+Y), backrest behind.
- Collision is 15 separate boxes matching the slats, legs and backrest. The space under the seat should be **open** (no invisible box). Player should be blocked by legs, seat and back.
- Collision material is wood (`HAV_MAT_WOOD`): footsteps/impacts should sound like wood, not metal.
- Reflections are deliberately faint (original mask mean 16/255) using the vanilla `shinydull_e.dds` cubemap.

## After the test

- Run `build/candidates/O00_20261009/ROLLBACK_O00.ps1` only if the owner asks to remove the candidate. It deletes only the five files above and the plugins.txt line.
- Restore plugins.txt from your backup after testing unless the owner wants the sidecar left on.

## Update 2026-10-09 11:35

Codex credits ran out; Claude Opus ran O00-R1..R7 on the owner's instruction. All PASS as an Opus self-test (not independent): `build/candidates/O00_20261009/o00_runtime_selftest_20261009.json`. If Codex becomes available, an independent rerun is still welcome, mainly for audio and daylight appearance.
