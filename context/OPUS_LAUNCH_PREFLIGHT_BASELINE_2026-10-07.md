# Opus Launch Preflight Baseline — 2026-10-07

This is the current one-page launch checkpoint for Claude Opus preparation.

## Branch/state
- repository: `bertjerk660-dotcom/REM1`
- preparation branch: `prep/opus-ready-20261007`
- compared with current `main`: **145 ahead / 0 behind**
- preparation readiness: **81/100**
- remaining 19 points: C01-C08 Codex evidence only

## First Opus task
**O00 Golden Source Bench — READY FOR OPUS**

Use:
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`
- `build/templates/OPUS_O00_CANDIDATE_MANIFEST_SEED.json`
- `context/OPUS_SESSION_1_EXECUTION_CHECKLIST_2026-10-07.md`

After implementation, freeze the exact candidate and hand it to Codex using:
`context/HANDOFFS/CODEX_O00_GOLDEN_BENCH_RUNTIME_VALIDATION_2026-10-07.md`

## Current machine-checked preparation

### Source packages
`research/validate_opus_visual_source_packets.py`
- O00 PASS
- O01 PASS
- O08a PASS
- O08b PASS
- O08c PASS
- **87 files / 0 errors**

### Candidate-manifest preflight
`research/validate_opus_candidate_manifest.py --mode preflight`
- O00 PASS
- O01 PASS
- O08a PASS
- O08b PASS
- O08c PASS
- **0 errors**

Before Codex receives any candidate, run the same validator using:
`--mode freeze`

Freeze mode requires implementation/parent commits, hashed outputs, load order, test save/location, resolved static/build checks and rollback.

### Semantic package gates
`research/validate_opus_gate_state.py`
- PASS
- computed readiness: **81/100**
- false-unlock errors: **0**

Blocked behavior packages remain blocked.

## Post-O00 queue
Only after reviewed O00 PASS:
- O01 Toolgun presentation → READY FOR OPUS
- O08a Crowbar presentation → READY FOR OPUS
- O08b Pistol presentation → READY FOR OPUS
- O08c SMG1 presentation → READY FOR OPUS

Their common Codex presentation-validation packet is:
`context/HANDOFFS/CODEX_VISUAL_WEAPON_PRESENTATION_RUNTIME_VALIDATION_2026-10-07.md`

O00 PASS does not itself validate those packages.

## Codex evidence track
Next new investigation:
`context/HANDOFFS/NEXT_CODEX_REQUEST_THUG2_C04_2026-10-07.md`

C04 is investigation/evidence only. It must not perform Opus-owned implementation.

Existing parallel GMod closure:
`context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

## Stop rules
- no speculative increase above 81 without reviewed C01-C08 evidence;
- no behavior package starts before its Codex gate is COMPLETE;
- no candidate reaches Codex without freeze-validation PASS;
- no runtime candidate is promoted merely because its version is newer;
- no historical Astra/GPT6 role label overrides current ownership.
