# Opus Package Intake Checklist — 2026-10-07

Use this checklist each time Codex finishes C01-C08 or produces a runtime failure report. Normal GPT owns this review/assembly step.

## A. Evidence identity
- [ ] Codex report path exists in GitHub.
- [ ] Branch and commit SHA recorded.
- [ ] Source executable/game build identity recorded.
- [ ] Source files / archive paths recorded.
- [ ] Hashes supplied where meaningful.
- [ ] IDA version requirement satisfied where native reversing was needed (IDA Pro 6.8).
- [ ] Direct observation is separated from inference.
- [ ] Unresolved facts are explicitly marked unresolved.

## B. Evidence completeness
- [ ] Required functions/classes are mapped.
- [ ] Callers/callees or state dependencies are mapped.
- [ ] Important constants and state variables are mapped.
- [ ] Asset/UI/model/audio dependencies are mapped.
- [ ] Device/input semantics are mapped where relevant.
- [ ] Native engine boundaries are identified.
- [ ] Host adaptation requirements are explicit.
- [ ] Existing approximation/current-runtime delta is documented.

## C. Conflict/reconciliation check
- [ ] Compare against EVIDENCE_INDEX.
- [ ] Compare against PROVENANCE_INDEX.
- [ ] Compare against FAILURE_KNOWLEDGE + FAILURE_LEDGER.
- [ ] Compare against CURRENT_STATE.
- [ ] Older Astra/GPT6 labels are treated as historical only.
- [ ] Branch-only runtime claims remain quarantined unless separately validated.
- [ ] Conflicting evidence is recorded, not silently rewritten.

## D. Opus packet contents
Every implementation packet must contain:
1. player-visible objective;
2. source-faithful behavioral specification;
3. reviewed Codex evidence links;
4. function/state/dependency maps;
5. provenance / asset references;
6. exact host adapter/interface contract;
7. implementation boundaries;
8. explicit non-goals;
9. preserved working behavior;
10. known failure modes;
11. acceptance criteria;
12. deterministic Codex runtime test pack;
13. exact artifacts Opus must produce;
14. rollback strategy.

## E. Unlock decision
Use exactly one:
- READY FOR OPUS
- READY WITH PREFLIGHT
- PARTIAL / PACKAGE-SPECIFIC
- WAITING FOR CODEX
- BLOCKED ON PROVENANCE
- BLOCKED ON CONFLICT
- IMPLEMENTED CANDIDATE — WAITING FOR CODEX RUNTIME
- RUNTIME FAILED — OPUS FIX REQUIRED
- VALIDATED

Never use vague “basically ready” wording.

## F. Implementation candidate freeze
Before handing an Opus build to Codex:
- [ ] branch
- [ ] commit
- [ ] source hash
- [ ] DLL hash
- [ ] ESP hash
- [ ] changed asset hashes
- [ ] manifest
- [ ] load order
- [ ] test save
- [ ] test location
- [ ] required inventory/state
- [ ] logs enabled
- [ ] rollback path

## G. Promotion rule
Do not update CURRENT_STATE to claim success until:
- the exact candidate passed the applicable Codex runtime test pack;
- regressions were checked;
- human playability evidence was recorded where required;
- no critical failure entry contradicts the claim.
