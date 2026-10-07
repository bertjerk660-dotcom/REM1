# Agent Ownership — effective 2026-10-07

This document records the current project-agent split supplied by the project owner. It supersedes all older role labels that grouped GPT-6/Astra with Opus or assigned runtime work to GPT-6/Astra. Historical filenames may remain for traceability, but they no longer define ownership.

## Non-negotiable separation

**Claude Opus is the sole implementation/integration agent.**

**GPT-6/Astra is not to be used for this project.**

**Codex owns both investigation/evidence work and runtime investigation/testing/debugging/validation.**

Historical repository names such as `gpt6_opus`, `ASTRA_*`, `runtime/astra-*`, or `feature/*-g6` are legacy path/branch names only. Do not dispatch new work to GPT-6/Astra because of those names.

## Owners

### Codex — investigation, reverse engineering, runtime testing and debugging
Codex owns:
- codebase analysis;
- reverse-engineering research;
- function tracing;
- state-machine mapping;
- dependency discovery;
- UI/system internals;
- call graphs;
- asset identification;
- binary/decompiled behavior;
- source-behavior documentation;
- executing candidate builds where the available Codex environment supports it;
- live-game/runtime investigation;
- crash diagnosis;
- memory/runtime failures;
- camera/input/animation runtime validation;
- difficult integration debugging;
- performance/regression tests;
- state-transition tests;
- confirming behavior in the running game;
- preparing precise failure evidence for Opus when fixes are needed.

Codex does **not** own final implementation. Its investigation outputs should end in evidence packages, function/asset maps, dependencies and implementation-facing specifications. Its runtime outputs should end in deterministic pass/fail reports, logs, crash evidence and fix-focused handoffs to Opus.

### Claude Opus — sole implementation and visual integration owner
Opus owns all substantive implementation:
- code integration;
- source-faithful GMod and THUG2 system ports;
- model integration and conversion;
- textures and materials;
- weapon/board attachments;
- animation implementation;
- retargeting and skeleton work;
- UI rendering/hosting;
- gameplay-system implementation;
- effects;
- audio integration;
- physics/gameplay code;
- final asset placement;
- fixes resulting from Codex runtime failure reports.

Opus should consume prepared Codex evidence and repository handoffs rather than rediscovering the whole subsystem unless evidence is demonstrably incomplete.

### Normal GPT-5.5 workflow lane
Owns orchestration only:
- planning and decomposition;
- documentation;
- manifests and provenance;
- inventories;
- dependency tracking;
- handoffs;
- acceptance criteria;
- deterministic test plans;
- validation matrices;
- milestone tracking;
- branch reconciliation;
- evidence indexing;
- stale/conflicting-state detection;
- duplicate-work prevention;
- comparing Codex investigation/runtime reports against Opus implementation claims.

This lane must not implement Opus-owned systems or perform Codex-owned reverse-engineering/runtime-debugging work.

## Required flow

Codex investigation
-> evidence report
-> asset/function/dependency manifest
-> implementation interface/work package
-> Opus implementation
-> candidate build
-> Codex runtime validation/debugging
-> failure report if needed
-> Opus fix
-> Codex regression test
-> workflow lane records validated completion.

## Interpretation of historical files

Older files such as `build/handoffs/gpt6_opus/MASTER_EXECUTION_QUEUE.json` use combined or obsolete labels. Preserve technical task ordering and evidence where still valid, but remap ownership:

- investigation/evidence portions -> Codex
- implementation/visual/model/animation/runtime-code portions -> Opus
- live testing/debug/runtime validation -> Codex
- manifests/checklists/coordination -> GPT-5.5 workflow lane

Do not silently change product or architecture decisions while remapping ownership.

## Opus investigation exception

Codex remains the **default** owner of reverse-engineering investigation, evidence closure and runtime validation.

Claude Opus may perform narrowly scoped investigation when it is inseparable from, or necessary to unblock, Opus-owned implementation. This is an exception, not a transfer of the investigation lane.

When Opus performs such investigation:
- record branch, commit, source identity and hashes;
- use IDA Pro 6.8 for native reversing that requires IDA;
- separate direct evidence from inference;
- review the result against the same C01-C08 stop conditions before awarding readiness points;
- do not treat implementation success as proof that the original-game behavior was correctly recovered.

The Haiku findings branch `prep/haiku-findings-20261007` proposed broader Opus ownership of reverse engineering. That proposal is preserved as historical findings, but it does not supersede this current ownership document without a later explicit owner directive.