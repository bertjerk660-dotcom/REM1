# THUG2 native UI replacement — work in progress

## Requested outcome
Use IDA Pro 6.8 and original local THUG2 material. Left-click on the skateboard must hide Fallout's HUD and enter THUG2 gameplay with matching models, animations, camera, HUD, pause menus, popups, combo scoring and special meters. Exit restores normal Fallout gameplay.

## Verified this session
- Connected GitHub repository: bertjerk660-dotcom/REM1.
- Source baseline: v85, raw main.cpp SHA256 ce3628ae131f42424459f5441051817ec132a7ae53414765047eba6a9a4727a5.
- Live DLL remains v85, SHA256 bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41.
- IDA Pro 6.8 analysis ran against a separate copy of THUG2_skate_batch.idb. The user's open IDA database was not modified.
- Input SLES_526.21 is PS2 R5900 MIPS; SHA256 91c3d11bf0f1546f8ea20a22e7c1708ea91697f3c1393f36d9d7f2d4449963d1.
- IDA discovered 390 relevant strings and references. Twelve selected HUD/score/special entrypoint records and 63 decompiled script symbol locations are in builds/g6_source_audit.json. Data-table neighbors are candidates, not proven callable function pointers.
- Extracted 1,868 original script/UI-related files (145,293,803 bytes) with path, offset, size and SHA256 manifests. Broad matching also includes special animations and menu models.
- NeversoftMultitool reported decompiling 415/416 files, 4,720 scripts and 9,350 globals, with one unresolved error. This is parser output, not proof of source equivalence or a working interpreter.
- Candidate v86 compiles with MSBuild Release/Win32. See builds/g6_hud_candidate.json for final DLL hash.
- The candidate was NOT deployed or played. No replacement model or animation was installed.

## Candidate behavior
src/plugin/thug2_hud_visibility.inc owns the New Vegas HUD root's visible trait while skate mode is active and restores the captured value on exit. It resolves the current root each time, avoids dereferencing stored root identities, preserves an initially hidden HUD, and releases ownership during load/menu transitions.
The candidate links the SDK GameUI.cpp and disables all post-build auto-install events. The known v85 camera/retarget quarantines remain enabled. The existing GDI skate overlay is still an approximation; this change does not implement original THUG2 UI.

## Local locations
Workspace: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
Candidate source: third_party/NVSE-6.4.9/fnv_gmod_thug2_g6_candidate
Candidate DLL: build/g6_candidate/FNVGModTHUG2.dll
Original extracted material: build/thug2_ui_original
Decompiled output: build/thug2_ui_decompiled
Full IDA audit: research/thug2_ida/hud_score_audit68.json
All original source archives and the active plugin source remain unchanged.

## Rebuild and source layout
This branch records the inspected baseline main.cpp, candidate source, overlay, project, new module, transformation scripts, hashes and manifests. It is NOT yet a standalone clean-checkout build: the existing NVSE-6.4.9 SDK and generated include dependencies are required from the inspected local workspace.
Repository src/plugin maps to the candidate directory above, alongside ../nvse and ../common from the existing SDK. Generated asset/data includes remain local; do not redistribute extracted proprietary data merely to make the repository self-contained.
research/prepare_g6_hud_candidate.py creates a new isolated candidate from the exact hashed baseline and uses research/thug2_hud_visibility.inc. It intentionally refuses to overwrite an already modified candidate.
research/finalize_g6_candidate.py rebuilds the existing candidate, removes auto-install events, uses separate plugin/common intermediate directories, and verifies live source/deployment hashes.
The extractor takes source-directory and output-directory arguments. The IDA script expects THUG2_AUDIT_OUTPUT and must run with IDA 6.8 on an isolated database copy.
Use the local NeversoftMultitool qb command on extracted scripts with an explicit output directory. Preserve nonzero exit status as a partial failure.

## Required before promotion
1. Obtain an actual v85 left-click playtest and its matching runtime/crash log. No observation yet proves whether retarget quarantine removes the crash. One successful run would support a hypothesis, not prove causality.
2. Test candidate HUD visibility at activation, initially hidden HUD, exit, death, save/load success and failure, loading transitions, returning to main menu, and UI-root rebuild. Native rendering and third-party HUD compatibility remain unverified.
3. Validate the QB parser's missing file and semantics, resolve HUD/theme/font assets, map script-native calls and score/special object state. PS2 instructions cannot execute directly inside the x86 New Vegas process.
4. Implement and verify a source-grounded script/runtime adapter and renderer, including pause/menu input ownership and popup transitions.
5. Repair the established activation/attachment/animation faults from evidence, then compare movement/camera/animation/scoring against the source game.
6. Run sustained playability and save/load regressions before enabling or deploying the replacement.

Do not describe this branch as a complete THUG2 merge, exact-code port, fixed crash, or completed model/animation replacement.
