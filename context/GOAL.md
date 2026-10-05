# Product Goal

Create a polished, stable and playable Fallout: New Vegas mashup that integrates selected Garry's Mod functionality and THUG2 skateboarding behavior while retaining coherent Fallout gameplay.

## Intended systems
- Normal Fallout: New Vegas gameplay remains active by default.
- A skateboard exists as a normal inventory/weapon item that can be dropped and picked up.
- Activating skateboard gameplay switches into third-person THUG2-style skating behavior; the player can explicitly return to normal Fallout gameplay.
- Skate mode is intended to become a complete THUG2 free-roam gameplay runtime inside Fallout: New Vegas. Once skate mode is active, the player-facing skating experience should behave as though the player has switched into THUG2 itself, while still physically occupying the Fallout world.
- GPT-6 Astra should reverse engineer the full set of THUG2 code paths required for normal free-roam skating gameplay and port/rebuild that behavior into the skate-mode integration: skater state machine, board physics, acceleration/momentum/friction, turning/carving, ollies/air state, landing, balance systems, manuals, grinds, lips, wallrides/wallplants, reverts, grabs, flip tricks, specials, trick chaining/combo logic, bail/recovery behavior where required, camera, controls, board attachment, animation selection/blending/transitions, score/special/balance HUD state, and other gameplay systems that are part of actually skating around.
- The target is a seamless mode transition: Fallout gameplay before activation, THUG2 free-roam skating gameplay after activation, and a reliable return to Fallout gameplay on exit. The transition should feel like changing game modes rather than running a loose approximation of THUG2 mechanics.
- THUG2 maps, missions/goals, THUG2 NPC populations, story scripting, dialogue, cutscenes and campaign progression are explicitly out of scope for skate mode. The Fallout world remains the world being traversed; THUG2 supplies the skating/free-roam gameplay system.
- Skate camera movement/rotation and skating animation behavior should be based on reverse-engineered THUG2 behavior rather than an arbitrary visual approximation.
- The complete skateboard experience should use THUG2-derived code paths, physics/state logic and original animation data for normal riding, pushing/coasting, turning, mounting/dismounting, board-equipped walking/holding behavior and all supported tricks/specials, with source-faithful transition timing and board attachment.
- Garry's Mod Tool Gun integration should expose appropriate GMod-style tool selection, including Duplicator and Remover.
- Garry's Mod Physics Gun behavior should reproduce the relevant weapon interaction, beam/target highlighting and manipulation behavior.
- GMod-derived weapons/items should integrate with the Pip-Boy inventory model, including dropping/picking up and world-name presentation where appropriate.

## Quality bar
A technically completed merge is not sufficient. Features must be reachable, understandable, stable and enjoyable, without obvious regressions to core Fallout progression, controls, saving/loading or world interaction.

For skate mode specifically, success means the free-roam skating loop is functionally and perceptually source-faithful enough that movement, tricks, transitions, controls, camera, animation, board behavior and skating HUD/state feel like THUG2 operating inside the Fallout world, not a Fallout movement system with THUG2-looking effects layered on top.
