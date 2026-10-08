# Normal-GPT live pre-Opus audit — 2026-10-08

**Scope:** non-implementation coordination, read-only validation, and local workflow-tool synchronization. Neither game runtime, ESP, NIF, original assets, nor Opus/Codex evidence were edited. GitHub coordination base: `prep/gpt55-coordination-20261008`; working report branch: `prep/normal-gpt-preopus-local-audit-20261008`.

## Authority and readiness

- Canonical `main` retains the authenticated GMod evidence, while the coordination branch compared 170 commits ahead / 0 behind `main` when checked. This does not establish promotion to main.
- Readiness remains **81/100**. C01–C08 are not completed. GitHub issue #5 remains open; only reviewed Codex evidence can earn the remaining 19 points.
- The previous 20-point support preparation tracker is **support-prep complete**, **not game-runtime complete**. Do not redo asset inventories, icon thumbnails, or source staging without a specific new defect.
- Prior 2026-10-08 work already explained the held-board identity transition: historical v82 `4F12178D...` -> later v90 material repair `1FB3CE19...`. Do not reopen it as unexplained drift.

## Direct checks performed on the authorized PC today

| Check | Result | Interpretation |
|---|---|---|
| `research/validate_opus_visual_source_packets.py` against local original-source packets | **PASS: 87 files / 0 errors** | O00/O01/O08a/O08b/O08c source hashes resolved; no in-game visual pass implied |
| `research/validate_opus_gate_state.py` | **PASS: 81/100 / 0 errors** | No false unlocks; scoring unchanged |
| `research/validate_opus_candidate_manifest.py --mode preflight` on the **five candidate seeds in `build/templates/`** | **PASS: O00, O01, O08a, O08b, O08c; 0 errors each** | Seed preflight only. O01/O08x are still blocked until O00 succeeds |
| `research/validate_codex_readiness_outputs.py --mode baseline` after synchronizing the GitHub v2 script and contract | **CONSISTENT; 46 PENDING; invalid JSON 0** | These files do not exist yet because Codex has not delivered them. Structural delivery and semantic review remain pending |
| Local installed GMod/New Vegas DLL + ESP + source hashes | **MATCH canonical 2026-10-07 runtime snapshot** | Protect these identities until a deliberate implementation candidate is frozen |
| Installed `skateheldx.nif` | **Matches documented v90 material-repaired hash** | Provenance consistency only; skating animation still incomplete |
| Goodsprints Combine/Deathclaw companion ESP/DLL/voice asset static inspection | **Assets present and parse; no playtest** | Separate encounter sidecar, not verification of any named Combine Elite objective |

**Important test invocation distinction:** passing the prepared-package manifest JSON (not a candidate seed) to `validate_opus_candidate_manifest.py` produces 19 expected schema/field errors. That invocation was corrected; all five actual candidate seeds passed.

## Local workflow improvement completed

The local Codex evidence validator and its contract were an older v1 copy that treated 46 future deliverables as structural failure before Codex had even run.

- Copied the exact existing v1 files into `build/workflow/backups_20261008/` on the Windows machine.
- Synchronized `research/validate_codex_readiness_outputs.py` and `build/prepared/codex_c01_c08_output_contract_20261007.json` directly from `prep/gpt55-coordination-20261008` (v2 contract and baseline/delivery validator).
- Re-ran baseline mode and observed **CONSISTENT, 46 pending, 0 invalid JSON**.
- Do **not** use `--mode delivery` until Codex explicitly submits the corresponding evidence output package. File presence alone never awards points.

This local synchronization touched only workflow files and their backups, not any game/Opus implementation source.

## Protected local runtime identity observed today

- Installed `Data/NVSE/Plugins/FNVGModTHUG2.dll` SHA256: `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206`
- Installed `Data/REM_GModTHUG2.esp` SHA256: `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7`
- Current local `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp` SHA256: `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE`
- Installed `Data/meshes/rem/thug2/skateheldx.nif` SHA256: `1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852`

These are preserved identities, not evidence of gameplay stability. Rehash immediately before an Opus edit or Codex test because another session may change the PC.

## O00 launch blocker requiring explicit decision

Current local FalloutNV `plugins.txt` includes four non-comment lines:

1. `FalloutNV.esm`
2. `REM_GModTHUG2.esp`
3. `REM_CombineArmor_Test_TorsoLowered.esp`
4. `REM_Goodsprings_CombineDeathclawEncounter.esp`

The two additional test sidecars are **currently listed as enabled**; previous status notes may refer to differently named disabled prototype sidecars. Do not silently alter the load order, delete sidecars or claim a clean O00 test with these unexplained.

Before O00, Opus/the test owner must either isolate unrelated test ESPs reversibly with a backup and exact before/after manifest, or explicitly include them in the frozen candidate's load order and acceptance boundaries.

The local historical `research/check_opus_launch_state.ps1` guard hard-codes older expected source/DLL hashes (`CE3628...`/`BC24E9...`); this is **stale against the current independently verified baseline**. Do not treat a failure from that old guard as evidence the active game source is broken. Refresh the guard from pinned source evidence before reusing it; this pass did not edit or run it.

## Targeted work before the next Codex / Opus sessions

1. **Codex at the user-chosen 10:45 PM slot:** give the targeted C01–C03 GMod gap-closure prompt already drafted (Q menu/tool mode/Physgun native boundaries, popup/prop-spawning and player-model-changing gaps). This prompt has **not yet been sent**. Keep original source evidence separate from FNV adapter proposals. After C01–C03, move to C04 THUG2 state/physics, which the repository names the next *new* investigation.
2. **Normal GPT immediately after a Codex delivery:** use `research/validate_codex_readiness_outputs.py --mode delivery --package C0x`, then `context/OPUS_PACKAGE_INTAKE_CHECKLIST_2026-10-07.md`; review source hashes/functions/states, resolve contradictions, create final O02/O03/O04 packet only if proven, update issue #5 and the gate score accordingly.
3. **Opus first session:** use `context/HANDOFFS/OPUS_SESSION_1_START_HERE_2026-10-07.md`, then `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`. Branch/freeze parent and exact hashes, choose sidecar policy, run candidate `--mode preflight`. Opus alone implements the isolated golden bench. Codex later validates, using the frozen manifest `--mode freeze` before handoff.
4. **After O00's actual accepted runtime PASS:** O01 Toolgun visuals and selected O08a/b/c visuals may unlock. O02/Q, O03/Toolgun behavior, O04/Physgun behavior must remain blocked without their respective Codex gate evidence.
5. **Separate deferred lane:** Goodsprings/Combine Soldier encounter and armor variants are locally staged/installed but have no recorded authoritative live completion test; do not mix them into O00 regression scope without explicit declaration.

## Remaining normal-GPT scope

Work on evidence/provenance indexing, package intake, manifest completeness, documentation/ownership drift, branch quarantine, preflight automation, test matrices, reversible load-order records, acceptance/rollback packets and playtest session checklists. **Do not implement GMod/THUG2 mechanics, change gameplay, run IDA in Codex's place, award evidence points, or merge quarantined code.**

No new C01–C08 gate is complete; readiness remains **81/100**. This is a documentation/workflow checkpoint, not a software release or live-game validation.
