# Combine armor render-fix candidate — 2026-10-06

Human observation after the biped-mask test:
- Combine armor remained invisible.
- Player head and hands became visible again.
- Slave collar and Pip-Boy remained visible.
- This confirms the broad 0x461F biped mask was hiding normal body regions, but was not the root cause of the missing Combine mesh.

Static root-cause evidence:
- Combine wearable NIF NiMaterialProperty alpha was 0.0.
- Fallout Remnants Power Armor donor NiMaterialProperty alpha is 1.0.
- A material alpha of 0.0 makes the Combine mesh fully transparent.
- Original test ESP also had no female biped/world model subrecords.

Render-fix candidate:
- Corrected NIF: Data\meshes\rem\gmod\armor\CombineSoldierFullBody_alpha1.nif
- Corrected NIF SHA256: 78D1ED7732C065EE236FC197D9AFAA4CE5E69341F2B90B59E4FC3E72ECB333B4
- NiMaterialProperty alpha corrected from 0.0 to 1.0 only. Shader flags and skin data were not changed in this pass.
- New sidecar: Data\REM_CombineArmor_Test_RenderFix.esp
- Sidecar SHA256: E9B0D5E071302D36B8B70FA0130DE3721321BB379A92DE76A173A0797C412297
- BMDT biped mask remains donor-proven 0x00000004 with armor flags 0xA0.
- Male biped MODL -> rem\gmod\armor\CombineSoldierFullBody_alpha1.nif
- Female biped MOD3 -> rem\gmod\armor\CombineSoldierFullBody_alpha1.nif
- Male/Female world paths -> rem\gmod\Combine_Soldier.nif

Next-start plugin order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_RenderFix.esp

Validation:
- NIF material alpha readback = 1.0.
- Sidecar contains MODL, MOD2, MOD3, MOD4.
- Byte-level BMDT = 424d4454080004000000a0000000.
- Human runtime validation is pending after a full FalloutNV.exe restart.
- If still invisible, next isolated candidate is BSShaderPPLightingProperty shader flags; do not change skin/bind/partition data until the alpha-corrected model has been tested.
