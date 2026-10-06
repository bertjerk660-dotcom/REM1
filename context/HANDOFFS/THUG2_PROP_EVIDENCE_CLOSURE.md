# THUG2 unresolved-prop evidence closure — 2026-10-06

Status: OLD 21-ITEM 'UNRESOLVED PROP' BACKLOG RETIRED.

The phase-4 catalog reported 21 not-ready targets. Reinspection of the decompiled level QB evidence shows this was a classification backlog, not 21 missing standalone models.

## Result
- 14/21 were already classified semantic_or_gap_identifier: gap, transfer, hit or trigger semantics. They are gameplay metadata, not extractable standalone prop geometry.
- The remaining 7 named targets have no reliable independent Name-block/position/geometry binding in the recovered QB evidence. Their occurrences are script/event/sound semantics:
  - AP_circlebench — invoked by AP_Counter scripts; no independent geometry binding recovered.
  - BE_Bench2Ledge — gap/transfer-style script calls with BE_ledge2bench01; no independent geometry binding.
  - BE_ledge2bench01 — paired gap/transfer-style script call; no independent geometry binding.
  - DJ_WoodBarrier — recovered as SoundType = DJ_WoodBarrier near level-geometry component data; the identifier itself is not proven to name a standalone mesh.
  - CPF_PershingRamp1 — called by rail trigger scripts; no independent mesh binding recovered.
  - PH_LedgeToHandE — called by trigger script; no independent mesh binding recovered.
  - ST_BigRamp — called by camera/huge-ramp trigger script; no independent mesh binding recovered.

## Corrected interpretation
These 21 entries must not block the THUG2 prop handoff. None has sufficient evidence to justify inventing or guessing a standalone mesh. If later extraction discovers a concrete scene-component/mesh binding, it can be promoted as new evidence; until then these identifiers belong to gameplay/level semantics, not the prop conversion queue.

## Existing prop readiness remains authoritative
- 106 catalog targets were audited.
- 85 have evidence-backed component/position readiness from the existing phase-4 pipeline.
- The 21 old not-ready entries are now excluded from standalone-geometry expectations rather than counted as missing models.
- This closure does not assert that all 85 are already converted/placed in FNV; it asserts the input evidence needed for the integration/conversion agent is ready and the false 21-model requirement is removed.

## Handoff rule
Do not recreate assets for these 21 identifiers. Use only recovered original THUG2 geometry/component bindings. Semantic identifiers should be implemented only if/when the corresponding gameplay/gap/trigger behavior is intentionally ported.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]