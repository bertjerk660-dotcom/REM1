# Opus packet — unified input layer

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C01/C02/C03/C04/C08.**

Implement one explicit mode-owned action layer for NORMAL_FALLOUT, GMOD_MENU, GMOD_TOOL_ACTIVE, THUG2_SKATE_MODE and THUG2_WALK_MODE if C04 confirms it.

Use INPUT_OWNERSHIP_MATRIX as host policy and C08 as source evidence. Keyboard/mouse and Xbox must express the same gameplay actions/state semantics.

Acceptance: no double consumption, no stuck cursor/focus, Q cleanly captures/restores, Toolgun/Physgun semantics source-faithful, THUG2 controls source-faithful, protected skate exit, deterministic Pip-Boy/pause/console compatibility. Codex runs R08/R09.
