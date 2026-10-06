# GMod overlay evidence package — 2026-10-06

Status: preparation/evidence for external Opus 5.5. This is not runtime implementation.

## Product interpretation
The final compiled game remains Fallout: New Vegas as the host world/runtime, but GMod systems should feel like a genuine GMod interaction layer over that world whenever they are invoked. The player should not feel that Fallout menus are imitating GMod. The GMod UI, tool state, weapon feedback and interaction conventions should temporarily own the relevant presentation/input, then yield cleanly back to Fallout.

This is an overlay architecture, not a permanent total HUD replacement: normal Fallout remains visible/interactive by default; GMod UI appears in the contexts where GMod itself would present it.

## Durable source evidence already staged
The existing readiness audit records:
- 105 relevant GMod Lua files inventoried for Q-menu/spawnmenu work.
- 40 stool/tool files inventoried.
- 46 VGUI classes inventoried.
- 29/29 directly referenced Q-menu UI/material assets resolved.
- Real gmod_tool shared.lua/stool.lua sources inventoried.
- Exact c_toolgun and w_toolgun Source model components resolved and hashed.
- Tool Gun screen/material assets, ToolTracer effect and Toolgun.Single event dependencies staged.
- w_physics world-model/collision components resolved and hashed.
- physbeam/physgun glow materials and Weapon_Physgun.On/Off/Special1 sound definitions indexed.
- installed weapon_physgun definition and GMod physgun hooks inventoried.
- 290-entry curated prop catalog prepared (170 FNV + 120 GMod/Source), with thumbnails audited.
These are evidence inputs, not proof of working runtime parity.

## Documentation gap found during this audit
context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md references:
- context/HANDOFFS/ASTRA_GMOD_QMENU.md
- context/HANDOFFS/ASTRA_TOOLGUN.md
- context/HANDOFFS/ASTRA_PHYSGUN.md
Those paths are currently absent from canonical GitHub. Do not assume their content is durable until recovered/imported or replaced by equivalent handoff documentation.

## Overlay state contract

### 1. Fallout baseline
Normal Fallout HUD, Pip-Boy, combat, inventory and world interaction remain the default. GMod systems must not permanently suppress Fallout presentation simply because GMod-derived weapons/items exist.

### 2. Q-menu overlay
Holding/pressing the configured Q-menu input should invoke the real/source-faithful GMod spawn/tool menu over the live Fallout world.
Required perceptual behavior:
- GMod menu chrome/layout/fonts/icons/materials and original menu hierarchy are presented, not Fallout-styled equivalents.
- World remains recognizably behind the menu rather than transitioning to a Fallout menu screen.
- Q-menu takes the mouse/cursor and the input required for tabs, categories, search, scrolling, icon selection and tool selection.
- Fallout gameplay inputs that would conflict with menu operation are suppressed while Q is active.
- Releasing/closing Q destroys or hides the overlay cleanly and restores Fallout input/cursor state without residual focus or stuck controls.
- Menu state that GMod preserves (selected tool/category/search where applicable) should remain consistent with source behavior.

### 3. Spawnmenu/content overlay
The original/ported GMod menu logic should consume the project's curated content adapter. Fallout/GMod/THUG2 spawnable props can therefore appear inside a GMod-native browsing experience without rewriting the menu as Fallout UI.
Each exposed entry must have validated icon/thumbnail, category, model mapping, collision/scale suitability and spawn action.
The current visually correct menu is only a placeholder and cannot satisfy this gate.

### 4. Toolgun overlay/state
Tool selection is owned by Q-menu tool state. Q -> selected stool/tool -> actual/source-faithful gmod_tool behavior is the required chain.
No Fallout top-left prompt, message box or custom selector should sit between Q and Toolgun behavior.
Toolgun screen/material, firing/tracer effect, sounds, traces and per-tool feedback should follow the preserved GMod sources.
Duplicator and Remover are minimum critical proof tools because they demonstrate persistent selected-tool state and meaningful interaction with spawned entities.

### 5. GMod notification overlay
Where GMod normally emits transient notifications/tool feedback, use the recovered GMod notification/VGUI presentation rather than Fallout top-left messages.
Notifications should stack/time/fade according to recovered GMod behavior and coexist with the Fallout world behind them.
Fallout alerts remain valid for Fallout-owned gameplay; GMod-owned actions should not masquerade as Fallout alerts.

