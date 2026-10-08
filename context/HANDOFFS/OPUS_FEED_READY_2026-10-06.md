# Opus feed bundle readiness — 2026-10-06

Status: READY FOR OPUS VISUAL IMPLEMENTATION; NO OPUS IMPLEMENTATION HAS BEEN PERFORMED BY THIS PREPARATION PASS.

## What is prepared
- A six-step Opus-only visual/model/animation queue exists at `build/handoffs/gpt6_opus/feed_bundle/OPUS_VISUAL_QUEUE.json`.
- A generated code-context pack exists at `build/handoffs/gpt6_opus/feed_bundle/CODE_CONTEXT.md`, anchored to current `main.cpp` SHA256 `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`.
- A metadata-only asset/provenance index exists at `ASSET_REFERENCE_INDEX.json`; proprietary game payloads remain local and are not copied to GitHub.
- Eleven pre-Opus source packets are indexed for the golden bench and initial Source/GMod weapon visuals.
- A ready-to-paste Opus prompt exists at `OPUS_START_PROMPT.md`.
- `research/validate_opus_feed_bundle.ps1` verifies bundle hashes, protected runtime hashes, queue ownership, and required local source components.

## Validation result
The feed validator passed:
- generated feed files: all hashes match;
- required local source components checked: 34;
- required source component failures: 0;
- deployed v85 DLL unchanged;
- active REM_GModTHUG2.esp unchanged;
- active project source hash matches the runtime integration map;
- no proprietary source-game asset payload is embedded in the GitHub-safe feed metadata.

## First Opus task
O01 is the only task to start initially: prove the authentic Half-Life 2 `models/props_c17/bench01a.mdl` end to end in an isolated Fallout candidate/sidecar. Stop on any visibility/material/scale/collision/persistence failure and repair the conversion pipeline before batch work.

## Ownership boundary
Opus: visual/model/material/rigging/conversion/animation implementation and related visual integration code.

Astra: native/deep runtime mechanics, real Q-menu compatibility runtime, Tool Gun execution mechanics, Physics Gun manipulation mechanics, THUG2 movement/physics/camera state machine, crash-sensitive hooks, and final runtime promotion.

ChatGPT support lane: orchestration, manifests, evidence, validators, regression planning and project-state recording.
