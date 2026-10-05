# Open Work

This is a requirements/backlog ledger, not proof of implementation.

## Repository reconciliation
- Inventory the current local Fallout NV / GMod / THUG2 project tree.
- Identify latest actual build and its parent/history.
- Reconcile historical labels v35, v54 and v68 with real artifacts/manifests.
- Import project-authored source, scripts, converters and configuration that currently exist only locally.
- Record hashes/provenance for proprietary source assets without treating them as redistributable repository source.

## Skateboard
- Reproduce or disprove historical right-click crash.
- Reproduce or disprove invisible skateboard.
- Verify skateboard inventory/drop/pickup behavior.
- Verify explicit normal-Fallout <-> skate-mode state transitions.
- Verify THUG2-derived camera, movement, physics and animation behavior against source evidence.
- Verify skeleton/rig adaptation.
- GPT-6 Astra must treat skate mode as a complete THUG2 free-roam gameplay subsystem, not as a small collection of THUG2-inspired mechanics.
- Reverse engineer and extract/rebuild the complete set of THUG2 code paths required to actually free-roam and skate: skater state machine, controller/input interpretation, ground/air movement, acceleration, momentum, friction, turning/carving, ollie/air/landing logic, manuals, grinds, lips, wallrides/wallplants, reverts, grabs, flip tricks, specials, trick/combo chaining, balance behavior, collision/ground interaction, bails/recovery where required, camera coupling, board attachment, animation selection/blending/transitions, scoring/special state and all other systems that participate in ordinary skating gameplay.
- The target behavior in active skate mode is source-faithful THUG2 free roam inside the Fallout world: entering skate mode should feel like seamlessly switching from Fallout into THUG2 gameplay, and exiting should restore Fallout cleanly.
- Do not import THUG2 maps, missions/goals, NPC population, dialogue, cutscenes, campaign/story progression or unrelated game modes. Fallout supplies the world/content; THUG2 supplies the complete skating/free-roam gameplay system.
- Do not replace a discovered THUG2 subsystem with a hand-authored approximation merely because an approximation is easier. Use the user's local THUG2 executable/data, IDA Pro 6.8, extracted scripts/assets and project tooling to recover the real behavior where technically possible.
- Cover the full skating animation/state set: normal riding/pushing/coasting, turning/carving, crouch/ollie/landing, manuals, grinds, lips, wallrides/wallplants, reverts, grabs, flips, specials and every other reachable THUG2 trick/state used by the selected skater runtime.
- Reproduce the original transition logic, timing, velocity/momentum changes, balance behavior, collision/ground interaction and camera coupling for those states.
- Extract and port the correct non-trick board-use animation states as well, including carrying/holding the skateboard weapon, walking/running with the board equipped, mounting into skate mode, normal riding and returning from skate mode to Fallout movement.
- Retarget the original THUG2 animation data to the Fallout player rig without changing the intended motion, timing or trick logic, and validate that the board remains correctly attached to hand/feet across every transition.
- Preserve keyboard/mouse and Xbox-controller operation for the complete trick/state machine once the source-faithful behavior is stable.
- Validate the integrated free-roam stack subsystem-by-subsystem and then as a complete loop: enter mode -> push/ride -> turn -> ollie -> perform tricks -> land -> grind/manual/lip -> chain combo -> use SPECIAL -> bail/recover where applicable -> continue riding -> exit mode -> normal Fallout restored.

## GMod Q / spawn menu
- Replace the current custom/Fallout-style GMod prop menu rather than extending it as the final implementation.
- Use the user's installed Garry's Mod game files as the primary source for the real Q/spawn menu implementation.
- Inventory and preserve the actual GMod Lua/Derma menu scripts, spawnmenu definitions, tool-menu scripts, icons/materials, category definitions and dependencies needed by the original Q menu.
- Port/reuse those actual scripts/definitions wherever technically compatible instead of manually recreating the menu by appearance.
- Use IDA Pro 6.8 for any required native Source/GMod behavior, interface calls or engine-side menu logic that cannot be recovered from Lua/scripts alone.
- Reconstruct the minimum compatibility layer needed to make the real GMod menu logic function in the Fallout/xNVSE host.
- Preserve source-faithful behavior for opening/closing the Q menu, tabs/categories, prop browsing, icons, search/filtering, tool selection, Duplicator/Remover access and selected-tool state passed to the Tool Gun.
- Feed the real/ported Q menu the curated project prop libraries rather than exposing the raw source archives.
- Validate that the menu remains responsive and usable with the curated prop library, and that closing it restores normal Fallout input cleanly.
- Do not describe a hand-authored Fallout menu that merely resembles GMod as the finished Q menu.

## GMod-style prop menu content
- Do NOT expose the entire 13,003-model Fallout prop candidate archive in the player-facing menu.
- Use the curated approximately 300-prop set as the intended default Fallout library.
- Prioritize useful environmental objects and skateable geometry: rails, railings, benches, ramps, stairs, ledges, barriers, tables, counters, crates, large boxes and pipes.
- Include a smaller supporting set of fences, signs, lamps, poles, street clutter, furniture, storage, vending machines, terminals, rocks, trees and plants.
- Keep the full 13,003-model catalog only as archive/search data so individual curated props can be swapped later.
- Before exposing a prop, validate collision, Havok behavior, scale, independent-spawn safety and practical usefulness.
- Generate clear categories/thumbnails so the menu remains fast and usable rather than becoming a raw asset dump.

## Tool Gun
- Verify real GMod Q-menu tool selection controls Tool Gun mode.
- Verify Duplicator.
- Verify Remover.
- Verify selected menu tool controls Tool Gun mode.

## Physics Gun
- Verify firing/beam/highlight/manipulation behavior.
- Add regression checks for target acquisition, hold/release and rendering.

## Fallout regression
- Verify boot and target area loading.
- Verify save/load.
- Verify normal inventory and combat behavior outside imported modes.
- Check for progression-breaking regressions.
