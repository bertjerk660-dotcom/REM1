# Astra Handoff — Real Garry's Mod Q Menu

## Prepared support evidence
- Installed GMod build ID: 25375506.
- 105 relevant installed Lua files have been inventoried and hashed.
- 33 files belong to the Q/spawn-menu stack.
- 46 VGUI classes are referenced/created by that stack.
- 29 direct menu/material asset references were indexed and all 29 resolve in loose/VPK-mounted content.
- The compact content adapter contains 290 ready prop entries: 170 native Fallout forms + 120 converted GMod/Source sidecar forms.
- Every ready entry has a form binding, category, model path, search tokens and support/fallback thumbnail.
- The player-facing target stays near 300–320 useful entries rather than exposing the raw 13k/7.5k archives.

## Source-of-truth inputs
- Local: build/prepared/gmod_qmenu_source_inventory/manifest.json
- Local: build/prepared/qmenu_content_adapter/manifest.json
- Local: build/prepared/final_prop_catalog_handoff/manifest.json
- Repository tooling: research/inventory_gmod_qmenu_sources.py
- Repository tooling: research/build_qmenu_content_adapter.py

## Astra runtime work
1. Port/reuse the actual installed GMod Lua/Derma spawnmenu stack rather than drawing a Fallout imitation.
2. Implement only the Fallout/xNVSE compatibility boundary that the original menu requires.
3. Preserve Q open/close behavior, tabs/categories, prop browser, search/filter, real SpawnIcon/model-icon behavior and tool panels.
4. Feed the prepared 290-entry adapter into the real/ported content registration path.
5. Keep Duplicator/Remover/tool selection inside the real Q-menu workflow.
6. Restore normal Fallout input cleanly when Q closes.
7. Use IDA Pro 6.8 only when native Source/GMod interfaces are required.

## Hard prohibitions
- No Fallout top-left tool-selection prompts.
- No hand-authored Fallout menu that merely resembles GMod.
- No raw dump of every archived prop into the default player-facing browser.

## Validation gate
Open Q -> browse categories -> search -> inspect icons -> spawn representative props -> select Remover/Duplicator -> close Q -> normal Fallout input restored. No flashing/icon loss/crash.
