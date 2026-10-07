# Held Skateboard Provenance Resolution — 2026-10-08

Scope: documentation/provenance reconciliation only. No NIF, DLL, ESP or game file was modified.

## Resolution

The previously reported `skateheldx.nif` hash discrepancy is **not an unexplained identity drift**.

It is a documented asset supersession:

1. v82 deployed the held-board container candidate with SHA256:
   `4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A`

2. The later v90 board-material repair explicitly used that exact hash as the **before** identity and produced:
   `1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852`

3. The v90 deployment manifest states:
   - `deployed: true`;
   - `roundtrip: pass`;
   - scope = `Opaque original board material restoration; geometry and placement unchanged`.

4. The later release-install inventory records the deployed `Data/meshes/rem/thug2/skateheldx.nif` as:
   `1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852`

5. The Haiku local re-hash on 2026-10-07 found the same `1FB3...` hash.

## Evidence chain

Historical v82 manifest:
- `builds/v82.json`
- preserved by commit `1733d70cb4f4d20d5b339d4510aceb7b356c5794`
- recorded v82 deployed hash: `4F121...`

Historical v90 material deployment:
- source branch evidence: `feature/thug2-native-ui-g6:builds/board_material_deployment90.json`
- Git blob: `27aa43117a633eb942616eade6fd16cadfd1fc0a`
- same manifest also exists on `runtime/astra-phase1-input92`
- exact transition:
  - before: `4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A`
  - after: `1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852`

Later installed-release inventory:
- `build/prepared/pre_opus_20261006/release_install_overlay.json`
- records `1FB3...` as installed support asset.

## Correct interpretation

- `4F121...` = **historical v82 held-board identity before v90 material repair**.
- `1FB3...` = **later deployed material-repaired held-board identity**.
- v82 itself remains a historical build record; its hash should not be rewritten.
- Current documentation must not describe `1FB3...` as unexplained drift from v82.
- This resolution does **not** prove full THUG2 board-to-feet, animation or skate-mode runtime correctness.
- The human-verified held-board visibility/placement evidence remains a separate runtime observation.

## Status

**PROVENANCE DRIFT RESOLVED.**

No owner choice between the two files is required: the repository records a valid before→after transformation.
