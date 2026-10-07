# O00 — Golden Source Bench Conversion Proof — 2026-10-07

**Status: READY FOR OPUS**

Purpose: prove the Source/HL2 → Fallout visual/material/collision conversion pipeline on one isolated static prop before applying the same pipeline to weapon presentation.

This is a pipeline proof package, not a player-facing feature milestone.

## Source identity

Model:
`models/props_c17/bench01a.mdl`

Original archive provenance:
- Half-Life 2 `hl2_misc_dir.vpk`;
- matching SourceEngine mount copy where recorded.

Required source companions, current-machine re-verified:
- `bench01a.mdl` — 1520 bytes — `8751F7E234A4212016FF93C50C8951ECB793B628819957B06BA1831A899CE846`
- `bench01a.vvd` — 55232 bytes — `BC9AFFE6F4EFC8766FE77961C2BD41748D677432A1E141D6CA7F56AB1E048F7D`
- `bench01a.dx90.vtx` — 35672 bytes — `E651BB00300CFD6F843D8882BFC2FC43813CAAF3D2A6AC350AEBA5496AEDB097`
- `bench01a.phy` — 6795 bytes — `0EB277C8A413F1E27E97BF5D9FD872FCB2ED1981064F592645D23F9C4E17E475`

Decompiler/reference evidence:
- `bench01a.qc` — `DCFE2C49C592732FB20745A2097B4B60588F6191DCAF15D96CB87055083C7B36`
- `bench01a_reference.smd` — `6E4AB2DB5E4BBFBC348F1DDC5C47519BA96D247CBC500290CA8714F3B9B719E3`
- `bench01a_physics.smd` — `1B903062D35C2B880D828CDA0BF741124BCC0D7CE30573810DCBCD77BD353340`

Material closure:
- `bench01a.vmt` — `086AC1E48FBD5531C162005775F84EA2958D892894C24D188951FD00345EBE57`
- `bench01a.vtf` — `8DCB834BD3D7454363D0A3DECC77EE3F2992F6A39CCD9076422E6BD40096E432`
- `bench01a_mask.vtf` — `E3B3973D40D7EA1C12286121A94BABE6B2DEF2380CE0F2B14F4A3244E233734A`

All hashes above were rechecked on the current local machine on 2026-10-07 and match the existing source packet.

## Source geometry/collision facts

QC bbox:
`-12.025 -38.104 -19.786 11.667 38.011 19.945`

Reference SMD:
- 448 triangles;
- source-coordinate dimensions approximately 74.6756 × 23.3342 × 38.911.

Physics SMD:
- 180 triangles;
- dimensions approximately 75.5521 × 23.0279 × 39.1688.

QC:
- surfaceprop `Wood_Furniture`;
- mass 20;
- concave collision;
- max convex pieces 16.

These are Source-space measurements, not approved Fallout scale.

## Known legacy conversion defects this gate must prevent

1. Original `bench01a_mask.vtf` was previously omitted by older extraction/conversion flow. It is now present and must be used where required.
2. Older worker flow mapped `Wood_Furniture` to Fallout metal Havok material. Do not silently repeat that fallback.
3. Existing live/old bench NIFs are not golden acceptance evidence.
4. Static converter success is not visual/collision acceptance.

## Isolated output contract

Use candidate-only paths:
- mesh: `meshes/rem/golden_bench/bench01a.nif`
- textures: `textures/rem/golden_bench/*`

Use a disabled isolated sidecar:
- proposed plugin: `REM_GoldenBench_Test.esp`
- EDID: `REM_GoldenBench01a`

Choose STAT vs MSTT deliberately based on intended physics behavior and document the choice. Do not invent a FormID in preparation docs before the record exists.

Do not replace:
- active `REM_GModTHUG2.esp`;
- main NVSE DLL;
- any current runtime candidate.

## What Opus must implement/prove

- preserve original geometry/UV/material grouping;
- convert materials to Fallout-compatible shader properties;
- preserve the mask/detail intent rather than substituting textures;
- document scale and axis conversion;
- produce FNV-compatible root/node hierarchy;
- reproduce appropriate collision using original source evidence;
- map the wood-furniture collision intent to a justified Fallout Havok material;
- ensure no absolute development paths;
- ensure all referenced textures exist;
- create the isolated test record/sidecar;
- generate a complete implementation manifest.

## Static acceptance

Before runtime:
- source hashes match this packet;
- output NIF parses cleanly;
- all texture paths resolve;
- no absolute paths;
- geometry counts/bounds transformation documented;
- collision hierarchy exists and is justified;
- shader/material mapping documented;
- sidecar contains only the intended test record(s);
- main runtime files are unchanged.

## Runtime/human acceptance

O00 passes only after the isolated candidate is observed in Fallout and:
- bench is visible;
- texture/material appearance is credible/source-faithful;
- scale is credible;
- orientation is correct;
- collision behaves as intended;
- player cannot walk through it unexpectedly;
- no obvious floating/sinking;
- spawn/load is stable;
- save/load with the object does not crash;
- no unrelated runtime regression is observed.

## Downstream gate

**O01 Toolgun presentation may begin only after O00 passes this visual/collision proof.**

A failed O00 is a conversion-pipeline failure. Fix the pipeline before using it on weapon models.

## Haiku audit addendum (2026-10-07): O00 rollback, sidecar and freeze rules

- Rollback: reset the implementation branch to the parent_commit recorded in build/templates/OPUS_O00_CANDIDATE_MANIFEST_SEED.json. Delete the outputs under meshes/rem/golden_bench/ and textures/rem/golden_bench/. Restore every touched file from its recorded hash. Remove the sidecar from every plugin list.
- Sidecar disabled means: REM_GoldenBench_Test.esp is absent from the default plugins.txt and loadorder.txt. It is enabled only in a recorded candidate load order for the O00 test. It is never merged into REM_GModTHUG2.esp or the main NVSE DLL.
- Core validation: O00 results are isolated sidecar evidence. They must not be counted as core Fallout baseline or as THUG2 or GMod validation.
- Freeze: only preflight has passed (validate_opus_candidate_manifest.py --mode preflight). Freeze mode must pass on the completed candidate before Codex receives it.
- Protected files: main NVSE DLL FNVGModTHUG2.dll and REM_GModTHUG2.esp must not be modified by O00. Their live hashes are in the CURRENT_STATE 2026-10-07 audit section.
- Live identity: re-check live deployed hashes and source hashes before the candidate is built (P-F007).