# Project Evidence Index — 2026-10-07

Purpose: durable index of important technical evidence. This is not itself proof of implementation. "Runtime tested" means a specific human/live-game observation exists; it does not imply exhaustive parity.

| ID | Date | Subsystem | Source / agent | Evidence location | Confidence | Independently verified | Implemented | Runtime tested | Notes |
|---|---|---|---|---|---|---|---|---|---|
| E001 | 2026-10-06 | GMod Q menu | support inventory | context/HANDOFFS/GMOD_OVERLAY_EVIDENCE_2026-10-06.md | high for inventory, medium for full behavior | partial | placeholder only | placeholder visually tested | 105 Lua, 46 VGUI, 29/29 direct UI/material refs staged; real Q menu not implemented. |
| E002 | 2026-10-06 | Toolgun | support inventory | context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md | high for staged source/assets | partial | historical/partial only | not parity-tested | gmod_tool + 40 stools, c_toolgun/w_toolgun and effects/sounds staged. |
| E003 | 2026-10-06 | Physgun | IDA 6.8 + support package | context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md; build/handoffs/gpt6_opus/PREFLIGHT_RESULT.json | high for known evidence package | partial | partial/broken | yes, failed parity | Exact v_physics first-person triplet remains unresolved. |
| E004 | 2026-10-06 | Physgun runtime failures | human playtest | context/CURRENT_STATE.md; context/FAILURE_KNOWLEDGE.md F009 | high | human-observed | yes, defective | yes | Range too short, wrong held-loop audio, actor effect can hit player. |
| E005 | 2026-10-06 | THUG2 skateboard held model | human playtest | context/CURRENT_STATE.md; FAILURE_KNOWLEDGE F004 | high | human-observed | yes | yes | Board visible and correctly positioned in hand. |
| E006 | 2026-10-06 | Skate enter/exit transition | human playtest | context/CURRENT_STATE.md; THUG2_OVERLAY_EVIDENCE_2026-10-06.md | high | human-observed | yes | yes | LMB enters skate mode; holster exits. Must remain regression invariant. |
| E007 | 2026-10-06 | THUG2 HUD | human playtest | context/CURRENT_STATE.md; FAILURE_KNOWLEDGE F008 | high | human-observed | incomplete | yes, failed | Fallout HUD/top-left alerts remain; THUG2 HUD not source-faithful. |
| E008 | 2026-10-06 | THUG2 grind eligibility | human playtest | context/CURRENT_STATE.md; FAILURE_KNOWLEDGE F010 | high | human-observed | defective | yes, failed | G can trigger grind without valid geometry/contact. |
| E009 | 2026-10-06 | THUG2 animation/board-to-feet | human playtest | context/CURRENT_STATE.md; FAILURE_KNOWLEDGE F011 | high | human-observed | defective | yes, failed | Animation set not functioning; board does not transition to feet. |
| E010 | 2026-10-06 | THUG2 source/staging package | support evidence | context/HANDOFFS/THUG2_OVERLAY_EVIDENCE_2026-10-06.md | high for staged inputs | partial | not complete | partial | 17 decompiled Q source files, original physics/controller/trick evidence, 20 parsed board SKA assets, HUD/input package. |
| E011 | 2026-10-06 | Runtime integration map | support/tooling | build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json | high for recorded source snapshot | static hash gate | source exists | no | Maps physgun, qmenu/toolgun, THUG2 animation/camera/props entry points and native-address verification rules. |
| E012 | 2026-10-06 | Preflight readiness | support validator | build/handoffs/gpt6_opus/PREFLIGHT_RESULT.json; runtime_harness/READY_VERDICT.json | high for static snapshot | validator | n/a | no | Static handoff passes; does not prove gameplay stability. |
| E013 | 2026-10-06 | Curated GMod props | support inventory | GPT6_OPUS_READINESS_2026-10-06.md | high for catalog counts | static | staged | sample runtime validation pending | 290 curated entries: 170 FNV + 120 GMod/Source; thumbnails audited. |
| E014 | 2026-10-05/06 | Skate crash safety rules | crash diagnosis/history | context/FAILURE_KNOWLEDGE.md F001-F005 | high | logs + iterative fixes | mitigations exist | mixed | Preserve persistent ESP-owned board, GetNiNode path, root-aware retarget caches. |
| E015 | branch-only | Support tracker/regression packs | GPT workflow lane | prep/code-preservation-20: context/SUPPORT_20_POINT_TRACKER.md; REGRESSION_PACKS.md | medium until reconciled | branch static evidence | support artifacts only | some human gates pending | Useful support work is not present on main; do not claim canonical promotion. |
| E016 | branch-only | THUG2 v84-v92 candidate work | specialist branches | feature/thug2-native-ui-g6; runtime/astra-phase1-input92; prep/pre-opus-thursday | medium until branch reconciliation | branch manifests vary | candidate implementations | not uniformly verified | Version number alone is not evidence of superiority or stability. |

| E017 | 2026-10-06 branch snapshot | THUG2 executable/skeleton provenance | support provenance | prep/code-preservation-20: context/THUG2_INTEGRATION_PROVENANCE.json | high for recorded snapshot; current hash re-check required | target bone names statically validated | no final animation integration implied | no | PS2 SLES_526.21 hash, FNV skeleton hash, IDA 6.8 native function evidence and zero-missing-target bone-name map recorded. Unlocks C04/C06 inputs after re-check. |
| E018 | 2026-10-06 branch snapshot | installed GMod interface provenance | support inventory | prep/code-preservation-20: context/GMOD_INTERFACE_PRESERVATION.md | high for recorded installed snapshot | inventory cross-referenced by support manifests | no final Q/Tool/Physgun implementation implied | no | Steam build/VPK hashes, 105 Lua, 40 stools, 46 VGUI and 29 resolved UI asset refs. Unlocks C01-C03 inputs after installed-content hash re-check. |
| E019 | 2026-10-06 branch snapshot | GMod/HL weapon model staging | support audit | prep/code-preservation-20: builds/gmod_hl_weapon_staging_audit_20261006.json | high for staging coverage; current path/hash re-check required | static audit | staged only | no | 71/71 concrete model refs staged; final FNV attachment/presentation remains Opus work and Codex validation. |
| E020 | 2026-10-06 | Physgun view-model provenance gap | support audit | prep/opus-feed-bundle-20261006: build/prepared/pre_opus_20261006/physgun_provenance_gap.json | high | corroborates main preflight gap | blocked | no | v_physics MDL/VVD/DX90.VTX unresolved; do-not-substitute remains active. C03 must close. |
| E021 | 2026-10-07 | branch reconciliation | GPT workflow coordination | context/SELECTIVE_BRANCH_RECONCILIATION_2026-10-07.md | high for classification | based on GitHub branch inspection | n/a | n/a | Separates promotable evidence from historical/runtime-candidate state and prevents wholesale merges/version-number promotion. |

## Intake rule for new evidence

Every new Codex or Opus report should add or update an entry with:
- source agent and date;
- subsystem;
- exact repository path/commit or build/hash;
- what was directly observed versus inferred;
- confidence;
- whether another source independently supports it;
- implementation status;
- runtime-test status;
- downstream task unlocked.

Never convert an inference or branch-only candidate into a verified fact without the required evidence and runtime gate.
