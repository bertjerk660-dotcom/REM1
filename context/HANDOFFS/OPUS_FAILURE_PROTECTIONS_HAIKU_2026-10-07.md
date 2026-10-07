# Opus Failure Protections — Haiku audit 2026-10-07

Purpose: give every Opus package a single list of proven failure protections, so Opus does not repeat documented failures. Rules come from context/FAILURE_KNOWLEDGE.md (F001-F012) and context/FAILURE_LEDGER.md. This file adds no new failures. Each protection names the packets it applies to.

## Protections

| ID | Source failure | Protection Opus must keep | Applies to |
|---|---|---|---|
| P-F001 | Runtime skateboard CloneForm / serialized weapon forms caused load crashes (v73-v78) | Skateboard identity is an ESP-owned persistent WEAP. Never clone or rebind runtime weapon forms during load. | THUG2 core, animation/board, O01, O06, O08a, O08b, O08c |
| P-F002 | Direct PlayerCharacter::playerNode dereference crashed skate activation | Use TESObjectREFR::GetNiNode() for 3D roots. Defer animation binding until an active 3D root exists. Never assume conditional playerNode fields stay valid across camera or 3D transitions. | THUG2 camera, animation/board, core |
| P-F003 | Unsafe retarget bone caching across camera and root rebuilds | RTTI-validate every target as NiAVObject. Track the owning NiNode root. Discard caches when the root changes. Validate clip bounds and finite quaternions. Keep the 900 ms delay after camera transition unless new evidence replaces it. | THUG2 animation/board, camera |
| P-F004 | Held skateboard invisible (wrong NIF container) | Held board uses a BSFadeNode root with Prn=Weapon and authentic board geometry. Human playtest on 2026-10-06 confirmed visibility and hand placement. The live deployed NIF hash has drifted from the v82 record (see CURRENT_STATE). Re-verify before any candidate claim. | THUG2 animation/board, O01, O08a, O08b, O08c |
| P-F005 | v80/v81 LMB skate activation crash (c0000005) | Treat the LMB enter path and holster exit path as a regression risk. Re-test both after any change to the skate or camera path. | THUG2 core, camera, O07b |
| P-F006 | Stale documentation disagrees with source and runtime | Source, deployed hashes and logs override prose. Re-check before any claim. | All packets |
| P-F007 | Concurrent workspace edits | Re-check source version, hashes and mtimes immediately before modify, deploy or candidate freeze. Do not overwrite newer state from stale reads. | All implementation and freeze steps |
| P-F008 | Fallout HUD and top-left alerts stayed visible in skate mode | Suppress the Fallout HUD while THUG2 mode is active. Remove Fallout top-left alerts from skate mode. Restore the Fallout HUD on exit. | THUG2 HUD, unified input, O07 |
| P-F009 | Physgun short usable range, wrong held-target loop audio, and actor unconscious effect applied to the player | Acquisition range follows the GMod semantics that Codex documents. Held-state audio is a continuous loop with start and stop. The acquired target stays distinct from PlayerCharacter, and actor ragdoll or unconscious handling applies only to the acquired target. Source-level candidate: the pushactoraway player argument (unverified until Codex isolates it). | O04, GMod Physgun packet |
| P-F010 | G started grinding anywhere | Grind entry requires THUG2 eligibility from real world-query evidence (geometry, contact, state). A key press alone never creates a grind state. | THUG2 core, O07b |
| P-F011 | Board did not move from hand to feet; THUG2 animation set not functioning | Preserve enter and exit. Repair attachment, animation selection, retargeting and blending. Do not treat mode-switch success as runtime success. | THUG2 animation/board, THUG2 core |
| P-F012 | Visually correct GMod prop menu is a placeholder | The placeholder is not the Q menu. Final acceptance needs the source-faithful GMod Q/spawn-menu port. | O02, O03, GMod Q-menu packet |

## Cross-cutting protections (not F-numbered in the ledger but proven by handoffs)

- Input ownership cleanup: closing Q, leaving skate mode or changing weapons must not leave stuck input or cursor state. Ownership follows context/INPUT_OWNERSHIP_MATRIX.md. Applies to O02, O03, O04 and unified input.
- No grenade or type regression: a load-order or weapon-form change once made the skateboard behave like a grenade (THUG2_OVERLAY_EVIDENCE_2026-10-06). Re-test weapon identity and type after any load-order or form change.
- Support sidecars stay isolated: sidecar plugins such as REM_GoldenBench_Test.esp are never counted as core validation and are never merged into REM_GModTHUG2.esp.
- Build identity before runtime claims: record DLL, ESP, NIF and source hashes for every candidate. Use the identities in the CURRENT_STATE 2026-10-07 audit section.
- Quarantined candidates are not promoted by version number: v84 through v92, feature/thug2-native-ui-g6, prep/pre-opus-thursday and runtime/astra-phase1-input92 stay quarantined (RUNTIME_CANDIDATE_QUARANTINE.md).

## Gaps the Haiku audit found

- Most Opus packets contain no protection references. The O02 Q-menu preassembly, THUG2 animation/board packet and THUG2 HUD packet had none. The Haiku audit appended a pointer to this file to every live Opus packet.
- No Opus packet cites failure IDs (F001-F012) by ID. The packets state protections in prose or not at all, so this table is the authoritative list.