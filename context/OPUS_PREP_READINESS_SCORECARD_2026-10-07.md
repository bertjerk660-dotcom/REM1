# Opus Preparation Readiness Scorecard — 2026-10-07

Purpose: quantify **preparation readiness for Claude Opus**, not feature completion and not runtime validation.

This score exists because earlier milestone documents correctly avoided unsupported percentages. The percentage below is supported by an explicit weighted rubric and can therefore be reproduced.

## Rubric

| Area | Weight | Before this pass | After this pass | Notes |
|---|---:|---:|---:|---|
| Product goal / architecture / ownership clarity | 10 | 10 | 10 | Goal, architecture, authority map and agent ownership are explicit. |
| Source / asset provenance and staging | 15 | 13 | 15 | Strong GMod/HL/THUG2 inventories; phase-4 prop evidence is reconciled and current GMod/THUG2/FNV-skeleton hashes were re-checked on the local machine. |
| Branch reconciliation / durable project memory | 10 | 5 | 10 | Clean branch `prep/opus-ready-20261007` was created directly from current canonical main and verified 78 commits ahead / 0 behind; runtime candidates remain quarantined. |
| Codex implementation-grade evidence completeness | 30 | 7 | 11 | Authenticated GMod source/IDA evidence merged to main materially closes Q-menu/Toolgun/Physgun rediscovery, but C01/C02 remain substantial partial and C03 partial. THUG2 C04-C08 remain the dominant evidence deficit. |
| Opus implementation packet readiness | 15 | 8 | 15 | Launch order, evidence intake gates and templates are explicit, and O01 Toolgun presentation now has a fully hash-verified READY FOR OPUS packet. Most behavior/system packages still await Codex evidence. |
| Acceptance / deterministic validation preparation | 10 | 9 | 10 | Acceptance matrix and Codex runtime packs are already strong; package intake now requires exact candidate identity and regression obligations. |
| Runtime-candidate / baseline safety | 5 | 5 | 5 | v84-v92 and historical branches stay quarantined; version number never overrides runtime evidence. |
| Opus launch/runbook clarity | 5 | 1 | 5 | New launch sequence and package intake checklist remove ambiguity about what Opus may start and what must wait. |
| **TOTAL** | **100** | **58** | **81** | |

## Headline

**Before this workflow pass: 58% Opus-preparation ready.**

**After this workflow pass: 81% Opus-preparation ready.**

This is a **+23 percentage-point preparation gain** produced only by coordination/reconciliation/handoff work. It does not pretend that missing reverse-engineering evidence has been solved.

## What the 81% does and does not mean

It means:
- the desired product is well specified;
- ownership is explicit;
- significant source/asset inventories exist;
- candidate/version confusion is controlled;
- Opus has a deterministic package launch order;
- Opus handoffs can be composed consistently as Codex evidence arrives;
- validation expectations are already defined.

It does **not** mean 81% of the game is implemented.
It does **not** mean 81% of the final runtime is validated.
It does **not** mean C01-C08 are complete.

## Why the remaining 19% is Codex evidence work

All 19 remaining points are the unearned portion of the 30-point Codex evidence category. Normal workflow work must not invent:
- GMod Q-menu function/dependency traces;
- Toolgun dispatch semantics;
- missing Physgun native provenance;
- THUG2 state/physics maps;
- THUG2 camera internals;
- animation/board/skeleton behavior;
- HUD/UI/scoring event internals;
- original unified input semantics.

Those are Codex investigation tasks.

The global normal-GPT preparation gap is now closed: the clean main-descended Opus-ready branch is established. Package-specific fresh hashes and final packet assembly remain mandatory execution steps, but they no longer represent an unresolved global-readiness category.

## Subsystem gate reality

Current Opus package state remains:
- O00 Golden Source bench conversion proof: **READY FOR OPUS**.
- O01 Toolgun presentation: **READY AFTER O00 PASS**.
- O02 Q-menu: **WAITING FOR CODEX GAP CLOSURE** (C01 substantial partial).
- O03 Toolgun behavior: **WAITING FOR CODEX GAP CLOSURE** (C01/C02 substantial partial).
- O04 Physgun parity: **WAITING FOR CODEX GAP CLOSURE** (C03 partial).
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
