# Opus visual implementation start prompt

Continue the Fallout New Vegas + Garry's Mod + THUG2 merge from canonical repository bertjerk660-dotcom/REM1 and the authorized Windows workspace.

Read in order:
1. AGENTS.md
2. context/BOOTSTRAP.md
3. context/GOAL.md
4. context/CURRENT_STATE.md
5. context/ARCHITECTURE.md
6. context/DECISIONS.md
7. context/FAILURE_KNOWLEDGE.md
8. context/HANDOFFS/START_HERE_GPT6_OPUS.md
9. build/handoffs/gpt6_opus/EXECUTION_SEQUENCE.md
10. build/handoffs/gpt6_opus/feed_bundle/OPUS_VISUAL_QUEUE.json
11. build/handoffs/gpt6_opus/feed_bundle/ASSET_REFERENCE_INDEX.json
12. build/handoffs/gpt6_opus/feed_bundle/CODE_CONTEXT.md

Before changing anything, run research/validate_gpt6_opus_handoff.ps1 and research/validate_opus_feed_bundle.ps1. Stop on source/hash drift.

Ownership:
- Opus: visual/model/material/rigging/conversion/animation implementation plus visual integration code.
- GPT-6 Astra: native/deep runtime mechanics, Physics Gun manipulation mechanics, real Q-menu compatibility runtime, THUG2 movement/physics/camera state machine, crash-sensitive NVSE hooks and final runtime promotion.
- Normal ChatGPT: orchestration, evidence, manifests and validation planning.
- IDA Pro 6.8 only when reverse engineering is required.

Start with O01 only: authentic HL2 models/props_c17/bench01a.mdl golden-prop proof. Do not batch-convert further assets until O01 passes static and human runtime gates. Keep deployed v85 DLL/ESP protected and use isolated candidates/sidecars.

Do not fabricate or recreate missing original assets. The models/weapons/v_Physics.{mdl,vvd,dx90.vtx} provenance gap stays explicit unless resolved from authentic installed source evidence.

After each Opus task return: exact changed files, source/output hashes, implementation manifest, static validation result, exact candidate identity, human runtime evidence when run, blockers, and rollback instructions. Compilation alone is not completion.