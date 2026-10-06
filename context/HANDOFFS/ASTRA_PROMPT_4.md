# Astra Prompt 4 — Runtime implementation pass

Paste the following into GPT-6 Astra / Work mode:

> Continue my Fallout New Vegas + Garry's Mod + THUG2 merge from the latest canonical repository state.
>
> Before changing anything, re-read and obey:
> - AGENTS.md
> - context/BOOTSTRAP.md
> - context/GOAL.md
> - context/CURRENT_STATE.md
> - context/ARCHITECTURE.md
> - context/DECISIONS.md
> - context/FAILURE_KNOWLEDGE.md
> - context/HANDOFFS/START_HERE_GPT6_OPUS.md
> - build/handoffs/gpt6_opus/MASTER_EXECUTION_QUEUE.json
> - build/handoffs/gpt6_opus/DEPENDENCY_GRAPH.json
> - build/handoffs/gpt6_opus/REGRESSION_SPEC.json
> - build/handoffs/gpt6_opus/ACCEPTANCE_GATES.json
> - build/handoffs/gpt6_opus/SIDECAR_STRATEGY.json
> - build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json
> - build/handoffs/gpt6_opus/runtime_harness/READY_VERDICT.json
>
> Reconcile GitHub, the local workspace and installed Fallout files before trusting any prior state. Other agents may have changed the project since this prompt was written.
>
> The most recent support preflight I ran reported:
> - GPT-6/Opus handoff preflight: PASS.
> - READY_FOR_IMPLEMENTATION: YES.
> - runtime source drift: false.
> - active main.cpp SHA256: CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5.
> - installed v85 DLL SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
> - active REM_GModTHUG2.esp SHA256: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
> - isolated v88 DLL SHA256: 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.
> - support validator: PASS, 112 checks, zero errors.
>
> Verify all of those again yourself before implementation. Do not assume they are still current.
>
> **Your lane in this pass is runtime integration, native behavior, state machines, debugging and validation.** Do not overwrite normal-ChatGPT workflow/support preparation, and do not silently take over model/visual conversion work that is being left for the dedicated visual/model implementation lane. You may inspect those artifacts as dependencies.
>
> Follow the master execution queue and dependency graph. Do not skip a dependency merely to make a build complete. If a prerequisite is not actually proven, keep the dependent task isolated and do not mark it complete.
>
> **Primary objective for Prompt 4: close the Physics Gun runtime path first.**
>
> 1. Re-run research/validate_gpt6_opus_handoff.ps1 and confirm READY_FOR_IMPLEMENTATION remains YES.
> 2. Inspect G02 and the prepared Physics Gun implementation/evidence package. The unresolved Source-declared models/weapons/v_physics.mdl + VVD + DX90.VTX triplet must not be replaced with an invented or unproven substitute. Use the installed Garry's Mod/Source files and IDA Pro 6.8 only if further native provenance is needed.
> 3. If G02 can be proven, record the provenance/evidence and then implement G04 in an isolated Physgun candidate, following the IDA 6.8 contract and SIDECAR_STRATEGY. If G02 cannot be closed, record exactly why and keep the presentation gap explicit; do not claim G04 complete.
> 4. For G04, implement source-grounded target acquire, stable hold, beam endpoint/highlight feedback, distance adjustment, rotation, freeze/reacquire, normal release, punt/launch, NPC/ragdoll handling and cleanup on weapon switch/cell/save transitions. Preserve the project-required mouse semantics: RMB pickup/hold and LMB launch.
> 5. Use original/source-faithful GMod sounds/materials/beam feedback already inventoried by the project. Do not use Fallout prompts or Fallout substitute effects.
> 6. Keep THUG2 runtime, Q-menu runtime and unrelated weapon presentation untouched unless a dependency requires inspection. Do not combine multiple risky subsystems into one candidate.
> 7. Build the isolated candidate, run all applicable R_BOOT, R_GMOD_WEAPONS and R_PHYSGUN gates, and capture hashes/logs/crash evidence. Do not promote to the main installed DLL unless every applicable gate passes and a human playability check is explicitly completed.
> 8. If the Physgun milestone passes, proceed to the next dependency-ready runtime item from MASTER_EXECUTION_QUEUE.json. Do not jump to G09.
>
> Never reintroduce known failures:
> - no runtime CloneForm skateboard identity;
> - no direct PlayerCharacter::playerNode assumptions;
> - no unsafe retarget bone caches across 3D-root rebuilds;
> - no raw camera-node writes without re-verifying the real camera object/layout in IDA Pro 6.8;
> - no Fallout-style substitute for the GMod Q menu/tool selector;
> - no fabricated/recreated source assets where original evidence is required.
>
> At the end of the pass, update CURRENT_STATE.md, relevant handoff/decision/failure documents, the build manifest and validation evidence. Commit/push the work on a traceable branch. Report exactly: what changed, what compiled, what was actually playtested, which gates passed/failed, current hashes, remaining blockers, and which MASTER_EXECUTION_QUEUE task is next. Do not call the subsystem stable unless the required runtime and human validation gates passed.

This prompt intentionally sends Astra into the next runtime milestone without asking it to redo support inventories or claim the separate THUG2/model work is already complete.
