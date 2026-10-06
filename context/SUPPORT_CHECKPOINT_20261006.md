# Support checkpoint — 2026-10-06

This checkpoint covers non-Astra preparation only. No THUG2/GMod runtime mechanics, plugin source or Astra v88 candidate was modified.

## GMod / Half-Life weapon packages
- 52 weapon classes reference 73 unique Source model paths.
- 71 model refs belong to concrete weapon classes and all 71 are staged: 100% concrete coverage.
- The two unstaged paths are abstract-base placeholders only: `models/weapons/v_eq_flashbang.mdl` and `models/weapons/v_pistol.mdl`.
- No blocking concrete weapon-model dependency remains in this staging audit.

## Fallout prop pool
- The 300-item curated research pool was statically audited.
- 300/300 NIFs parse.
- 278 pass the static-clean gate: geometry + Havok collision + resolved DDS refs + non-extreme bounds.
- 22 are excluded from the ready shortlist due to missing texture refs, no Havok collision and/or extreme size.
- 290/300 contain Havok collision, but only 31 show mass > 0 authored-mobility evidence. Fixed obstacles remain useful for skating; Physgun mobility must not be assumed from native FNV static NIFs.

## GMod Q-menu source handoff
- Indexed 105 relevant installed GMod Lua files.
- Includes 33 Q/spawn-menu files, 48 Tool Gun files, 40 stool/tool files, notification modules and Physgun-visible gamemode hooks.
- 46 VGUI classes are referenced/created by the inspected stack.
- 29 direct UI/material refs were found; all resolve after indexing the installed `garrysmod_dir.vpk`.
- Script evidence includes SpawnMenu lifecycle entrypoints, Tool Gun `spawnmenu.AddToolMenuOption` registration, Duplicator APIs, notification APIs, and Physgun pickup/drop/freeze/beam hooks.
- Core `weapon_physgun` manipulation remains engine-native and is explicitly handed to Astra/IDA Pro 6.8 rather than approximated here.

## GMod/Source prop pool
- Curated 120 converted props from the 7,507-entry registry.
- Every selected entry already has successful conversion status, collision, existing NIF and resolved materials.
- Selection is intentionally biased toward rails/fences, benches/tables, planks/ladders/beams, crates/pallets, barrels/canisters, street props, furniture and playground objects.

## THUG2 embedded prop queue
- Existing whole-level GEOM + QB work was filtered into 106 named embedded skate/environment extraction targets across 16 levels.
- Targets include quarterpipes/halfpipes/ramps, rails/handrails, ledges/hubbas/curbs, benches/tables/chairs and other environment pieces.
- These are NOT standalone props yet. Astra/model-extraction work must correlate each target with QB/GEOM, split it from the level, convert it and validate collision/scale. No THUG2 map import is intended.

## Compact menu-content handoff
- Ready candidate pool: 290.
- 170 statically-clean native Fallout props.
- 120 converted GMod/Source props.
- THUG2 queue: 106 future extraction targets, excluded from the ready count.
- Menu policy: keep the normal player-facing library near 300–320 useful items. When good THUG2 props are promoted, replace redundant lower-priority entries instead of continually growing the menu.

## Next support work
1. Audit which of the 290 ready candidates already have usable ESP/base forms and identify only the missing form records.
2. Audit/generate thumbnail coverage for the ready content set without implementing the menu runtime.
3. Prepare a disabled sidecar catalog ESP only for missing GMod/custom prop forms, avoiding duplicate FNV forms.
4. Add asset-reference and sidecar consistency validators.
5. Keep the source/dependency handoff current for Astra while leaving Q-menu/Tool Gun/Physgun runtime behavior untouched.
