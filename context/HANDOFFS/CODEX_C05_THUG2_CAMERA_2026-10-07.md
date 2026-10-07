# Codex C05 — THUG2 skate camera investigation

## Objective
Recover and document original THUG2 free-roam skate-camera behavior so **Claude Opus** can implement it through a host-safe Fallout adapter. After Opus implementation, **Codex** performs runtime validation/debugging.

Codex must not implement the final camera.

## Investigate
Trace:
- camera state/controller classes/functions;
- initialization on skate-mode entry;
- follow target/position;
- yaw/heading relationship to velocity/board heading;
- pitch;
- follow distance and vertical offset;
- smoothing/interpolation;
- speed coupling;
- crouch/ollie/air/landing changes;
- grind/manual/lip/wall/bail special cases;
- user camera input/recentering;
- camera collision/clipping if present;
- walk/skate transitions;
- pause/death/load/exit reset;
- timestep/unit assumptions.

## Required questions
1. Which functions update the camera each frame?
2. Which state variables feed target, yaw, pitch, distance and smoothing?
3. Which skating states override camera behavior?
4. Which inputs directly rotate it versus indirectly alter heading?
5. How does speed/air/landing affect camera motion?
6. Is collision handled by THUG2, native engine code, or both?
7. Which native interfaces require IDA Pro 6.8 evidence?
8. What host-safe adapter should Opus expose rather than raw Fallout camera-node writes?
9. What Fallout camera state must be preserved/restored?
10. Which historical FNV camera crash paths must be avoided?

## Required outputs
- context/CODEX/THUG2_C05_CAMERA_EVIDENCE_2026-10-07.md
- build/evidence/thug2_c05/camera_function_map.json
- build/evidence/thug2_c05/camera_state_map.json
- build/evidence/thug2_c05/state_coupling_matrix.json
- build/evidence/thug2_c05/opus_camera_adapter_contract.json

Record source/function/address, inputs, outputs, state dependencies and confidence.

## Stop condition
Stop when Opus can implement source-faithful camera behavior without approximating THUG2 or using unverified Fallout camera pointers.

Do not perform final implementation. Runtime validation happens in a later Codex pass after Opus produces a candidate.
