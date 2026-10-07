# Codex Master Closure Packet for 100% Opus Readiness — 2026-10-07

## Objective

Finish only the missing investigation/evidence required to move Claude Opus preparation from the clean 81/100 workflow baseline to 100/100.

Do not implement the Fallout runtime. Do not repeat already-complete broad inventories.

## Canonical starting state

Repository:
`bertjerk660-dotcom/REM1`

Use current canonical `main` for original GMod evidence and the latest clean Opus-preparation branch when available:
`prep/opus-ready-20261007`

Read:
- AGENTS.md
- context/BOOTSTRAP.md
- context/GOAL.md
- context/ARCHITECTURE.md
- context/CURRENT_STATE.md
- context/DECISIONS.md
- context/FAILURE_KNOWLEDGE.md
- context/AGENT_OWNERSHIP.md
- context/OPUS_READINESS_BOARD.md
- context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md

IDA requirement:
**IDA Pro 6.8 only** where native reverse engineering is required.

## Phase 1 — GMod narrow closure

Do not redo the authenticated broad GMod pass on main commit:
`19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`

Use:
`context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

Close C01, C02 and C03 against their original stop conditions.

For each, state:
- COMPLETE or PARTIAL;
- exact newly proven facts;
- source files/functions/addresses;
- exact unresolved items;
- final Opus adapter-contract delta;
- confidence;
- commit SHA.

## Phase 2 — THUG2 free-roam evidence

Execute in this order:

1. C04 state machine + movement/physics:
   `context/HANDOFFS/CODEX_C04_THUG2_STATE_PHYSICS_2026-10-07.md`

2. C05 camera:
   `context/HANDOFFS/CODEX_C05_THUG2_CAMERA_2026-10-07.md`

3. C06 animation/skeleton/board:
   `context/HANDOFFS/CODEX_C06_THUG2_ANIMATION_BOARD_2026-10-07.md`

4. C07 HUD/UI/scoring:
   `context/HANDOFFS/CODEX_C07_THUG2_HUD_UI_2026-10-07.md`

5. C08 unified GMod/THUG2/Fallout input:
   `context/HANDOFFS/CODEX_C08_UNIFIED_INPUT_2026-10-07.md`

C04 is the vocabulary/state dependency hub. C05/C06/C07 should bind to the recovered C04 states/events rather than invent parallel state names. C08 should consume finalized GMod and THUG2 action semantics.

## Required discipline

For every important behavior:
- source path;
- function/class/address where available;
- caller/callee or state transition;
- inputs/preconditions;
- outputs/state changes;
- dependent animation/camera/audio/UI/input hooks;
- original asset/resource identities where relevant;
- native boundary;
- confidence and unresolved ambiguity.

Do not promote inventory presence into behavior proof.

Do not substitute Fallout mechanics because the original path is difficult.

Do not perform final FNV integration.

## Completion response

Finish with a compact table:
C01 through C08 | COMPLETE/PARTIAL | commit SHA | remaining blocker | Opus package unlocked.

If any gate remains PARTIAL, explain exactly what evidence is missing and do not call the overall package 100% ready.
