# Current Verified State

Verified 2026-10-05 from the actual local workspace, deployed-file records, build manifests and crash logs.

## Local workspace
Path: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
The workspace contains the NVSE plugin source, research/conversion/patch tooling, build outputs, backups, context documents and third-party tooling.

## Active runtime
> Haiku audit note (2026-10-07): the DLL/ESP hashes and 'source version remains 81' lines below are superseded. Live deployed hashes on the Windows machine: FNVGModTHUG2.dll D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206; REM_GModTHUG2.esp 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7. Plugin main.cpp labels itself version 85. Authority: manifests/gmod_2026-10-07/runtime_snapshot.json.
- DLL source version remains 81 for the current diagnostic branch.
- Deployed FNVGModTHUG2.dll SHA256: A801DC80F96F6269CB8516ECC47CE48E4FAA2DDB315308A8476F4658D7FB5EF5.
- Active REM_GModTHUG2.esp SHA256: 3E30300C00241A044F73D476F9497716413DA467278A72AFE29CCAE6767DFEBB.
- Canonical GitHub repository is now bertjerk660-dotcom/REM1. Earlier local documentation saying no canonical repository existed is superseded.

## Historical verified milestone v59
PROJECT_STATUS_V59.md records 7,474 GMod converted-registry entries: 5,655 successful converted models with collision and 1,819 missing-source entries. It records Tool Gun, Physics Gun, Crowbar/imported weapons, Pip-Boy/drop-pickup integration, THUG2 skate mechanics/SFX and broader GMod conversion/runtime work as implemented by v59. Later regressions mean this does not imply the current THUG2 path is stable.

## v80
Compile/deploy/asset parse/game boot passed; human playtest failed. Skateboard was invisible and left-click entered initialization then crashed with c0000005 after HUD completion.

## v81
Retarget lifecycle was hardened: RTTI bone validation, active-root tracking/cache invalidation, clip/quaternion validation, 900 ms post-camera delay and first-update diagnostics. Compile/deploy passed. DLL SHA256 above. Human playtest then still reported invisible board and LMB crash; diagnostic log reached camera profile update complete.

## v82 current asset-only diagnostic
v81 DLL intentionally remains unchanged. The held skateboard NIF was replaced with authentic converted THUG2 board geometry in a Fallout held-weapon BSFadeNode container with Prn=Weapon.
Deployed skateheldx.nif SHA256: 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A.
Structural/PyFFI validation passes. Human confirmation of visibility and whether LMB crash persists is pending.

## Status
THUG2 is NOT VERIFIED STABLE until v82 is playtested.


## 2026-10-06 support-lane reconciliation
- GPT-6/Opus implementation package exists under build/handoffs/gpt6_opus/.
- Physics Gun IDA 6.8 evidence closure is complete for handoff; native FNV implementation/playtest is NOT complete.
- Physics Gun known presentation gap: models/weapons/v_physics.mdl + VVD + DX90.VTX provenance remains unresolved.
- THUG2 prop evidence correction: 85 evidence-backed conversion targets are queued; the former 21 not-ready identifiers are semantic/unproven geometry and are not missing standalone models.
- Master execution queue, dependency graph, regression spec, acceptance gates, sidecar strategy and preflight validator are prepared.
- Preflight passed locally on 2026-10-06: 85 targets, zero semantic overlap, 16/16 source level GLBs available, both IDA 6.8 Physgun evidence exports present.
- These preparation results do not change the verified deployed runtime version or establish THUG2/Physgun runtime success.

