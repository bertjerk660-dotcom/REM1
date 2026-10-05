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
- The user's latest crash report occurred before v85 was loaded. Evidence: FNVGModTHUG2.log still begins with "bridge loaded, version 84" and was last written at 18:08:29, while the v85 DLL was deployed at 18:11:46. Therefore v85 has not yet received a valid human playtest.

## Status
v85 compile/deploy validation passed. Human playability validation is pending. THUG2 remains NOT VERIFIED STABLE.


## Isolated G6 UI candidate
2026-10-05: v86-g6-hud compiles but is not deployed or playtested. Live source and DLL remain v85. IDA 6.8 source discovery and original UI extraction/decompilation are recorded in context/G6_NATIVE_UI_STATUS.md and builds/g6_*.json. Original THUG2 UI runtime, model/animation replacement and exact gameplay parity remain incomplete. This branch is a work-in-progress candidate, not a stable release.
