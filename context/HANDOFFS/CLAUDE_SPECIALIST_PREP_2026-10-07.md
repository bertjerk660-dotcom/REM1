# Claude Specialist Preparation — 2026-10-07

Status: preparation notes only. This file adds no runtime, source, asset or build change. It records what was checked on 2026-10-07 and how the Claude lane should trace and merge code, scripts and UI from Fallout: New Vegas, Garry's Mod and THUG2 once implementation instructions arrive.

Evidence grades used below: H = hash re-verified on the local machine; S = read from repository text; I = IDA 6.8 build-specific evidence per the repository; R = human runtime playtest; U = unverified or unresolved. Nothing graded S, I or U is treated as runtime proof.

## 1. Verified local state (2026-10-07, DESKTOP-6PTSS3D)

- Clone: C:\Users\BRAD\REM1, a Git checkout of bertjerk660-dotcom/REM1 (H).
- main: 19a8046. prep/opus-ready-20261007: 14aee9a, 151 commits ahead of main (H).
- Plugin source main.cpp SHA-256 4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE matches the runtime snapshot (H).
- gmod_overlay.inc SHA-256 E6EF0C484AFDDC1A74C02F6BA8A72CD0899D6E80F5BA5459CD61B9C67183250F matches (H).
- Deployed Data\NVSE\Plugins\FNVGModTHUG2.dll SHA-256 D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206 matches (H).
- Deployed Data\REM_GModTHUG2.esp SHA-256 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7 matches (H).
- Garry's Mod garrysmod.ver reports 260917 / 1920 / prerelease, matching the recorded install (H).
- Installed under Steam common: Fallout New Vegas, Garry's Mod, Fallout 3 GOTY, Fallout 4 (H).
- THUG2 was not found in the default Steam or Program Files locations (U). Its install or extracted-data path is an open item for the owner.
- The Windows project folder FNV_GMOD_THUG2 is not a Git checkout, as the repository states (H).
- Source label is version 85 (S). Older CURRENT_STATE text says the DLL is version 81. Both are recorded in the repository and the hash is the binding identity.

## 2. Project state the Claude lane must respect

- Preparation readiness for Opus is 81/100. The remaining 19 points are Codex evidence gates C01 to C08 (S, OPUS_READINESS_81_TO_100_PLAN).
- Next implementable package: O00 Golden Source Bench, an isolated sidecar proving Source to Fallout model, material and collision conversion on bench01a. O01 Toolgun, O08a/b/c weapon presentation wait for O00 PASS (S).
- Verified positives (R, 2026-10-06): held skateboard presentation and placement; left-click enters skate mode; holster key exits; THUG2 sounds appear to work in the tested path, not yet exhaustively validated.
- Verified failures (R): board does not move from hand to feet; THUG2 animation set not functioning; G can start a grind anywhere; Fallout HUD and top-left alerts still show in skate mode; Physics Gun short acquisition range, wrong held-beam audio, and unconscious effect applied to the player instead of the acquired target; the GMod-style prop menu is a placeholder and not the Q menu.
- Ownership (S, AGENT_OWNERSHIP.md): Claude Opus is the sole implementation and integration agent. Codex owns investigation, reverse engineering and runtime validation. Normal GPT coordinates. GPT-6/Astra is not used.

## 3. Open question on role

The request asks the Claude lane to prepare for implementation tomorrow. The repository assigns implementation to Claude Opus, and runtime validation to Codex. This preparation covers the Opus lane's evidence intake and tracing. Before any runtime or source change, the owner should confirm which lane this session takes tomorrow.

## 4. How to trace a subsystem (method)

For each behavior, trace in this order and record the grade of every claim:

1. Entry point. What triggers it: a key poll, a Lua hook, a concommand or bind, a weapon event, a state transition. Fallout: PollControls and GetAsyncKeyState in main.cpp. GMod: hooks, concommands, spawnmenu panels, SWEP and stool callbacks, and native Physgun. THUG2: the skate controller and state machine, which C04 has not yet documented.
2. Input ownership. Which mode owns the input (INPUT_OWNERSHIP_MATRIX: NORMAL_FALLOUT, GMOD_MENU, GMOD_TOOL_ACTIVE, THUG2_SKATE_MODE, THUG2_WALK_MODE).
3. State machine. States, transitions, guards, timers and cleanup. Record every transition, not only the happy path.
4. Data. Models, animations, materials, sounds and fonts with source path, archive, size and SHA-256. Proprietary payloads stay local; GitHub holds metadata only.
5. Host boundary. Where each original API call lands in the Fallout runtime, with the adapter contract and its invariants.
6. Presentation. Draw, audio and UI calls, render order, and restoration of Fallout state on exit.
7. Lifecycle. Load, save, cell change, death, weapon switch, menu close, and mode exit.
8. Evidence grade. Static (S), hash (H), IDA (I), runtime (R) or unresolved (U).

