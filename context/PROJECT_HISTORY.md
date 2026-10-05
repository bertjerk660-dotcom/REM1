# Project History and Requirements Ledger

This file preserves durable project intent and historically reported work from the FALLOUT NV - GARRYS MOD project conversations. Historical statements are not automatically verified implementation state; CURRENT_STATE.md remains the authority for verified state.

## Core mashup
Host game: Fallout: New Vegas.
Integrated content/systems requested from Garry's Mod and Tony Hawk's Underground 2 (THUG2).
Reverse-engineering work requiring IDA must use IDA Pro 6.8.

## THUG2 skateboard requirements
- A skateboard model exists as a normal Fallout weapon/item.
- It can be held like a melee weapon, dropped, and picked up.
- Before activation, normal Fallout: New Vegas mechanics apply.
- Attacking/activating the skateboard switches into third-person skating mode.
- A separate/manual action returns the player to normal Fallout gameplay.
- Camera movement and rotation while skating are intended to match THUG2 behavior 1:1, based on reverse engineering rather than merely approximating the feel.
- Skating physics/mechanics are intended to derive from THUG2 behavior.
- Skate animation is intended to match THUG2 skating animation behavior.
- Player-character bones/rig behavior must be adapted so the Fallout playable character correctly matches the imported skating animation/skateboard geometry.

## Garry's Mod Tool Gun requirements
- Tool Gun should link directly to a GMod-style prop/tool menu rather than a Fallout-themed substitute UI.
- Menu must expose Duplicator and Remover tools.
- Highlighting/selecting a tool in the menu should make that the active Tool Gun mode.
- Integration should preserve the functional relationship between menu selection and Tool Gun behavior.

## Garry's Mod Physics Gun requirements
- Physics Gun behavior is intended to be integrated from GMod behavior rather than superficially recreated.
- Preserve relevant firing/interaction behavior.
- Preserve the beam visual.
- Target highlighting should correspond to the beam/player color as appropriate.
- Preserve object manipulation behavior through an integration suitable for the Fallout runtime.

## Inventory/world integration
- GMod weapons should integrate into the Pip-Boy weapons tab.
- GMod weapons/items should be droppable.
- Dropped items should present the item's name when looked at, consistent with usable Fallout world items.

## Historical tooling/converter work
Prior conversations referenced work around runtime tooling, converter improvements, XML override testing, continue-string capture, and locating PS3ObjectMdlParser. These references are retained as historical leads only until corresponding source/files/build evidence is inventoried.

## Historical build labels
Prior conversations referenced build/version labels including v35, v54, and v68. These labels are NOT presently accepted as verified repository builds because their manifests/artifacts have not yet been reconciled into GitHub.

## Historical defect reports
- Game reportedly crashed when right-clicking with skateboard.
- Skateboard reportedly appeared invisible.
These remain candidate failures pending reproduction against the current local build.

## Engineering rule
When local source/build evidence is recovered, convert historical leads into one of:
1. verified current state;
2. superseded history;
3. confirmed failure knowledge;
4. rejected/incorrect historical assumption.
