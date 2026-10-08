# Garry's Mod UI and Physics Gun: specialist host-adapter research, 2026-10-08

**Status:** documentation-only, partial native closure; no engine, DLL, ESP, models, or game runtime changed. **Source authorities:** original installed Garry's Mod Lua at `C:\Program Files (x86)\Steam\steamapps\common\GarrysMod`, existing `context/GMOD_2026-10-07/*` and `manifests/gmod_2026-10-07/*`. Original Lua and proprietary binaries are NOT stored here. This is not a declaration that C01/C02/C03 have passed.

## What was directly re-read today (source-grounded)

1. `garrysmod/gamemodes/sandbox/gamemode/shared.lua`:
   - `GM:PhysgunPickup` checks persistence first, defers to the entity's own `PhysgunPickup` override, then checks `PhysgunDisabled` and excludes class `player`. With `physgun_limited` enabled (the installed convar defaults to `0`), dynamic props/doors, mapper motion-disabled or prevent-pickup flags, and most `func_` entities are restricted; `func_physbox` is handled separately.
   - `GM:EntityKeyValue` sets `PhysgunDisabled` from `gmod_allowphysgun=0`; `gmod_allowtools` populates a *different* allowed-tool list. Never conflate Physics Gun eligibility with Tool Gun permission.
   - `GM:CanTool` permits entity-specific tool policy and an allowed-mode list. These are *source eligibility* rules and do not alone authorize grabbing FNV actors.
2. `garrysmod/gamemodes/sandbox/gamemode/init.lua`:
   - `GM:OnPhysgunFreeze` delegates to `BaseClass.OnPhysgunFreeze` after persistence validation, then schedules an unfreeze hint after 0.3 s and suppresses the freeze hint. This does **not** disclose the actual native/base physical-body freeze operation.
   - `GM:OnPhysgunReload` calls `ply:PhysgunUnfreeze()`, sends the client callback `GAMEMODE:UnfrozeObjects(count)` for a positive count, then suppresses the hint. `GM:CreateEntityRagdoll` replaces old entity identity in undo and cleanup. Preserve entity-lifetime changes in the FNV adapter.
   - `GM:ShowHelp` dispatches `StartSearch`, linking user help and search UI.
3. `garrysmod/gamemodes/sandbox/gamemode/cl_init.lua`:
   - The original UI includes `cl_spawnmenu.lua`, `cl_notice.lua`, `cl_hints.lua`, `cl_worldtips.lua`, `cl_search_models.lua`, and `gui/IconEditor.lua`.
   - `GM:OnUndo` uses `NOTIFY_UNDO`, duration 2 s and `buttons/button15.wav`; `GM:OnCleanup` uses `NOTIFY_CLEANUP`, 5 s and the same sound; `GM:UnfrozeObjects` uses `NOTIFY_GENERIC`, 3 s and `npc/roller/mine/rmine_chirp_answer1.wav`. These exact callback types/timers are separate from the continuous held-beam sound.
   - `GM:DrawPhysgunBeam` queues a valid acquired target for halo drawing while `physgun_halo` is enabled; it returns true, leaving the underlying original beam drawing active. `PreDrawHalos` consumes its queue; the existing native report details source-derived weapon-color variation, passes and occlusion. **A Lua halo callback is not native beam-renderer proof**.
4. `garrysmod/lua/includes/modules/spawnmenu.lua`:
   - The original module wraps an existing engine `spawnmenu` table, maintaining tool menus, creation tabs, selected control panel, custom/engine prop tables. `ActivateTool` resolves `ItemName`, optionally runs the item's console command, lazily fills its control panel and switches the tool panel. Therefore clicking a tool must propagate a stable original tool identifier, not a hover-derived numeric index.
   - `PopulateFromEngineTextFiles` clears its existing prop table and delegates reading to native `spawnmenu_engine.PopulateFromTextFiles`. This is a concrete safeguard against repeated tree duplication on reload and establishes a separate native path/precedence gap.

## Existing evidence retained, not rediscovered

- `context/GMOD_2026-10-07/QMENU_ARCHITECTURE.md` establishes `+menu/-menu` press/release dispatch, the persistent CreationMenu/ToolMenu/ContentSidebar/ContentContainer hierarchy, held-open text focus, click-to-`gm_spawn`, search and SpawnIcon/ModelImage dependencies. Q toggle and FNV polling alone are **not** equivalent.
- `context/GMOD_2026-10-07/PHYSGUN_ARCHITECTURE.md` and `IDA68_NATIVE_REPORT.md` establish a build-identified, but incompletely traced, native `CWeaponPhysGun` class/controller/beam network-state investigation. Do not mistake `weapon_physcannon`, `OnPhysGunPunt` strings or convar defaults for the registered Physgun's final input/callflow.
- The latest recorded human playtest identifies three *symptoms*, not proven root causes: too-short acquisition range; wrong held sound; target-actor unconscious effect applied to player. The current model view-asset provenance is also incomplete.
- Project input requirement of **LMB grab/interact and RMB desired launch/release** is an explicit FNV adaptation; record original Source semantics separately from it.

