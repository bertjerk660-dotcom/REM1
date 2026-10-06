# Combine armor torso-lower-only candidate — 2026-10-06

Human direction:
- Previous head-fix candidate still looked wrong through the torso/back/shoulder region.
- Requested correction: do not rescale or rotate the torso; just lower it.

Implementation:
- Preserved the validated Head1 180-degree local-X correction.
- Preserved material alpha=1.0.
- Preserved Fallout BSShaderPPLightingProperty flags 0x82000003.
- Preserved all three BSDismember partition flags at 257.
- Preserved original uniform Source->Fallout local scale 1.75.
- Added one isolated world-space translation only:
  - TORSO_WORLD_Z_OFFSET = -3.0
  - weighted only by Bip01 Spine, Spine1, Spine2, L/R Clavicle and L/R UpperArm.
- No X or Y vertex coordinates are changed by this correction.
- Head, neck, pelvis, legs, hands and forearms are not directly translated.

Static validation:
- 3535 vertices / 4682 triangles.
- 835 vertices receive some downward Z translation.
- X/Y changed vertices: 0.
- Head-dominant changed vertices: 0.
- Z delta range: -3.0 to approximately -0.151 due to skin-weight blending.
- No source weights lost.
- Partition flags remain [257,257,257].

Artifacts:
- Data\meshes\rem\gmod\armor\CombineSoldierFullBody_torsolowered.nif
- NIF SHA256: A46A20E984FF113C25D7285BCD081EEED06746FE4275919A3541EB197E9785E2
- Data\REM_CombineArmor_Test_TorsoLowered.esp
- ESP SHA256: 99F4B59D498E52A21423869210579609C8DC5B981AF2F3FF7C95247ACE7BBE16

Next-start load order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_TorsoLowered.esp

Human runtime validation pending after full FalloutNV.exe restart.
