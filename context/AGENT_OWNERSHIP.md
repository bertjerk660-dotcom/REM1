# Agent Ownership — effective 2026-10-07

This document records the current project-agent split supplied by the project owner. It supersedes older **role labels** that grouped GPT-6 and Opus together, but it does not invalidate the technical evidence inside those older handoffs.

## Owners

### Codex — investigation and evidence
Owns investigation of original-game code and data: codebase analysis, reverse-engineering research, function tracing, state-machine mapping, dependency discovery, UI/system internals, call graphs, asset identification, binary/decompiled behavior, and source-behavior documentation.

Codex must not be treated as the final implementation owner. Its output should end in evidence packages, function/asset maps, dependencies, and implementation-facing specifications.

### Claude Opus — implementation and visual integration
Owns actual implementation: code integration, source-faithful GMod/THUG2 system ports, models, textures, attachment, animation, retargeting, skeleton work, UI rendering/hosting, gameplay behavior, effects, audio integration, difficult coding, and final asset placement.

Opus should consume prepared Codex evidence and repository handoffs rather than rediscovering the whole subsystem unless the evidence is demonstrably incomplete.

### GPT-6 / Astra — runtime investigation and validation
Owns live-game/runtime work: executing candidate builds, crash diagnosis, memory/runtime failures, camera/input/animation validation, difficult integration debugging, performance/regression tests, state-transition testing, and confirming behavior in the running game.

Astra should not be used as the primary implementation owner under the current split.

### Normal GPT-5.5 workflow lane
Owns orchestration only: planning, decomposition, documentation, manifests, provenance, inventories, dependency tracking, handoffs, acceptance criteria, test plans, validation matrices, milestone tracking, branch reconciliation, evidence indexing, stale/conflicting-state detection, and duplicate-work prevention.

This lane must not implement Opus-owned game systems, perform Codex-owned reverse engineering, or replace Astra-owned runtime validation.

## Required flow

Codex investigation
-> evidence report
-> asset/function/dependency manifest
-> integration interface/work package
-> Opus implementation
-> candidate build
-> Astra runtime validation
-> failure report if needed
-> Opus fix
-> Astra regression
-> workflow lane records validated completion.

## Interpretation of historical files

Older files such as `build/handoffs/gpt6_opus/MASTER_EXECUTION_QUEUE.json` use combined labels such as `GPT6_OPUS`. Preserve their technical task ordering and gates, but remap ownership under this document:

- investigation/evidence portions -> Codex
- implementation/visual/runtime-code portions -> Opus
- live testing/debug/runtime validation -> Astra
- manifests/checklists/coordination -> GPT-5.5 workflow lane

Do not silently change product/architecture decisions while remapping ownership.
