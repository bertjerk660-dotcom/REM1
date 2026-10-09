# Source -> Fallout: New Vegas static conversion pipeline (O00)

Reusable, job-file driven tooling that converts an original Source Engine static
prop into an FNV NIF plus an isolated test plugin. Built for O00 (HL2
`models/props_c17/bench01a.mdl`); intended to be reused for O01/O08 weapon models
once O00 passes runtime validation.

No proprietary payload lives in this folder. Jobs reference the user's local,
hash-verified source files relative to the workspace root.

## Files

| File | Purpose |
|---|---|
| `convert_source_static.py` | SMD/QC/VMT/VTF -> NIF + DDS. Verifies input hashes, writes only to a staging dir. |
| `build_static_sidecar.py` | Writes/inspects a minimal FNV plugin holding STAT records (deterministic). |
| `validate_o00_static.py` | The 12 static acceptance checks, including an independent byte-for-byte rerun. |
| `render_preview.py` | Software render (front/side/top) to review UVs, orientation and scale without the game. |
| `nif_dump.py` | Read-only NIF structure dump. |
| `bsa_read.py` | Read-only FO3/FNV BSA (v104) reader for vanilla reference files. |
| `dds_write.py` | Uncompressed A8R8G8B8 DDS writer with full mip chain. |
| `jobs/o00_bench01a.json` | O00 job: inputs + hashes, scale, cubemap, vanilla references, output paths. |

## Run (O00)

```
python convert_source_static.py jobs/o00_bench01a.json --root <workspace> --fnv-data "<FNV>\Data" --stage <stage>
python build_static_sidecar.py --out <stage>\REM_GoldenBench_Test.esp --edid REM_GoldenBench01a --model rem\golden_bench\bench01a.nif --obnd -67 -21 0 67 21 70
python validate_o00_static.py --job jobs/o00_bench01a.json --root <workspace> --fnv-data "<FNV>\Data" --stage <stage> --repro-stage <stage2> --protected <protected_hashes.json> --report <report.json>
```

Requires Python 3.13 with pyffi 2.2.3 and Pillow, plus VTFCmd at `third_party/tools/VTFEdit_Reloaded/VTFCmd.exe`.

## Conversion rules and evidence

| Rule | Value | Evidence |
|---|---|---|
| Scale | 1 Source unit -> 1.7778 FNV units | Source: 1 unit = 1 inch. FNV: 64 units per yard (0.5625 in). Cross-check: Source player 72u -> 128 FNV units. Result: bench 133 x 41 x 69 units, seat ~37 units; vanilla `benchmuseumstatic01.nif` seat is ~32 units. |
| SMD -> model frame | model = (-smd_y, smd_x, z) | studiomdl rotates `$staticprop` 90 deg about Z. Verified per asset against the hull in the `.mdl` header (offset 0x68); converter refuses if the error exceeds 0.6 units. Bench01a error: 0.38 (studiomdl hull padding). |
| Model -> FNV axes | fnv = (-model_y, model_x, z) | Source props face +X; FNV forward is +Y. Bench faces +Y, backrest at -Y, long axis on X. |
| Origin | visual base moved to z = 0 | Source bench origin is at mid-height; FNV placement drops refs at ground level. Engine-compatibility change only. |
| UV | v' = 1 - v | SMD UVs are bottom-origin; NIF/DDS are top-origin. Checked visually with `render_preview.py`. |
| Collision | one `bhkConvexVerticesShape` per Source convex solid, in a `bhkListShape` | Source `.phy` is already a convex decomposition (QC `$concave`, `$maxconvexpieces 16`). Bench01a: 15 boxes, convexity error 5e-6. No single-hull fallback (that produced an oversized invisible box). |
| Havok scale | NIF units / 7 | Vanilla `benchmuseumstatic01.nif`: Havok length 28.6 -> ~200 NIF units. |
| Havok material | explicit `$surfaceprop` table, unknown = hard error | Fixes the legacy `Wood_Furniture` -> metal fallback in `research/convert_gmod_props.py`. `Wood_Furniture` -> `MAT_WOOD` (9): Source treats it as light wood (prop_data `Wooden.Large`). |
| Rigid body | copied from vanilla `furniture\benchmuseumstatic01.nif` | Layer 1 OL_STATIC, motion system 7 (fixed), quality 1, mass 0. |
| Root / BSX | `BSFadeNode`, BSX = 2 | Same vanilla static. Legacy worker used BSX 3 (animated + Havok), wrong for a static. |
| Shader | `BSShaderPPLightingProperty` flags `0x82000081` copied from vanilla `bouldercity\nv_warmemorial.nif` | Vanilla env-masked static pattern: slot 4 = shared cubemap, slot 5 = `_m.dds`. |
| Env map | `textures\effects\shinydull_e.dds` | Source uses `env_cubemap` (per-map, baked). FNV statics use shared cubemaps; the mask is faint (mean 16/255), so the dull cubemap fits. Engine-driven difference, documented. |
| Env mask | original `bench01a_mask.vtf` -> `bench01a_m.dds` | Fixes the legacy omission (`parse_vmt` never read `$envmapmask`). |
| Normal map | flat `_n.dds`, alpha 0 | Source material has no `$bumpmap` or `$phong`. FNV PP-lighting needs a normal map; a flat one adds no information and keeps specular at zero. |
| Tangents | stored in geometry data (`extra_vectors_flags` 16) | Matches vanilla FNV. |
| NIF header | little-endian flag set explicitly; `PYTHONHASHSEED=0` | pyffi 2.2.3 wrote endian byte 0 by default and orders the header string table by Python string hash. Both caused failures that the read-back and rerun checks now catch. |
| Record type | STAT | QC declares `$staticprop`; MSTT is for movable/animated statics. |

## Legacy converter

`research/convert_gmod_props.py` + `research/blender_prop_worker.py` (local workspace,
2026-10-05) remain unchanged. They write straight into the game `Data` folder, fall
back to metal Havok material, drop env masks, ignore the SMD/model frame rotation
and use a single convex hull. Do not use them for golden or weapon work.
