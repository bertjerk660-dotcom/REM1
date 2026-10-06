# Pre-Opus preparation handoff — 2026-10-06

Current instruction: preparation only. Opus has not started. Planned first session: Thursday 2026-10-08 (Europe/London).
Read this alongside AGENTS.md and context/BOOTSTRAP.md. This update supersedes older ownership/order wording, not historical evidence.

## Ownership and order
1. Normal ChatGPT prepares inventories, dependency evidence, validators, sidecar specifications, human test packs and provenance.
2. Opus 5.5 implements and validates the authentic Source bench visual/conversion pipeline.
3. ChatGPT records actual bench acceptance. Conversion output or a PASS from static checks alone never unlocks the next gate.
4. Opus proceeds to weapon model/material/rig/animation/presentation work after the bench passes.
5. Astra remains inspection/planning-only until corresponding visual dependencies pass and the user releases runtime work. Astra later owns native mechanics, hooks, runtime input/camera, Q-menu/tool/Physgun compatibility. Opus owns animation creation/conversion/retargeting and attachment transforms.
The existing input92 candidate is historical isolated work, not a deployment or a new instruction to continue runtime.

## Protected state
Freshly verified installed v85 DLL SHA256 BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
Active ESP SHA256 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
v88 remains protected and isolated. v89/v90/v92 remain unpromoted; no candidate was modified by this preparation.
The before/after inventories in build/prepared/pre_opus_20261006 record exact protected files. All three known support ESPs remain disabled.
GitHub main still has obsolete v81/v82 prose. Actual installed hashes override that prose. F011/F012 numbering differs between support and runtime branches: use the failure title/source branch, not the number alone.

## Bench: exact inputs ready, visual acceptance pending
Read build/prepared/pre_opus_20261006/bench_source_packet.json first.
Original installed HL2 archives and member paths/hashes are recorded; byte-identical source companions/materials are staged beneath its source_payload/bench directory.
Model: models/props_c17/bench01a.mdl, with MDL/VVD/DX90.VTX/PHY plus optional legacy LOD/render companions.
Original existing decompile: build/gmod_batch/props_c17__bench01a/decompiled/bench01a.qc and referenced SMDs.
QC bbox: (-12.025, -38.104, -19.786) to (11.667, 38.011, 19.945), source-coordinate extents (23.692, 76.115, 39.731). Actual SMD bounds/triangle counts are separately indexed; these are not approved Fallout units.
Collision source: bench01a_physics.smd + original PHY; QC declares mass 20, concave collision, maxconvexpieces 16 and wood_furniture.
Materials: bench01a.vmt, bench01a.vtf and referenced bench01a_mask.vtf; env_cubemap is an engine-generated resource, not a missing file.
Two concrete legacy issues: missing texture-mask extraction and worker wood_furniture -> FO_HAV_MAT_METAL fallback. The original mask is now staged. Opus must resolve shader/collision-material conversion rather than silently retaining the metal fallback.
Do not treat the already-existing live bench NIF or old batch log as a golden acceptance result.

## Expected isolated Fallout output contract
Proposed sidecar name: REM_GoldenBench_Test.esp; unique record EDID REM_GoldenBench01a. These are specifications, not created records.
Opus/record preparer chooses and documents STAT versus MSTT based on intended physical behavior. Do not invent a FormID before the sidecar exists.
Candidate-only mesh path: meshes/rem/golden_bench/bench01a.nif; candidate textures under textures/rem/golden_bench/.
Use the existing project FNV NIF version/conventions and a host-compatible root/shader/collision hierarchy, verified against a working FNV donor. No absolute development paths, missing shader textures or geometry substitutions.
The manifest must map original geometry, UVs, material groups, scale/axis transform and source collision to the output; require source/converted bounds comparison and actual collision testing.
No active DLL or REM_GModTHUG2.esp replacement. Sidecar remains disabled until an explicitly authorized isolated human test.

## Tools already present
converter_inventory.json lists exact paths/hashes for Crowbar, Blender, VTFCmd and project converter scripts.
Existing converters can write directly into Fallout Data. Opus must isolate output destinations before running them.
No converter, IDA session, compilation or game was launched during this preparation.

## Weapon packets after bench PASS
Ten presentation packages are indexed: c/w Tool Gun, w_physics, candidate c_superphyscannon, c/w crowbar, c/w pistol and c/w SMG1.
Each packet contains exact model companions, archive hashes, material dependency closure, QC sequences/bones/attachments, source bounds and existing package-file hashes.
c_superphyscannon is not proven equivalent to the missing declared v_Physics first-person model. The MDL/VVD/DX90.VTX provenance gap remains BLOCKED. Do not fabricate a replacement.
Do not activate native tool/Physgun mechanics to test presentation.

## THUG2 and curated content
72 checked source/evidence payloads match: 17 controller/trick/physics scripts, 49 UI/font/audio assets, six original board-animation assemblies.
Board assemblies are existing data, not proof of rig/attachment correctness. 51 earlier animation export failures and native handler/camera evidence gaps remain owner work.
The 85-target conversion/orchestration queues agree by level+identifier; 16 source level GLBs are indexed and structurally checked. The 20-item diversified review wave agrees with leaf review and promotion ledger.
The former 21 identifiers remain semantic/unproven geometry references, not missing models. Proximity candidates are not visually confirmed standalone props.
Original Q-menu/tool inventories and the 290-prop content adapter remain prepared inputs, not implemented runtime.

## Validation and history
Existing support validator: 112 checks passed.
New pre-Opus validator: 1267 checks passed, including missing/stale-file rejection, malformed GLB rejection, sidecar enablement rejection, archive/staged identity and protected hashes.
One old release-manifest hash was stale: build/validation/prop_support_phase4.json. The release overlay records both old and current hashes; previous manifests/history are retained.
No runtime/human visual pass is claimed. Human test templates are in human_playtest_checklists.json.
Re-run research/validate_pre_opus_packets.py --root <workspace> before using these packets. A failure blocks use/promotion until explained.
