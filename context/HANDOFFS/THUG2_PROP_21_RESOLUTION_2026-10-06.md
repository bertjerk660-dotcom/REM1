# THUG2 21-Unresolved Prop Evidence Resolution - 2026-10-06

The prior 21 not_ready count did not mean 21 missing models.

Re-analysis of build/prepared/thug2_prop_catalog/target_classification.json plus decompiled original THUG2 QB evidence resolves the set as:
- 14 semantic gap/trigger/hit/transfer identifiers, not standalone prop geometry.
- 7 named identifiers without a LevelGeometry/position binding. Their available occurrences are script/event/sound semantics rather than independently extractable geometry.
- 0 of these 21 can be promoted as a real prop without inventing geometry.

The extractable embedded-geometry pool therefore remains the 85 spatial_geometry_candidate records already backed by original QB positions and nearby converted level geometry.

The 21 are closed as an extraction backlog and retained as semantic/research records. Stronger original-game evidence can reopen an individual entry later.

Machine-readable result: build/prepared/prop_support_phase4/thug2_21_resolution.json
Reproducer: research/resolve_thug2_21.py

This follows the project rule: do not recreate assets or turn a trick/gap identifier into fabricated geometry.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]