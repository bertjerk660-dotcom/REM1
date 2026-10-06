# Current Verified State

Verified 2026-10-05 from actual local source, deployed files, runtime logs and human playtests.

## Canonical repository
- GitHub repository: bertjerk660-dotcom/REM1.
- Default branch: main.
- Experimental crash-isolation branch: diag/v85-retarget-quarantine.
- Local workspace is the build/test environment; GitHub remains the durable project-memory/history layer.

## Active experimental build: v85
- Source/plugin version: 85.
- Deployed FNVGModTHUG2.dll SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Active REM_GModTHUG2.esp SHA256 at last verification: 3E30300C00241A044F73D476F9497716413DA467278A72AFE29CCAE6767DFEBB.
- Held skateboard path: rem\thug2\skateheldx.nif.
- Held skateboard NIF SHA256: 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A.
- Held NIF structure: Fallout BSFadeNode + Prn=Weapon containing authentic converted THUG2 board geometry.

## v84 human playtest result: FAIL
- Raw Camera3rd transform writes were quarantined.
- Left-click still crashed, proving the raw camera transform path was not the sole crash cause.
- v84 log completed the entire first active skate update, including ride-board update, retarget-selection/apply no-op during its delay, and HUD completion.
- Windows continued to report c0000005 / StackHash_2beb.

## v85 diagnostic change
- THUG2 skeleton retarget selection/application is fully quarantined while the rest of skate mode remains active.
- First 15 frames receive detailed stage diagnostics; later frames receive periodic heartbeat diagnostics through frame 180.
- Purpose: determine whether delayed retarget activation around 900 ms is causal.
- The user's latest crash report occurred before v85 was loaded. Evidence: FNVGModTHUG2.log still begins with "bridge loaded, version 84" and was last written at 18:08:29, while the v85 DLL was deployed at 18:11:46. That earlier report was not a valid v85 test; see the subsequent matched test below.

## Status
v85 compile/deploy validation passed. One user-reported left-click playtest passed, corroborated by a version-85 runtime log through skate frame 180. Sustained playability, exit, and save/load regressions remain unverified. THUG2 remains NOT VERIFIED STABLE.


## Isolated G6 UI candidate
2026-10-05: v86-g6-hud compiles but is not deployed or playtested. Live source and DLL remain v85. IDA 6.8 source discovery and original UI extraction/decompilation are recorded in context/G6_NATIVE_UI_STATUS.md and builds/g6_*.json. Original THUG2 UI runtime, model/animation replacement and exact gameplay parity remain incomplete. This branch is a work-in-progress candidate, not a stable release.

## Matched v85 activation playtest — 2026-10-05
- User reports: "Works without no crash" in response to the requested v85 restart/left-click test.
- Read the actual installed DLL: SHA256 BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41, matching recorded v85.
- Actual FNVGModTHUG2.log starts with "FNVGModTHUG2 bridge loaded, version 85" and records completed skate frame 180, with retarget skipped throughout diagnostic heartbeats.
- Result: PASS for this reported activation test only. This supports the retarget-path hypothesis; it does not establish the precise crash cause or broad stability.
- Camera/retarget quarantines remain enabled. No runtime code or deployed DLL changed in this follow-up.
- v86 remains an undeployed HUD candidate. Next: review lifecycle cleanup and failed-load behavior before candidate deployment; test activation, exit, and HUD restoration.

## 2026-10-06 integration checkpoint
See context/THUG2_INTEGRATION_CHECKPOINT_87.md. Installed v85 and undeployed v86 candidate remain unchanged. IDA 6.8 identified obsolete SDK skeleton virtual-method signatures/slots. Full skater export: 838/889 GLBs pass container checks, 51 failed; no new runtime integration. HUD sprite conversion 44/44; PS2 testtitle font decoding unsupported by current converter. Original THUG2 HUD/menu runtime, complete animations/tricks, Xbox input and board attachment validation remain unfinished.


## Integration checkpoint 88 — original bitmap HUD candidate
See context/THUG2_INTEGRATION_CHECKPOINT_88.md. PS2 font blocker resolved using IDA 6.8 loader analysis: 8/8 original fonts decoded, seven tests pass. Isolated v88 original-bitmap HUD candidate compiles; no deployment/playtest. Original sprites/fonts are now integrated into candidate rendering, but QB runtime, combo morph/alignment, gameplay/animation/controller/menu parity remain incomplete. Live v85 hash reverified unchanged; camera/retarget quarantines retained. Checkpoint 87 font-converter limitation describes the old stock converter, superseded by the new custom decoder.


## Integration checkpoint 89 — 2026-10-06
Isolated v89 (parent v88) compiles with skate lifecycle cleanup on preload/main-menu exit and board/retarget cache invalidation. Not deployed or playtested; live v85 unchanged. Audited all 838 exported GLB board roots: 767 animated, 71 static, all parented to control_root. Board animation placement remains unimplemented; current ride board still uses fixed player offset. See context/THUG2_INTEGRATION_CHECKPOINT_89.md for exact evidence, remaining regression gates and concrete hand/skating attachment plan. Full original THUG2 gameplay remains incomplete.


## Checkpoint 90 — 2026-10-06
Board material-only repair DEPLOYED: original textures restored, opacity repaired in three NIFs; lossless pixel and NIF roundtrip checks passed. Geometry/attachment placement unchanged; in-game visibility not tested. Live plugin remains v85. Separate v90 scene-ABI adapter candidate compiles, not deployed; animation quarantine retained. See context/THUG2_INTEGRATION_CHECKPOINT_90.md and builds/board_material_deployment90.json. Previous held-NIF hash is superseded by the deployment manifest.


## Checkpoint 91 — original animated board assets
Assembled original textured board mesh under original bone_board_root in six GLBs: idle, push, ollie, land, manual and kickflip. Source animation/mesh binary preserved. Offline hierarchy sampling passes; four clips animate the board, idle/push correctly remain static. No visual or Fallout runtime validation/deployment. This is asset assembly, not yet a native THUG2 code/runtime port. See context/THUG2_INTEGRATION_CHECKPOINT_91.md.
