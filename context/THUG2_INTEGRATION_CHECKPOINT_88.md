# THUG2 integration checkpoint 88

## Verified outcome
- Continued from main project requirements and feature/thug2-native-ui-g6 checkpoint 87.
- Used IDA Pro 6.8 on an isolated copy of THUG2_SLES_52621.idb; user's open databases untouched.
- Recovered PS2 font parsing from loader 0x1A7468..0x1A819C, reached from fonts/<name>.fnt.ps2 path routine 0x1A73C0.
- Implemented research/decode_thug2_ps2_font.py: version 1/2 records, glyph aliases/special indexes, texture dimensions, indexed pixels, PS2 CLUT permutation and alpha, exact record/bounds/EOF checks.
- All 8 original PS2 fonts decode, including Xbox/PS2/NGC button fonts. The testtitle atlas was visually inspected. Seven unit tests pass.
- Independent testtitle.img.ps2 conversion produces a 2623x30 strip whereas FNT is a 256x256 packed atlas. Direct pixel comparison is not applicable; do not claim independent pixel parity.
- Implemented original bitmap text and source-derived score/special/balance placement in research/thug2_bitmap_hud88.inc. Removed the old invented mode/speed/help text from this candidate HUD.
- research/prepare_hud88.py reconstructs an isolated v88 candidate from verified v86, generates local glyph tables and stages original fonts/sprites; it refuses to overwrite an existing candidate and asserts live v85 hashes.
- Release Win32 compile PASS; candidate DLL SHA256 6e977cc672317af160b823f0b6159d8d893b56717fb3edff0f645a7aa110a439.
- No deployment or gameplay test. Live v85 hash remains bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41.

## Local artifacts
Root: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
- third_party/NVSE-6.4.9/fnv_gmod_thug2_hud88_candidate
- build/hud88/fonts (8 decoded atlases and metric JSON files)
- build/hud88/package (original assets staged, not installed)
- build/hud88/bin/FNVGModTHUG2.dll
- build/hud88/build.log and build_manifest.json
Original proprietary font/sprite binaries and generated glyph data remain local, not committed.

## Exact limitations / next work
1. This is a partial GDI host renderer, NOT the original QB UI runtime or completed HUD parity. Font vertical-metric draw semantics need further loader/draw-routine verification and in-game visual QA. Colors/theme/glow/timing/morphs remain.
2. Combo placement remains temporary. Source panelstuff.qb.q reset_just_trick_text_appearance normal-screen container pos is (320,410), trick text top-centered with internal_scale 0.7; score pot is bottom-centered at its parent origin. Port those alignments before deployment.
3. Bridge scoring is still bridge scoring, not original THUG2 scoring/gameplay. No Xbox input adapter implemented; decoding Xbox glyphs is not controller support.
4. HUD is conditional on g_skate.active; full unified gameplay is not done. Preserve explicit separate exit and restore Fallout HUD, controls, camera, animations, attachments. Review PreLoadGame/ExitToMainMenu lifecycle cleanup and failed-load paths inherited from v86.
5. Camera and retarget quarantines remain. Apply verified Fallout ABI adapter before retarget activation; checkpoint 87 records wrong SDK virtual slots/signatures. 838/889 exported animation GLBs pass only structural checks; 51 failures and binding/keyframe/visual validation remain.
6. Actual GMod Q-menu Lua/Derma behavior, tools and notification bubbles still need implementation. Follow main GOAL/OPEN_WORK/DECISIONS, including real ToolGun/Physgun and curated useful/skate props.
7. Held/riding authentic board alignment and complete tricks remain unverified. Do not represent this candidate as full THUG2 integration.
8. Keep v85 installed until candidate lifecycle and runtime validation gates are satisfied. User's v85 activation pass is not proof of broad stability.

## Durable reproduction/evidence
research/decode_thug2_ps2_font.py, research/test_thug2_ps2_font.py,
research/thug2_bitmap_hud88.inc, research/prepare_hud88.py,
builds/hud88_build_manifest.json, builds/hud88_font_manifest.json,
builds/ida68_thug_font_loader88.json and builds/ida68_thug_font_scan88.json.
