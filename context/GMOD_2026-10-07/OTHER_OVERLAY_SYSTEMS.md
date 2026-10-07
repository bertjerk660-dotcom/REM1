# Original GMOD transient UI, HUD and font evidence — 2026-10-07

This is source investigation, not a runtime port. Paths below are relative to the supplied `C:\Program Files (x86)\Steam\steamapps\common\GarrysMod`. Original payloads remain local. Source descriptions are authored here; the original Lua is not redistributed.

## Notifications are a separate original system

`garrysmod/lua/includes/modules/notification.lua` SHA-256 `869769B67A4C505F62BE7F7410E37E0A430A3995932FA853CCB266CB8C170690` defines the complete notice panel and movement/lifetime loop. It is not a Fallout message box and not a generic substitute toast widget.

- `AddLegacy` creates a `NoticePanel` parented to `GetOverlayPanel()` when that native helper exists. It records `SysTime`, a nonnegative lifetime, horizontal/vertical velocity and a position starting 200 pixels beyond the right edge.
- `AddProgress` keys panels by a caller-supplied UID. Updating an existing UID updates its text/progress and makes its lifetime indefinite. New progress panels have the same original panel/position contract. `Kill(uid)` transitions that panel to a 0.8 second expiry.
- The `Think` hook updates each panel using `RealFrameTime`. The stack anchor is 80% of screen height; the horizontal gap is 1.5% of screen width. Notices move toward a right-aligned position with velocity and friction. At less than 0.7 seconds remaining the target moves left by 4% of screen width; at less than 0.2 seconds it moves right by two panel widths. Expired panels are removed. This is motion followed by removal; a generic fade must not be claimed as the recovered implementation.
- `NoticePanel` derives from `DPanel`. It contains a `DLabel`, and a legacy notice adds a left-docked `DImage`. It sizes itself from native text metrics plus icon/padding/progress height. It uses the original label shadow, centered alignment and dark translucent panel background.
- Five original material identities map to generic/error/undo/hint/cleanup: `vgui/notices/generic`, `error`, `undo`, `hint`, `cleanup`. The image paint pushes anisotropic minification and magnification filters and restores them afterward.
- `GModNotify` is created from system family Arial, weight 500, extended glyph support. Text height is the larger of 12 and the ceiling of `ScreenScaleH(9)`; icon height is its 1.25 multiple. Preserve these font metrics rather than drawing Fallout text.
- Progress draws its original green bar with either the supplied fraction or an animated moving segment driven by `SysTime`. `Paint` hides notice visuals while the active weapon is `gmod_camera`.
- The module itself does not emit a generic notification sound. Call sites own sounds. Do not invent a sound for every bubble.

The compatibility boundary is a panel host, clock/frame timing, text measurement, original material lookup, texture filtering and the active-weapon identity query. A Fallout action can dispatch to the original notification API through a bridge, but must not replace its panel lifecycle.

`garrysmod/gamemodes/sandbox/gamemode/cl_notice.lua` SHA-256 `BB15A9B66EE9CB03DF07F4125FEE145F806D0951B731E7DB10E569635AC9E584` delegates `GM:AddNotify` to `notification.AddLegacy`; its `PaintNotes` method is empty. It is a compatibility call surface, not the actual painter.

## Sandbox hints

`garrysmod/gamemodes/sandbox/gamemode/cl_hints.lua` SHA-256 `D3EACF4A4AA1496C8F3A30B02809822AC67D7561F68039BFD95B9118A21DDCD5` owns `cl_showhints`, one-shot named timers and a processed-hint table. `ThrowHint` resolves `Hint_<name>` through `language.GetPhrase`, substitutes command bindings using `input.LookupBinding`, emits a hint notice for 20 seconds, then plays one of `ambient/water/drip1.wav` through `drip4.wav`.

`AddHint` schedules a hint once; `SuppressHint` removes its timer. This makes the menu's `SpawnMenuOpened`/context callbacks meaningful: they suppress introductory hints and schedule later ones. A hardcoded key name would be wrong after rebinding. The FNV adapter needs binding lookup with Source command identities, not a Fallout popup telling the player to select a tool.

## Death notices and kill icons

`garrysmod/gamemodes/base/gamemode/cl_deathnotice.lua` SHA-256 `029D702602E6D5A6D4EC2D3E550B28680B019ADB3553B56164A6E86B5626B3F1` defines the original kill feed. `hud_deathnotice_time` defaults to 6; `cl_drawhud` gates drawing. The module registers font icons and aliases, consumes several legacy net events and `DeathNoticeEvent`, resolves player/NPC names and friendliness, and dispatches `AddDeathNotice`.

