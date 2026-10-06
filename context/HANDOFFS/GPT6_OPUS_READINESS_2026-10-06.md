# GPT-6 / Opus integration readiness audit — 2026-10-06

Status: support-lane audit of staged inputs. This document does not claim runtime integration or playtest success.

## Ready to feed into the integration agent

### GMod Tool Gun
- Original installed GMod Tool Gun source is inventoried: gmod_tool shared.lua/stool.lua plus 40 stool files.
- Exact c_toolgun and w_toolgun Source model components are resolved and hashed from the installed GMod VPK.
- Tool Gun materials, screen assets, ToolTracer effect and Toolgun.Single source/event dependencies are staged/inventoried.
- Concrete weapon staging provides source MDL/VVD/VTX/PHY where available, decompiled QC/SMD/animation output, materials and provenance.
- Real Q-menu source inventory and content adapter are prepared. Tool selection must flow Q-menu -> gmod_tool rather than Fallout prompts.

### GMod Physics Gun
- w_physics Source world model components and collision are resolved and hashed.
- Original physbeam/physgun glow materials and Weapon_Physgun.On/Off/Special1 definitions are indexed.
- Installed weapon_physgun definition and GMod physgun hooks are inventoried and hashed.
- Native behavior requirements are documented: target acquisition, held transform, rotation, freeze/unfreeze, release and launch.

### Broader weapon/model staging
- 49 concrete weapon classes are mapped.
- 48 view and 48 world presentation candidates are prepared; camera/fists are special cases.
- Dedicated actual GMod/Half-Life model staging found 71/73 referenced Source model packages.
- Sound dependency handoff has a later resolved inventory; older runtime-candidate summary with 21 unresolved sound refs is stale and must not be treated as final.
- Converted world/prop staging: 49/49 definitions have an available converted NIF mapping.

### GMod Q menu / props
- 105 relevant GMod Lua files, 40 stool files and 46 VGUI classes inventoried.
- 29/29 direct UI/material refs resolve.
- 290-entry curated ready catalog: 170 FNV + 120 GMod/Source; thumbnails audited.
- Disabled sidecars exist so content can be integrated without mutating the active runtime first.

### THUG2
- Skate runtime source handoff includes 17 decompiled Q source files and original physics/controller/trick state evidence.
- 20 board SKA animation assets parsed.
- HUD/input handoff indexes 49 files with no missing source files and 22/22 image previews.
- Board source/converted geometry and attachment evidence are staged.
- THUG2 prop queue is staged as evidence, but not all props are integration-ready.

## Not yet ready / integration-agent work required

1. Physics Gun exact first-person model: installed GMod declares models/weapons/v_physics.mdl, but v_physics MDL/VVD/DX90.VTX are absent from the mounted install. Do not silently substitute c_superphyscannon as proof of parity. Resolve provenance from mounted Source content or determine the actual current GMod presentation path.
2. Tool Gun/Physics Gun FNV held/view conversion: Source packages are staged, but FNV first-person skeleton/hand attachment, third-person attachment, scale and animation bindings are not validated.
3. Physics Gun native behavior: use IDA Pro 6.8 for engine-side behavior not exposed by Lua/scripts. Port target acquisition, beam endpoint, held-object transforms, rotation, freeze/unfreeze, release/launch and actor handling.
4. Tool Gun runtime compatibility: port DoToolTrace, LeftClick/RightClick/Reload, tool lifecycle, selection state and Duplicator/Remover constraints into the FNV/NVSE boundary while retaining original semantics.
5. Q-menu runtime renderer/bridge: source/UI/content are staged, but real Derma/VGUI behavior must be hosted/ported into FNV and wired to Tool Gun state.
6. Weapon animation/presentation: preserve QC/SMD sequences; validate each chosen weapon as FNV view/held/world model before ESP/runtime promotion.
7. THUG2 runtime remains complex integration work: movement/collision/state machine, animation retargeting, board attachment, camera, scoring/HUD and input switching are not validated as source-faithful runtime behavior.
8. THUG2 props: 21/106 targets remain script-only/unresolved; extracted level geometry still needs safe component splitting, scale/collision validation and promotion.
9. Combine armor test currently requires a fresh human retest after the wearable was rebuilt with BSDismemberSkinInstance + NiSkinPartition. Do not record it as fixed until visible in game.
10. Runtime regressions remain: current verified project state does not establish THUG2 stability; historical implementation claims must not be treated as current playtest proof.

## Integration order recommended
1. Prove Tool Gun c_toolgun/w_toolgun view/world presentation in an isolated sidecar.
2. Resolve exact Physics Gun view-model provenance; prove w_physics world/drop presentation.
3. Port Tool Gun Lua/tool lifecycle and Q-menu selection bridge.
4. Port Physics Gun native manipulation/beam behavior with IDA Pro 6.8 evidence.
5. Validate inventory/drop/pickup, first/third person, save/load and controller paths.
6. Integrate THUG2 runtime from its dedicated handoffs after weapon/Q-menu regressions are isolated.
7. Promote only playtested candidates into the main plugin.

## Canonical local inputs
- build/prepared/gmod_hl_weapon_models/
- build/prepared/gmod_tool_physgun_assets/
- build/prepared/gmod_tool_physgun_asset_handoff/
- build/prepared/gmod_weapon_runtime_candidates/
- build/prepared/gmod_qmenu_source_inventory/
- build/prepared/qmenu_content_adapter/
- build/prepared/final_prop_catalog_handoff/
- build/prepared/thug2_skateboard_asset_handoff/
- build/prepared/thug2_ui_asset_handoff/
- context/HANDOFFS/ASTRA_TOOLGUN.md
- context/HANDOFFS/ASTRA_PHYSGUN.md
- context/HANDOFFS/ASTRA_WEAPON_MODELS.md
- context/HANDOFFS/ASTRA_GMOD_QMENU.md
- context/HANDOFFS/ASTRA_THUG2_SKATE_RUNTIME.md
- context/HANDOFFS/ASTRA_SKATEBOARD_ATTACHMENT.md
- context/HANDOFFS/ASTRA_THUG2_HUD_INPUT.md
- context/HANDOFFS/ASTRA_PROP_CONTENT.md

Proprietary game assets remain local. GitHub should contain this readiness state, tooling, manifests/hashes and provenance—not redistributed game binaries.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]