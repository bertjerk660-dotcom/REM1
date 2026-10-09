# Combine armor shader-fix candidate — 2026-10-06

Latest human result:
- After the alpha=1.0 render-fix test, the Combine armor remained invisible.
- Player head/hands, slave collar and Pip-Boy remained visible.
- Therefore the corrected biped mask is behaving as intended, but the Combine mesh still failed to render.

Static comparison:
- Working Remnants Power Armor first BSShaderPPLightingProperty flags: 0x82000003.
- Combine wearable before this pass: 0x00000000.
- Both use shader type 1.
- Donor flags resolve to: Specular=1, Skinned=1, RemappableTextures=1, ZBufferTest=1.
- Missing Skinned/ZBuffer shader flags are a strong render-failure candidate for a skinned armor mesh.

Candidate:
- NIF: Data\meshes\rem\gmod\armor\CombineSoldierFullBody_shaderfix.nif
- NIF SHA256: F5E3E1998AB8C073BDE918FC62CEA6483339AD3886D4FD40AFA728E8526869E9
- Material alpha remains 1.0.
- BSShaderPPLightingProperty shader flags changed only from 0x00000000 to donor 0x82000003.
- Shader type remains 1.
- Skin, bones, partitions, transforms and textures are unchanged in this pass.
- ESP: Data\REM_CombineArmor_Test_ShaderFix.esp
- ESP SHA256: 8E77CB7B9E24F92F380630C2A6DB04417D6F769B363D69D5E67234C6589083F3
- Male and female biped paths both point to CombineSoldierFullBody_shaderfix.nif.
- BMDT remains donor-proven 0x00000004 / armor flags 0xA0.

Next-start plugin order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_ShaderFix.esp

Validation:
- NIF readback alpha = 1.0.
- NIF readback shader flags = 0x82000003.
- ESP MODL/MOD3 paths validated as full .nif paths.
- Human runtime retest requires a full FalloutNV.exe restart.
- If still invisible, the next isolated target is the BSDismemberSkinInstance partition/body-part mapping or bind data, not another ARMO slot change.
