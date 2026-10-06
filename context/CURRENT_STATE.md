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
