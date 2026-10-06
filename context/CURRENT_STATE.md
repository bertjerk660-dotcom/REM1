# Current Verified State

Verified 2026-10-06 from the actual local workspace, deployed files, build manifests and static validation.

## Canonical repository
- GitHub repository: bertjerk660-dotcom/REM1.
- Default branch: main.
- Astra THUG2/UI work branch: feature/thug2-native-ui-g6.
- Support/preparation work branch: prep/support-workflow.
- Local workspace: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2.

## Installed runtime
- Installed NVSE plugin remains v85.
- Installed FNVGModTHUG2.dll SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- A matched v85 activation playtest previously reached skate frame 180 with skeleton retarget quarantined. This is not broad stability proof.
- Current REM_GModTHUG2.esp SHA256: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
- The active ESP currently contains the support-pass Pip-Boy origin-icon assignments and a staging Combine armor record. No existing Enclave/Remnants records were replaced.

## Astra v88 candidate
- feature/thug2-native-ui-g6 contains the isolated v88 bitmap-HUD candidate and checkpoint 88 evidence.
- Local hud88 candidate DLL SHA256: 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.
- v88 is not installed and has not been gameplay-tested.
- Support-lane work must not overwrite, deploy, rebuild in-place or otherwise alter the v88 candidate unless explicitly assigned.

## Pip-Boy origin icons
- GMod and THUG2 Pip-Boy origin icons were generated from the user's installed source-game assets and installed as loose FNV DDS files.
- xEdit support report recorded 49 REMGW_ weapons assigned the GMod icon and 1 REMTHUG2 weapon assigned the THUG2 icon.
- GMod large icon SHA256: 9D22854C96241AFC6C3FC596E15356D38DCFA75EB073E61F943B8FC094F3161E.
- GMod small/glow icon SHA256: 9CAC7740C145C1CAE6F6823EAB03F6ADEAAB9D06A14ABA647E0AC4619EBCD25B.
- THUG2 large icon SHA256: 5820CA60BA0EFC811F5D623F1D53BA12AADE4194A5252FC8E3A7A42FEA4B9633.
- THUG2 small/glow icon SHA256: 4DA787896197E76DF3C2E04BC17F929064EEB8FF65833A39B3B20362F6B62F40.

## Combine Soldier full-body armor staging
- A separate Combine Soldier full-body wearable NIF now exists for later testing.
- Biped NIF SHA256: 90A836EEF689C50994ED6E5BECC7B37CEFA0B32DA6E20D88C34DC193837B6728.
- Geometry: 3,535 vertices / 4,682 triangles.
- Skin: NiSkinInstance, 41 Fallout humanoid bones, every vertex weighted, maximum 3 influences, weight-sum maximum error 4.47e-08.
- Source-faithful Combine textures resolve locally.
- World NIF SHA256: 1878E5E9E776F70897504EBC31A4B9E13CDF0C496384974453FDF4601D68D3A5.
- A dedicated sidecar test plugin REM_CombineArmor_Test.esp was created from the Remnants Power Armor donor, using the Combine full-body biped/world model. SHA256: 52B06C9D1FA087B32BD2F83120603903893D24781BC9490D89C3D9EEE105979E.
- The sidecar plugin is NOT enabled in plugins.txt and no runtime armor playtest has been run.
- Do not replace Enclave/Remnants NPC equipment until deformation, clipping, world-drop, first/third-person, save/load and NPC equipment tests pass.

## Status
- v85 remains the installed runtime.
- v88 remains an isolated Astra candidate.
- Combine armor staging passes static validation but is not runtime-verified.
- Project is NOT yet verified stable/complete.

## Support asset checkpoint — 2026-10-06
- Concrete GMod/HL weapon model staging: 71/71 concrete model references covered; two missing model refs are abstract-base placeholders only.
- FNV curated prop audit: 300 parse, 278 static-clean; 290 have collision and 31 have mass>0 authored-mobility evidence.
- Real GMod Q-menu handoff: 105 relevant Lua files, 40 stool/tool files, 46 VGUI classes and 29/29 direct asset refs resolved.
- GMod/Source curated prop pool: 120 conversion/collision/material-clean candidates.
- THUG2 embedded environment extraction queue: 106 named targets across 16 levels; not standalone/spawn-ready.
- Compact ready prop-content handoff: 290 candidates = 170 FNV + 120 GMod/Source. Keep normal menu near 300–320 and promote THUG2 by replacement where practical.
- See context/SUPPORT_CHECKPOINT_20261006.md and the 20261006 build summaries.
