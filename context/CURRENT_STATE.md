# Current State

Verified 2026-10-05 from actual source, deployed files, runtime logs and human playtests.

## Canonical repository
- GitHub repository: bertjerk660-dotcom/REM1.
- Default branch: main.
- Latest inspected main commit: 1733d70cb4f4d20d5b339d4510aceb7b356c5794.
- Local workspace remains the build/test environment; GitHub is the durable source/history layer.

## Active experimental build: v85
- Source/plugin version: 85.
- Deployed FNVGModTHUG2.dll SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Active REM_GModTHUG2.esp SHA256 at last verification: 3E30300C00241A044F73D476F9497716413DA467278A72AFE29CCAE6767DFEBB.
- Held skateboard path: rem\thug2\skateheldx.nif.
- Held skateboard NIF SHA256: 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A.
- Held NIF structure: BSFadeNode + Prn=Weapon containing authentic converted THUG2 board geometry.

## v84 human playtest result: FAIL
- Raw Camera3rd transform writes were quarantined.
- Left-click still crashed, proving the raw camera transform path was not the sole crash cause.
- v84 log completed the entire first skate update, including ride-board update and the delayed-retarget no-op for that first frame.
- Therefore the crash occurs after at least one complete active skate frame.
- Windows still reported c0000005 / StackHash_2beb.

## v85 diagnostic change
- THUG2 skeleton retarget selection/application is fully quarantined while the rest of skate mode remains active.
- First 15 frames receive full stage diagnostics; later frames receive periodic heartbeat diagnostics up to frame 180.
- Purpose: test whether the delayed retarget activation around 900 ms is causal. If v85 does not crash, retarget is proven causal. If v85 still crashes, retarget is cleared and the heartbeat timing will narrow the remaining asynchronous/frame-path failure.

## Status
v85 compile/deploy validation passed. Human playability validation is pending. THUG2 remains NOT VERIFIED STABLE.


## G6 native UI work, 2026-10-05
An isolated v86 HUD ownership candidate compiles but is not deployed or playtested. Active source and DLL remain v85. IDA 6.8 HUD/score discovery and original UI extraction/decompilation completed with a partial parser failure. Exact THUG2 UI/runtime, model and animation replacement remain incomplete. See G6_NATIVE_UI_STATUS.md and build/manifests/g6_hud_candidate.json. GitHub work branch: feature/thug2-native-ui-g6.

## Support lane update — 2026-10-06
- Installed runtime is v85; deployed DLL SHA256 BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Astra v88 remains isolated and undeployed; local candidate DLL SHA256 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.
- Current active REM_GModTHUG2.esp SHA256 is 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
- Pip-Boy source-game origin icons are installed for the staged GMod/THUG2 weapons.
- Combine Soldier full-body armor NIF is staged and statically validated. Wearable NIF SHA256 90A836EEF689C50994ED6E5BECC7B37CEFA0B32DA6E20D88C34DC193837B6728.
- REM_CombineArmor_Test.esp SHA256 52B06C9D1FA087B32BD2F83120603903893D24781BC9490D89C3D9EEE105979E exists but is disabled and unplaytested.
- Support work is separated from Astra runtime/mechanics work; see SUPPORT_WORKFLOW.md and COMBINE_ARMOR_STAGING.md.

## Support phase 2 — 20-point workflow progress
- Unified support validator now passes 94 static/preflight checks with zero errors. This is not gameplay validation.
- Final curated content remains 290 ready props: 170 native Fallout existing-form entries + 120 converted GMod/Source entries.
- Q-menu data adapter now exposes all 290 ready entries with category/search/form-binding metadata for the future real GMod Q-menu port.
- 290/290 fallback/support prop thumbnails pass the local quality audit.
- THUG2 embedded-prop queue remains 106 targets. Source QB evidence now records 86 targets with level-component evidence and 85 with position evidence; 85 targets have spatial GLB candidate mappings. These are not yet standalone/promoted props.
- GMod/HL weapon staging has a 49-class inventory QA matrix, 48 view candidates and 48 world candidates; camera/fists remain intentional special cases.
- Original Source/GMod sound dependency handoff resolves all named weapon sound references used by the staged 49-class set; unresolved runtime refs: 0.
- Tool Gun/Physgun source asset/script handoff is indexed; one legacy Source-declared path (models/weapons/v_Physics.mdl) is absent from mounted content and is explicitly recorded rather than recreated.
- THUG2 controller/trick/physics handoff contains 17 decompiled source files plus source-backed Xbox equivalence/trigger evidence.
- Three isolated support sidecars exist and are all disabled: Combine armor test, GMod prop catalog, RPG presentation fix.
- Playtest preflight/postflight capture, regression packs and a session-plan generator are prepared.
- A non-destructive inventory classifies legacy version-labelled artifacts; known-bad v74 evidence is preserved and must not be reapplied.
- Release/install staging manifest reports no currently missing required baseline files. This does not mean release-ready.
- Eight Astra handoff packets plus context/SUPPORT_20_POINT_TRACKER.md define the current support-to-Astra boundary.
- Installed runtime remains v85 and Astra v88 remains isolated/not installed.