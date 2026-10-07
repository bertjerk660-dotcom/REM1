# Implementation-Ready Work Packages — 2026-10-07

These packages separate evidence, implementation and runtime validation. Never combine Codex and Opus ownership.

## WP-GMOD-QMENU

**Objective:** replace the placeholder menu with the real/source-faithful GMod Q/spawn-menu behavior over the Fallout world.

- Source system: Garry's Mod sandbox spawnmenu/Q menu.
- Required evidence: Codex C01.
- Prerequisites: installed GMod provenance; prepared 105-Lua/46-VGUI/29-asset inventory; curated content adapter.
- Investigator: Codex.
- Implementer: Claude Opus.
- Runtime validator/debugger: Codex.
- Likely files/assets: spawnmenu Lua/Derma definitions, VGUI classes, icons/materials/fonts, content adapter, FNV UI/renderer bridge.
- Dependencies: input/focus ownership; Toolgun selected-mode state.
- Implementation success:
  - real menu lifecycle and visual structure;
  - Q opens intended menu only;
  - categories/search/icons/prop browser work;
  - cursor/focus behave correctly;
  - selected tool state reaches Toolgun;
  - no Fallout-style substitute selector.
- Runtime success: repeated open/close without flashing, duplicated panels, stuck cursor/input or icon failures.
- Risks: placeholder code accidentally retained as final path; dual input ownership; stale source inventory.

## WP-GMOD-TOOLGUN

**Objective:** source-faithful Toolgun driven directly by real Q-menu tool state.

- Required evidence: Codex C01 + C02.
- Investigator: Codex.
- Implementer: Opus.
- Runtime validator/debugger: Codex.
- Assets: c_toolgun/w_toolgun, screen/materials, ToolTracer, Toolgun.Single, stools.
- Minimum proof tools: Remover and Duplicator.
- Success:
  - tool selected in Q persists when menu closes;
  - Toolgun actions dispatch to selected stool;
  - correct traces/effects/sounds;
  - no Fallout prompt selector;
  - drop/pickup/save-load do not corrupt state.

## WP-GMOD-PHYSGUN

**Objective:** source-faithful Physgun presentation and manipulation.

- Required evidence: existing IDA 6.8 package + Codex C03 closure.
- Investigator: Codex.
- Implementer: Opus.
- Runtime validator/debugger: Codex.
- Blocker: unresolved `v_physics.mdl/.vvd/.dx90.vtx` provenance unless C03 proves another exact source path.
- Success:
  - correct first/world presentation;
  - source-grounded acquisition range;
  - beam/glow/highlight;
  - stable hold and distance adjustment;
  - rotation;
  - freeze/unfreeze/reacquire;
  - release/drop and launch;
  - correct actor target identity;
  - correct held-state audio loop;
  - cleanup on weapon/cell/load transitions.

## WP-THUG2-CORE

**Objective:** implement source-faithful THUG2 free-roam movement/state/physics inside Fallout world.

- Required evidence: Codex C04 + C08.
- Investigator: Codex.
- Implementer: Opus.
- Runtime validator/debugger: Codex.
- Preserve:
  - visible held board;
  - LMB enter;
  - holster exit;
  - persistent skateboard identity.
- Success:
  - push/coast/turn/brake/crouch/ollie/air/land;
  - slope/ground handling;
  - manuals;
  - valid-surface grinding only;
  - lips/walls/reverts;
  - bail/recovery and board-break state where source behavior requires;
  - no Fallout movement leakage underneath skating.

## WP-THUG2-CAMERA

**Objective:** exact source-grounded THUG2 skate camera through a safe host adapter.

- Required evidence: Codex C05.
- Implementer: Opus.
- Validator: Codex.
- Success: follow/yaw/pitch/distance/smoothing/speed/air/landing coupling behave source-faithfully; exit restores Fallout camera; no zoom/transition crash.

## WP-THUG2-ANIMATION-BOARD

**Objective:** full original animation family integration and correct board attachment across states.

- Required evidence: Codex C06.
- Implementer: Opus only.
- Validator: Codex.
- Assets: original THUG2 animations/board resources plus validated FNV skeleton map.
- Success:
  - all required animation families work;
  - correct selection/blending/timing;
  - board hand->feet->trick/bail/break/recovery->exit transitions;
  - no Fallout animation leakage;
  - no stale bone-cache/root-rebuild crashes.

## WP-THUG2-HUD

**Objective:** source-faithful THUG2 HUD/UI/scoring presentation while skate mode owns gameplay.

- Required evidence: Codex C07 plus state/event outputs from C04.
- Implementer: Opus.
- Validator: Codex.
- Success:
  - score/trick/combo/multiplier;
  - SPECIAL;
  - grind/manual/lip balance meters;
  - popups/resolution;
  - Fallout HUD/top-left skate alerts suppressed;
  - Fallout HUD restored on exit.

## WP-UNIFIED-INPUT

**Objective:** one explicit mode-owned input layer for Fallout, GMod and THUG2 across keyboard/mouse and Xbox.

- Required evidence: Codex C01/C02/C03/C04/C08 and `context/INPUT_OWNERSHIP_MATRIX.md`.
- Implementer: Opus.
- Validator: Codex.
- Success:
  - no simultaneous conflicting consumers;
  - Q-menu cursor/focus clean;
  - Toolgun/Physgun actions source-faithful subject to project-level override;
  - THUG2 action semantics match across devices;
  - protected skate exit works;
  - Pip-Boy/pause/console compatibility is deterministic.

## WP-CROSS-SYSTEM-STABILITY

**Objective:** prove Fallout, GMod and THUG2 coexist without state leakage or persistence failures.

- Prerequisites: all packages above implemented in frozen candidate(s).
- Implementer for fixes: Opus.
- Validator/debugger: Codex.
- Coordination: GPT-5.5.
- Required sequence:
  Fallout baseline -> Q menu -> Toolgun -> Physgun -> Fallout -> skateboard equip -> THUG2 -> exit -> Fallout -> save/load -> repeat.
- Success: all acceptance gates pass, no known critical failure remains open, exact hashes/manifests are recorded, human playability check succeeds.
