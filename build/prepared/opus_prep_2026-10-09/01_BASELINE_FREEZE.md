# 01 — Baseline freeze (BL-2026-10-09-A)

Status: local, unmanifested baseline. Documentation only. No runtime file was modified to produce this record.
Purpose: give Opus one frozen identity for "what is running now" before any implementation starts. Follows the preflight rule in `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`.

## Source

| File | SHA-256 | Size | Last modified |
|---|---|---|---|
| `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp` | `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE` | 237,209 | 2026-10-06 20:21:40 |
| `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/gmod_overlay.inc` | `E6EF0C484AFDDC1A74C02F6BA8A72CD0899D6E80F5BA5459CD61B9C67183250F` | 31,840 | 2026-10-05 15:48:12 |

- The plugin source labels itself v85 (per `CURRENT_STATE.md`, 2026-10-07 section).
- Not a git checkout locally. No commit can be read from the workspace.
- **Stale value, do not use:** the 2026-10-06 feed-bundle `main.cpp` hash `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5` does not match the current file.

## Deployed binaries (Fallout New Vegas `Data\NVSE\Plugins` and `Data`)

| File | SHA-256 | Size | Last modified |
|---|---|---|---|
| `NVSE\Plugins\FNVGModTHUG2.dll` | `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206` | 908,800 | 2026-10-06 20:22:26 |
| `NVSE\Plugins\REMGoodspringsResponse.dll` | `2FCEAC8BB4B3AD11B774F9B9B0D9F97A08E9D9372205C9A7E4E34F2BF4F0F13F` | — | 2026-10-07 06:37:49 |
| `Data\REM_GModTHUG2.esp` | `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7` | — | 2026-10-05 17:45:24 |

Relationship between source and DLL: the DLL was written 46 seconds after `main.cpp` was last saved. That fits a build from this source, but it is **not proven**. Confirm by rebuilding from the frozen source and comparing hashes, or by recording the compiler command and output.

Not re-hashed in this pass: the held-board NIF `Data\meshes\rem\thug2\skateheldx.nif`. The v82 manifest records `4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A`. Re-hash before relying on it.

Hashes that do **not** match the deployed DLL, so none of these describe what was tested:
- v81 `A801DC80...`, v83 `423742E0...`, v84 `273CEB41...`, v85 `BC24E9B1...`.

## Load order (`%LOCALAPPDATA%\FalloutNV\plugins.txt`)

Active:
1. `FalloutNV.esm`
2. `REM_GModTHUG2.esp`
3. `REM_CombineArmor_Test_TorsoLowered.esp` — **support sidecar, not core**
4. `REM_Goodsprings_CombineDeathclawEncounter.esp` — **support sidecar, not core**

The 2026-10-09 playtest ran with sidecars 3 and 4 enabled.

Present in `Data` but not active: 7 `REM_CombineArmor_Test_*` variants, `REM_CombineSolider_GoodspringsRampage.esp`, `REM_GModProps_Catalog.esp`, `REM_WeaponPresentation_Fixes.esp`, `REM_GModTHUG2_firstperson_patch.esp`, `REM_GModTHUG2.pre_v79_persistent_board.esp`.

## Frozen baseline definition for Opus

For the core test, Opus should use this configuration:
- Disable sidecars 3 and 4 unless the test explicitly targets them.
- Record the load order above in the implementation manifest.
- Use the deployed hashes above as the "before" state.

## Open items to close before implementation

1. Identify the exact git commit that `main.cpp` (`4517D804...`) came from, or commit it to a named branch and record that commit. The workspace has no git history.
2. Confirm the DLL was built from this source (rebuild and compare, or record the build command).
3. Re-hash `skateheldx.nif`.
4. Resolve the branch name. Two prep branch names appear in the handoffs: `prep/opus-ready-20261007` and `prep/opus-readiness-finalization-20261007`. The launch sequence requires one to be chosen and recorded.
5. Note that the main-branch snapshot (`REM1-main.zip`) does not include the `build/prepared` folders, most `OPUS_*` handoffs, or the GMod bundle. See `02_THUG2_EVIDENCE_INVENTORY.md`.

## Update 2026-10-09 (after the five-item pass)

- **Held-board NIF mismatch.** Re-hashed `Data\meshes\rem\thug2\skateheldx.nif`: SHA-256 `1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852`, 57,753 bytes, modified 2026-10-06 07:22:09. The v82 manifest records `4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A`. The deployed NIF is therefore **not** the v82 asset. It was changed after v82 and no manifest records the change. Identify it before any claim about held-board appearance.
- **Sidecars disabled.** `plugins.txt` now lists only `FalloutNV.esm` and `REM_GModTHUG2.esp`. Original saved at `%LOCALAPPDATA%\FalloutNV\plugins.txt.pre_opus_2026-10-09.bak`.
- **Not yet disabled:** `NVSE\Plugins\REMGoodspringsResponse.dll` still loads, because NVSE loads plugin DLLs from the folder regardless of `plugins.txt`. Moving it out is a separate decision.
- **Git:** `git` is installed locally, but the workspace is not a repository and `gh` is not installed. Committing or pushing to GitHub needs an authenticated remote and a chosen branch.
- **Rebuild check:** MSVC is installed but not on PATH, and no build script was located. Item 2 (rebuild and compare hash) is not done.
