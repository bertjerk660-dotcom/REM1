# Combine armor visibility runtime fix candidate — 2026-10-06

Observed human playtest:
- Combine Soldier Full-Body Armor (Test) equips, but the player body is invisible.
- Slave collar and Pip-Boy remain visible.
- Therefore the ARMO record is active, but the wearable presentation failed.

Reconciliation:
- Original test sidecar BMDT first field: 0x0000461F.
- FalloutNV.esm Remnants Power Armor donor BMDT first field: 0x00000004.
- Donor model path is direct MODL/MOD2; the Combine test also uses direct MODL/MOD2.
- Combine wearable NIF and donor both use Fallout-format BSDismemberSkinInstance/NiSkinPartition and matching root/shape transforms.
- Combine NIF has three partitions; body-part data is present. This remains a follow-up target only if the biped-mask correction does not restore visibility.

Fix candidate:
- Original locked runtime file left untouched while FalloutNV.exe is running: Data/REM_CombineArmor_Test.esp
- New next-launch sidecar: Data/REM_CombineArmor_Test_Fixed.esp
- Changed only the BMDT biped mask from 0x0000461F to donor-proven 0x00000004.
- General armor flags (0xA0), model paths, icons, stats and FormID-local record remain unchanged.
- Fixed sidecar SHA256: A938C892F3D36CED1492918E0FB3DA597DCB5A1D6D2AF10DE3103F0C9C0A5AC1.
- plugins.txt next-start order:
  1. FalloutNV.esm
  2. REM_GModTHUG2.esp
  3. REM_CombineArmor_Test_Fixed.esp
- Legacy skateboard duplicate sidecars remain disabled.

Validation:
- Byte-level BMDT check: 424d4454080004000000a0000000
- Human runtime retest required after fully closing and restarting Fallout New Vegas.
- Do not promote this fix to stable until the Combine model is visibly rendered while equipped.
- If still invisible, next isolated test is the NIF partition flags/body partition mapping; do not alter multiple subsystems at once.
