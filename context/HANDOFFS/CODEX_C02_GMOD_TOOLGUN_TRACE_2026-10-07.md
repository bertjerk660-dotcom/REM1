# Codex C02 — Garry's Mod Toolgun dispatch and tool-state trace

## Objective
Investigate the original installed Garry's Mod Toolgun sufficiently for **Claude Opus** to implement it source-faithfully in Fallout: New Vegas.

This is evidence/reverse-engineering work only. Do not perform final implementation.

## Required starting context
Read the canonical project documents plus:
- context/AGENT_OWNERSHIP.md
- context/MASTER_AGENT_QUEUE.md
- context/HANDOFFS/GMOD_OVERLAY_EVIDENCE_2026-10-06.md
- context/HANDOFFS/CODEX_C01_GMOD_QMENU_DEPENDENCY_TRACE_2026-10-07.md when C01 output exists
- context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md for staged legacy paths only
- prepared gmod_tool / stool source inventories and model/effect/sound manifests.

Use installed Garry's Mod source files first. Use IDA Pro 6.8 only where native Source behavior is not exposed in Lua/scripts.

## Questions
1. Which exact files define gmod_tool and the stool/tool registry?
2. How is a tool registered, named, selected, initialized and switched?
3. What state object/table carries the selected tool from Q-menu to Toolgun?
4. What is the exact dispatch path for LeftClick, RightClick and Reload?
5. How does DoToolTrace work and what filters/range/target semantics does it require?
6. How do per-tool client/server/shared files participate in the lifecycle?
7. What common base/helper APIs do stools depend on?
8. What exact call/dependency path is required for Remover?
9. What exact call/dependency path is required for Duplicator?
10. What undo/cleanup/convar/notification/state dependencies are required by those proof tools?
11. Which Toolgun screen/material/tracer/sound hooks are source-defined?
12. What state is preserved when switching tools, closing Q, weapon switching, death/respawn, save/load equivalents or map changes?
13. Which behavior is engine-native and must be adapted at the FNV/xNVSE boundary?
14. What minimum host adapter interfaces must Opus expose to preserve original tool semantics?
15. Which current Fallout-authored selection/prompt paths must be disabled once the real Toolgun bridge is ready?

## Evidence outputs
For every important function/tool dependency record original path, symbol/hook, data/table state, caller/callee relationship, required materials/sounds, convars and native interfaces.

Create:
- context/CODEX/GMOD_TOOLGUN_C02_EVIDENCE_2026-10-07.md
- build/evidence/gmod_toolgun_c02/function_map.json
- build/evidence/gmod_toolgun_c02/tool_registry_manifest.json
- build/evidence/gmod_toolgun_c02/remover_dependency_graph.json
- build/evidence/gmod_toolgun_c02/duplicator_dependency_graph.json
- build/evidence/gmod_toolgun_c02/opus_interface_contract.json

## Stop condition
Stop when Opus can implement Q-selected Toolgun behavior, Remover and Duplicator without rediscovering Toolgun internals.

Do not implement the FNV bridge, final UI, models, animations or runtime behavior yourself.
