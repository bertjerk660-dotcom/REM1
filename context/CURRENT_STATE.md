# Current State

Verified 2026-10-06 from actual source, deployed files, support manifests and prior runtime logs/playtests. New support sidecars remain unplaytested unless explicitly stated.

## Canonical repository
- GitHub repository: bertjerk660-dotcom/REM1.
- Default branch: main.
- Latest inspected main commit: 8082e64b10a40fcd451225e0a0d37847f5a0ff3e.
- Local workspace remains the build/test environment; GitHub is the durable source/history layer.

## Active experimental build: v85
- Source/plugin version: 85.
- Deployed FNVGModTHUG2.dll SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Active REM_GModTHUG2.esp SHA256 at last verification: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
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
- Unified support validator now passes 111 static/preflight checks with zero errors. This is not gameplay validation.
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
## Support completion C — 2026-10-06
- The 20-point non-Astra support pass is complete to the intended support/human/Astra boundary; see SUPPORT_20_POINT_TRACKER.md.
- Unified support validator passes 111 checks with zero errors; report SHA256 68ABA18984574DB48985953B29402CFA3E216E8439CE7F21554544BC4AA2BBDD.
- All 15 previously unresolved staged Source/GMod named weapon sound events now resolve to original installed sound-script definitions; 14/15 have all payload paths confirmed in mounted VPKs.
- Tool Gun/Physgun exact visual/model dependency audit covers 36 paths: 33 resolve; the only absent source-declared triplet is models/weapons/v_Physics.{mdl,vvd,dx90.vtx}. No substitute was invented.
- THUG2 embedded prop classification is complete: 85 spatial geometry candidates, 14 semantic/gap identifiers and 7 unresolved named targets.
- Input/control handoff contains 22 source-backed matrix entries synthesized from 17 decompiled THUG2 QB evidence files.
- Final 290-prop catalog has 290/290 form bindings and 290/290 clean fallback thumbnails.
- Eight regression packs, a 63-artifact non-destructive history registry and an eventual release/install manifest are prepared.
- Dedicated Astra handoffs exist for Q menu, Tool Gun, Physgun, skate physics, animation/board, camera, HUD/input, weapon presentation and THUG2 embedded props.
- The later main-branch Fallout 3 Combine staging handoff has been carried into the support branch; no Fallout 3 runtime replacement was performed.
- New support sidecars remain disabled. Human gameplay validation is still required and no staged feature is promoted to stable by these static checks.

## Prop support phase 3 — 2026-10-06
- New non-Astra/non-Opus prop-focused workflow is tracked in context/PROP_SUPPORT_NEXT_20.md.
- Runtime/Astra code was not modified. Installed v85, main ESP and isolated v88 hashes remain protected.
- Ready player-facing prop catalog remains 290: 170 native FNV + 120 converted GMod/Source.
- A unified static quality/utility ledger now covers all 290 ready props; all retain form binding, collision evidence and generated support thumbnails.
- 56 representative props are prepared in 5 human runtime test batches; runtime results are still pending.
- GMod dependency audit covers all 120 curated props, 85 unique material files and source-authored mobility evidence.
- Native mounted GMod SpawnIcon lookup found 0 matching prebuilt icons for this curated set; 120/120 generated geometry previews remain fallback/audit assets only.
- THUG2 prop work is ranked, not falsely promoted: all 85 spatial geometry candidates are scored and a top-20 visual leaf review packet is prepared.
- Menu growth policy targets 310 first while staying inside 300-320. Up to 20 validated THUG2 props can be added before replacement pressure; 40 lower-priority current entries are ranked as a later replacement reserve only.
- Dedicated prop validator passes 52 checks with zero errors. Unified support validator passes 111 checks with zero errors.
- Release/install metadata now indexes 15 support manifests and still reports no missing core files.
- No phase-3 prop has been called gameplay-verified; sidecars remain disabled and human collision/scale/contact testing is required.

## Preservation prep - 2026-10-06 (read-only pass, Claude)
Scope: dependency and evidence preservation ahead of THUG2 / GMod script extraction for Astra. No runtime source, ESP, DLL, NIF or deployed file was changed; installed runtime remains v85. This is not gameplay validation.

What was done
- Re-read the repo context documents and inspected the live local workspace through Desktop Commander (device DESKTOP-6PTSS3D). GitHub was not available in that session: nothing was committed or pushed, and the workspace has no .git.
- Hashed and dependency-mapped 138 files in four groups: IDA 6.8 scripts/xrefs (37), THUG2 animation/bone/camera (36), GMod Q-menu/Tool Gun/Physgun (34), runtime ownership (35). 0 seed files missing.
- Inventoried C:\IDA68WORK, the THUG2 source dump, Steam build IDs and tool versions.
- Indexed third_party\NVSE-6.4.9\fnv_gmod_thug2_plugin\main.cpp with a heuristic regex index: 212 functions, 104 globals, 3 raw native addresses (0x011D8A80, 0x00C9C1D0, 0x011E07D4), no SafeWrite/WriteRel* inline patches.
- Created: builds\preservation_prep_20261006\ (scan_preservation_deps.py, dependency_scan.json, inventory_external_deps.py, external_dependency_inventory.json, provenance_addendum.json, PRESERVATION_PREP.md, pre_edit_backups\). Appended (existing text untouched) to CURRENT_STATE.md, FAILURE_KNOWLEDGE.md (F011-F013) and OPEN_WORK.md. Pre-edit copies of those three files are in pre_edit_backups\.

Verified findings (as of 07:20 local)
- IDA 6.8 (idaq.exe PID 23616, running since 01:43) is analysing DUMPS\thug2\SLES_526.21 into research\thug2_ida\THUG2_PS2_68.idb. No packed .idb exists; id0/id1/nam are locked. Do not terminate it; save/close normally when idle.
- C:\IDA68WORK is outside the workspace and outside the 247-row code preservation inventory: 50 scripts, 45 outputs, 5 packed IDBs (FNV_attachment90, FNV_skeleton87, FalloutNV_live, GMODCLIENT, GMODSERVER), 3 binaries. 102 of 103 top-level files have no same-name file in research\.
- Workspace xref exports are address-only (see F012). The THUG2 reverse-engineering baseline is the PS2 PAL build (SLES_526.21, MIPS); GOAL.md/ARCHITECTURE.md do not state this.
- Provenance: Fallout NV Steam buildid 1510068; Garry's Mod buildid 25375506; THUG2 DATAP.WAD SHA256 BDBFACF570024191B95FD920808A2CAEBA755FF94EEB19EB839B43ADB9902895; IDA 6.8 idaq.exe SHA256 EC5095959B5B09EA039CAF2F4239E9B712A9C02CF01395EDE0C82FFFC61F5461; SLES_526.21, DATAP.HED, SYSTEM.CNF hashes in external_dependency_inventory.json. Python 3.13.15; capstone 5.0.9, pefile 2024.8.26, pillow 12.3.0, PyFFI 2.2.3, vpk 1.4.0.
- Concurrency: another session was writing to context\ and research\ throughout (89/90 lifecycle, attachment and prop phase 3 work). Re-check mtimes/hashes before writing (F007).

Status: preservation actions P0-P7 are pending (see OPEN_WORK.md). None executed beyond the read-only pass. Full detail: builds\preservation_prep_20261006\PRESERVATION_PREP.md.