Each notice retains creation `CurTime`, attacker/victim labels, icon identity, flags and team/NPC colors. Drawing obtains icon dimensions, clamps the remaining lifetime multiplied by 255 for alpha, renders the icon and names, then computes the next stacked position. Position smooths using current and previously drawn coordinates. The table is cleared when all notices have expired, preserving ordering until then. Native networking is a dependency of event delivery, not of the visible notice formatting itself.

`garrysmod/lua/includes/modules/killicon.lua` SHA-256 `946C83AAF9DB57A3374D0203C972DC79515137E066B1CD7895C29DF739020234` is its original registry/renderer. It supports font glyphs, materials, texture-coordinate regions and aliases; caches measured dimensions; and applies original legacy height corrections. Unknown icons resolve to `HUD/killicons/default`. Do not replace the weapon glyph font with hand-drawn lookalikes.

`garrysmod/gamemodes/base/gamemode/cl_init.lua` includes this death-notice module. Its `HUDPaint` calls target-ID, pickup-history and `DrawDeathNotice(0.85,0.04)` hooks. Its `HUDShouldDraw` first delegates to the active weapon's `HUDShouldDraw` method when present. Therefore the camera/tool weapon can control relevant original HUD elements through the weapon interface.

FNV death/reference events require explicit translation of actor/ref identity, display name, source weapon class/icon and friendliness to this event record. Fallout remains the host and normal HUD owner. Whether every ordinary Fallout kill should enter the GMOD feed is a product/integration policy still unresolved; this investigation does not enable that behavior.

## Fonts and crosshair resources

The installed `garrysmod/resource/ClientScheme.res`, SHA-256 `AA083DCFFB5E5A2A75CB7F4EB6FDE741243C2DBB485484FF5DD662F149B90564`, defines Source scheme fonts and `CustomFontFiles`. `HL2MPTypeDeath` starts at line 639, `ChatFont` at 652 and custom font file registrations at 808–812.

| Identity | Original family/resource | Dependency class |
| --- | --- | --- |
| GModNotify | Arial, created by notification Lua | font + engine text metrics |
| ChatFont | Verdana, resolution-dependent heights in ClientScheme | configuration + system font |
| HL2MPTypeDeath | HL2MP, tall 64, additive/antialiased | font + surface renderer |
| Crosshairs | HalfLife2 glyph font, tall 40 | font + native HUD draw path |
| CustomFontFiles | resource/HALFLIFE2.ttf, resource/HL2MP.ttf, resource/HL2crosshairs.ttf | original font assets |

The existence of `gui/crosshair.png` in earlier asset inventories does not prove every weapon uses that PNG. The original native crosshair scheme and scripted Tool Gun HUD are distinct paths. Native weapon HUD/crosshair dispatch still needs narrow IDA 6.8 evidence before reproducing an exact Physgun crosshair.

These original font resources must be staged from the supplied install/package and attributed to their actual owner. System fonts should be represented as host requirements; this session does not copy Windows system font files into GitHub or invent substitute font assets.

## Boundaries and unresolved evidence

| System | Original responsibility | Thin bridge responsibility | Evidence status |
| --- | --- | --- | --- |
| Notification | panel registry, UID progress state, text/icon layout, motion/expiry | VGUI panel host, clocks, material/text backend | Lua traced; stage manifest verifies files |
| Hints | timers, language lookup, source bind substitution, original sound choice | bind lookup and original sound playback | Lua traced; source sound payload resolution recorded by staging |
| Death feed | net-event decoding, labels/colors/icons, lifetime/stacking | host death/ref event translation | Lua traced; event integration absent |
| Kill icons | glyph/material/UV registry, cached sizing and corrections | exact fonts/materials and draw calls | Lua and scheme traced |
| Weapon HUD gates | active weapon callback dispatch | host HUD element names/ownership policy | Lua traced; native HUD dispatch unresolved |
| Cursor/focus | original spawn/context panel lifecycle | one input owner and native cursor/focus services | detailed in QMENU_ARCHITECTURE.md |

`GetOverlayPanel`, `surface` font/draw APIs, material loading, clocks, native HUD panels and the Lua/native engine interface are not recovered implementations merely because their names appear in Lua. The native report records which portions actually have IDA evidence. Executing these scripts inside FNV still requires a compatible GMOD Lua environment, metatables/global helpers, VGUI primitives and host services; staging alone does not provide those services.

The original files and source-backed dependency edges are indexed in `manifests/gmod_2026-10-07`; content stays in Windows local staging. No runtime HUD, input binding, weapon, ESP, DLL or THUG2 subsystem was changed by this evidence work.
