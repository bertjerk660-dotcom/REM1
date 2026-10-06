# External Opus 5.5 exclusive integration handoff — 2026-10-06

## Authority
External Claude Opus 5.5 is the sole implementation/integration owner for substantive game-asset merging and the GMod/THUG2 systems below. Support agents prepare evidence and validation only and must not compete with or overwrite Opus runtime work.

## GMod outcome
Implement the real/source-faithful GMod Q/spawn menu and its functional runtime bridge to the actual/source-faithful GMod Tool Gun. Preserve opening/closing, categories, prop browser, icons, search/filtering, tools, Duplicator, Remover, selected-tool state, notifications, scripts, behavior, animations, effects and sounds. Use the user's installed sources and IDA Pro 6.8 wherever native GMod/Source behavior requires reverse engineering. Fallout-style prompts and hand-authored lookalikes are not final parity.

## THUG2 outcome
Activating the skateboard must transition Fallout into a complete source-faithful THUG2 free-roam skating subsystem inside the Fallout world; holstering/exiting restores Fallout cleanly.

Opus owns the complete stack: camera; physics; movement; collision; controls; board hand/feet attachment; idle/carry/walk/mount/push/ride/turn/crouch/ollie/air/land/manual/grind/lip/wallride/wallplant/revert/grab/flip/special/bail/fall-off/recovery/board-break behavior and animations; grind eligibility; trick state machine; combos; balance; scoring; SPECIAL; HUD; menus; UI; popups; Fallout-HUD suppression/restoration; sounds; animation selection/blending/timing/retargeting; and every dependency needed for ordinary THUG2 free-roam skating.

## Preserve these verified positives
- Held skateboard is visible and correctly positioned in the player's hand.
- Left-click with skateboard equipped enters skate mode.
- Holster key exits skate mode.
- THUG2 sounds appear functional in the tested path, pending exhaustive parity validation.
- Current GMod-style prop menu looks correct but is only a placeholder.

## Resolve these known failures
- THUG2 HUD/UI/popups absent/incomplete; Fallout HUD/top-left alerts remain.
- Board does not transition to feet.
- THUG2 animation set is not functioning.
- G can trigger grinding anywhere.
- Current GMod prop menu is not the real functional Q menu.
- Physics Gun parity regressions remain: very short range, wrong held-target loop audio and actor-target unconscious effect applied incorrectly.

## Prepared inputs
Start with context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md and the existing Toolgun, Q-menu, THUG2 skate-runtime, skateboard-attachment and THUG2 HUD/input handoffs plus build/prepared inventories. Do not redo completed discovery without evidence it is stale.

## Support-lane boundary
Non-Opus agents may accelerate Opus only with inventories, hashes/provenance, IDA 6.8 evidence organization, manifests, dependency graphs, conversion queues, validation tooling, regression matrices, acceptance criteria and handoff packaging. They must not modify Opus-owned runtime integration.

## Acceptance
Appearance or mode activation alone is not completion. Require source/provenance evidence, integration, human playtest and regression validation. Preserve Fallout behavior outside imported modes. Do not commit proprietary game binaries/assets to GitHub; record hashes, provenance, mappings, tooling and reproducibility metadata.


## Reconciliation with latest "Choose Asset Merger" chat — 2026-10-06

### Combine armor / Enclave replacement gate
- The isolated Combine armor test remains a prerequisite before any Enclave/Remnants replacement or promotion.
- Recent human tests progressed from invisibility to partial visibility and then visible armor, but the Combine head orientation is backwards and the torso appears slightly stretched. Treat fit/orientation/rigging as unresolved until corrected and human-validated.
- Earlier symptoms included only head/hands/slave collar/Pip-Boy visibility and later a visible right lower leg; preserve these as regression cases.
- Do not promote the Combine suit as an Enclave/Remnants replacement merely because the mesh now renders.

### External-asset proof gate
- Do not batch-promote converted external props/models based on records or conversion success alone.
- The integration pipeline must first prove at least one externally sourced Half-Life/GMod reference prop visibly renders in Fallout with correct texture, scale and collision. Only then use the proven path for batch work.
- Records existing in the ESP or successful conversion output are not proof that an external asset works in runtime.

### Skateboard/runtime plugin discipline
- The skateboard remains a normal droppable/pickup-able weapon while Fallout gameplay is active; attacking/left-click enters THUG2 skate mode and the holster/exit control returns to Fallout.
- Plugin/load-order changes can alter weapon behavior; a recent test with all plugins enabled caused the THUG2 skateboard to behave like a grenade. Preserve weapon-form/type/load-order integrity as a regression gate.
- Preserve the now-working held-board model placement while Opus repairs board-to-feet attachment and the complete THUG2 animation/free-roam stack.

### Ownership clarification
- External Opus 5.5 owns the substantive coding/visual/runtime integration: models, textures, NIF/rigging, animations, physics, camera, GMod/THUG2 code and behavior, Q-menu/Toolgun integration, and cross-game asset implementation.
- The support/GPT lane owns preparation and orchestration only: manifests, provenance/hashes, dependency inventories, test plans, validation, load-order tracking, naming, regression/failure documentation and reproducibility evidence.
- IDA Pro 6.8 remains the only reverse-engineering version authorized for this project.


## GMod overlay evidence expansion
A dedicated preparation document now defines the required GMod presentation/input architecture:
- context/HANDOFFS/GMOD_OVERLAY_EVIDENCE_2026-10-06.md

Treat GMod as a contextual interaction/UI layer over the live Fallout world, not as a permanent Fallout HUD reskin. Fallout owns normal play; the real/ported Q menu temporarily owns menu/cursor input while visible; Toolgun and Physgun own their source-faithful actions/feedback while equipped; GMod-owned transient feedback uses GMod presentation rather than Fallout alerts; closing the GMod layer returns input/presentation cleanly to Fallout.

The overlay evidence document also records the currently durable inventories (105 Q-menu Lua files, 40 stools, 46 VGUI classes, 29/29 direct UI/material refs, Toolgun/Physgun assets/hooks, curated 290-prop catalog), an implementation-grade evidence checklist, and 12 acceptance tests.

Documentation warning: the readiness audit references ASTRA_GMOD_QMENU.md, ASTRA_TOOLGUN.md and ASTRA_PHYSGUN.md, but those three paths are currently absent from canonical GitHub. Opus must not assume they are durable inputs until recovered/imported or replaced.
