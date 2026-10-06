# Astra Handoff — THUG2 HUD, Menus and Input

## Prepared UI assets
- 49 source assets indexed with no missing files.
- 6 controller font assets, 4 HUD font assets, 9 HUD panel sprites, 8 controller/menu sprites, 12 UI scripts and 10 HUD/menu audio assets.
- 22 IMG sources converted successfully to PNG previews for inspection.
- Original timer/trick font descriptors and Xbox/PS2/NGC button atlases are preserved; no substitute font metrics were invented.

## Prepared input evidence
- 17 decompiled THUG2 source-QB files indexed for control research.
- 22-entry control matrix generated.
- Direct Xbox/PS2 menu remap evidence is recorded.
- Direct gameplay evidence includes manual Up/Down, nose manual Down/Up, L2 nollie, R2 switch/revert use, Triangle grind/lip families, Square/Circle air families and PS2 L1+R1 / Xbox Black walking-skating switch trigger.

## Astra runtime work
Use the original HUD/menu scripts/assets/state behavior for score/combo/SPECIAL/balance/trick feedback and controller glyphs. Integrate input-mode switching while respecting Fallout bindings outside skate mode.

## Validation gate
Enter skate mode -> Fallout HUD suppressed -> THUG2 HUD/state/glyphs present -> trick/combo/special/balance updates correctly -> walking/skating control transitions source-faithfully -> exit restores Fallout HUD/input.
