# GPT-6 / Opus implementation input package — 2026-10-06

This directory is the machine-readable entrypoint for the next integration agent.

## Physics Gun
Use `physgun_implementation_package.json` with `context/HANDOFFS/PHYSGUN_IDA68_EVIDENCE_CLOSURE.md` and the existing original-asset/source handoffs. The native behavior evidence is closed. Runtime integration is intentionally not claimed. Preserve the explicit state machine and cleanup gates.

Known presentation gap: the installed GMod content references legacy `v_physics` view-model components that were not found in the mounted install. Do not silently substitute another model and call it source-faithful.

## THUG2 props
`thug2_85_conversion_inputs.json` contains exactly 85 evidence-backed geometry candidates. Each record carries the recovered level, identifier, category, source position, candidate-leaf count, source GLB and conversion gate.

The old 21-item unresolved list is retired by `context/HANDOFFS/THUG2_PROP_EVIDENCE_CLOSURE.md`. Those identifiers are not a requirement to fabricate 21 meshes.

## Rules
- Original game assets stay local; GitHub stores manifests, hashes, tooling and provenance.
- Do not mark a candidate integrated merely because conversion completed.
- Prop promotion requires visual identity/isolation, material provenance, NIF structure, texture resolution, collision, scale, spawn/contact stability, cleanup and Q-menu metadata checks.
- Physics Gun promotion requires all behavior gates in its package plus inventory/drop/pickup and save/load regression testing.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]