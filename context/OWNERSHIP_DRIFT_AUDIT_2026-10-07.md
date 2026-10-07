# Ownership Drift Audit — 2026-10-07

## Scope
Audit current authority documents for obsolete GPT-6/Astra ownership wording before Claude Opus implementation begins.

## Authority reviewed
- `context/AGENT_OWNERSHIP.md`
- `context/DOCUMENTATION_AUTHORITY_MAP.md`
- `context/DECISIONS.md`
- `context/GOAL.md`
- `context/CURRENT_STATE.md`
- `context/OPEN_WORK.md`
- `context/OPUS_READINESS_BOARD.md`

## Finding
`AGENT_OWNERSHIP.md` and `DOCUMENTATION_AUTHORITY_MAP.md` already correctly define:
- Codex = investigation/evidence + runtime validation/debugging;
- Claude Opus = sole implementation/integration;
- normal GPT = workflow/coordination;
- GPT-6/Astra = retired historical label.

One authoritative conflict remained:
- D-007 in `DECISIONS.md` still named GPT-6 Astra as Toolgun/Physgun implementation owner.

## Resolution
D-007 was amended without changing its technical decision:
- real GMod systems remain mandatory;
- real scripts/assets/native evidence remain mandatory;
- Toolgun selection remains owned by the real/ported Q menu;
- the obsolete agent label is explicitly superseded.

D-009 now records the current ownership rule as a durable accepted decision.

## Historical files
Files/branches containing Astra/GPT6 names are not renamed wholesale because their names preserve history and references. They remain technical evidence only; current ownership is interpreted through D-009 and `AGENT_OWNERSHIP.md`.

## Result
Current authority documents no longer require a fresh agent to infer that Astra might still own implementation.
