# Codex C03 — Physics Gun provenance and remaining native behavior closure

## Objective
Close the remaining Garry's Mod / Source Physics Gun evidence gaps so **Claude Opus** can implement/fix the final FNV integration and **Codex runtime-validation pass** can validate it at runtime.

Codex owns investigation only. Do not patch the live game.

## Existing evidence to reuse
Do not redo proven work. Read:
- context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md
- context/HANDOFFS/GMOD_OVERLAY_EVIDENCE_2026-10-06.md
- context/CURRENT_STATE.md
- context/FAILURE_KNOWLEDGE.md, especially F009
- build/handoffs/gpt6_opus/PREFLIGHT_RESULT.json
- build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json
- existing IDA 6.8 Physgun evidence/implementation manifests referenced by the handoff.

## Required questions
1. Resolve the exact current first-person presentation path associated with Source/GMod's declared `models/weapons/v_physics.mdl`.
2. Determine whether the missing MDL/VVD/DX90.VTX triplet is expected to come from another mounted Source game/content package, generated/mounted content, or whether the actual current GMod path uses another proven representation.
3. Record exact provenance and hashes for any confirmed source package. Do not accept a visually similar substitute.
4. Confirm source-faithful target acquisition range and trace/filter rules.
5. Confirm hold-distance behavior and distance adjustment semantics.
6. Confirm target transform update, rotation and angular behavior.
7. Confirm freeze/unfreeze/reacquire semantics.
8. Confirm ordinary release/drop versus punt/launch behavior and inputs.
9. Confirm actor/NPC/ragdoll behavior and which object receives state changes.
10. Trace continuous held-beam audio start/loop/stop semantics and exact sound events/assets.
11. Trace beam/glow/highlight endpoint/state hooks and color relationships.
12. Confirm cleanup behavior on weapon switch, target destruction, cell transition, death/load and invalid target.
13. Identify any remaining native Source interfaces that require IDA Pro 6.8 evidence.
14. Compare these source findings directly against the current FNV failures: short range, wrong hold-loop audio, PlayerCharacter incorrectly receiving actor effect.

## Required output
Create/update:
- context/CODEX/GMOD_PHYSGUN_C03_EVIDENCE_2026-10-07.md
- build/evidence/gmod_physgun_c03/viewmodel_provenance.json
- build/evidence/gmod_physgun_c03/native_behavior_map.json
- build/evidence/gmod_physgun_c03/audio_visual_state_map.json
- build/evidence/gmod_physgun_c03/fnv_failure_delta.json
- build/evidence/gmod_physgun_c03/opus_interface_contract.json

The final report must clearly state what is:
- already proven,
- newly proven,
- still unresolved,
- directly contradicted by current FNV runtime behavior,
- ready for Opus implementation.

## Stop condition
Stop once Opus can implement the remaining Physgun parity work without guessing provenance or source semantics.

Do not modify the FNV runtime. Codex owns the subsequent live-game validation pass after Opus implementation.
