# THUG2 integration follow-up (2026-10-06)
This is an extraction/reverse-engineering checkpoint, NOT a new game build or completed port.

## Existing work retained
- Installed v85 DLL rechecked: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41. No deployment or runtime-source changes in this checkpoint.
- Existing v86 G6 candidate main.cpp SHA256: 52BA85FA1D6968D0868CCC58AB7D73FBB23EC1CBD6623CA44021B1D4CD87A1FA.
- v86 previously compiled HUD visibility ownership, but was not deployed/playtested.
- Original panel sprites were already used by the temporary GDI overlay. This is not the original THUG2 UI runtime.
- Reviewed newer main-branch GOAL/OPEN_WORK/DECISIONS through 1a5450bbe5d79a0292bdd48dfd51b74ae9469b49 and prep/gmod-weapon-props PROP_ASSET_PREP. Main CURRENT_STATE still lags the verified feature branch.
- New requirements concern real GMod scripts/menu/tool feedback and source-faithful THUG2 free roam. They do not establish those systems as implemented.

## Unified mode requirement
Left-click with the board equipped must enter one integrated mode: original THUG2 HUD, gameplay, animations, board motion and input ownership together. A separate exit action must restore Fallout HUD, controls, camera and animation ownership. Keyboard/mouse and Xbox input must cover the resulting state machine. The real GMod Q menu remains a separate unfinished source-port task, not the existing custom menu.

## IDA Pro 6.8 evidence
Isolated database copies were used; no changes to the user's open databases.
- THUG2 source animation audit: 29 matching string records. Discovery only.
- FNV NiNode vtable 0x109B5AC, NiAVObject vtable 0x109B00C.
- Actual slot 0x27 (39): NiNode search 0xA5E560; base search 0xA59E20. Base search dereferences its argument and compares an interned name pointer at object+8.
- SDK NiObjects.h explicitly says UNMODIFIED OBSE FILE. Its GetObject(const char*) declaration occupies slot 0x26, where this FNV binary has nullsub_3 (retn 4).
- SDK UpdateTransform(void) occupies slot 0x2D, where this binary also has nullsub_3 (retn 4), incompatible with a zero-stack-argument call.
- This is concrete ABI mismatch evidence, NOT a proven runtime crash cause. Do not re-enable retarget/camera calls until a version-checked adapter, correct transform layout and update semantics are verified. A delay and RTTI cast cannot repair a wrong virtual-method slot/signature.

## Animation extraction
- Source: local DATAP/anims/thps6_skater* directories; original 50-bone THPS6_Human skeleton.
- 889 SKA inputs, 838 structurally valid GLBs, 51 failures.
- Includes basics, on-foot/partial, flip/grab, grind/lip/manual-related, specials and other skater sets.
- Output: build/skater87/glb; complete provenance/failure manifest: builds/skater87_extraction.json in GitHub.
- Validation only checked container version/size, nodes and animation channels. Numeric keyframe validity, bone binding, root/board motion, retargeting, visual parity and in-game playback remain unverified.
- Failure examples: partial throw clips rejected by parser; several flatland clips returned without expected GLB output. Exit code alone is insufficient.
- Reproduction: research/extract_skater87.py. It does not install assets or modify the live plugin.

## HUD extraction findings
- panelstuff.qb.q contains full decompiler output with screen-element hierarchy, positions/scales, font references and balance arrow path. panelstuff.q is truncated after script hide_panel_stuff and must not be used as a complete script.
- Original fonts: testtitle, newtrickfont, newtimerfont and small. startup.qb.q supplies spacing.
- NeversoftMultitool ps2tex build/thug2_ui_original/images/panelsprites -o build/hud87/sprites converted 44/44 files.
- NeversoftMultitool fnt build/thug2_ui_original/fonts/testtitle.fnt.ps2 -o build/hud87/fonts converted 0/1, reporting 'not this format'. Do not silently substitute a Windows font and call it an exact HUD port.
- No new renderer/menus/popups or controller adapter were implemented in this checkpoint.

## Next implementation gates
1. Repair PS2 font decoding using the original loader/metrics; validate glyph mapping and script semantics.
2. Implement source-driven screen hierarchy/rendering and HUD lifecycle restoration; test exit and successful/failed loads.
3. Replace obsolete skeleton ABI calls with verified FNV bindings; first validate read-only skeleton resolution.
4. Resolve failed SKA exports and validate all keyframe/board tracks; integrate via a safe engine animation ownership/update path.
5. Map source trick transitions/input for M&K/Xbox; prevent Fallout/GMod input leakage during skating.
6. Validate held/ride board attachment visually, then complete sustained enter/trick/exit/save/load regression tests.
