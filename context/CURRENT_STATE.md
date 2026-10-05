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
