# Runtime integration map — GPT-6 / Opus

Verified 2026-10-06 from the actual local workspace.

## Critical source-location finding
`src/` is empty. The preserved active plugin source candidate is `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp`, SHA256 `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`. Do not implement against `src/` or infer a newer tree without first reconciling it.

## Central runtime path
`NVSEPlugin_Load` (~6967) registers the plugin. `MessageHandler` (~6761) owns lifecycle readiness. `PollControls` (~6263) is the central dispatcher and currently sequences Q/build-menu input, skate-mode ownership, equipped GMod weapon behavior, Tool Gun/Physgun input, then subsystem updates.

## Physics Gun insertion map
Primary existing paths: `GetCrosshairTarget` 868; Havok velocity helpers 905/919/934; `DropHeld` 2374; `TogglePhysgun` 2405; `GrabCrosshairRef` 4986; `ThrowHeld` 5059; `UpdateHeldObject` 5129; dispatch in `PollControls` 6263. Replace/upgrade behavior behind these boundaries rather than scattering another Physgun loop. Preserve cleanup on weapon switch. Verify native addresses with IDA Pro 6.8.

## Tool Gun / Q-menu
Tool actions converge at `ToolgunPrimaryAction` 4411 and `ToolgunSecondaryAction` 4458. Current menu path is `OpenBuildMenu` 4752 / `ToggleBuildMenu` 4810 / `UpdateBuildMenuControls` 4861 and is explicitly transitional: it is not proof of the required source-faithful GMod Q-menu. The final Q-menu bridge should own tool selection while retaining action boundaries.

## Weapon presentation
`ApplyGModWeaponAnimationProfile` 1449, `GetEquippedGModRuntimeWeapon` 1519 and `EnsureGModWeaponForms` 1526 are the key current boundaries. Runtime form creation is delayed in `PollControls`; do not undo that safety merely to simplify model integration.

## THUG2 animation/camera
Retarget path: `ResolveTHUG2RetargetBones` 476, `StartTHUG2RetargetClip` 567, `ApplyTHUG2RetargetAnimation` 595. Camera/mode: `GetThirdPersonCameraNode` 988, `ApplyTHUG2NativeCameraProfile` 1032, `EnterSkateMode` 1745, `ExitSkateMode` 1842, `UpdateSkateMode` 5462. Respect F002/F003/F005 before changing these areas.

## THUG2 props
Current spawn boundary is `SpawnConvertedProp` 4522 with pending-spawn/menu integration nearby. The 85-target queue supplies conversion evidence. Static THUG2 level geometry does not imply Physgun mobility; create dynamic wrappers only after explicit validation.

## Native address warnings
Current source contains FNV 1.4.0.525 address literals around `0x011D8A80`, `0x00C9C1D0`, and `0x011E07D4`. They are evidence-backed historical integration points, not permission to assume semantics. Reverify in IDA Pro 6.8 before relying on them.

## Change impact
Physgun changes => R_PHYSGUN + R_GMOD_WEAPONS + R_BOOT. Q-menu/Tool Gun => R_QMENU + R_GMOD_WEAPONS + R_BOOT. Weapon presentation => R_GMOD_WEAPONS + R_BOOT. THUG2 animation/camera => R_SKATE + R_BOOT. THUG2 prop conversion/spawn => R_PROPS + R_QMENU.

## Concurrency rule
Before Opus edits this source, rerun the preflight and compare the main.cpp SHA256. A changed hash means this map must be reconciled before modification (F007).

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]