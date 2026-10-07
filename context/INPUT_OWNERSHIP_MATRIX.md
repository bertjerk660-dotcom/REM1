# Unified Input Ownership Matrix — 2026-10-07

Purpose: define input ownership before Opus implementation and Codex runtime validation. This is a coordination specification, not proof of implementation.

## Modes

### NORMAL_FALLOUT
Owner: Fallout / xNVSE host.

Expected:
- Fallout movement, combat, camera, Pip-Boy and HUD behave normally.
- GMod Q input may request entry to GMOD_MENU.
- Equipping the skateboard alone does not transfer gameplay ownership to THUG2.
- Skateboard activation requests THUG2_SKATE_MODE only when the skateboard weapon is the active gateway item.

### GMOD_MENU
Owner: real/ported GMod Q-menu UI.

Expected:
- Q-menu owns cursor, click, scroll, text entry, category/tool selection and menu navigation.
- Conflicting Fallout attack/use inputs are suppressed while Q is open.
- Fallout world remains behind the menu.
- Closing Q restores Fallout cursor/input state cleanly.
- Tool selection persists according to original GMod behavior.

### GMOD_TOOL_ACTIVE
Owner: selected GMod weapon/tool while Q is closed.

Expected:
- Toolgun actions route through selected GMod stool/tool state.
- Physgun actions route through source-faithful Physgun semantics.
- Fallout must not also consume conflicting clicks/keys.
- Opening Q transfers input ownership to GMOD_MENU.

### THUG2_SKATE_MODE
Owner: THUG2-derived free-roam controller/state system.

Expected:
- THUG2 owns movement, turning, crouch/ollie, tricks, grind/manual/lip/wall actions, camera semantics, board state and skating HUD interactions.
- Conflicting Fallout movement/combat is suppressed.
- Protected exit/holster control remains available.
- Fallout HUD is suppressed; THUG2 HUD owns skating feedback.
- Pip-Boy/pause/console require explicit compatibility rules.

### THUG2_WALK_MODE
Owner: THUG2 walking/free-roam state if Codex evidence confirms it is required.

Expected:
- THUG2 walking controls/state own movement while THUG2 mode remains active.
- Board carry/pickup/mount transitions remain inside the THUG2 layer.
- Exiting THUG2 returns control to NORMAL_FALLOUT.

## Required control families to map

| Control family | NORMAL_FALLOUT | GMOD_MENU | GMOD_TOOL_ACTIVE | THUG2_SKATE_MODE | THUG2_WALK_MODE |
|---|---|---|---|---|---|
| movement axes | Fallout | suppressed/menu-safe | Fallout unless weapon semantics override | THUG2 | THUG2 |
| mouse look / right stick | Fallout camera | cursor/menu or source Q semantics | Fallout aim / weapon-specific | THUG2 camera | THUG2 camera |
| primary attack | Fallout attack | menu click if applicable | Toolgun/Physgun action | THUG2 action/activation semantics | THUG2 action |
| secondary attack | Fallout secondary | menu action if applicable | Toolgun/Physgun action | THUG2 action | THUG2 action |
| use/interact | Fallout | blocked or menu-safe | Fallout unless conflicting | source-mapped THUG2 only | THUG2 |
| Q menu | enter GMOD_MENU | menu lifecycle | enter GMOD_MENU | blocked unless explicit rule | blocked unless explicit rule |
| Pip-Boy | Fallout | explicit compatibility rule | explicit compatibility rule | explicit compatibility rule | explicit compatibility rule |
| pause | Fallout | explicit compatibility rule | Fallout | explicit compatibility rule | explicit compatibility rule |
| skate activation | skateboard gateway only | blocked | blocked unless explicit rule | already active | mount/return-to-skate if source behavior says so |
| skate exit/holster | n/a | n/a | n/a | protected transition to Fallout | protected transition to Fallout |
| trick buttons | Fallout/no THUG2 ownership | n/a | n/a | THUG2 | THUG2 where applicable |
| grind/manual/lip | Fallout/no THUG2 ownership | n/a | n/a | THUG2 eligibility-gated | THUG2 where applicable |
| controller profile | host setting | preserve | preserve | equivalent THUG2 actions | equivalent THUG2 actions |

## Conflict rules

1. One mode owns each conflicting input at a time.
2. Fallout attack/use must not fire underneath Q-menu clicks.
3. Fallout movement/combat must not continue underneath THUG2 skating.
4. Q-menu and Pip-Boy must never simultaneously own cursor/focus.
5. Toolgun selected mode comes from real Q-menu state, never a Fallout selector.
6. Grind/trick actions must pass THUG2 state/geometry eligibility.
7. Xbox and keyboard/mouse must map to the same gameplay actions/state semantics.

## Evidence needed before Opus implementation

- Codex C01: Q-menu bind/focus/cursor lifecycle.
- Codex C02: Toolgun action/mode dispatch.
- Codex C03: Physgun exact control semantics where unresolved.
- Codex C04/C08: THUG2 controller/state action mapping.
- Host-menu conflicts requiring Fallout/xNVSE compatibility handling.

## Codex runtime validation requirements

Codex validates every implemented adjacent transition:
- NORMAL_FALLOUT -> GMOD_MENU -> NORMAL_FALLOUT
- NORMAL_FALLOUT -> GMOD_TOOL_ACTIVE -> GMOD_MENU -> GMOD_TOOL_ACTIVE
- NORMAL_FALLOUT -> THUG2_SKATE_MODE -> NORMAL_FALLOUT
- THUG2_SKATE_MODE <-> THUG2_WALK_MODE if present

Each test verifies no stuck cursor, no double-consumed input, no hidden residual mode and correct HUD/camera restoration.