## Minimal bridge contract for Opus

**UI (C01/O02):**
- Source command identity -> source-compatible menu open/close event -> persistent panel state; preserve held-key release, optional toggle, HangOpen text-entry focus, real cursor restoration and panel visibility independent of callback names.
- VGUI/Derma-compatible panel hierarchy and event dispatch; keyboard input to text boxes, mouse hit tests, GUI/world input isolation, draw state restoration. Avoid an independently hand-built lookalike as proof of the real Q menu.
- Original CreationMenu + ToolMenu content providers, original tool click dispatch and string mode, `gm_spawn` host translation after catalogue authorization, server-style ownership, undo/cleanup.
- Original search Enter/click behavior, deferred update/rebuild semantics and caching; do not recreate the spawnlist tree every frame/open. Native `SpawnIcon/ModelImage` preview/cache and mounted-path semantics must be either proven or explicitly adapted.
- Tooltip, undo/cleanup notifications and sound events map to original time/priority/stacking rules, not Fallout top-left messages.
  
**Physics Gun (C03/O04):**
- A typed acquire result containing immutable **target reference identity**, current lifetime/generation, physical body/bone, trace origin/mask/limit, hit point/normal and local-space hit anchor. Reject player self-target and forbidden targets before entering held state; invalidate across cell/load/delete.
- Separate IDLE -> ACQUIRE -> HELD -> RELEASE/FREEZE/LAUNCH -> CLEANUP transitions, with native-vtable/IDA-derived ordering required before claiming parity. Map held-point controller to FNV Havok with measured damping/offset/rotation and explicit detach; do not teleport the latest crosshair reference.
- Treat normal release, freeze, reload-unfreeze and *requested* RMB launch as distinguishable actions. Keep source-original behavior and host adaptation in separate columns of the eventual validation matrix.
- Beam endpoint must bind to the acquired local grab point. Halo requires the recorded original callback/color/occlusion and is separate from native beam geometry. Start/hold-loop/stop audio should transition once per state change, not restart every render tick.
- Per-frame action must be guarded by weapon-equip state, menu focus and valid player/world state; teardown on unequip, reload, cell/load transition, invalid/deleted target, death, or partial initialization failure. Never apply actor-state changes to `PlayerCharacter` when targeting another actor.
- Preserve authentic mounted MDL/VVD/VTX/PHY, VMT/VTF materials, animation and event provenance, with the unresolved `v_physics` first-person identity **blocking a definitive model-selection claim**.

## Next Codex evidence requirements (do not mark closed from this document)

**C01**: recover exact native `+menu/-menu` registration -> Lua hook dispatch; ModelImage render/cache; engine spawnlist precedence; search.GetResults backing implementation; IconEditor, Derma/native focus and property dependencies. Return function offsets/addresses and independent evidence, or an explicitly scoped unsupported boundary.

**C02**: resolve ToolTracer, RenderScreen/RT update, Toolgun.Single original event payload/dispatch, `util.GetPlayerTrace` native semantics, prediction/realm double-mutation guards, and Remover/Duplicator constraint subset.

**C03**: connect registered `CWeaponPhysGun` input-vtable callers -> acquisition range/mask/filter -> local held point/controller simulation -> freeze/drop/punt and cleanup; native client beam/halo callsite and original sound start/loop/stop; runtime first-person model. Inspect FNV `main.cpp` and `gmod_overlay.inc` against each recovered rule and test acquired actor vs PlayerCharacter identity.

## Acceptance checks before Opus can call functionality complete

1. Original Q press/hold/release and optional toggle; repeated open/close without flashing/rebuilding; cursor restored, search text focus survives release, Pip-Boy/combat input blocked only while Q owns focus.
2. Real tabs/icons/search/preview and selected Tool Gun mode survive menu exit; original click-to-select; one authorized prop spawn and exact undo/cleanup chain.
3. Physgun valid prop acquire from source-evidenced distance; stable hold/rotate/adjust/freeze/unfreeze/drop/launch; no acquire of player; original beam endpoint, tint/halo, sounds and model attachments verified.
4. Manipulated FNV actor, nonphysics actor, unloaded target, weapon switch, save/load and cell change never confuse acquired identity; clean teardown and no player unconscious side effect.
5. Regression: normal Fallout movement/combat, Pip-Boy, saves, THUG2 held-board/enter-exit remain intact.
6. Record source hashes, Code/IDA evidence pointers, bridge/Opus commit, compiled DLL+ESP SHA-256 and per-gate live test logs. **This document passes no gameplay gate**.

## Provenance and ownership

Observed by connected Remote Desktop Commander on 2026-10-08 using the user's installed Lua, compared to prior canonical evidence. No new IDA execution or runtime test occurred. Local project workspace is **not a Git checkout**; GitHub writing is performed through the connected GitHub integration. Codex owns deep native tracing and runtime verification; Opus owns implementation; normal GPT owns evidence indexing and coordination. Do not import proprietary source scripts/binaries into public GitHub.
