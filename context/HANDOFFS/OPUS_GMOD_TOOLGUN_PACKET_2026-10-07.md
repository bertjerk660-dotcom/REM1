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
