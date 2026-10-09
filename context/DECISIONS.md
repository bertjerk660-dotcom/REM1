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

## D-009A Opus may investigate when necessary as an implementation exception
Accepted: 2026-10-07 by owner instruction, recorded by the Haiku final audit. Claude Opus may perform narrowly scoped Codex-type investigation when necessary to unblock Opus-owned implementation. Codex remains the default investigator and runtime validator. Evidence must be recorded and reviewed under the same stop conditions. See `context/AGENT_OWNERSHIP.md`.

## D-010 Documentation fixes do not change the readiness score
Accepted: 2026-10-07 by the Haiku final audit. Readiness is scored only from reviewed evidence under context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md. Contradiction fixes and added failure-protection notes improve consistency but do not raise the score.

## D-011 Current reverse-engineering routing clarification
Accepted: 2026-10-08 during documentation/provenance reconciliation.

Current dispatch remains:
- Codex = default reverse-engineering investigation/evidence closure + runtime validation/debugging;
- Claude Opus = sole substantive implementation/integration owner;
- normal GPT = coordination/documentation/provenance.

Opus may use the D-009A investigation exception only when a narrow evidence gap is necessary to unblock its own implementation.

The broader routing proposed in `prep/haiku-findings-20261007` is retained as historical findings and does not supersede D-009/D-009A unless the project owner later gives an explicit new directive.


## D-012 Standalone Bevy/Rust successor alongside legacy NVSE edition
Accepted by project owner: 2026-10-09.

The product now has **two distinct editions during migration**:
1. `legacy-fnv`: the historical Fallout: New Vegas host/NVSE merge; preserve code, deployed runtime, saves, hashes, rollback, and historical tests unchanged as reference/fallback.
2. `bevy-standalone`: the future primary standalone Bevy/Rust game, implementing a coherent Fallout-world, GMod systems and THUG2 skating crossbreed without requiring FalloutNV.exe or NVSE to run.

Bevy must **coexist as a separate edition** until its functionality, playability, stability, asset provenance, regression checks and human validation establish an acceptable replacement. Future development should prioritize Bevy; the legacy edition will **likely** be discontinued later, but is **not discontinued or deleted** by this decision. Record explicit cutover criteria and owner review before any discontinuation or destructive cleanup.

Do not silently reinterpret historical context/GOAL.md or context/ARCHITECTURE.md references to 'Fallout is the host' as the Bevy goal. Those documents record the legacy design. Create a versioned Bevy architecture/goal and progress status. Preserve candidate/legacy branch isolation. Claude Opus remains the substantive implementation owner; Codex is default investigation/independent validation, with D-009A narrow Opus investigation exception using IDA Pro 6.8. New edition lives on an isolated engine branch with separate build manifests and reproducible Cargo toolchain.

Reference: `context/HANDOFFS/OPUS_BEVY_STANDALONE_SUCCESSOR_2026-10-09.md` on `prep/bevy-opus-handoff-20261009`.
