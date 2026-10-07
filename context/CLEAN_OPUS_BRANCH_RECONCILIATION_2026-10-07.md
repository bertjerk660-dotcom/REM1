# Clean Opus-Ready Branch Reconciliation — 2026-10-07

## Result

Preferred preparation branch:
`prep/opus-ready-20261007`

Base:
canonical `main` at GMod evidence merge commit
`19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`.

GitHub comparison after the coordination bundle was layered onto the fresh branch:
- status: **ahead**;
- ahead of main: **78 commits** at the verification point;
- behind main: **0 commits**.

Later coordination-only commits may increase the ahead count. The required invariant is zero behind until canonical main changes again.

## Why this branch exists

The older `prep/opus-readiness-finalization-20261007` branch had independently imported files that overlap canonical main's authenticated GMod merge. A direct main→old-prep PR therefore produced add/add conflicts.

That PR was closed without merge. No force merge occurred.

The clean branch was instead created directly from current main, then received only current coordination/readiness/handoff/manifests. This preserves:
- canonical main evidence;
- preparation history;
- runtime-candidate quarantine;
- no speculative merge of v84-v92 runtime candidates.

## Readiness consequence

Branch reconciliation/durable memory is now **10/10** in the preparation rubric.

Overall preparation baseline becomes:
**81/100**

The remaining 19 points are exclusively C01-C08 evidence gates:
`context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md`.

## Freshness rule

Before any future Opus session:
1. compare `main` → `prep/opus-ready-20261007`;
2. if behind > 0, reconcile new canonical evidence first;
3. re-run `research/validate_opus_visual_source_packets.py`;
4. do not treat a higher local runtime version as canonical merely because it exists.
