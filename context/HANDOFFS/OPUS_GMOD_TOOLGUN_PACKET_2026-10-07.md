# Opus packet — GMod Toolgun

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C01 + C02.**

## Objective
Integrate source-faithful GMod Toolgun behavior driven directly by Q-selected stool/tool state, with Remover and Duplicator as proof tools.

## Required evidence
C01 Q-menu state bridge + C02 Toolgun dispatch/tool registry/Remover/Duplicator dependency graphs and Opus interface contract.

## Assets
Use staged c_toolgun/w_toolgun, screen/materials, ToolTracer, Toolgun.Single and source stool definitions after current hash/provenance check.

## Preserve
Pip-Boy/drop/pickup identity and normal Fallout behavior outside tool ownership.

## Remove
Fallout-style tool selection prompts and any independent tool-state approximation.

## Acceptance
Q select -> close -> Toolgun uses exact selected tool; primary/secondary/reload semantics; Remover/Duplicator; effects/sounds/notifications; state cleanup; drop/pickup/save-load. Codex runs R02 and neighboring baseline regressions.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.