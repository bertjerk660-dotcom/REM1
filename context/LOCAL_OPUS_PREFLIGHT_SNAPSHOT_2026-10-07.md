# Local Opus Preflight Snapshot — 2026-10-07

This is a current-local **identity/provenance check**, not a runtime-success claim.

## Provenance that still matches exactly

Remote Desktop Commander re-hashed the current machine:

- GMod Steam appmanifest:
  `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`
- `garrysmod_dir.vpk`:
  `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`
- THUG2 PS2 executable `SLES_526.21`:
  `91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1`
- extracted FNV skeleton used by the THUG2 evidence lane:
  `C6667DD94FD10392F851F748438B7C69C0D2CB407448BECAE6431D5ED1994C4C`

These match the existing provenance index exactly.

## Current project source/runtime identity

Current local `main.cpp`:
`4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE`

Old 2026-10-06 Opus feed-bundle source hash:
`CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`

**They do not match.** Therefore the old feed bundle remains useful as provenance/reference material but must not be treated as the exact current source baseline for a new Opus implementation branch.

Current installed main DLL:
`D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206`

Current active main ESP:
`0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7`

## Enabled support state

Current `plugins.txt` also enables:
- `REM_CombineArmor_Test_TorsoLowered.esp`
- `REM_Goodsprings_CombineDeathclawEncounter.esp`

Current support plugin:
- `REMGoodspringsResponse.dll`

These are separate support lanes and must not silently become part of an Opus core-system validation candidate.

## Opus preflight rule

Before the first Opus implementation:
1. select the exact source branch/commit to implement from;
2. freeze its source hash;
3. record installed DLL/ESP hashes;
4. decide whether unrelated support sidecars are disabled for the test or explicitly included;
5. record that load order in the build manifest;
6. never reuse the old feed-bundle source hash as if it still described the current local source.

Machine-readable companion:
`build/prepared/opus_readiness_20261007/local_preflight_snapshot.json`
