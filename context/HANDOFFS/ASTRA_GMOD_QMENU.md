# Astra handoff — real Garry's Mod Q menu

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Installed GMod source inventory: 105 relevant Lua files; 40 stool/tool files; 46 VGUI classes.
- Direct UI/material refs: 29; unresolved: 0.
- Curated menu data adapter: 290 ready model entries.
- Final ready prop catalog: 290 total; sources: {'Fallout New Vegas': 170, "Garry's Mod / mounted Source content": 120}.
- Primary source evidence includes gamemodes/sandbox/gamemode/cl_spawnmenu.lua and spawnmenu/* plus real Derma/VGUI classes.
- Tool selection must flow from the real/ported spawnmenu tool state to gmod_tool; Fallout popup selectors are not acceptable.
- Use original GMod notification/notice code for transient tool feedback.
- Runtime/native compatibility work remains Astra-owned. Use IDA Pro 6.8 where native Source/GMod behavior is required.

Relevant local manifests:
- build/prepared/gmod_qmenu_source_inventory/manifest.json
- build/prepared/qmenu_content_adapter/manifest.json
- build/prepared/final_prop_catalog_handoff/manifest.json


## 2026-10-07 reconciliation

Recovered from canonical branch `prep/support-workflow`, commit `492c3dc7c23bbcac9eb8c2a52b5e61e32fda775b`, original Git blob `6853e09c0b30fd3d0e664813c97ef2ca0086c35c`. This preparation handoff was absent from `main`; it was not lost from GitHub. Its historical inventory counts are not proof of a running source-faithful integration. Read the new [original-system investigation](../GMOD_2026-10-07/README.md) for current source traces, provenance/staging, native-evidence limits and compatibility status.
