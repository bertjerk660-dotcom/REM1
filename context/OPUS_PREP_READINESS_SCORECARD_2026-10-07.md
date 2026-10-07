# Opus Preparation Readiness Scorecard — 2026-10-07

Purpose: quantify **preparation readiness for Claude Opus**, not feature completion and not runtime validation.

This score exists because earlier milestone documents correctly avoided unsupported percentages. The percentage below is supported by an explicit weighted rubric and can therefore be reproduced.

## Rubric

| Area | Weight | Before this pass | After this pass | Notes |
|---|---:|---:|---:|---|
| Product goal / architecture / ownership clarity | 10 | 10 | 10 | Goal, architecture, authority map and agent ownership are explicit. |
| Source / asset provenance and staging | 15 | 13 | 15 | Strong GMod/HL/THUG2 inventories; phase-4 prop evidence is reconciled and current GMod/THUG2/FNV-skeleton hashes were re-checked on the local machine. |
| Branch reconciliation / durable project memory | 10 | 5 | 8 | Runtime candidates remain quarantined; high-value branch-only prop/manifests are now classified. Main still does not contain the full coordination layer, so canonical promotion remains deliberate future work. |
| Codex implementation-grade evidence completeness | 30 | 7 | 7 | This cannot be increased by the workflow lane. C01-C08 result packages are still the dominant blocker. Existing source inventories and partial Physgun/THUG2 evidence earn partial credit only. |
| Opus implementation packet readiness | 15 | 8 | 14 | Launch order, evidence intake gates, hardened implementation/fix packet templates and a machine-readable candidate-manifest template are now explicit. Most system packages still await Codex evidence. |
| Acceptance / deterministic validation preparation | 10 | 9 | 10 | Acceptance matrix and Codex runtime packs are already strong; package intake now requires exact candidate identity and regression obligations. |
| Runtime-candidate / baseline safety | 5 | 5 | 5 | v84-v92 and historical branches stay quarantined; version number never overrides runtime evidence. |
| Opus launch/runbook clarity | 5 | 1 | 5 | New launch sequence and package intake checklist remove ambiguity about what Opus may start and what must wait. |
| **TOTAL** | **100** | **58** | **74** | |

## Headline

**Before this workflow pass: 58% Opus-preparation ready.**

**After this workflow pass: 74% Opus-preparation ready.**

This is a **+16 percentage-point preparation gain** produced only by coordination/reconciliation/handoff work. It does not pretend that missing reverse-engineering evidence has been solved.

## What the 74% does and does not mean

It means:
- the desired product is well specified;
- ownership is explicit;
- significant source/asset inventories exist;
- candidate/version confusion is controlled;
- Opus has a deterministic package launch order;
- Opus handoffs can be composed consistently as Codex evidence arrives;
- validation expectations are already defined.

It does **not** mean 74% of the game is implemented.
It does **not** mean 74% of the final runtime is validated.
It does **not** mean C01-C08 are complete.

## Why the remaining 26% cannot all be closed by normal ChatGPT

The largest remaining block is the 23 unearned points inside the 30-point Codex evidence category. Normal workflow work must not invent:
- GMod Q-menu function/dependency traces;
- Toolgun dispatch semantics;
- missing Physgun native provenance;
- THUG2 state/physics maps;
- THUG2 camera internals;
- animation/board/skeleton behavior;
- HUD/UI/scoring event internals;
- original unified input semantics.

Those are Codex investigation tasks.

The remaining non-Codex preparation gap consists mainly of:
- selecting/promoting the coordination artifacts onto the branch the user chooses as the long-term canonical integration base;
- package-specific asset/source reconciliation immediately before each Opus package;
- final package assembly after each Codex result arrives.

## Subsystem gate reality

Current Opus package state remains:
- O01 Toolgun presentation: **READY WITH PREFLIGHT**.
- O08 model/asset visual work: **PARTIAL / package-specific**.
- O02/O03/O04/O05/O05b/O06/O07/O07b: **WAITING FOR CODEX**.
- O09 polish/fixes: waits for implemented candidates + Codex runtime failures.

Therefore this score measures **quality/completeness of preparation**, not the percentage of implementation packages currently unlocked.

## Re-score rule

Only change this score when underlying evidence changes. Do not raise it because:
- a branch version number increased;
- code compiled;
- an untested runtime candidate exists;
- an old Astra/GPT6 handoff says “ready”;
- an implementation visually resembles the source game.

Re-score after each reviewed Codex C01-C08 package, after package-specific preflight reconciliation, or after deliberate canonical-branch promotion.