## 5. Per-game notes from the repository

Garry's Mod (Source / GLua)
- Q-menu is a persistent Derma/VGUI panel hierarchy in garrysmod/gamemodes/sandbox and related Lua. Loading icons into the existing C++ menu does not reproduce it (S).
- Tool Gun: the original chain is Q, then gmod_toolmode, then the selected stool's LeftClick, RightClick and Reload. Click selects; the current C++ path arms on hover (S).
- Physics Gun: the Lua side passes DrawPhysgunBeam and halo data, but the beam endpoint and grab controller are native and need IDA (I, S).
- Archives: VPK and GMAD content must be extracted with CRC checks. Mount precedence is not established offline (S, U).
- First-person Physgun model v_physics.mdl, .vvd and .dx90.vtx is unresolved. Do not invent a replacement (U).

Fallout: New Vegas (NVSE, Gamebryo, Havok)
- Plugin main.cpp is roughly 7,000 lines plus gmod_overlay.inc (H, S).
- Skateboard identity comes from an ESP-owned persistent WEAP. Do not clone serialized runtime forms during load (F001).
- Use TESObjectREFR::GetNiNode() and defer animation binding until a 3D root exists (F002).
- Retarget bone pointers must be RTTI-validated and discarded when the root changes (F003).
- Physics Gun acquisition currently uses InterfaceManager::crosshairRef, which likely explains the short range. Confirm with a measurement before changing it (S, U).
- The GMod actor command pushactoraway runs with the player as its argument. This is the leading candidate for the knockdown bug. Confirm in an isolated test before swapping arguments (S, U).

THUG2
- Decompiled Q-source set of 17 files and 20 parsed board SKA animations are staged (S, per the repository).
- HUD and input evidence indexes 49 files with no missing sources (S).
- Core state, physics, camera, animation and HUD evidence is pending in Codex packets C04 to C08 (S).
- Do not import THUG2 maps, missions, NPCs, dialogue or cutscenes (S, GOAL.md).

## 6. Merge pipeline the repository requires

Source identified and hashed, then extracted with provenance, then converted into isolated candidate paths (meshes/rem/..., textures/rem/...), then adapter contract, then Opus implementation in a sidecar or isolated branch, then candidate freeze (validate_opus_candidate_manifest.py --mode freeze), then Codex runtime validation, then failure report to Opus if needed, then update of FAILURE_KNOWLEDGE and CURRENT_STATE.

Gate order: O00 golden bench first. Weapon conversion waits for O00 PASS and human acceptance (S).

## 7. Known traps to avoid

- Do not present the placeholder prop menu as the Q menu (F012).
- Do not run research/patch_v74_advdupe_physgun.py. It is marked known-bad (S).
- Do not select tools through Fallout top-left prompts or popups (D-007, D-008).
- Current mapping: LMB grab or interact, RMB launch or release. The older RMB-grab/LMB-launch handoffs are historical (S, CURRENT_STATE 2026-10-07).
- Do not let the acquired actor and PlayerCharacter share one reference (F009).
- Do not treat successful mode switching as successful THUG2 integration (F011).
- Grind entry requires THUG2 eligibility (F010).
- Do not copy the older CE3628 integration-map hash as current. The supplied source changed (S).
- Build JSON under build/ carries an appended "[executed on device ...]" footer and is not strict JSON. New manifests must be strict JSON and must not be edited in place (S).
- Never commit proprietary game binaries or assets. Commit tooling, manifests, hashes and reports (AGENTS.md, ASSET_POLICY.md).
- Do not write to GPT-6/Astra. Historical ASTRA_* and gpt6_opus paths are path labels only (LEGACY_ROLE_PATH_MAP.md).

## 8. Expected instruction format for tomorrow

For each task the owner should give:
- the goal and the subsystem (GMod Q, Toolgun, Physgun, THUG2 state, camera, animation, HUD, input, or O00 bench);
- the gate it should satisfy;
- allowed write paths and branch name;
- whether it is investigation, implementation or validation;
- any local paths that must be checked before use.

The Claude lane will then re-verify the hashes above, read the matching handoff, trace the entry point and state machine, state which claims are graded U, and report back before any file change.

## 9. Open items for the owner

1. Location of the THUG2 install or extracted data on this PC.
2. Confirmation of tomorrow's lane (implementation, investigation or coordination).
3. Whether this preparation branch should stay separate or merge after review.
4. Whether to continue tracking readiness in GitHub issue #5.