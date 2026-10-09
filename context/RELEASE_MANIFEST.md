# Release / Install Manifest

This is the current staging/install ledger, not a claim that the mashup is release-ready.

## Current baseline
- Installed runtime: v85.
- Installed DLL SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Active REM_GModTHUG2.esp SHA256: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
- Astra v88 remains isolated/not installed: 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.

## Indexed install/staging content
- 6 core runtime/test-plugin files indexed with no missing core file.
- 4 Pip-Boy source-origin icon files indexed.
- 4 THUG2 skateboard NIFs indexed.
- 2 Combine Soldier test NIFs indexed.
- 205 unique converted GMod prop payload files (NIF/material payloads) indexed.
- Final content catalog: 290 entries = 170 native FNV references + 120 custom GMod/Source entries.
- Native FNV assets remain host-game dependencies and are not duplicated into the package.
- Reproducibility/support manifests are indexed separately; current count: 15.

## Disabled support plugins
- REM_CombineArmor_Test.esp — static validation pass; human armor pack pending.
- REM_GModProps_Catalog.esp — 120 records; static validation pass; representative spawn/collision pack pending.
- REM_WeaponPresentation_Fixes.esp — RPG presentation only; static validation pass; human presentation pack pending.

All three remain disabled.

## Promotion gates
- Unified support validator must pass with zero errors. Current result: 111 checks / zero errors.
- Baseline Fallout boot/load/save/load regression.
- GMod/THUG2 inventory icon/name/drop/pickup/container/trade checks.
- Representative prop material/scale/collision checks.
- Combine armor player/NPC/world/save-load checks before any Enclave/Remnants replacement.
- Astra-owned THUG2 skating physics/animation/camera/HUD/input integration.
- Astra-owned real GMod Q-menu/Tool Gun/Physgun runtime integration.
- First-person/world animation and weapon presentation validation.

## Packaging policy
Do not commit or package original game archives/executables. Proprietary source-game assets remain local; repository history carries project-authored tooling, mappings, hashes, validation results and handoff knowledge. Any distributable transformed payload must be reviewed separately for release rights.

Machine-readable local manifest:
`build/prepared/release_install_manifest/manifest.json`

Latest local manifest SHA256:
`0CD126920013F0766F80F3579A704C50235D81102659AC2BC765A99E87046377`
