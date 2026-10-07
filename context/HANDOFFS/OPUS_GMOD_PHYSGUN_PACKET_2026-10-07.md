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

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.