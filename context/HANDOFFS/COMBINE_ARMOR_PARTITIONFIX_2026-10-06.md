# Combine armor partition-fix candidate — 2026-10-06

Latest human result:
- With alpha=1.0 and Fallout shader flags applied, only the character's right lower leg became visible while the rest of the Combine armor remained missing.
- Head, hands, slave collar and Pip-Boy remained visible.
- This strongly indicates only one skin partition was being rendered.

Static evidence:
- Combine BSDismemberSkinInstance had three partitions:
  - partition 0: part_flag 257, body_part 0
  - partition 1: part_flag 0, body_part 0
  - partition 2: part_flag 0, body_part 0
- The only rendering fragment observed matches the fact that just partition 0 had Fallout's visible/start-boneset flags.
- Working Fallout armor partitions commonly use part_flag 257 for visible skinned sections.

Candidate:
- NIF: Data\meshes\rem\gmod\armor\CombineSoldierFullBody_partitionfix.nif
- NIF SHA256: 5ABD1284F876B233A12D4F2B0BB2E1708250FA2DFECA69B7581C8D44E5103491
- All three Combine partitions now use part_flag 257.
- body_part values remain unchanged at 0 in this isolated test.
- Alpha remains 1.0.
- BSShaderPPLightingProperty flags remain 0x82000003.
- Skin weights, bone bindings, transforms, texture paths and ARMO biped mask are unchanged.
- ESP: Data\REM_CombineArmor_Test_PartitionFix.esp
- ESP SHA256: CBE0DBAEDD0B0EE49B06AAE4825C46E85BDCB584538FA1FB2497C3D5416A126F
- Male and female biped paths both point to CombineSoldierFullBody_partitionfix.nif.
- BMDT remains 0x00000004 / armor flags 0xA0.

Next-start plugin order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_PartitionFix.esp

Validation:
- NIF readback partitions = [(0,257,0),(1,257,0),(2,257,0)].
- NIF alpha = 1.0.
- Shader flags = 0x82000003.
- MODL/MOD3 full paths verified.
- Human runtime validation requires a full FalloutNV.exe restart.
- If only fragments still render, next isolated target is body-part assignment per partition and then bind/partition vertex mapping.
