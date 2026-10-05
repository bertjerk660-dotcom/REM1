# Product Goal

Create a polished, stable and playable Fallout: New Vegas mashup that integrates selected Garry's Mod functionality and THUG2 skateboarding behavior while retaining coherent Fallout gameplay.

## Intended systems
- Normal Fallout: New Vegas gameplay remains active by default.
- A skateboard exists as a normal inventory/weapon item that can be dropped and picked up.
- Activating skateboard gameplay switches into third-person THUG2-style skating behavior; the player can explicitly return to normal Fallout gameplay.
- Skate camera movement/rotation and skating animation behavior should be based on reverse-engineered THUG2 behavior rather than an arbitrary visual approximation.
- The complete skateboard experience should use THUG2-derived code paths, physics/state logic and original animation data for normal riding, pushing/coasting, turning, mounting/dismounting, board-equipped walking/holding behavior and all supported tricks/specials, with source-faithful transition timing and board attachment.
- Garry's Mod Tool Gun integration should expose appropriate GMod-style tool selection, including Duplicator and Remover.
- Garry's Mod Physics Gun behavior should reproduce the relevant weapon interaction, beam/target highlighting and manipulation behavior.
- GMod-derived weapons/items should integrate with the Pip-Boy inventory model, including dropping/picking up and world-name presentation where appropriate.

## Quality bar
A technically completed merge is not sufficient. Features must be reachable, understandable, stable and enjoyable, without obvious regressions to core Fallout progression, controls, saving/loading or world interaction.
