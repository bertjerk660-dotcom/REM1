# Haiku Session Findings — 2026-10-07

Status: findings record for the audit lane. Documentation only. No runtime, asset or game-file change. No reverse engineering, IDA work, decompilation or runtime test was performed.

## 1. Access and environment (no credentials recorded)
- Desktop Commander device: DESKTOP-6PTSS3D, online.
- Git for Windows 2.55. Git identity: bertjerk660-dotcom with the GitHub no-reply address.
- GitHub CLI 2.102.0, signed in as bertjerk660-dotcom through device-code login.
- Working clone: C:\Users\BRAD\REM1. An earlier clone attempt stalled on a credential prompt and left a broken .git folder. That folder was removed and the repo reinitialised against origin. The clone folder also holds an NVIDIA Corporation\umdlogs folder created by the graphics driver. It is untracked and must not be committed.
- Python 3.14.8 via the py launcher, used to run the validators.

## 2. Repository state at the time of this record
- Canonical main: 19a8046 (unchanged).
- prep/opus-ready-20261007: 2c3f72c after the fast-forward merge of prep/haiku-final-audit-20261007. 152 ahead of main, 0 behind.
- prep/claude-specialist-prep-20261007: 1471895. Earlier specialist notes. Not merged. Not part of the Opus launch baseline.
- No codex/* branch exists on origin. No C01 to C08 evidence output has landed.
- Required paths for the Opus packet set: 58 checked, 0 missing.

## 3. Validator results (re-run 2026-10-07 after the documentation edits)
| Validator | Inputs | Result |
|---|---|---|
| research/validate_opus_visual_source_packets.py | --root = local FNV_GMOD_THUG2 workspace | TOTAL PASS, 87 files, 0 errors |
| research/validate_opus_candidate_manifest.py | build/templates/OPUS_O00_CANDIDATE_MANIFEST_SEED.json, --mode preflight | PREFLIGHT PASS, 0 errors |
| research/validate_opus_gate_state.py | opus_readiness_gate_matrix and codex_semantic_gate_status (build/prepared) | GATE STATE PASS, readiness 81/100, 0 errors |

These results check metadata and hashes only. They do not validate any game feature. Freeze mode has not been run.

## 4. Live file identity on the Windows machine
| File | Location | SHA256 (first 16 hex) | Against record |
|---|---|---|---|
| main.cpp | workspace third_party NVSE plugin folder | 4517D804A6B61B51 | matches runtime snapshot |
| gmod_overlay.inc | workspace third_party NVSE plugin folder | E6EF0C484AFDDC1A | matches runtime snapshot |
| FNVGModTHUG2.dll | Fallout New Vegas Data\NVSE\Plugins | D6C8881699852B6A | matches runtime snapshot |
| REM_GModTHUG2.esp | Fallout New Vegas Data | 0A81B42990EEA170 | matches runtime snapshot |
| skateheldx.nif | Fallout New Vegas Data\meshes\rem\thug2 | 1FB3CE190CC0E32D | DRIFT: v82 record expects 4F12178D6D4004B2 |
| SLES_526.21 | Engineer Station DUMPS\thug2 | 91C3D11BF0F1546F | matches PROVENANCE_INDEX |
| garrysmod.ver | Steam GarrysMod folder | 260917 / 1920 / prerelease | matches record |

Full hashes are in build/prepared/haiku_final_opus_preflight_audit_20261007.json.

Unresolved drift: the deployed skateheldx.nif does not match the v82 record. The cause is not established. Do not claim v82 identity for the held board until this is reconciled.

## 5. THUG2 source identity (verified locally)
- Engineer Station\Tony Hawk's Underground 2 (Europe, Australia)\ holds one ISO file of about 3.13 GB. Engineer Station also holds the matching 7z archive of about 2.07 GB.
- Engineer Station\DUMPS\thug2\ holds the extracted disc contents.
- SYSTEM.CNF: BOOT2 = cdrom0:\SLES_526.21;1, VER 1.00, VMODE PAL.
- SLES_526.21 header: ELF magic, 32-bit, little-endian, machine type 0x0008 (MIPS).
- No PC THUG2 executable was located in the default install locations.
- Conclusion: the disc target is the PAL PS2 build. Confirmation as the investigation target is an open owner decision.
- Scope limit: only the boot configuration, the ELF header and the top-level disc listing were examined.

## 6. Ownership routing (owner instructions this session)
- Reverse engineering of THUG2 and Garry's Mod belongs to Claude Opus, under D-009. GPT-5.5 coordinates it. Haiku and GPT-5.5 do not perform it. Recorded as D-011 in context/DECISIONS.md.
- AGENT_OWNERSHIP.md and LEGACY_ROLE_PATH_MAP.md still name Codex as the investigator and exclude Opus from investigation. That wording conflicts with D-009 and D-011. A rewrite is drafted in the GPT-5.5 prompt for owner approval. It has not been applied.
- Whether Codex keeps any investigation role is an open owner decision. Until it is answered, Opus is the investigator and Codex is the runtime validator.

## 7. Contradictions and drift
Fixed in 2c3f72c:
- O01, O08a, O08b and O08c were marked READY FOR OPUS in the preflight baseline and scorecard. Corrected to READY AFTER O00 PASS.
- Branch commit counts of 78 and 145 were dated against the live count.
- Superseded runtime hashes in CURRENT_STATE were annotated.
- Most Opus packets had no failure protections. An addendum now links each live packet to context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md.
- O00 had no rollback section and did not define a disabled sidecar. Both are now defined.

Open:
- skateheldx.nif identity drift (section 4).
- Ownership wording conflicts with D-009 and D-011 (section 6).
- The C01 structural baseline expects five evidence files that do not exist (structural_pass false).
- Superseded branches are still cited as evidence sources. They carry quarantine labels, so they were left unchanged.

## 8. Failure-protection coverage
Before the addenda, these packets had no protection keyword hits at all: O02 Q-menu preassembly, THUG2 animation and board, and THUG2 HUD. Most other packets had one or two hits. Keyword counts are indicators only. After the addenda, every live Opus packet links to the protections file. No packet cites failure IDs by number, so the protections file is the authoritative list.

## 9. Process lessons
- Searches for failure IDs must use word boundaries. An unbounded F0\d\d pattern matched inside SHA-256 hex strings and produced false references. The first pass was discarded and re-run before any conclusion was drawn.
- The visual validator's recorded report points at the local workspace root. Reruns must use the same root or they will not reproduce the recorded result.
- The validators write a JSON file only when --report is given. Reruns in this pass omitted it, so the working tree stayed clean.
- Windows PowerShell stalled once on a nested pipeline with string interpolation. Splitting the command into smaller steps resolved it.
- Git reported CRLF conversion warnings when LF text was appended. The committed content was not affected.

## 10. Not done
- No reverse engineering, IDA work, decompilation or disassembly.
- No runtime test, deployment, or change to the DLL, ESP, NIF or any game file.
- No proprietary payload committed. GitHub holds manifests, hashes and provenance only.
- PROJECTS\LCS_MC3_MERGE was not opened. Only its top-level names appeared in an earlier folder survey, and nothing inside it was read.
- Freeze-mode candidate validation not run, because no candidate exists.

## 11. Open decisions for the owner
1. Confirm SLES_526.21 (PAL PS2) as the THUG2 investigation target.
2. Decide whether Codex keeps any investigation role, or Opus takes all of it.
3. Approve the rewrite of the ownership wording in AGENT_OWNERSHIP.md and LEGACY_ROLE_PATH_MAP.md.
4. Confirm which skateheldx.nif is intended: the deployed file or the v82 record.
5. Decide whether to merge this findings branch into prep/opus-ready-20261007.