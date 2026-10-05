# Prop and weapon-model preparation handoff

Prepared 2026-10-05 for later GPT-6 Astra integration. This work is asset preparation only: it does not alter the active NVSE DLL, ESP, THUG2 HUD candidate, animation runtime, weapon behavior, or Fallout Data deployment.

## GMod / Half-Life actual weapon model packages
- Referenced Source weapon/view/world models: 73.
- Existing project extraction/decompile packages staged: 71.
- Unmatched references: 2: models/weapons/v_eq_flashbang.mdl; models/weapons/v_pistol.mdl.
- Local root: build/prepared/gmod_hl_weapon_models.
- Each matched package preserves raw Source components (MDL/VVD/VTX/PHY when present), QC/SMD decompile output and animations, extracted materials, plus conversion worker provenance.

## Fallout New Vegas prop catalog
- The broad extraction/index remains available as research data: 14,909 unique native NIF paths and 13,003 environmental/world candidates.
- The 13,003-candidate set is NOT the intended GMod-style spawn menu.
- A curated 300-prop library is now the intended menu target.
- Local curated root: build/prepared/fnv_prop_catalog_curated.
- Curated categories deliberately favor skateable and useful environment pieces:
  - Rails & railings: 30
  - Benches: 18
  - Ramps & stairs: 30
  - Ledges & barriers: 20
  - Tables & counters: 20
  - Crates & large boxes: 16
  - Pipes: 10
  - Fences: 16
  - Signs: 20
  - Lamps & poles: 16
  - Small street props: 20
  - Chairs & couches: 16
  - Storage furniture: 18
  - Desks: 10
  - Vending machines & terminals: 10
  - Rocks: 10
  - Trees & plants: 10
  - Misc environment: 10
- The full 13,003-prop catalog remains useful only for future search/replacement if a better prop is needed.
- Astra should expose only the curated set after collision, scale, Havok and independent-spawn validation, then optionally swap individual props based on playtesting.

## THUG2 prop catalog
- Standalone .mdl.ps2 models inventoried: 174; converted to GLB: 173.
- Conversion failures: 1 (models/fireball/fireball.mdl.ps2).
- Primary non-_net level GEOM bundles: 45; converted whole-level GLBs: 45.
- Decompiled level QB files: 154; broad prop-keyword index contains 57,814 matching lines and 25,472 identifiers.
- Local root: build/prepared/thug2_prop_catalog.
- Standalone assets are directly separable. Benches, railings, ledges, barriers and other map furniture are frequently embedded inside level GEOM. The prepared whole-level GLBs expose their mesh leaves; later Astra work must correlate those leaves with QB/scene identifiers and split/convert them into independent FNV props before menu registration.

## Later Astra integration order
1. Read the summary manifests and this handoff.
2. For GMod/Half-Life weapons, use the staged actual Source packages and validate first-person attachment/animation separately from world/drop models.
3. For FNV props, use the curated 300-prop set as the spawn-menu target, not the full 13,003 archive.
4. Favor skateable environment pieces in the first menu categories: rails, benches, ramps, stairs, ledges, barriers, tables, crates and pipes.
5. For THUG2, use standalone GLBs directly as conversion inputs and use the prepared level GEOM + QB correlation data for embedded props such as benches/rails.
6. Only after asset validation should runtime/ESP/spawn-menu coding be performed.
