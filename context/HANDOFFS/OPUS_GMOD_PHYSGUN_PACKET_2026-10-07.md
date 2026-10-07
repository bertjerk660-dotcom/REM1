# Opus packet — GMod Physics Gun

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C03.**

## Objective
Implement/fix source-faithful Physgun presentation and behavior inside Fallout.

## Hard blocker
Do not substitute for unresolved source-declared v_physics MDL/VVD/DX90.VTX. C03 must resolve provenance or prove the actual exact presentation path.

## Required evidence
Existing IDA 6.8 package + C03 viewmodel provenance, native behavior map, audiovisual state map, FNV failure delta and Opus interface contract.

## Known current failures
- acquisition range too short;
- wrong held-target loop audio;
- actor effect can apply to PlayerCharacter rather than acquired target.

## Acceptance
Correct model/world presentation, acquire/range, beam/highlight, hold/distance, rotation, freeze/reacquire, release, punt/launch, actor/ragdoll target identity, correct loop audio, cleanup and save/load. Codex runs R03.
