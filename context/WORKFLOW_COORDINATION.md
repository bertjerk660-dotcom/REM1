# Workflow Coordination — Prompt 4 onward

Verified coordination checkpoint: 2026-10-06 19:33 BST.

## Current verified preflight
- GPT-6/Opus handoff preflight: PASS.
- runtime-harness readiness: READY_FOR_IMPLEMENTATION = YES.
- active runtime-source drift: false.
- support validator: PASS, 112 checks, zero errors.
- active source SHA256: CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5.
- installed v85 DLL SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- active REM_GModTHUG2.esp SHA256: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
- isolated v88 DLL SHA256: 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.
- no FalloutNV/FNVScript/xFOEdit process was active when the workflow checkpoint was captured.

This proves implementation readiness only. It does not prove gameplay stability or satisfy promotion/human-playability gates.

## Lane boundaries
Normal ChatGPT/support lane owns orchestration, repository reconciliation, manifests, dependency tracking, preflight/static validation, asset/source inventories, provenance, sidecar isolation, playtest-plan preparation, build-history recording and project-knowledge updates.

GPT-6 Astra owns runtime integration/debugging/state-machine work, native behavior, runtime validation and candidate testing. The dedicated visual/model lane owns complex model conversion/visual implementation where assigned. Do not silently reassign work between lanes; record blockers instead.

## Active workflow queue
1. Re-run the workflow checkpoint before every Astra/Opus implementation pass and immediately after any candidate build/deploy.
2. Track every candidate by branch, commit, parent build, DLL/ESP hashes, source hash, target MASTER_EXECUTION_QUEUE task and validation status.
3. Enforce dependency order from MASTER_EXECUTION_QUEUE.json and DEPENDENCY_GRAPH.json; compile success is not completion.
4. Keep one risky subsystem per isolated candidate using SIDECAR_STRATEGY.json.
5. Prepare the exact regression suite from REGRESSION_SPEC.json before deployment; capture preflight and postflight evidence around every human test.
6. Reconcile GitHub, local workspace and installed hashes before any promotion because concurrent agents can change state.
7. Update CURRENT_STATE.md only with verified facts; record new crash/failure knowledge in FAILURE_KNOWLEDGE.md with symptom, cause evidence, proven fix and prevention rule.
8. Preserve all proprietary game assets locally; commit only project-authored tooling, hashes, manifests, mappings, extracted behavioral knowledge and reproducible instructions.
9. Maintain the known Physgun first-person provenance gap explicitly until the Source-declared v_physics MDL/VVD/DX90.VTX triplet is proven or source behavior proves another exact path.
10. Do not promote any subsystem to the main installed runtime until applicable acceptance gates include build, assets, boot, reachability, behavior, cleanup, save/load, regression and human playability.

## Immediate support action already started
research/capture_project_workflow_checkpoint.ps1 now automates the repeated preflight workflow: protected-file hashes, GPT-6/Opus handoff validation, support validation, active-process detection and a machine-readable build/workflow/CURRENT_CHECKPOINT.json. It performs no deployment or runtime mutation.

The current static snapshot is builds/workflow_checkpoint_20261006_prompt4.json.
