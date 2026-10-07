# Codex Investigation Request Sequence — 2026-10-07

Purpose: keep Codex in the investigation/evidence lane and prevent duplicate work or accidental implementation overlap with Claude Opus.

## Ownership rule

Codex:
- investigates;
- reverse engineers;
- traces functions/state/dependencies;
- produces evidence/manifests/contracts;
- later runtime-validates frozen Opus candidates.

Claude Opus:
- implements;
- integrates;
- writes final gameplay/runtime code;
- converts/retargets final models/animations;
- implements UI/camera/audio/physics adapters;
- fixes candidates from Codex runtime failures.

Normal GPT:
- coordinates;
- reviews evidence;
- assembles final Opus packets;
- tracks readiness and promotion.

## Existing GMod closure track

Packet already exists:
`context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

Scope:
- C01 Q-menu remaining native/service gaps;
- C02 Toolgun remaining effect/trace/prediction/duplicator-host gaps;
- C03 Physgun remaining provenance/controller/render/audio/actor-state gaps.

Do not repeat the broad GMod investigation already merged to canonical main.

## Next new request — C04

Use:
`context/HANDOFFS/NEXT_CODEX_REQUEST_THUG2_C04_2026-10-07.md`

Goal:
recover THUG2 master free-roam state machine, movement/physics, collision queries and grind/manual/lip eligibility.

Why first:
C04 defines the source state vocabulary needed by C05, C06, C07 and C08.

Codex must stop at evidence/contracts and must not implement the Fallout skate system.

## After C04 review

### C05 — camera
Run after the C04 state vocabulary is reviewed.

Use:
`context/HANDOFFS/CODEX_C05_THUG2_CAMERA_2026-10-07.md`

C05 should bind camera transitions to the exact C04 states/events.

### C06 — animation/skeleton/board
May run after C04 review, in parallel with C05 if desired.

Use:
`context/HANDOFFS/CODEX_C06_THUG2_ANIMATION_BOARD_2026-10-07.md`

C06 must map animation/attachment selection to the C04 state vocabulary.
No retargeting or board implementation in Codex.

### C07 — HUD/UI/scoring
May run after C04 review, in parallel with C05/C06 if desired.

Use:
`context/HANDOFFS/CODEX_C07_THUG2_HUD_UI_2026-10-07.md`

C07 must bind HUD surfaces to C04 gameplay/scoring events.
No HUD implementation in Codex.

## Final source-input closure — C08

Run after:
- GMod C01-C03 source semantics are sufficiently closed;
- THUG2 C04-C07 action/state vocabulary is reviewed.

Use:
`context/HANDOFFS/CODEX_C08_UNIFIED_INPUT_2026-10-07.md`

C08 maps actions/devices/conflicts and returns the adapter contract.
It does not implement the input layer.

## Runtime-validation phase

Do not run implementation validation until Opus freezes an exact candidate.

Then Codex uses:
- `context/CODEX_RUNTIME_TEST_PACKS.md`
- `context/HANDOFFS/CODEX_RUNTIME_VALIDATION_TEMPLATE_2026-10-07.md`

Any runtime failure goes back to Opus as evidence, not as a Codex final implementation patch.

## Readiness scoring

- C01 = 3 points
- C02 = 3
- C03 = 3
- C04 = 3
- C05 = 2
- C06 = 2
- C07 = 2
- C08 = 1

Clean baseline: 81/100.
No points are awarded until normal GPT semantically reviews each returned package against its stop condition.
