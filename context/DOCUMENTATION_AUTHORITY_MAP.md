# Documentation Authority and Reconciliation Map — 2026-10-07

Purpose: prevent stale branch notes, higher version numbers, legacy agent labels or static build success from overriding verified project truth.

## Authority order by question

| Question | Primary authority | Secondary evidence | Must not override it alone |
|---|---|---|---|
| What game are we trying to build? | context/GOAL.md | accepted decisions | old handoffs, implementation convenience |
| What architecture should integrations follow? | context/ARCHITECTURE.md | DECISIONS + interface contracts | experimental branch structure |
| What is currently verified? | context/CURRENT_STATE.md | exact build manifest + Codex runtime report + hashes | version number, branch name, compile success |
| What work is open/next? | MASTER_AGENT_QUEUE + OPEN_WORK | MASTER_PROJECT_MAP + WORK_PACKAGES | old agent prompts |
| Who owns a task? | AGENT_OWNERSHIP.md | LEGACY_ROLE_PATH_MAP.md | historical GPT6_OPUS/Astra labels |
| What original-game behavior is proven? | reviewed Codex evidence package | provenance/source inventories | current approximation or user-interface resemblance |
| What may Opus implement? | gated Opus packet + reviewed Codex evidence | WORK_PACKAGES + ACCEPTANCE_MATRIX | unsupported assumptions |
| Is an implementation candidate valid? | Codex runtime validation tied to exact branch/commit/hashes | acceptance matrix + regression packs | static validation alone |
| What failures must not recur? | FAILURE_KNOWLEDGE.md + FAILURE_LEDGER.md | crash logs/build reports | later version number |
| Where did an asset/code reference come from? | PROVENANCE_INDEX + raw hash manifest | EVIDENCE_INDEX | filename similarity |
| Can branch-only work become canonical? | SELECTIVE_BRANCH_RECONCILIATION plan + evidence gate | branch manifests/diffs | wholesale merge or newest-version preference |

## Current baseline rule

Until a newer candidate passes the required Codex runtime gates and is deliberately promoted, main's documented verified runtime remains the baseline even when divergent branches contain v84-v92 labels or later code.

A branch can be:
- technically newer;
- statically cleaner;
- more feature-rich;
- or compile successfully;

and still **not** be the verified runtime baseline.

## Evidence promotion ladder

1. DISCOVERED — artifact/source/branch exists.
2. INVENTORIED — identity/path/hash recorded.
3. INVESTIGATED — Codex maps source behavior/dependencies.
4. REVIEWED — workflow review confirms evidence is sufficient and contradictions are classified.
5. READY FOR IMPLEMENTATION — gated Opus packet may be dispatched.
6. IMPLEMENTED CANDIDATE — Opus freezes branch/commit/build/hashes.
7. READY FOR RUNTIME TEST — candidate identity and deterministic pack complete.
8. RUNTIME VALIDATED — Codex passes applicable tests on that exact candidate.
9. REGRESSION VALIDATED — neighboring/cross-system tests pass.
10. CANONICAL PROMOTION — CURRENT_STATE/build history updated deliberately.

Skipping a rung requires an explicit documented reason; compile/static success never substitutes for runtime validation.

## Fresh-session reconciliation checklist

Before changing project truth:
1. compare coordination branch against main;
2. inspect recent commits and active specialist branches;
3. check CURRENT_STATE against newest runtime reports/manifests;
4. check AGENT_OWNERSHIP before reading legacy handoff names literally;
5. check FAILURE_KNOWLEDGE/FAILURE_LEDGER for the subsystem;
6. resolve evidence IDs/provenance before creating duplicate investigation work;
7. update queue/readiness/milestone documents only after the underlying evidence changes.

## Conflict recording format

When two artifacts disagree, record:
- artifact A path/branch/commit/date;
- artifact B path/branch/commit/date;
- exact conflicting claim;
- which authority rule applies;
- evidence still required;
- temporary working conclusion;
- owner of resolution;
- downstream documents that must be updated after resolution.

Never silently rewrite a conflict into certainty.
