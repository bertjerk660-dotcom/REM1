# Codex C07 — THUG2 HUD, UI, scoring and popup investigation

## Objective
Recover original THUG2 free-roam HUD/UI state, renderer dependencies and event bindings so **Claude Opus** can implement the source-faithful overlay in Fallout. After Opus implementation, **Codex** validates it live.

Codex performs evidence work only.

## Scope
Investigate:
- score;
- trick name;
- combo score;
- multiplier;
- SPECIAL meter/state;
- grind/manual/lip balance meters;
- trick/status popups;
- combo resolution;
- bail/land feedback;
- free-roam pause/menu surfaces needed by the selected runtime;
- HUD enable/disable lifecycle.

Exclude campaign/story UI not needed for free-roam skating.

## Required questions
1. Which files/functions/classes create/update each surface?
2. Which gameplay state variables/events feed them?
3. How are score/combo/multiplier/SPECIAL represented and updated?
4. How are balance meters parameterized/rendered?
5. How do popups queue, animate, stack, fade and resolve?
6. Which fonts/textures/sprites/materials are required?
7. What coordinate/safe-area/scaling rules are used?
8. What aspect/resolution behavior exists?
9. Which renderer calls are script/data-defined versus native?
10. What happens during pause, bail, mode change and exit?
11. What host renderer/event adapter must Opus expose?
12. Which Fallout HUD/top-left paths must be suppressed during THUG2 ownership?

## Required outputs
- context/CODEX/THUG2_C07_HUD_UI_EVIDENCE_2026-10-07.md
- build/evidence/thug2_c07/hud_surface_manifest.json
- build/evidence/thug2_c07/gameplay_event_binding.json
- build/evidence/thug2_c07/ui_asset_font_manifest.json
- build/evidence/thug2_c07/scaling_layout_contract.json
- build/evidence/thug2_c07/opus_ui_adapter_contract.json

## Stop condition
Stop when Opus can implement score/combo/SPECIAL/balance/popups and HUD ownership without inventing a replacement UI.

No final renderer implementation in Codex.
