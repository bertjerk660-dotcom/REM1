# Canonical Coordination Promotion Plan — 2026-10-07

Purpose: define how to promote preparation/workflow artifacts without merging specialist/runtime candidate branches wholesale.

## Current state

Preparation branch:
`prep/opus-readiness-finalization-20261007`

This branch is derived from:
`prep/workflow-coordination-20261007`

Runtime/specialist candidates remain intentionally separate.

## Promotion principle

Promote **coordination truth**, not candidate implementation history.

Do not merge:
- v84-v92 runtime candidate branches;
- historical Astra/GPT6 implementation branches;
- support test sidecars as if they are core-runtime proof;
- stale ownership text;
- branch-local runtime claims without Codex validation.

## Coordination artifacts safe to promote selectively

Core workflow/authority:
- `context/AGENT_OWNERSHIP.md`
- `context/DOCUMENTATION_AUTHORITY_MAP.md`
- `context/MASTER_AGENT_QUEUE.md`
- `context/OPUS_READINESS_BOARD.md`
- `context/MILESTONE_STATUS.md`
- `context/OPEN_WORK.md`

Evidence/provenance:
- `context/EVIDENCE_INDEX.md`
- `context/PROVENANCE_INDEX.md`
- `context/SELECTIVE_BRANCH_RECONCILIATION_2026-10-07.md`
- `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`
- `build/prepared/opus_readiness_20261007/local_preflight_snapshot.json`

Opus preparation controls:
- `context/OPUS_PREP_READINESS_SCORECARD_2026-10-07.md`
- `context/OPUS_LAUNCH_SEQUENCE_2026-10-07.md`
- `context/OPUS_PACKAGE_INTAKE_CHECKLIST_2026-10-07.md`
- `context/NORMAL_GPT_PRE_OPUS_BACKLOG_2026-10-07.md`
- `context/HANDOFFS/OPUS_IMPLEMENTATION_PACKET_TEMPLATE.md`
- `context/HANDOFFS/OPUS_FIX_PACKET_TEMPLATE.md`
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`

Ready package:
- `context/HANDOFFS/OPUS_O01_TOOLGUN_PRESENTATION_2026-10-07.md`
- `build/prepared/opus_o01_toolgun_presentation_20261007.json`

Finalization record:
- `context/HANDOFFS/NORMAL_GPT_OPUS_READINESS_FINALIZATION_2026-10-07.md`

## Promotion method

Preferred:
1. select the long-term integration branch;
2. fetch the current version of each file above;
3. compare with destination;
4. update/create files individually or via tightly scoped documentation commits;
5. run a terminology/ownership drift check;
6. verify runtime candidate files did not enter the promotion;
7. verify bootstrap/current-state links point to the promoted coordination layer.

Avoid wholesale merge because the source branch contains historical context inherited from earlier workflow work and future specialist branches may contain unvalidated code.

## Post-promotion checks

- current ownership says Codex investigates/runtime-validates and Claude Opus implements;
- no current instruction assigns work to Astra/GPT6;
- CURRENT_STATE contains only verified/current facts;
- OPUS_READINESS_BOARD package states survive unchanged;
- evidence indexes retain unresolved markers;
- candidate-version numbers are not treated as validation;
- quarantined runtime branches remain quarantined.

## Promotion readiness

The plan is complete. Actual promotion is deliberately deferred until the user selects the long-term integration branch or explicitly authorizes promotion to `main`.
