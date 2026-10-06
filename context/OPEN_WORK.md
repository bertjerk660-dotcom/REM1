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
- Replace any current Fallout-authored Tool Gun recreation/approximation with a source-faithful port of the actual Garry's Mod Tool Gun system.
- Inventory the installed GMod Tool Gun SWEP/Lua/tool scripts, stool definitions, materials, sounds, UI hooks, tool state and dependencies.
- Reuse/port the real GMod scripts and data wherever possible; use IDA Pro 6.8 for native Source/GMod implementation details or interfaces not present in Lua.
- Tool selection must happen inside the real/ported Q menu. Remove/disable any Fallout top-left prompts, Fallout message-box style selectors or ad-hoc control prompts used to choose Tool Gun functions.
- The Tool Gun should receive its selected mode directly from the real Q-menu tool state, including Duplicator, Remover and later supported tools.
- Preserve original GMod-style Tool Gun firing/use feedback, sounds, traces/effects and per-tool behavior where applicable.
- Any Tool Gun feedback/notifications that GMod normally presents should use a port of the original GMod notification/bubble UI logic and assets rather than Fallout HUD notifications.
- Validate that changing a tool in Q immediately changes Tool Gun behavior and that closing/reopening Q preserves the expected selected-tool state.

## Physics Gun
- Replace any current Fallout-authored Physics Gun recreation/approximation with a source-faithful implementation grounded in the actual local GMod/Source weapon behavior.
- Inventory and preserve the relevant Physics Gun scripts/assets/materials/sounds and reverse engineer required native Source/GMod behavior using IDA Pro 6.8 where script is insufficient.
- Reproduce the real target acquisition, beam rendering, held-object transform/manipulation, rotation, freeze/unfreeze, drop/release, launch behavior, highlighting/feedback and relevant input semantics.
- Use original/source-faithful GMod visual/audio feedback rather than Fallout prompts.
- If transient notifications are required, use the real/ported GMod notification/bubble system rather than Fallout top-left notifications or menu prompts.
- Add regression checks for target acquisition, hold/release, rotation, freeze, launch and beam/highlight rendering.

## GMod notifications/UI feedback
- Inventory the actual Garry's Mod notification system used by the Q menu, Tool Gun and related tools.
- Port/reuse the relevant GMod Lua/Derma notification code, materials, fonts/icons and timing/stacking behavior where technically possible.
- Tool Gun/Physics Gun feedback should appear through these GMod-style notification bubbles/indicators when the original game uses them.
- Do not use Fallout top-left HUD messages or Fallout menu prompts as substitutes for Tool Gun selection or normal GMod tool feedback.

## Fallout regression
- Verify boot and target area loading.
- Verify save/load.
- Verify normal inventory and combat behavior outside imported modes.
- Check for progression-breaking regressions.


## Support/workflow lane
- Keep feature/thug2-native-ui-g6 reserved for Astra's complex THUG2/UI/mechanics work.
- Use the support lane for reproducible asset staging, xEdit records, Pip-Boy icons, manifests, validation scripts, provenance, prop curation, dependency audits, packaging and regression preparation.
- Do not modify or deploy the v88 candidate from the support lane.
- Re-check installed DLL, active ESP and candidate hashes immediately before any deployment because concurrent work can occur.
- Prefer sidecar test plugins and isolated build directories for support features so gameplay/runtime changes remain attributable.

## Combine Soldier armor staging
- Static full-body Combine Soldier armor conversion exists and passes structural/skin/texture validation.
- Dedicated REM_CombineArmor_Test.esp exists locally but remains disabled.
- Next test gate: equip on male/female player where applicable, inspect idle/walk/run/crouch/weapon poses, first/third person, dropped world model, NPC equip, save/load and clipping.
- Do not replace Enclave/Remnants armor records or NPC outfits until that isolated test passes.

## Support lane backlog
- Reconcile and import project-authored local conversion/validation scripts that are still missing from GitHub.
- Maintain hashes/provenance for source-game assets without committing proprietary binaries.
- Finish asset-only Pip-Boy icon and inventory presentation audits.
- Continue GMod/HL weapon model staging and missing-dependency reports without rewriting weapon mechanics.
- Continue curated prop-library indexing, collision/scale validation and thumbnail preparation for the eventual real GMod Q menu.
- Inventory real GMod Q-menu/Tool Gun/Physics Gun script/assets and dependencies for Astra, but leave the native/runtime port and behavior implementation to Astra.
- Prepare THUG2 UI/font/controller-glyph asset manifests and test data, but leave animation, camera, physics, scoring-runtime and model-rig behavior changes to Astra.
- Expand repeatable boot/save/load/inventory/asset-reference validation so candidate promotion requires less manual checking.

### Support phase 2 status
- Prop catalog data/form bindings/thumbnails/Q-menu adapter are prepared; human representative spawn/collision tests are still required.
- THUG2 prop extraction is advanced to QB component/position evidence and spatial leaf candidates; standalone split/conversion/validation remains open.
- Weapon sound/source dependencies are resolved for the staged set; first/third-person presentation and inventory/drop behavior still require gameplay checks.
- Combine armor is still static-validation-only and must not replace Enclave/Remnants records until its isolated test pack passes.
- Runtime Q menu, Tool Gun, Physgun, complete THUG2 skate physics/animation/camera/HUD remain Astra-owned.
- Run research/validate_support_lane_state.py before promoting support artifacts; current pass count is 94.
- Follow context/SUPPORT_20_POINT_TRACKER.md for exact per-task progress.