# Opus Readiness 81 → 100 Closure Plan — 2026-10-07

Purpose: define the exact remaining work required for **100% preparation readiness for Claude Opus** without awarding readiness for unsupported assumptions.

This is preparation readiness, not game-completion percentage.

GitHub tracker: issue #5 — `Opus readiness: close C01-C08 evidence gates to reach 100%`.

## Current position

After normal-GPT reconciliation is moved onto the clean main-descended branch `prep/opus-ready-20261007`, the score becomes:

**81 / 100**

The final 19 points are exclusively evidence-gated. Normal GPT must not manufacture them.

## 81-point baseline composition

- product/architecture/ownership: 10/10;
- source/asset provenance and staging: 15/15;
- branch reconciliation/durable memory: 10/10 on the clean branch;
- Codex implementation-grade evidence: 11/30;
- Opus implementation packets: 15/15;
- acceptance/runtime-test preparation: 10/10;
- runtime-candidate safety: 5/5;
- Opus launch/runbook clarity: 5/5.

## Exact remaining 19 points

| Gate | Points | Current state | What earns the points | Unlocks |
|---|---:|---|---|---|
| C01 GMod Q-menu closure | 3 | substantial partial | original/native opener dispatch, ModelImage/icon service, spawnlist/search/editor closure, final host interface contract | O02 |
| C02 Toolgun closure | 3 | substantial partial | ToolTracer/RenderScreen/audio, trace range/filter, prediction/realm and supported Duplicator host representation | O03 |
| C03 Physgun closure | 3 | partial | exact FP provenance, acquisition/controller/launch/freeze/audio/render/actor-state/cleanup evidence | O04 |
| C04 THUG2 state/physics | 3 | required | complete free-roam state machine, movement/physics, collision/grind/manual/lip eligibility and host-world contract | O05 |
| C05 THUG2 camera | 2 | required | update functions, state coupling, smoothing/collision/reset and host-safe adapter | O05b |
| C06 THUG2 animation/board | 2 | required | implementation-grade animation catalogue, skeleton/bone contract and board attachment state machine | O06 |
| C07 THUG2 HUD/UI | 2 | required | score/combo/SPECIAL/balance/popups, assets/fonts/layout and event/renderer contract | O07 |
| C08 unified input | 1 | required | action-level M&K/Xbox map, conflicts, ownership and device-switch contract | O05/O07/input integration |
| **TOTAL** | **19** |  |  | **100/100** |

Points are awarded only after normal GPT reviews the exact evidence package against the original stop condition.

## Execution order

### Track A — GMod closure
Use:
`context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

Codex should close C01, C02 and C03 without repeating the broad GMod investigation already merged to canonical main at:
`19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`

Normal GPT then:
1. reviews C01/C02/C03;
2. converts O02/O03/O04 preassemblies into final implementation packets;
3. updates score to 90/100 if all three pass.

### Track B — THUG2 evidence closure
Run C04 first because movement/state is the dependency hub.

Then C05/C06/C07 can use C04's state/event vocabulary.

C08 should consume both:
- finalized GMod input semantics from C01-C03;
- finalized THUG2 action semantics from C04-C07.

Normal GPT reviews each result and converts the pre-existing Opus placeholders into final packets.

If C04-C08 all pass after Track A, readiness reaches 100/100.

## Zero-credit conditions

No readiness point is awarded for:
- source inventory without behavior trace;
- function names without caller/state evidence;
- screenshots or visual resemblance;
- compile/build success;
- an untested implementation candidate;
- historical Astra/GPT6 text;
- a substitute Physgun model;
- a partial THUG2 animation list missing state bindings;
- a HUD asset list without gameplay-event bindings;
- a control map that does not resolve host conflicts.

## Normal-GPT work remaining after this plan

Normal GPT should continue only in these ways:
- keep the clean branch synchronized with canonical main;
- review each Codex result;
- update evidence/provenance indexes;
- finalize the corresponding Opus packet;
- re-run source/preflight validators;
- update readiness score using this fixed point map;
- preserve quarantine of runtime candidates.

No additional speculative preparation should be allowed to masquerade as the final 19 evidence points.

## 100% definition

Preparation is **100/100** when:
- the clean branch is current with main;
- C01-C08 have all satisfied their original stop conditions;
- final O02-O07/input packets reference reviewed evidence rather than placeholders;
- O00/O01/O08 visual source validation still passes;
- all runtime test packs and candidate-freeze templates are present;
- no known authority/ownership/version contradiction remains.

100% preparation does **not** mean the game is implemented or runtime validated. It means Opus can implement every planned package without first rediscovering core source behavior.


## Next new Codex request

Use:
`context/HANDOFFS/NEXT_CODEX_REQUEST_THUG2_C04_2026-10-07.md`

Reason:
- the broad GMod pass already exists and C01-C03 have a separate narrow closure packet;
- the THUG2 evidence branch currently contains no new evidence beyond main;
- C04 is the dependency hub whose state vocabulary is needed by C05 camera, C06 animation/board, C07 HUD/scoring and C08 unified input.

Ownership rule:
Codex investigates and produces evidence/contracts only. Claude Opus performs all final implementation, retargeting, visual/UI work and gameplay integration.
