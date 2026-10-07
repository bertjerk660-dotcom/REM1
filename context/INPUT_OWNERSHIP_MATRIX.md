# Unified Input Ownership Matrix — 2026-10-07

Purpose: define who owns each input context before Opus implementation and Astra runtime validation. This is a coordination specification, not proof of implementation.

## Modes

### NORMAL_FALLOUT
Owner: Fallout / xNVSE host.

Expected:
- Fallout movement, combat, camera, Pip-Boy and HUD behave normally.
- GMod Q input may request entry to GMOD_MENU.
- Equipping the skateboard alone does **not** transfer gameplay ownership to THUG2.
- Skateboard activation input requests THUG2_SKATE_MODE only when the skateboard weapon is the active gateway item.

### GMOD_MENU
Owner: real/ported GMod Q-menu UI.

Expected:
- Q-menu owns cursor, click, scroll, text entry, category/tool selection and menu navigation.
- Conflicting Fallout attack/use inputs are suppressed while Q is open.
- Fallout camera/world remains visually present unless the real menu behavior requires otherwise.
- Closing Q restores Fallout cursor/input state cleanly.
- Tool selection persists according to original GMod behavior and becomes the active Toolgun mode.

### GMOD_TOOL_ACTIVE
Owner: selected GMod weapon/tool while Q is closed.

Expected:
- Toolgun actions route through selected GMod stool/tool state.
- Physgun actions route through source-faithful Physgun semantics.
- Fallout must not also consume the same clicks/keys for conflicting actions.
- Opening Q transfers input ownership to GMOD_MENU; closing returns ownership here.
- Opening hard Fallout menus requires an explicit compatibility rule.

### THUG2_SKATE_MODE
Owner: THUG2-derived free-roam controller/state system.

Expected:
- THUG2 owns movement, turning, crouch/ollie, tricks, grind/manual/lip/wall actions, camera-control semantics, board state and skating HUD interactions.
- Fallout combat/movement inputs that conflict with skating are suppressed.
- Protected exit/holster control remains available.
- Fallout HUD is suppressed; THUG2 HUD owns skating feedback.
- Pip-Boy/pause/console behavior must be explicitly defined so both stacks never consume input simultaneously.

### THUG2_WALK_MODE
Owner: THUG2 walking/free-roam state if Codex evidence confirms this state is required by the selected runtime.

Expected:
- THUG2 walking controls/state own movement while THUG2 mode remains active.
- Board carry/pickup/mount transitions remain within the THUG2 gameplay layer.
- Exiting THUG2 returns control to NORMAL_FALLOUT.

## Required control families to map

| Control family | NORMAL_FALLOUT | GMOD_MENU | GMOD_TOOL_ACTIVE | THUG2_SKATE_MODE | THUG2_WALK_MODE |
|---|---|---|---|---|---|
| movement axes | Fallout | suppressed/menu-safe | Fallout unless weapon semantics override | THUG2 | THUG2 |
| mouse look / right stick | Fallout camera | cursor/menu or source Q semantics | Fallout aim / weapon-specific | THUG2 camera | THUG2 camera |
| primary attack | Fallout attack | menu click if applicable | Toolgun/Physgun action | THUG2 action/activation semantics | THUG2 action |
| secondary attack | Fallout secondary | menu action if applicable | Toolgun/Physgun action | THUG2 action | THUG2 action |
| use/interact | Fallout | blocked or menu-safe by compatibility rule | Fallout unless conflicting | THUG2-mapped only if source behavior requires | THUG2 |
| Q menu | enter GMOD_MENU | menu lifecycle | enter GMOD_MENU | blocked unless explicit cross-mode rule | blocked unless explicit cross-mode rule |
| Pip-Boy | Fallout | explicit compatibility rule | explicit compatibility rule | explicit compatibility rule | explicit compatibility rule |
| pause | Fallout | explicit compatibility rule | Fallout | explicit compatibility rule | explicit compatibility rule |
| skate activation | only with skateboard equipped | blocked | blocked unless explicitly allowed | already active | mount/return-to-skate if source behavior says so |
| skate exit/holster | n/a | n/a | n/a | protected transition to Fallout | protected transition to Fallout |
| trick buttons | Fallout/no THUG2 ownership | n/a | n/a | THUG2 | THUG2 where applicable |
| grind/manual/lip | Fallout/no THUG2 ownership | n/a | n/a | THUG2 eligibility-gated | THUG2 where applicable |
| controller mode switch | host setting | preserve setting | preserve setting | route to equivalent THUG2 actions | route to equivalent THUG2 actions |

## Conflict rules

1. One mode owns each conflicting input at a time.
2. Do not let Fallout attack/use fire underneath Q-menu clicks.
3. Do not let Fallout movement/combat continue underneath THUG2 skate input.
4. Do not let Q-menu and Pip-Boy both own cursor/focus.
5. Toolgun selected mode comes from the real Q-menu tool state, never a Fallout selector.
6. Skate-mode grind/trick actions must pass THUG2 state/geometry eligibility, never key-only activation.
7. Xbox and keyboard/mouse must map to the same gameplay actions/state semantics, not separate approximations.

## Evidence needed before Opus implementation

- Codex C01: Q-menu bind/focus/cursor lifecycle.
- Codex C02: Toolgun action/mode dispatch.
- Codex C03: Physgun exact control semantics where unresolved.
- Codex C04/C08: THUG2 controller/state action mapping.
- Any host menu conflicts that require xNVSE/Fallout compatibility handling.

## Astra validation requirements

Astra must validate transitions between every adjacent mode that is actually implemented:
- NORMAL_FALLOUT -> GMOD_MENU -> NORMAL_FALLOUT
- NORMAL_FALLOUT -> GMOD_TOOL_ACTIVE -> GMOD_MENU -> GMOD_TOOL_ACTIVE
- NORMAL_FALLOUT -> THUG2_SKATE_MODE -> NORMAL_FALLOUT
- THUG2_SKATE_MODE <-> THUG2_WALK_MODE if present

Each test must verify no stuck cursor, no double-consumed input, no hidden residual mode, and correct HUD/camera restoration.
