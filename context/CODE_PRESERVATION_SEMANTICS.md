# Code Preservation Semantics and Dependency Policy

Verified 2026-10-06 against the local engineering workspace and the support branch.

## Evidence classes
- **AUTHORITATIVE_PROJECT_TOOLING**: project-authored extraction, analysis, conversion, validation or packaging scripts. Preserve source and hash.
- **SOURCE_DERIVED_EVIDENCE**: xrefs, disassembly summaries, decompiled-QB hashes, manifests and mappings derived from installed source games. Preserve evidence/metadata; do not treat reconstructed output as original source.
- **GENERATED_HANDOFF**: generated manifests/catalogs/contracts. Rebuild from authoritative tooling when possible.
- **RUNTIME_EXPERIMENT**: version patches/candidates. Historical evidence only unless explicitly promoted and playtested.
- **PROPRIETARY_PAYLOAD**: original game binaries/assets. Do not commit to GitHub; preserve path, container, hash, extraction procedure and provenance.
- **SUPERSEDED_OR_CONFLICTING**: older or conflicting evidence retained for history but barred from silent promotion.

## Dependency rules
- Reverse engineering requiring IDA uses **IDA Pro 6.8**.
- IDA automation scripts are durable; IDB databases are local evidence and are not the sole source of discoveries.
- Python tooling must declare imported non-stdlib modules and expected input/output paths before promotion.
- Source-game payload dependencies are represented by hashes and paths, not copied into GitHub.
- Generated handoffs must name their generator and upstream evidence.
- Runtime experiments cannot be promoted merely because they compile.

## Current conflict requiring resolution
`research/thug2_fnv_bone_map.json` contains suspicious/dirty FNV targets such as `Bip01 PelvisE`, `Bip01 Neck/`, `Bip01 L Hand+` and `Bip01 R Hand-`. The later `thug2_exact_animation_manifest.json` contains clean targets such as `Bip01 Pelvis`, `Bip01 Neck`, `Bip01 L Hand` and `Bip01 R Hand`.

Until the provenance is re-run and validated against the actual FNV skeleton, the older map is **SUPERSEDED_OR_CONFLICTING**, not an authoritative retarget map. This also aligns with the known unsafe-retarget failure history.

## Current inventory
247 local research/code/metadata artifacts were frozen by hash. First-pass buckets: THUG2 63, GMod 59, FNV host 39, validation 17, general 69. Filename classification is discovery metadata only; semantic classification controls promotion.