## 2026-10-06 latest human playtest
- THUG2 skateboard held-weapon presentation is now visibly working: the skateboard weapon model appears in game and is positioned correctly in the player's hand. This verifies the held-weapon visibility/placement path only; board-to-feet attachment and full skate-animation transitions still require separate validation.
- Skate mode still presents only a simple text overlay rather than the original THUG2 HUD/UI system.
- Fallout-style alerts still appear in the top-left during skate mode. These are temporary/fallback behavior and must ultimately be replaced by the source-faithful THUG2 UI/notification/scoring presentation needed by the THUG2 skating subsystem.
- The Fallout HUD remains visible during skate mode. Required final behavior is to suppress the Fallout HUD while skate mode is active, run the THUG2 HUD/UI stack, and restore the Fallout HUD cleanly when skate mode exits.
- Physics Gun acquisition/manipulation range is currently extremely short compared with intended GMod behavior.
- Physics Gun audio is incorrect while a target is held by the beam: the correct continuous beam/hold loop sound is not playing.
- Physics Gun actor handling is mis-targeted: when the grab/lock finally engages an actor, the player is knocked unconscious instead of the acquired target.
- These observations are regressions/implementation gaps, not evidence that THUG2 or Physics Gun runtime integration is complete.

- Skate-mode state switching is now human-verified: with the skateboard equipped, left-click successfully activates skate mode and the configured holster key successfully deactivates it back to Fallout mode.
- THUG2 sounds currently appear to be working during the tested skate-mode path; this is a positive playtest observation, not yet an exhaustive audio-parity validation.
- Grinding is functionally broken: pressing G can initiate grinding anywhere instead of requiring valid grindable geometry/contact/state.
- THUG2 skating animation integration remains broken. The board does not transition from the held-weapon position to the skater's feet for riding, and the tested THUG2 animation set is not functioning.
- THUG2 UI/HUD remains unimplemented/broken in runtime as previously recorded.
- The currently visible GMod-style prop menu appears visually correct in playtest, but it is explicitly a placeholder. It must not be treated as the finished Q menu; the final implementation remains the real/source-faithful GMod Q/spawn-menu system and compatibility bridge.


