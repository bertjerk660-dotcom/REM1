# Prop and weapon-model preparation handoff

Prepared 2026-10-05 for later GPT-6 Astra integration. This work is asset preparation only: it does not alter the active NVSE DLL, ESP, THUG2 HUD candidate, animation runtime, weapon behavior, or Fallout Data deployment.

## GMod / Half-Life actual weapon model packages
- Referenced Source weapon/view/world models: 73.
- Existing project extraction/decompile packages staged: 71.
- Unmatched references: 2: models/weapons/v_eq_flashbang.mdl; models/weapons/v_pistol.mdl.
- Local root: build/prepared/gmod_hl_weapon_models.
- Each matched package preserves raw Source components (MDL/VVD/VTX/PHY when present), QC/SMD decompile output and animations, extracted materials, plus conversion worker provenance.

## Fallout New Vegas prop catalog
- Unique native NIF paths indexed from installed archives: 14909.
- Broad environmental/world spawn-prop candidates physically staged: 13003 (1654711813 bytes).
- Local root: build/prepared/fnv_prop_catalog.
- Full staged manifest: build/prepared/fnv_prop_catalog/manifest.json; complete NIF index including excluded actor/equipment roots: all_nifs_index.json.
- Useful name-tag counts include: sign=550, door=309, rock=306, tree=241, terminal=217, stairs=197, pipe=193, rail=145, fence=93, window=91, table=81, ramp=60, lamp=49, pole=49, barrier=44, crate=44, chair=33, bench=23, cabinet=21, trash=12, railing=10, ledge=8, vending=6, couch=3.
- Because these are already FNV-native NIFs, later menu work should normally reference their original meshes/... path; staging copies are for inspection/validation/thumbnail generation.

## THUG2 prop catalog
- Standalone .mdl.ps2 models inventoried: 174; converted to GLB: 173.
- Conversion failures: 1 (models/fireball/fireball.mdl.ps2).
- Primary non-_net level GEOM bundles: 45; converted whole-level GLBs: 45.
- Decompiled level QB files: 154; broad prop-keyword index contains 57814 matching lines and 25472 identifiers.
- Local root: build/prepared/thug2_prop_catalog.
- Standalone assets are directly separable. Benches, railings, ledges, barriers and other map furniture are frequently embedded inside level GEOM. The prepared whole-level GLBs expose their mesh leaves; later Astra work must correlate those leaves with QB/scene identifiers and split/convert them into independent FNV props before menu registration.

## Later Astra integration order
1. Read the three summary manifests in build/manifests/ and this handoff.
2. For GMod/Half-Life weapons, use the staged actual Source packages and validate first-person attachment/animation separately from world/drop models.
3. For FNV props, curate the native NIF candidate list by collision, scale and independent-spawn safety; generate menu thumbnails/categories without reconversion where possible.
4. For THUG2, use standalone GLBs directly as conversion inputs and use the prepared level GEOM + QB correlation data for embedded props such as benches/rails.
5. Only after asset validation should runtime/ESP/spawn-menu coding be performed.
