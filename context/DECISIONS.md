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