### 6. Physgun world/UI overlay
The Physgun is primarily a world-interaction system rather than a menu, but its visual/audio feedback is part of the GMod overlay identity:
- source-faithful beam and endpoint;
- target highlight matching beam/color behavior;
- continuous held-object audio loop with correct start/stop transitions;
- acquisition/manipulation range derived from GMod/Source behavior;
- rotate/freeze/unfreeze/release/launch semantics;
- actor handling applied to the acquired actor, never PlayerCharacter by pointer confusion;
- no Fallout prompt used as a substitute for normal Physgun feedback.

### 7. Input ownership
A single explicit owner should control each conflicting input context:
- Fallout owns normal play.
- Q-menu owns menu navigation/cursor while open.
- Toolgun owns its GMod weapon actions while equipped and Q is closed.
- Physgun owns its GMod manipulation inputs while equipped and Q is closed.
Opening Pip-Boy or another hard Fallout menu must either be blocked while Q owns input or transition ownership cleanly according to a documented compatibility rule. Never allow both UI stacks to consume the same click/key simultaneously.

## Evidence Opus should recover/verify from the installed GMod source
To turn the current inventories into implementation-grade evidence, preserve file/hash/function relationships for:
1. spawnmenu creation/open/close lifecycle and its hooks;
2. content type registration and prop icon creation;
3. creation menu/tool menu population and category ordering;
4. search/filter handling and icon grid behavior;
5. VGUI/Derma panel classes actually instantiated by the menu;
6. Q bind/input path and cursor/focus ownership;
7. tool registration, stool lifecycle, selected-mode state and gmod_tool dispatch;
8. Duplicator and Remover call paths/dependencies;
9. notification creation, type/icon mapping, stacking, lifetime and fade behavior;
10. Toolgun screen/tracer/sound hooks;
11. Physgun beam/glow/audio hooks and native manipulation boundary;
12. cleanup/undo/duplicator-related UI surfaces required by the selected supported tools.
Use Lua/script evidence first. Use IDA Pro 6.8 only for native engine behavior/interfaces not sufficiently exposed by scripts.

## Acceptance tests for the GMod overlay
1. Start in ordinary Fallout: Fallout HUD/input normal.
2. Open Q: genuine GMod presentation appears over Fallout world; cursor/menu navigation works; Fallout conflicting inputs do not fire.
3. Browse curated props: categories/icons/search work without flashing/missing icons.
4. Spawn a validated prop: it appears with correct model/texture/scale/collision.
5. Select Remover in Q, close Q, fire Toolgun: selected tool persists and removes the target using GMod-derived behavior/feedback.
6. Select Duplicator, close Q, use Toolgun: state/action path works without Fallout selection prompts.
7. GMod-owned notification appears using GMod presentation, not Fallout top-left alert.
8. Equip Physgun: beam/highlight/hold loop/range/rotation/freeze/release/launch behave source-faithfully.
9. Reopen/close Q repeatedly: no flashing, focus leaks, stuck cursor, duplicated panels or input leakage.
10. Open/close Pip-Boy before and after GMod overlays: Fallout UI recovers correctly.
11. Save/load with GMod-derived inventory/state: no corruption; selected tool/state behavior follows the chosen persistence rule.
12. Exit GMod interaction: Fallout HUD/input remain unchanged unless another explicit mode such as THUG2 owns presentation.

## Non-goals
- Do not permanently reskin Fallout's entire HUD into GMod.
- Do not recreate the Q menu by visual imitation.
- Do not expose all raw asset archives merely because the menu can display them.
- Do not replace GMod notifications/tool state with Fallout message boxes.
- Do not treat the placeholder menu as implementation evidence.

## Opus ownership
All runtime implementation, UI hosting/porting, GMod code behavior, animation/model integration and cross-game asset integration described here remains exclusive to external Opus 5.5 under context/HANDOFFS/OPUS_5_5_EXCLUSIVE_INTEGRATION_2026-10-06.md. This support document exists only to reduce rediscovery and sharpen acceptance criteria.
