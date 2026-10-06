# START HERE — GPT-6 / Opus integration handoff

Verified preparation date: 2026-10-06.

## Authority
Read AGENTS.md, context/BOOTSTRAP.md, context/GOAL.md, context/CURRENT_STATE.md, context/ARCHITECTURE.md, context/DECISIONS.md and context/FAILURE_KNOWLEDGE.md before modifying runtime. Actual source/deployed state overrides stale prose. Use IDA Pro 6.8 only.

## Lane ownership
Support agents prepare evidence, manifests, validators, dependency/order planning and documentation. GPT-6/Opus owns visual code, animations, physical model integration and complex runtime/physics implementation. Do not redo staged evidence unless validation fails.

## Execute
1. Run research/validate_gpt6_opus_handoff.ps1.
2. Consume build/handoffs/gpt6_opus/MASTER_EXECUTION_QUEUE.json in dependency order.
3. Use DEPENDENCY_GRAPH.json, REGRESSION_SPEC.json, ACCEPTANCE_GATES.json and SIDECAR_STRATEGY.json as mandatory constraints.
4. Keep risky subsystems isolated until their gates pass.
5. Record build hashes, validation and playtest result before promotion.

## Current prepared facts
- Physics Gun behavior evidence is closed and packaged; runtime implementation is not claimed complete.
- Exact legacy v_physics MDL/VVD/DX90.VTX remains a known presentation provenance gap. Do not silently substitute.
- THUG2 conversion queue contains 85 evidence-backed targets across 16 local level GLBs.
- The old 21 unresolved entries are semantic/unproven geometry identifiers and are excluded from the model queue.
- Two of the 85 prop targets remain review-confidence and require visual identity confirmation before promotion.
- Current deployed THUG2 runtime remains historically unstable until a fresh candidate is playtested.

## Do not regress
- No runtime CloneForm skateboard identity.
- No direct PlayerCharacter::playerNode assumptions.
- No unsafe bone pointer caching across 3D/camera rebuilds.
- No Fallout prompt replacement for GMod Q-menu/tool selection.
- No fabricated/recreated source-game assets when original evidence is required.
- Do not treat historical v59 implementation claims as proof of current runtime stability.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]