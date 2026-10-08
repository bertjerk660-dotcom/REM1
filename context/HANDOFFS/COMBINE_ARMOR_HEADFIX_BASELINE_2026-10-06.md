# Combine armor head-fix baseline — 2026-10-06

Latest human result:
- Previous alignment-fix corrected the backwards head.
- That same candidate made torso, back and shoulders visibly worse.

Conclusion:
- Head correction is validated.
- Bone-local anisotropic torso-depth scaling is rejected. Different Source/Fallout spine, neck and shoulder local frames make that approach deform the back/shoulders.

New baseline:
- Reverted torso/back/shoulder retargeting to the prior uniform 1.75 Source->Fallout local scale.
- Kept only the validated Head1 180-degree local-X correction.
- Retains all previously validated render fixes: material alpha 1.0, Fallout BSShaderPPLightingProperty flags 0x82000003, and all three generated BSDismember partition flags 257.
- No source weights lost; unmatched source weights = 0.

Artifacts:
- Data\meshes\rem\gmod\armor\CombineSoldierFullBody_headfix.nif
- NIF SHA256: 19289C8A32F256124A5D9A89089762C8791E8231B148313432EA002ED2E0680E
- Data\REM_CombineArmor_Test_HeadFix.esp
- ESP SHA256: 21009FDDD64A956F0C7EDFFCAF0D11D3D8A905D40483798E06E7A9E25D7D19C5

Next-start load order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_HeadFix.esp

Human validation pending:
- head remains forward;
- torso/back/shoulders return to the earlier mostly-correct state;
- armor remains fully visible.

Future torso refinement must use a world-space or region-fit correction, not per-bone local-axis compression.
