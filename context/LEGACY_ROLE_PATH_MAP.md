# Legacy Role and Path Mapping — 2026-10-07

Current ownership:
- **Codex:** investigation, reverse engineering, runtime testing, crash diagnosis, integration debugging, validation/regression.
- **Claude Opus:** sole implementation/integration/visual/model/animation/UI/gameplay coding.
- **Normal GPT-5.5:** workflow/planning/documentation/coordination.
- **GPT-6/Astra:** unused.

## Legacy names

The following names remain in repository history for traceability but must not determine future agent assignment:

| Legacy label/path pattern | Current interpretation |
|---|---|
| `build/handoffs/gpt6_opus/*` | mixed historical handoff namespace; investigation/test work -> Codex, implementation -> Opus |
| `ASTRA_*.md` / `context/HANDOFFS/ASTRA_*` | historical handoffs; review technical content and remap investigation/testing to Codex, implementation to Opus |
| `prep/astra-*` | historical workflow branch; do not send new work to GPT-6/Astra |
| `runtime/astra-*` | historical runtime candidate branch; Codex owns any future validation after reconciliation |
| `feature/*-g6` | historical specialist branch label; implementation evidence belongs to Opus lane unless only investigative; runtime validation belongs to Codex |
| combined owner value `GPT6_OPUS` | split by task nature: evidence/testing -> Codex; implementation -> Opus |
| prose saying "Astra-owned" | obsolete; map to Codex if runtime/investigation, Opus if actual implementation |
| prose saying "GPT-6/Opus" | obsolete grouping; never use as a new ownership label |

## No automatic renames

Do not mass-rename historical paths or rewrite old commits solely to remove names. That would damage traceability.

Instead:
1. preserve old evidence paths;
2. add current wrapper/index documents;
3. reference the old artifact with a current owner;
4. create new Codex or Opus handoffs for new work;
5. never use old role labels in new acceptance or queue documents.

## Dispatch rule

Before handing off work:
- if the task asks **how the original game works**, send to Codex;
- if it asks **to implement/change the merged game**, send to Opus;
- if it asks **to run/test/debug the candidate**, send to Codex;
- if it asks **to organize/plan/document**, keep in GPT-5.5 workflow lane.
