# Fallout 3 Combine -> Enclave Asset Handoff

Status: ASSET PREPARATION COMPLETE; FALLOUT 3 REPLACEMENT NOT IMPLEMENTED.

## Scope
Prepare the Source/Garry's Mod Combine Soldier visual assets for a later AI to integrate as an Enclave armor replacement in Fallout 3. Do not edit Fallout 3 Enclave ARMO/ARMA records, NPC inventories, leveled lists, plugins, or deployed game files in this staging step.

## Prepared source asset
- Source visual: installed Garry's Mod / Source Combine Soldier.
- Decompiled reference: build/gmod_batch/Combine_Soldier/decompiled/Soldier_reference.smd
- Converted static/world visual: local Data/meshes/rem/gmod/Combine_Soldier.nif
- Prepared skinned candidate: build/combine_armor/CombineSoldierFullBody.nif
- Candidate SHA256: 90A836EEF689C50994ED6E5BECC7B37CEFA0B32DA6E20D88C34DC193837B6728
- Geometry: 3,535 vertices / 4,682 triangles.
- Skinning: NiSkinInstance, 41 Bethesda humanoid Bip01 bones, zero uncovered vertices, maximum 3 influences/vertex.
- Source geometry contains body plus Combine head/helmet region.
- Texture dependencies: combinesoldier_noalpha.dds and combinesoldier_normal_n.dds under textures/rem/gmod/models/combine_soldier/.

## Validation boundary
The candidate passed static NIF/skin/weight/texture validation against the project's Fallout New Vegas humanoid target. It has not been validated in Fallout 3.

A local Fallout 3 GOTY installation was found at C:/Program Files (x86)/Steam/steamapps/common/Fallout 3 goty. Its Data directory is modded, so loose modded armor must not be treated as a verified vanilla Enclave donor without provenance checking.

## Later AI integration requirements
1. Preserve the original Combine geometry/materials rather than recreating the armor.
2. Verify the actual Fallout 3 humanoid skeleton and vanilla Enclave armor/helmet record/model paths from the installed game/archives.
3. Compare bones, bind transforms, partitions/body slots, shaders, male/female models, helmet/head coverage, and world models.
4. Retarget to the verified Fallout 3 skeleton if needed; do not assume the FNV candidate is runtime-compatible.
5. Split body/helmet only if the Fallout 3 equipment structure requires it, preserving Source geometry.
6. Before replacement, validate an isolated test item across movement/weapon poses, clipping, first/third person, NPC equip, dropped model, save/load, and male/female behavior.
7. Keep the final replacement reversible.

## Reproducibility
Relevant tooling and evidence:
- research/analyze_combine_smd_weights.py
- research/build_combine_fullbody_armor_nif.py
- research/compare_combine_armor_geometry.py
- build/combine_armor/manifest.json
- build/combine_armor/validation.json

Proprietary game assets remain local. GitHub stores tooling, hashes, mappings, validation evidence, and handoff instructions rather than redistributed game assets.
