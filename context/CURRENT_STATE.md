# Current Verified State

Verified 2026-10-05 from the actual local workspace, deployed-file records, build manifests and crash logs.

## Local workspace
Path: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
The workspace contains the NVSE plugin source, research/conversion/patch tooling, build outputs, backups, context documents and third-party tooling.

## Active runtime
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

## Goodsprings Deathclaw Response support candidate — 2026-10-07
A separate support encounter is staged and deployed without modifying the protected Astra runtime lane.

Verified deployed artifacts:
- `Data\REM_Goodsprings_CombineDeathclawEncounter.esp` SHA256 `B37B2087B75701AFAAE64FEA62B580774B99965A8B4C37CED32E4161FECB590F`
- `Data\NVSE\Plugins\REMGoodspringsResponse.dll` SHA256 `2FCEAC8BB4B3AD11B774F9B9B0D9F97A08E9D9372205C9A7E4E34F2BF4F0F13F`, Win32/x86
- `Data\Sound\fx\rem\goodsprings\captain_claw_thanks.wav` SHA256 `F0C6A0DAE22B6122DAC741E14CC3A8F255F50BC13A1A7B860AA42C8B4B74F62C`

Encounter facts:
- Combine Solider: 100,000 HP, speed 200, Frenzied/Foolhardy, Minigun, 10,000,000 5mm, current torso-lowered Combine armor.
- Ten `DEATHCLAW RESPONSE UNIT` actors are Unaggressive/factionless/package-free at base and the support DLL explicitly targets only the Combine guard while he is alive.
- Captain Claw local ref `080E` starts disabled and has Bethesda `RunToPlayerForever [000CAFC6]` persistently authored on his creature base.
- On guard defeat Captain is enabled + EVP, then naturally pathfinds to the player. No MoveTo/teleport command exists.
- At <=275 units one TTS-backed message-box prompt fires and grants one vanilla Deathclaw Egg `000E6627`.
- `REMCaptainClawRewarded` local global `080F` provides one-time save/load reward state.

Validation:
- ESP recursive binary validation: PASS.
- Support DLL build: PASS, 0 errors.
- xNVSE 6.4.9 runtime main-menu smoke test: PASS; loader logged `REMGoodspringsResponse` v2 loaded correctly alongside `FNVGModTHUG2`.
- Actual Goodsprings encounter/playability test: PENDING human observation.

See `context/HANDOFFS/GOODSPRINGS_DEATHCLAW_RESPONSE_2026-10-07.md` and `build/goodsprings_response/manifest_v2.json`.
