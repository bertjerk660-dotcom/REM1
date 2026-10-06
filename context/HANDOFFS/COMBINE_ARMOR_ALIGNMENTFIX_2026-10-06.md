# Combine armor alignment-fix candidate — 2026-10-06

Latest human result:
- Armor renders.
- Combine head/helmet faces backwards.
- Torso appears slightly stretched.

Root-cause evidence:
- The converter used one blanket bone-local scale of 1.75 for every Source bone.
- Source/Fallout bind segment ratios vary strongly (roughly 0.20 to 2.57 in the spine/neck chain), so a single scale deforms proportions.
- Source torso local Y corresponds to front/back depth. Current torso depth measured ~37.89 while the Remnants donor is ~30.95.
- Source/Fallout torso bone roll differs, while Head1/Bip01 Head roll is already similarly oriented. Generic retargeting therefore rotates the body relative to the helmet.

Pipeline fix:
- research/build_combine_fullbody_armor_nif.py updated locally for the candidate.
- Output candidate: Data\meshes\rem\gmod\armor\CombineSoldierFullBody_alignmentfix.nif
- NIF SHA256: 7881245734A956A07B686A37557A0B83363EE6513B944EA2840FE5DEE5C3937A
- Torso local depth scale changed from 1.75 to 1.43 while height/width remain 1.75.
- Head1 contribution receives a 180-degree rotation around Source Head1 local X before mapping to Bip01 Head.
- Material alpha=1.0, Fallout shader flags, and all generated partition flags=257 are now baked into the builder so future rebuilds do not regress.
- No source weights were lost; unmatched source weights = 0.
- Measured torso depth changed from ~37.89 to ~30.93.
- Male/female biped paths use the alignment-fix NIF.

ESP:
- Data\REM_CombineArmor_Test_AlignmentFix.esp
- SHA256: 13D455378FA9A80C86035BF0721D42D55E6FF6E814D64831900F229FA4C03320

Next-start load order:
1. FalloutNV.esm
2. REM_GModTHUG2.esp
3. REM_CombineArmor_Test_AlignmentFix.esp

Human validation pending after full FalloutNV.exe restart:
- helmet faces forward;
- torso proportions improved;
- idle/walk/run/crouch/weapon poses;
- no new neck seam or head clipping;
- arms/legs remain intact.
