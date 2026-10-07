# Haiku Final Opus Preflight Audit — 2026-10-07

Status: COMPLETE for the audit scope. Preparation readiness is 81/100 before and after the audit. Safe to start O00: YES, under the conditions in section 2.

Scope and limits: this audit read canonical main 19a8046 and prep/opus-ready-20261007 at 14aee9a (151 commits ahead, 0 behind). It checked 58 required paths (all present), re-ran the three Opus validators, and re-checked live hashes on the Windows machine. It performed no Codex reverse engineering, no runtime test and no gameplay or asset change. It did not open anything under PROJECTS\LCS_MC3_MERGE. It did not read every commit in the 151-commit range. It checked the status documents, the handoffs, the validators and the hashes listed below.

## 1. Repository and branch state

- Canonical repository: bertjerk660-dotcom/REM1.
- Canonical main: 19a8046 ("Merge authenticated GMOD investigation and local staging evidence").
- Preparation branch: prep/opus-ready-20261007 at 14aee9a. Merge-base with main is 19a8046, so it descends cleanly from current main: 151 ahead, 0 behind.
- Audit branch: prep/haiku-final-audit-20261007, based on prep/opus-ready-20261007. It contains only the documentation changes listed in section 6 and the JSON summary.
- Earlier specialist notes: prep/claude-specialist-prep-20261007 at 1471895. Not merged into the audit branch and not part of the Opus launch baseline.
- No codex/* evidence branch exists on origin. No C01-C08 evidence output has landed since the preparation baseline.
- Local Windows clone: C:\Users\BRAD\REM1 on DESKTOP-6PTSS3D.
- Live game workspace, not a Git checkout: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2.

## 2. Exact first task for Opus: O00 Golden Source Bench

Package: O00 Golden Source Bench Conversion Proof. Status: READY FOR OPUS.

Read in this order: context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md (including its Haiku addendum), build/prepared/opus_o00_golden_bench_20261007.json, build/templates/OPUS_O00_CANDIDATE_MANIFEST_SEED.json, and the protections in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md.

Conditions before Opus starts:
- Create the implementation branch from prep/opus-ready-20261007 (14aee9a, or the audit branch commit after it is merged). Record the parent commit in the candidate seed.
- Re-check the source hashes at the start of the work. The visual validator passed today (section 5).
- Keep the output isolated: meshes/rem/golden_bench/bench01a.nif and textures/rem/golden_bench/*, with the disabled sidecar REM_GoldenBench_Test.esp.
- Do not modify the main NVSE DLL, REM_GModTHUG2.esp, or any quarantined candidate.
- Do not hand a candidate to Codex until the freeze-mode validator passes.

Stop rule: a failed O00 is a conversion-pipeline failure. Fix the pipeline before any weapon conversion.

## 3. Tasks that may follow immediately

- Nothing after O00 may begin until O00 has passed the human or runtime gate in its packet.
- O01 Toolgun presentation, O08a Crowbar, O08b Pistol and O08c SMG1 are READY AFTER O00 PASS. They are source-hash-prepared and validator-passed, but they stay gated behind O00.
- Preparation work that does not touch the game (hash re-checks, candidate-seed filling) may run in parallel. Implementation may not.
- Haiku/normal GPT coordination continues on the documentation branch and does not block O00.

## 4. Packages still blocked

| Package | Gate | State | Reason |
|---|---|---|---|
| O02 Q-menu renderer | C01 | WAITING FOR CODEX GAP CLOSURE | C01 is SUBSTANTIAL_PARTIAL, 0 points |
| O03 Toolgun Q-state + Remover/Duplicator | C01 + C02 | WAITING FOR CODEX GAP CLOSURE | C02 is SUBSTANTIAL_PARTIAL, 0 points |
| O04 Physgun parity | C03 | WAITING FOR CODEX GAP CLOSURE | C03 is PARTIAL, 0 points; first-person provenance unresolved |
| O05 THUG2 movement/state/physics/input | C04 + C08 | WAITING FOR CODEX | No C04 or C08 evidence exists |
| O05b THUG2 camera | C05 | WAITING FOR CODEX | Depends on C04 vocabulary |
| O06 THUG2 animation and board attachment | C06 | WAITING FOR CODEX | Depends on C04 vocabulary |
| O07 THUG2 HUD/UI | C07 + C04 event interfaces | WAITING FOR CODEX | No C07 evidence exists |
| O07b THUG2 audio | C04/C06/C07 or a narrow audio addendum | WAITING FOR CODEX | No audio addendum exists |
| O09 cross-system fixes | Codex runtime failure reports | NOT READY | No candidate exists |

Codex gates are all at 0 points (codex_semantic_gate_status_20261007.json). C01 and C02 are SUBSTANTIAL_PARTIAL, C03 is PARTIAL, and C04 through C08 are WAITING_FOR_CODEX. The C01 structural baseline expects five evidence files that are not present (structural_pass false), which is consistent with 0 points.

## 5. Source and hash warnings

Verified on 2026-10-07:
- main.cpp 4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE matches. It labels itself version 85. The older 'version 81' lines are superseded.
- gmod_overlay.inc E6EF0C484AFDDC1A74C02F6BA8A72CD0899D6E80F5BA5459CD61B9C67183250F matches.
- Deployed FNVGModTHUG2.dll D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206 matches runtime_snapshot.json.
- Deployed REM_GModTHUG2.esp 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7 matches runtime_snapshot.json.
- Garry's Mod version files read 260917 / 1920 / prerelease, matching the record.
- THUG2 disc executable SLES_526.21 (PS2, 32-bit little-endian MIPS ELF) hashes 91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1, matching PROVENANCE_INDEX.
- O00 source files match the validator record: bench01a.mdl 8751F7E2..., bench01a.vvd BC9AFFE6..., bench01a.dx90.vtx E651BB00..., bench01a.phy 0EB277C8...

UNRESOLVED DRIFT:
- Deployed Data/meshes/rem/thug2/skateheldx.nif hashes to 1FB3CE190CC0E32D2F06EEC144605CE3E2EB84BE4E3A90A33B227B9639C6D852. The v82 record expects 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A. Either the file changed after the v82 record, or the record is stale. The cause is not established. Do not claim v82 identity for the held board until this is reconciled.

Historical hashes that must not be treated as current: deployed DLL A801DC80F96F6269CB8516ECC47CE48E4FAA2DDB315308A8476F4658D7FB5EF5 and ESP 3E30300C00241A044F73D476F9497716413DA467278A72AFE29CCAE6767DFEBB (both in older CURRENT_STATE text).

Missing dependencies, not to be substituted: v_physics.mdl/.vvd/.dx90.vtx (first-person Physgun), sound/weapons/physgun_on.wav, sound/weapons/flaregun/impact.wav, materials/phoenix_storms/thruster_bump.vtf.

## 6. Contradictions found, and what was done

Fixed in this audit:
1. O01, O08a, O08b and O08c were marked READY FOR OPUS in OPUS_LAUNCH_PREFLIGHT_BASELINE and the scorecard. The board, queue, milestones and launch sequence say READY AFTER O00 PASS. Changed to READY AFTER O00 PASS.
2. The branch commit count was 78 in the scorecard and CURRENT_STATE, 145 in the preflight baseline, and is 151 today. Each figure is now dated.
3. CURRENT_STATE's "Active runtime" section gave superseded DLL, ESP and source-version values. A dated note now points to the live hashes and to runtime_snapshot.json.

Recorded but not fixed (owner or Codex decision needed):
4. skateheldx.nif hash drift (section 5).
5. The owner directive that Opus may investigate when necessary conflicts with the exclusion wording in AGENT_OWNERSHIP.md and LEGACY_ROLE_PATH_MAP.md. An addendum records the directive as D-009 and marks the older wording as superseded for task assignment. The owner should decide whether to rewrite those sections in full.
6. The C01 structural baseline expects evidence paths that do not exist.
7. Superseded or quarantined branches still appear as evidence sources (EVIDENCE_INDEX, PROVENANCE_INDEX, SELECTIVE_BRANCH_RECONCILIATION). Their quarantine labels are present. They are not presented as current, so no change was made.

Gaps closed by addenda:
8. Most Opus packets carried no failure protections. The Haiku addendum now points each live packet to context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md.
9. O00 had no rollback section and did not define 'disabled sidecar'. Both are now defined in the O00 addendum.

## 7. Known failures to avoid

The full list with applicability is in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md. The headline items:
- Skateboard identity must be an ESP-owned persistent WEAP. Do not clone or rebind runtime weapon forms (F001).
- Do not dereference PlayerCharacter::playerNode directly (F002).
- Validate retarget bones and drop caches on root change. Keep the 900 ms camera delay (F003).
- The held board is a BSFadeNode with Prn=Weapon (F004).
- Re-test the LMB enter and holster exit paths after any change (F005).
- Re-check source, hashes and mtimes before every modify, deploy or freeze (F007).
- Suppress the Fallout HUD and top-left alerts in skate mode (F008).
- Physgun acquisition needs GMod-faithful range, a continuous hold loop, and actor effects applied only to the acquired target (F009).
- Grind must come from real world-query eligibility, never a key press (F010).
- The board must reach the feet and the animation set must actually run (F011).
- The GMod prop menu is a placeholder (F012).
- No grenade or type regression after load-order or form changes.
- Input and cursor ownership must be cleaned up when Q closes or a mode ends.

## 8. Active support-sidecar caveats

- REM_GoldenBench_Test.esp is a proposed isolated sidecar for O00. Disabled means absent from the default plugins.txt and loadorder.txt, and enabled only in a recorded candidate load order.
- It is never merged into REM_GModTHUG2.esp or the main NVSE DLL, and its results are never counted as core Fallout, THUG2 or GMod validation.
- The local staging payloads under build/ and the Engineer Station workspace are proprietary. GitHub holds manifests, hashes and provenance only. Do not commit them.
- The validators check the local workspace root for the visual packets. Run them there.
- prep/opus-feed-bundle-20261006 is stale (LOCAL_OPUS_PREFLIGHT_SNAPSHOT warns of this). Do not use it as input.
- Quarantined: prep/pre-opus-thursday, feature/thug2-native-ui-g6, runtime/astra-phase1-input92, and the v84-v92 candidates.

## 9. Candidate-freeze requirements

Before any Opus build goes to Codex (intake checklist section F and launch-sequence phase 4):
- implementation branch and commit, plus the parent commit;
- source hash and DLL hash, and ESP hash if an ESP changed;
- hashes of every mesh, texture, sound and UI output;
- plugins.txt and loadorder.txt, showing sidecar state;
- test save, test location and test inventory;
- rollback steps;
- confirmation that protected files are unchanged;
- the freeze-mode validator passing: python research/validate_opus_candidate_manifest.py <manifest> --mode freeze.

Only preflight has passed so far (O00 seed: 0 errors). Freeze has not been run.

## 10. Post-implementation Codex validation workflow

1. Opus publishes the candidate branch, commit and filled manifest.
2. The freeze validator passes. Normal GPT or Haiku records the candidate identity in CURRENT_STATE.
3. Codex runs the matching runtime pack: context/HANDOFFS/CODEX_O00_GOLDEN_BENCH_RUNTIME_VALIDATION_2026-10-07.md for O00, and the R-packs in context/CODEX_RUNTIME_TEST_PACKS.md.
4. Results are deterministic pass/fail. The O00 visual and collision acceptance is human-observed in Fallout, as its packet requires.
5. Any failure produces a Codex failure report: exact candidate identity, logs or crash evidence, expected versus observed behavior, and the suspected boundary. Opus then fixes the candidate, and Codex regresses the exact fixed build.
6. Only then is a status moved to VALIDATED, using the intake checklist vocabulary.

## 11. Files Opus should read first

1. AGENTS.md
2. CLAUDE.md
3. context/BOOTSTRAP.md
4. context/GOAL.md
5. context/CURRENT_STATE.md (the 2026-10-07 sections)
6. context/AGENT_OWNERSHIP.md (including the 2026-10-07 owner directive)
7. context/DECISIONS.md (D-009, D-010)
8. context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md
9. context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md (including the addendum)
10. build/templates/OPUS_O00_CANDIDATE_MANIFEST_SEED.json
11. build/prepared/opus_o00_golden_bench_20261007.json
12. context/HANDOFFS/HAIKU_FINAL_OPUS_PREFLIGHT_AUDIT_2026-10-07.md (this file)

## Final report

- Preparation readiness before audit: 81/100.
- Preparation readiness after audit: 81/100. Documentation fixes do not raise the score (D-010). No C01-C08 evidence was added.
- Contradictions found: 9 (section 6). Fixed: 3 directly, 2 by addenda. 4 recorded for owner or Codex decision.
- Missing Codex evidence: C01 remaining native and service gaps (+menu dispatch, ModelImage service, spawnlist, search, IconEditor); C02 Toolgun.Single, ToolTracer, RenderScreen, trace range, prediction, Duplicator host and stool closure; C03 first-person provenance, acquisition, controller, rotate, freeze, launch, audio loop, beam renderer, actor state and cleanup; C04 through C08 in full.
- Opus-ready packages: O00. Gated behind O00 PASS: O01, O08a, O08b, O08c.
- Blocked packages: O02, O03, O04, O05, O05b, O06, O07, O07b, O09 (section 4).
- Provenance issues: skateheldx.nif identity drift; the C01 baseline expects absent files; first-person Physgun model and the four other unresolved dependencies (section 5); THUG2 target is PS2 and IDA work must say so.
- Candidate and runtime risks: held-board identity is unproven against the v82 record; the LMB crash history (F005); the Physgun actor-target cause is a source-level candidate, not proven (F009); sidecar leakage if the O00 ESP is enabled by default.
- Safe to start O00: YES. No preparation blocker prevents O00. Its conditions are in section 2.