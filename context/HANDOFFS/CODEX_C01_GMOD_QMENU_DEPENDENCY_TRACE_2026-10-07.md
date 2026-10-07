# Codex C01 — GMod Q-menu dependency trace

## Objective

Investigate the **real installed Garry's Mod Q/spawn menu** deeply enough that Claude Opus can implement a source-faithful compatibility/renderer layer inside Fallout: New Vegas without rediscovering the menu system.

This is an investigation/evidence task only. **Do not perform the final Fallout implementation.**

## Start from canonical project state

Read:
- AGENTS.md
- context/BOOTSTRAP.md
- context/GOAL.md
- context/ARCHITECTURE.md
- context/CURRENT_STATE.md
- context/OPEN_WORK.md
- context/DECISIONS.md
- context/FAILURE_KNOWLEDGE.md
- context/AGENT_OWNERSHIP.md
- context/MASTER_PROJECT_MAP.md
- context/MASTER_AGENT_QUEUE.md
- context/HANDOFFS/GMOD_OVERLAY_EVIDENCE_2026-10-06.md
- context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md

Also inspect the prepared Q-menu inventories/content adapter under:
- build/prepared/gmod_qmenu_source_inventory/
- build/prepared/qmenu_content_adapter/
- any corresponding manifests/hashes referenced by those packages.

Use the original-path/provenance fields in those inventories to locate the actual installed Garry's Mod files. Do not guess missing dependencies.

If native Source/GMod behavior must be reverse engineered, use **IDA Pro 6.8 only**.

## Questions that must be answered

1. What exact script/hook/bind path opens and closes the Q/spawn menu?
2. Which Lua files and functions construct the root menu and major panels?
3. Which VGUI/Derma classes are instantiated, in what inheritance/composition relationships?
4. How are tabs/categories/content types registered and ordered?
5. How are prop icons/spawnicons created, populated, cached, rendered and activated?
6. How do search/filter operations update visible content?
7. What is the exact input/cursor/focus lifecycle while Q is open, including suppression/restoration of gameplay input?
8. What menu state persists across close/reopen?
9. How is the Tool section populated from stool/tool definitions?
10. What exact data/state object represents the currently selected Toolgun tool/mode?
11. What function/event path must Opus preserve so Q selection flows directly into gmod_tool without a Fallout selector?
12. Which Duplicator/Remover UI dependencies are required at menu level?
13. Which notification/undo/cleanup UI dependencies are directly required by the Q-menu path versus separable follow-up systems?
14. Which engine/native interfaces are required that are not available in Lua?
15. What is the minimal host compatibility surface that Fallout/xNVSE must expose so the **original menu logic/data flow** can operate?
16. Which parts of the existing project placeholder menu can be deleted/disabled once the real bridge is ready, and which content-adapter pieces are reusable without changing GMod behavior?

## Evidence requirements

For every important conclusion record:
- original source path;
- file hash if already available or useful;
- function/class/hook/concommand/bind name;
- caller/callee or event relationship;
- required globals/tables/convars;
- material/icon/font dependency;
- native interface dependency where applicable;
- whether the behavior is script-defined, data-defined or engine-defined;
- confidence level and any unresolved ambiguity.

Do not rely on screenshots or visual resemblance as proof.

## Required output

Create/update these durable outputs (or equivalent clearly named files if repository conventions require):
- `context/CODEX/GMOD_QMENU_C01_EVIDENCE_2026-10-07.md`
- `build/evidence/gmod_qmenu_c01/function_map.json`
- `build/evidence/gmod_qmenu_c01/dependency_manifest.json`
- `build/evidence/gmod_qmenu_c01/ui_state_machine.json`
- `build/evidence/gmod_qmenu_c01/opus_interface_contract.json`

The report must end with:
- answered questions;
- unresolved questions;
- exact blockers;
- confidence summary;
- files/functions Opus must touch;
- files/functions Opus must not replace with hand-authored approximations;
- acceptance evidence Opus should reproduce;
- downstream tasks now unblocked.

## Stop condition

Stop after the Q-menu evidence/interface package is complete and reviewable.

Do **not** implement the final FNV renderer, final Toolgun integration, models, animation, or runtime patch. Those are Opus-owned under the current agent split.
