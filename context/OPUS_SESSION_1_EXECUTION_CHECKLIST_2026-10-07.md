# Opus Session 1 Execution Checklist — O00 → O01 — 2026-10-07

Purpose: remove ambiguity from the first Claude Opus implementation session and the following Codex validation handoff.

This checklist is workflow control only. It does not implement any game system.

## Current baseline

Repository:
`bertjerk660-dotcom/REM1`

Preparation branch:
`prep/opus-ready-20261007`

Preparation readiness:
**81/100**

First implementation gate:
**O00 Golden Source Bench**

O01 and O08a/O08b/O08c remain gated behind O00 PASS.

## Stage A — normal-GPT preflight

Before Opus edits anything:

- [ ] compare `main` → `prep/opus-ready-20261007`; branch must be 0 behind;
- [ ] run `research/validate_opus_visual_source_packets.py`;
- [ ] confirm O00 source validation PASS;
- [ ] record current local main DLL/ESP hashes;
- [ ] record current enabled plugin/load order;
- [ ] identify unrelated support sidecars and whether they will be disabled for O00;
- [ ] choose a disposable/known-good save and a deterministic test location;
- [ ] confirm no quarantined runtime candidate is being promoted;
- [ ] create the Opus implementation branch from the intended parent;
- [ ] copy/fill the O00 candidate-manifest seed before editing.

## Stage B — Claude Opus O00 implementation

Opus reads:
- `context/HANDOFFS/OPUS_SESSION_1_START_HERE_2026-10-07.md`
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`
- `build/prepared/opus_o00_golden_bench_20261007.json`
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`

Allowed O00 scope:
- isolated Source→FNV bench conversion;
- materials/shader translation;
- collision conversion;
- scale/axis documentation;
- isolated sidecar test record;
- candidate-only mesh/texture paths.

Forbidden:
- modifying the main NVSE runtime as part of O00;
- changing Toolgun/Physgun/THUG2 behavior;
- overwriting source staging;
- promoting old runtime candidates.

## Stage C — candidate freeze

Before Codex receives O00:

- [ ] implementation commit exists;
- [ ] parent commit recorded;
- [ ] generated mesh hash recorded;
- [ ] generated texture hashes recorded;
- [ ] sidecar ESP hash recorded;
- [ ] any changed source/tooling hashes recorded;
- [ ] load order recorded;
- [ ] test save/location recorded;
- [ ] rollback path/revert commit recorded;
- [ ] known issues recorded;
- [ ] static validation result recorded;
- [ ] candidate manifest passes `validate_opus_candidate_manifest.py --mode freeze`.

If freeze validation fails, do not hand to Codex.

## Stage D — Codex O00 validation

Codex receives the exact frozen candidate only.

Use:
`context/HANDOFFS/CODEX_O00_GOLDEN_BENCH_RUNTIME_VALIDATION_2026-10-07.md`

Codex does not modify Opus implementation during validation.

Expected result:
- PASS → normal GPT records O00 validated and unlocks O01/O08a/O08b/O08c;
- FAIL → normal GPT produces a narrow Opus fix packet bound to the exact candidate hashes.

## Stage E — O00 PASS promotion rule

O00 PASS proves only the conversion/material/collision pipeline used for the tested bench candidate.

It does not validate:
- Toolgun;
- Crowbar;
- Pistol;
- SMG1;
- Physgun;
- Q-menu;
- THUG2.

After O00 PASS:
- O01 becomes READY FOR OPUS;
- O08a becomes READY FOR OPUS;
- O08b becomes READY FOR OPUS;
- O08c becomes READY FOR OPUS.

Each still requires its own candidate freeze and Codex visual/runtime validation.

## Failure routing

If O00 fails:
1. preserve exact candidate identity;
2. capture first failing gate;
3. determine whether failure is geometry, material, scale, collision, sidecar, path resolution, save/load or unrelated regression;
4. create `OPUS_FIX_PACKET`;
5. protect every passing gate;
6. Opus fixes;
7. Codex re-runs failed gate plus affected regressions.

Do not bypass O00 by starting weapon conversion with a known-bad pipeline.
