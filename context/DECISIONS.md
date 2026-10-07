# Decisions

## D-001 GitHub is canonical
Accepted: 2026-10-05.
GitHub is the durable source of truth for project source, documentation, pipeline configuration, manifests and project knowledge. Local tooling is used for build/extraction/decompilation/testing but must not become the sole holder of durable engineering knowledge.

## D-002 IDA version
Accepted: 2026-10-05.
Use IDA Pro 6.8 for project reverse-engineering work that requires IDA, rather than IDA 9.

## D-003 Preserve Fallout default gameplay
Normal Fallout: New Vegas mechanics remain active until the player explicitly activates the skateboard gameplay mode. Exiting skate mode restores normal Fallout-style gameplay.

## D-004 Reverse engineer rather than merely imitate
Where the project explicitly requires THUG2/GMod behavior to be merged, implementation should be grounded in analysis of the source game's behavior/code/assets where legally and technically appropriate, rather than claiming a 1:1 merge based only on a hand-authored approximation.

## D-005 Curated prop library
Accepted: 2026-10-05.
The player-facing GMod-style prop menu should use a compact curated environmental library rather than exposing the full Fallout asset archive. The initial Fallout target is approximately 300 useful props, strongly weighted toward skateable/environment-building objects. The larger 13,003-candidate catalog remains reference/search data only.

## D-006 Replace the custom prop menu with a source-faithful GMod Q menu
Accepted: 2026-10-05.
The existing custom/Fallout-style prop menu is not the final design. The target is a functional port of the real Garry's Mod Q/spawn menu using the user's installed GMod Lua/Derma scripts, menu definitions, icons/materials and related files as the primary source. IDA Pro 6.8 should be used for native Source/GMod behavior or interfaces that are not available directly from script. Only the compatibility layer required by Fallout/xNVSE should be rewritten; the menu's visible structure and behavior should remain as source-faithful as technically practical.

## D-007 Tool Gun and Physics Gun must use real GMod systems
Accepted: 2026-10-05.
The final Tool Gun and Physics Gun must not be Fallout-authored recreations. The implementation owner should reuse/port the user's installed Garry's Mod Lua/SWEP/tool scripts, tool definitions, assets, materials, sounds and source behavior wherever technically possible, and IDA Pro 6.8 must be used for required native Source/GMod evidence or interfaces not exposed in script. Tool selection is owned by the real/ported Q menu, not by Fallout top-left prompts or Fallout menu prompts.

**Ownership supersession, 2026-10-07:** the original D-007 wording named GPT-6/Astra. That role assignment is obsolete. Current ownership is defined by `context/AGENT_OWNERSHIP.md`: Codex owns investigation/evidence and runtime validation/debugging; Claude Opus is the sole implementation/integration owner. The technical decision to use real GMod systems remains unchanged.

## D-008 GMod notifications replace Fallout tool prompts
Accepted: 2026-10-05.
Normal Tool Gun/Physics Gun feedback and transient tool notifications should use a source-faithful port of Garry's Mod's own notification/bubble UI and related original scripts/assets where applicable. Fallout HUD notifications and Fallout-style popup menus must not be used as substitutes for GMod tool selection or normal GMod tool feedback.


## D-009 Current agent ownership supersedes historical model labels
Accepted: 2026-10-07.

`context/AGENT_OWNERSHIP.md` is authoritative for current role assignment:
- Codex owns investigation, reverse-engineering evidence, runtime investigation/testing/debugging and regression validation.
- Claude Opus is the sole substantive implementation/integration owner.
- Normal GPT owns workflow, documentation, provenance, manifests, handoffs and coordination.
- GPT-6/Astra is not used for current project work.

Historical branch/file names containing `ASTRA`, `GPT6`, `gpt6_opus` or `*-g6` remain traceability labels only and must not dispatch new work.

## D-009 Opus may investigate when necessary
Accepted: 2026-10-07 by owner instruction, recorded by the Haiku final audit. Claude Opus may perform Codex-type investigation when necessary. The evidence must be recorded and reviewed under the Codex stop conditions. Codex remains the default investigator and runtime validator. See context/AGENT_OWNERSHIP.md.

## D-010 Documentation fixes do not change the readiness score
Accepted: 2026-10-07 by the Haiku final audit. Readiness is scored only from reviewed evidence under context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md. Contradiction fixes and added failure-protection notes improve consistency but do not raise the score.

## D-011 Reverse engineering routing
Accepted: 2026-10-07 by owner instruction, recorded by the Haiku findings pass. Reverse engineering of THUG2 and Garry's Mod belongs to Claude Opus under D-009. GPT-5.5 coordinates it and writes the request. Haiku and GPT-5.5 do not perform reverse engineering. Codex's investigation role is pending an owner decision. See context/HANDOFFS/HAIKU_SESSION_FINDINGS_2026-10-07.md.