## 2026-10-07 authenticated GMod evidence intake
Canonical `main` commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0` now contains a source/IDA-backed GMod investigation bundle. The preparation branch selectively imported the primary reports and unresolved-dependency/validation manifests.

Coordination review result:
- C01 Q-menu: **SUBSTANTIAL PARTIAL**;
- C02 Toolgun behavior: **SUBSTANTIAL PARTIAL**;
- C03 Physgun closure: **PARTIAL**;
- O02/O03/O04 remain **WAITING FOR CODEX GAP CLOSURE**;
- broad GMod investigation should not be repeated;
- exact remaining gaps are enumerated in `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`.

The GMod evidence bundle passed 36,078 metadata/graph/report checks with 0 errors. This is evidence-package validation only and does not establish runtime parity or final implementation.


## 2026-10-07 Opus conversion-pipeline preflight
A fresh workflow review restored the original golden-conversion ordering before weapon visual work.

- O00 Golden Source bench conversion proof: READY FOR OPUS.
- Source bench MDL/VVD/DX90/PHY, QC/reference/physics SMD and VMT/VTF/mask inputs were re-hashed on the current local machine and match recorded provenance.
- O00 must be implemented in an isolated sidecar and pass visual/material/scale/orientation/collision/save-load acceptance before weapon conversion is trusted.
- O01 Toolgun presentation is fully hash-prepared but is now correctly classified as READY AFTER O00 PASS.

This changes preparation ordering only; no runtime feature was implemented or promoted.


## 2026-10-07 unified Opus visual-source validation
A reusable local validator now checks the prepared visual-source packages before Opus work:
- O00 golden bench: PASS;
- O01 Toolgun presentation: PASS;
- O08a crowbar: PASS;
- O08b pistol: PASS;
- O08c SMG1: PASS;
- total: 87 files;
- errors: 0.

Report: `build/validation/opus_visual_source_validation_20261007.json`.

One real staging omission was found and corrected during preparation: the original `w_smg2.vmt` references `w_smg2specularmask.vtf`; the old staged w_smg1 package omitted it. The exact VPK source file was copied into staging and hash-matches the original. No replacement texture was created.

The remaining path to 100% Opus preparation is fixed in `context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md`. After clean-branch reconciliation, all remaining readiness points are C01-C08 evidence work.


## 2026-10-07 clean Opus-ready branch
A new preparation branch was created directly from canonical main:
`prep/opus-ready-20261007`

GitHub comparison after coordination/transplant:
- status: ahead;
- ahead of main: 78 commits at that verification (Haiku audit 2026-10-07: 151 ahead / 0 behind);
- behind main: 0 commits.

This replaces the conflicted/diverged finalization branch as the preferred preparation branch for future Codex closure work and Claude Opus launch.

Preparation readiness on this branch is **81/100**. All remaining 19 points are explicitly assigned to C01-C08 evidence gates in `context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md`.


## 2026-10-07 clean Opus-ready branch finalized
The current preparation branch is `prep/opus-ready-20261007`, created from canonical main after the authenticated GMod evidence merge.

Latest GitHub reconciliation:
- compared against current `main`;
- branch status: ahead;
- behind main: **0**;
- older `prep/opus-readiness-finalization-20261007` remains diverged and is historical only;
- no runtime candidate branch was promoted.

Preparation baseline is therefore **81/100**.

The remaining 19 preparation points are exclusively C01-C08 Codex evidence gates. Normal GPT must not manufacture those points, and Claude Opus must not be asked to rediscover them during implementation.


## 2026-10-07 Opus launch preflight automation
Normal-GPT preparation now has machine-enforced implementation handoff gates without changing the 81/100 evidence score.

- reusable candidate-manifest validator: `research/validate_opus_candidate_manifest.py`;
- preflight mode passes O00/O01/O08a/O08b/O08c with 0 errors;
- freeze mode is mandatory before any Opus candidate is handed to Codex;
- semantic package-gate validator: `research/validate_opus_gate_state.py`;
- current semantic-gate validation PASS: 81/100, 0 false-unlock errors;
- O00 deterministic Codex runtime validation packet is prepared;
- common O01/O08a/O08b/O08c Codex visual-presentation validation packet is prepared;
- consolidated checkpoint: `context/OPUS_LAUNCH_PREFLIGHT_BASELINE_2026-10-07.md`.

This is preparation/pipeline evidence only. No Opus implementation or Codex C01-C08 completion is claimed.

## 2026-10-07 Haiku final preflight audit

- Preparation readiness: 81/100 before and after the audit. No C01-C08 gate changed state.
- Validators re-run on the audit branch on 2026-10-07. Visual source packets: PASS, 87 files, 0 errors, root = local FNV_GMOD_THUG2 workspace. Candidate preflight for the O00 seed: PASS, 0 errors. Gate state: PASS, 81/100, 0 errors. These are metadata and hash checks only. They do not validate any game feature.
- Live deployed hashes re-checked on the Windows machine. FNVGModTHUG2.dll D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206 and REM_GModTHUG2.esp 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7 match runtime_snapshot.json. main.cpp 4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE and gmod_overlay.inc E6EF0C484AFDDC1A74C02F6BA8A72CD0899D6E80F5BA5459CD61B9C67183250F also match.
- UNRESOLVED IDENTITY DRIFT: the deployed Data/meshes/rem/thug2/skateheldx.nif hashes to 1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852. The v82 record expects 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A. Either the file changed after the v82 record was written or the record is stale. The cause is not established (F007). Do not claim v82 build identity until this is reconciled.
- THUG2 platform: the local disc executable is PS2 SLES_526.21, SHA256 91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1, which matches PROVENANCE_INDEX. It is a 32-bit little-endian MIPS ELF. Any THUG2 IDA work must name this PS2 target. No PC THUG2 binary is recorded.
- Codex: no C01-C08 final delivery exists beyond the gap-closure and request packets. The old 2026-10-07 structural baseline treated future deliverables as missing/failing. This has been corrected: `research/validate_codex_readiness_outputs.py --mode baseline` now reports those not-yet-produced paths as PENDING. The 2026-10-08 baseline is CONSISTENT with 46 pending outputs and 0 invalid JSON. Delivery mode still fails missing outputs after a Codex delivery claim. Semantic gate points remain unchanged.
- Corrections made by this audit: O01/O08a/O08b/O08c described as READY AFTER O00 PASS, not READY FOR OPUS, in OPUS_LAUNCH_PREFLIGHT_BASELINE and the scorecard; commit counts dated; the Active runtime hashes above are marked superseded.

## 2026-10-08 documentation/provenance reconciliation

The held-board identity discrepancy is resolved as an intentional historical supersession:
- v82 pre-material-repair: `4F12178D...`;
- v90 material-repaired deployed identity: `1FB3CE19...`.

No game file was changed during this reconciliation.

Further documentation-only work in this pass:
- current ownership wording is normalized in `AGENT_OWNERSHIP.md` and `LEGACY_ROLE_PATH_MAP.md`;
- Codex C01-C08 output expectations are being separated into pre-delivery PENDING versus post-delivery structural validation;
- quarantined branch heads are being pinned in a current machine-readable index.

Preparation readiness remains evidence-scored; documentation cleanup alone does not award C01-C08 points.


### Codex output-contract semantics resolved
The required C01-C08 evidence paths are future Codex deliverables, not preparation-time files that should already exist.

Current validator behavior:
- baseline mode: missing future deliverables = `PENDING_EXPECTED_OUTPUT`;
- delivery mode: missing files after a delivery claim = structural failure;
- semantic review remains mandatory in both modes.

Recorded baseline:
`build/validation/codex_c01_c08_output_baseline_20261008.json`

Result:
- C01-C08 = PENDING_NOT_DELIVERED;
- pending = 46;
- invalid JSON = 0;
- baseline contract = CONSISTENT.

This clarification awards no readiness points by itself.


## 2026-10-08 normal-GPT local pre-Opus audit

Independent live checks on the Windows machine passed: all five O00/O01/O08a/O08b/O08c visual source sets (87 files / 0 errors), five correctly selected candidate-manifest preflight seeds (0 errors each), and the semantic package-gate validator (81/100 / 0 errors). The local Codex evidence validator/contract were safely backed up and synchronized from the newer coordination branch; baseline mode now correctly classifies 46 not-yet-produced deliverables as PENDING, with 0 invalid JSON. Protected installed DLL/ESP/main.cpp and skateboard material-repaired NIF SHA-256 hashes match their independently recorded GitHub provenance.

The active plugins.txt lists `REM_CombineArmor_Test_TorsoLowered.esp` and `REM_Goodsprings_CombineDeathclawEncounter.esp` alongside the main mod; a clean O00 test must explicitly isolate or account for these test sidecars. The historical local `research/check_opus_launch_state.ps1` hard-coded source/DLL expectations are stale; do not interpret that guard's potential mismatch as a game defect. Separate Goodsprings encounter static inspection found ESP/DLL/voice files but does not establish gameplay completion.

Full details and hashes: `context/HANDOFFS/NORMAL_GPT_PRE_OPUS_LIVE_AUDIT_2026-10-08.md` and `build/validation/normal_gpt_pre_opus_live_audit_20261008.json`. Readiness **remains 81/100**; no Codex gate was closed, Opus implementation was not started, and no runtime artifact or active plugin configuration was changed.

## 2026-10-09 GMod research intake on latest preparation successor

`prep/gmod-research-intake-20261009` selectively integrates the October 8 source-grounded GMod UI/Physgun specialist contract, research index and partial-status manifest from the diverged `research/gmod-ui-physgun-20261008` branch. The integrated content describes direct Lua checks and existing native evidence; it makes **no claim of new IDA Pro 6.8 execution**, runtime implementation or GMod parity. C01/C02/C03 remain PARTIAL and O02/O03/O04 remain blocked until Codex returns implementation-grade evidence and normal GPT reviews the original stop conditions. Research intake and provenance: `build/prepared/gmod_research_selective_intake_20261009.json`.

A new focused Codex evidence-only kickoff document is at `context/HANDOFFS/NEXT_CODEX_GMOD_C01_C03_KICKOFF_2026-10-09.md`. This is a **prepared request**, not proof it has been submitted or executed. Preparation readiness remains **81/100**. No game files were edited or runtime candidates promoted during this GitHub documentation reconciliation.

## 2026-10-09 O00 Golden Source Bench - FROZEN, WAITING FOR CODEX VALIDATION

Implementation branch `implementation/opus-o00-golden-bench-20261009`, parent `ba35ebe` (prep/gmod-research-intake-20261009), base merge `5cbe1be` (adds prep/opus-ready-20261007), tooling commit `94206ab`.

- New pipeline `research/source_to_fnv` converts the original HL2 bench01a (448 tris, 15 convex collision solids) with all 10 source hashes verified.
- Static gates: 12/12 PASS, including byte-identical rerun. Freeze validation: PASS, 0 errors.
- Candidate manifest: `builds/O00_golden_bench_candidate_20261009.json`. Reports: `build/candidates/O00_20261009/`.
- Deployed to the live game as new files only: `meshes/rem/golden_bench/bench01a.nif`, `textures/rem/golden_bench/bench01a{,_m,_n}.dds`, `REM_GoldenBench_Test.esp`. The sidecar is **not** in plugins.txt (default load order unchanged).
- Protected files re-hashed after deploy and unchanged: FNVGModTHUG2.dll D6C88816..., REM_GModTHUG2.esp 0A81B429..., main.cpp 4517D804..., skateheldx.nif 1FB3CE19....
- Runtime status: **not run**. O00 is not PASS until Codex returns a PASS on O00-R1..R7. O01/O08 stay READY AFTER O00 PASS.
- New failure knowledge: F013 (SMD frame rotation), F014 (pyffi header), F015 (legacy converter defects).

## 2026-10-09 O00 runtime self-test (Opus) - PASS, not independent

Codex credits ran out, so on the owner's instruction Claude Opus ran the Codex O00 test pack (R1-R7) on the live game. Result: `build/candidates/O00_20261009/o00_runtime_selftest_20261009.json`.

- R1 boot/load, R2 visibility/material, R3 scale/orientation, R4 collision, R5 sidecar disable, R6 save/load, R7 baseline: all PASS.
- Collision measured: player blocked from back (Y -2809.09) and front (Y -2742.44), blocked span 66.7 units (bench depth plus capsule, not inflated); player can stand on the bench at ~42-46 units, not on a backrest-height box.
- Disabling the sidecar and loading a save that contains benches: clean load, benches absent, no crash.
- Not covered: impact/footstep audio, daylight look, attack/equipment-change regression, first-person.
- Everything restored afterwards: plugins.txt and FalloutPrefs.ini byte-identical to backups, original Save 22 untouched, protected hashes unchanged. Candidate files remain deployed, sidecar not enabled.
- Because the implementer ran the tests, this is recorded as an Opus self-test. Whether it unlocks O01/O08 is the project owner's decision; it is not a Codex verdict.

## 2026-10-09 O01 Tool Gun presentation - first-person DELIVERED, world model BLOCKED

Candidate: `builds/O01_toolgun_candidate_20261009.json` (freeze PASS). Static 12/12 PASS. Opus runtime self-test: `build/candidates/O01_20261009/o01_runtime_selftest_20261009.json`.

- First-person: authentic c_toolgun geometry/materials in the FNV hand, 10mm grip registration, screen facing the player, LEDs glowing from recovered masks. Re-equip, Pip-Boy, save/load PASS. Sidecar `REM_O01_ToolGun_Test.esp` overrides only STAT 01000834 and is not enabled by default.
- World/third-person: new `w_toolgun.nif` built and validated (BSFadeNode + Prn=Weapon, grip-registered, dynamic collision) and deployed under `meshes/rem/gmod/weapons/toolgun/`, but not referenced. Overriding the WEAP model path crashed the game (F018). Legacy world model still shows in third person.
- Decision needed from the owner: (a) change DLL GMod weapon identity to EDID/FormID, (b) replace the legacy loose world NIF in place, or (c) stay first-person only for now.
- Correction to earlier notes: the Tool Gun WEAP stores animation type Melee, but the DLL copies the vanilla 10mm profile at runtime (type 3), so the 10mm animation family is already in effect.
- New failure knowledge: F017 (VTFCmd alpha loss), F018 (WEAP identity by path), F019 (console input leak into the build menu).
- Restored after testing: plugins.txt, FalloutPrefs.ini, Save 22, protected and legacy hashes unchanged.

## 2026-10-09 (evening) O01 world model unblocked - DLL v86 deployed

Owner chose option (a). FNVGModTHUG2.dll v86 (787F46B0...) identifies GMod weapons by owning plugin (F018 fixed). Deployed with the v85 DLL backed up (`backups/o01_dll_identity_20261009/`); main.cpp now 98CB5DE9... (patch in `research/dll_patches/`).

- O01 sidecar now overrides both the first-person STAT and the world WEAP model. Static 12/12 PASS against the v86 baseline.
- Opus runtime self-test (`build/candidates/O01_20261009/o01_runtime_selftest_v86_20261009.json`): load PASS (identity by plugin, 14/14 GMod weapons), third-person world model PASS (same stance as vanilla 10mm), drop safe, skate enter/exit PASS, save/load PASS.
- Outstanding for a human: pickup of a dropped Tool Gun; a first-person look under v86.
- New baseline hashes: FNVGModTHUG2.dll 787F46B0DD3077909924C8948F03325959F0DC52AB019E889408F8381BB36EC6; main.cpp 98CB5DE94648A450AD97A5CB55F6D34606995B8AEAAD63A0322D4D010D820165. REM_GModTHUG2.esp and skateheldx.nif unchanged.


## 2026-10-09 Bevy successor bootstrap (preparation only)

A **new standalone Bevy/Rust edition** has been chosen for future primary development. The original Fallout/NVSE merge is retained as a separate, protected legacy edition while Bevy coexists; discontinuation of legacy is a possible later owner decision only after functional/playability parity. See D-012 and `context/HANDOFFS/OPUS_BEVY_STANDALONE_SUCCESSOR_2026-10-09.md` on `prep/bevy-opus-handoff-20261009`.

**Verified on Windows DESKTOP-6PTSS3D via Desktop Commander:** IDA Pro 6.8 exists at `C:\Program Files (x86)\IDA 6.8`; Rust official installer checksum matched the vendor's SHA256 (`6F4BEF66261261FCB43131BE8720BAB817D403A09EDEC7455C371974B90BDB7E`), Rust 1.99.0 (x86_64-pc-windows-msvc) and Cargo 1.99.0 installed. In a separate local probe at `C:\Users\BRAD\Documents\------\Engineer Station\rem1_bevy_install_probe`, `cargo add bevy` resolved Bevy 0.20.0 and `cargo check` completed with exit code 0 (2026-10-09). **This is a dependency compilation check, not a running game, renderer/window/playtest or fully integrated Bevy build.** The local probe is not a Git checkout; no Bevy game code is yet recorded as committed to REM1.

**Repository state at first inspection:** main at `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`, `implementation/opus-o00-golden-bench-20261009` ahead by 194 commits with 0 behind. O00 independent Codex runtime validation and O01 independent human/runtime acceptance are NOT established by static pass or Opus self-test. Opus branch already has conversion and v86 sidecar evidence—preserve and reuse rather than claiming it constitutes the new Bevy edition.

The Bevy migration needs its own Cargo workspace, asset pipeline, engine validation, edition-specific manifest and independent test artifacts on a new isolated engine branch. Do not modify the installed legacy DLL/ESP, original saves or protected baseline to prepare this edition.
