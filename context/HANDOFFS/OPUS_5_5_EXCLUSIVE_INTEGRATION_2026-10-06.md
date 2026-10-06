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
