# Codex C08 — Unified GMod / THUG2 source input investigation

## Objective
Map original GMod and THUG2 input semantics against the Fallout host so **Claude Opus** can implement one conflict-free M&K/Xbox ownership layer. **Codex** later validates the integrated controls at runtime.

## Source behavior to map

### GMod
- Q-menu bind/open/hold/close semantics;
- menu cursor/focus;
- Toolgun primary/secondary/reload;
- Physgun acquire/hold/release/launch/rotate/freeze/distance;
- any tool-specific modifier keys used by the supported proof tools.

### THUG2
- movement/turning;
- crouch/ollie;
- flip/grab;
- grind/lip;
- manual;
- revert;
- specials;
- camera;
- walking/skating transitions;
- board-related state actions;
- pause/menu interactions;
- Xbox mappings;
- keyboard/mouse mappings.

### Fallout compatibility
- attack/secondary;
- use;
- Pip-Boy;
- pause;
- console;
- weapon switching/holster;
- camera;
- movement;
- any host menu focus ownership.

## Required questions
1. What gameplay action abstraction does each source game use beneath device-specific buttons?
2. What exact M&K and Xbox inputs map to those actions?
3. Which actions are edge-triggered, held, repeated or chorded?
4. Which modifiers alter Toolgun/Physgun/THUG2 behavior?
5. Which inputs collide with Fallout controls?
6. Which mode must own each collision?
7. How does Q-menu capture/release input?
8. How does THUG2 prevent underlying non-skate actions during active skating?
9. What input must remain protected for safe mode exit?
10. How should device switching preserve action semantics without making two different control systems?

## Required outputs
- context/CODEX/C08_UNIFIED_INPUT_EVIDENCE_2026-10-07.md
- build/evidence/input_c08/source_action_map.json
- build/evidence/input_c08/keyboard_mouse_map.json
- build/evidence/input_c08/xbox_map.json
- build/evidence/input_c08/conflict_matrix.json
- build/evidence/input_c08/opus_input_adapter_contract.json

Use context/INPUT_OWNERSHIP_MATRIX.md as the host-side coordination target, but verify original source semantics rather than assuming that matrix is proof.

## Stop condition
Stop when Opus can implement one mode-owned input layer for Fallout, Q-menu/Toolgun/Physgun and THUG2 without guessing controls.

Do not implement the final input layer in Codex.
