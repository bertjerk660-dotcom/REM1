# v89 activation lifecycle and board attachment handoff
Date: 2026-10-06. Branch: feature/thug2-native-ui-g6.

## Implemented and verified
Continued from v88, main GOAL/OPEN_WORK/DECISIONS, and failure knowledge. v88 source hash rechecked before cloning. Isolated candidate fnv_gmod_thug2_lifecycle89_candidate, original v88 untouched.
- PreLoadGame and ExitToMainMenu now call quiet normal skate exit before discarding active/readiness state, restoring camera/FOV, releasing injected W, removing riding reference and releasing combat suppression.
- Null-player exit releases injected input and invalidates board/retarget caches without dereferencing old world references.
- Retarget restoration follows the existing quarantine flag.
- PostLoadGame invalidates board and retarget pointers; logs load outcome using NVSE's pointer-value bool convention. Existing general runtime-reset behavior remains for success and failure; failed-load gameplay recovery still needs testing.
- Release Win32 build passed. No deployment or runtime test performed.
- Candidate DLL SHA256: 119491c453bc0bad97ade3aea76c2c312568ffcbfc75b297abac912a1f7a7051.
- Live v85 remains bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41.
This is host lifecycle integration, not a completed port of THUG2 physics/trick logic.

## Evidence for lifecycle
Local NVSE-6.4.9/nvse/nvse/PluginAPI.h documents PreLoadGame before Fallout reads the save.
Serialization.cpp:750 dispatches PreLoadGame; :763 dispatches PostLoadGame with (void*)bLoadSucceeded, length 1. Do not dereference msg->data as bool*.
Hooks_Gameplay.cpp:1073..1081 maps the quit message to ExitToMainMenu.
In-game timing/cleanup still needs validation: active skate -> successful load; failed load; main menu; new game; repeated exit; unequip; lost player. Ensure W never remains injected, fight control is restored, HUD returns, no stale ride board or cached bone is accessed.
Potential remaining issues: focus/menu pauses, save while skating, normal-gameplay weapon draw state restoration, and board ownership identified by base-form scan. Do not infer these are fixed.

## Board audit
research/audit_board_tracks89.py inspected all 838 GLB exports from checkpoint 87.
- 767 have board-root animation tracks; 71 use the static bind pose.
- All 838 parent bone_board_root to control_root.
- Validated board-track float types, finite values, ordered key times, sample counts, nonzero quaternion norms and file bounds.
- No visual parity or complete animation validation claimed. The 51 failed original SKA exports are still unresolved.
- Nodes include bone_board_nose, Bone_Trucks_Nose, Bone_Board_Tail, Bone_Trucks_Tail.
- Current v88/v89 riding visual still uses player position Z - 3 and synthetic spin/flip angles. This has NOT been replaced by original animated attachment.

## Concrete attachment implementation plan
1. Preserve the original converted THUG2 deck/trucks geometry, material provenance and scale. Inspect both held and ride NIF transforms/bounds and the ESP WEAP/STAT paths. Held container is expected BSFadeNode + Prn=Weapon per F004; structure alone is not proof of visibility.
2. Normal Fallout: keep ESP-owned inventory WEAP identity and its normal hand attachment. Audit first-/third-person model references, culling/materials and Weapon attachment transform against actual player skeleton. Fit the original mesh to the hand with an explicit measured bind transform; preserve dropping/picking up.
3. Active skating: sample original bone_board_root with the SAME clip time, loop, blend weights and coordinate conversion as the player pose. Compose control-root/board hierarchy plus measured mesh-bind transform into Fallout coordinates. Retain translation/rotation and source timing; do not pin to a foot or reconstruct flips from score state.
4. For the 71 clips without board channels, use source bind transforms as input to the source hierarchy/transition logic; verify source script attachment switches before declaring a missing track intentional.
5. Entry/exit: one board presentation owner. Normal equipped weapon visible in Fallout; riding visual visible only after valid actor root and clip binding. Hide the held visual without changing inventory identity. On exit destroy/detach only our riding visual and restore prior weapon presentation. On failed bind, roll back cleanly.
6. Source attach events may select hand/board behavior for carry, grab, bail and mounting. Trace original THUG2 scripts/native event code with IDA 6.8 and record mapping. Do not assume a palm parent solely from a clip name.
7. Repair the verified FNV scene-graph ABI mismatch before attaching/detaching or updating nodes. Never re-enable old GetObject/UpdateTransform SDK calls. Root changes invalidate all bindings. Keep current camera and animation quarantines until validated.
8. Validate stills and motion: held first/third person, idle, push, crouch, ollie, kickflip, grab, grind, manual, bail/recover, exit, camera switch, reload. Check feet/deck contact, hand grip, deck facing/scale, duplicate visibility and drop/pickup.

## Artifacts and reproduction
research/prepare_lifecycle89.py creates a new candidate from hash-checked v88 and compiles without deployment. It refuses an existing candidate destination.
builds/lifecycle89_main.patch records the full source change.
builds/lifecycle89_manifest.json records build/live hashes.
research/audit_board_tracks89.py and builds/board_track_audit89.json preserve board-track audit.
Local root: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
Local build: build/lifecycle89. Original proprietary assets stay local.
Remaining main objective: full source-faithful THUG2 free roam, original camera/physics/animations/tricks, Xbox input, exact HUD runtime and GMod systems remain incomplete.
