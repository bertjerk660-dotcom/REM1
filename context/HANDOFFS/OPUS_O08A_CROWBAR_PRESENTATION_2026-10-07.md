# O08a — GMod / HL Crowbar Presentation — 2026-10-07

**Status: READY AFTER O00 PASS**

Scope: authentic Source/GMod crowbar first-person and third-person/world visual presentation only.

This package is intentionally independent of Q-menu, Toolgun, Physgun, THUG2 and crowbar gameplay logic. It authorizes model/material/attachment integration only.

## Mandatory prerequisite

O00 Golden Source Bench must pass visual/material/collision/runtime acceptance first:
- `context/HANDOFFS/OPUS_O00_GOLDEN_BENCH_2026-10-07.md`

The crowbar sources are fully prepared, but they should not be converted through a pipeline that has not yet passed O00.

## Source provenance

### First-person crowbar

Installed archive:
`GarrysMod\garrysmod\garrysmod_dir.vpk`

Direct temporary extraction on 2026-10-07 produced:

- `models/weapons/c_crowbar.mdl`
  - 27,320 bytes
  - SHA256 `9FC2231AE94171609DE85781D567A9ED5380B84A7D77821ED3AD485586E59992`
- `models/weapons/c_crowbar.vvd`
  - 20,288 bytes
  - SHA256 `53521D9AE6116E853456B44BCA181E08DF9A3A0F43D7D95F82AA74749DC6D377`
- `models/weapons/c_crowbar.dx90.vtx`
  - 6,084 bytes
  - SHA256 `466FBF1DCDC2E8522EB134BA79F89D71E6BDEF36C4B3679EEFB0FD2B545DF853`

These hashes exactly match the current staged copies.

Decompiler/QC:
- `c_crowbar.qc`
- SHA256 `A66D996444B7DF4311EC9608FEFFD82D6182DE56AF3FAD0376DB318093C23C4B`

Recorded Source sequences include:
- idle01
- draw
- misscenter1
- misscenter2
- hitcenter1
- hitcenter2
- hitcenter3
- hitkill1
- holster

The presence of these sequences is source evidence only. O08a does not authorize rewriting Fallout melee behavior or claiming Source animation parity without implementation/runtime validation.

### Third-person / world crowbar

Installed archive:
`GarrysMod\sourceengine\hl2_misc_dir.vpk`

The installed VPK directly lists:
- `models/weapons/w_crowbar.mdl`
- `w_crowbar.vvd`
- `w_crowbar.dx90.vtx`
- `w_crowbar.phy`
- `w_crowbar.sw.vtx`

Direct temporary extraction on 2026-10-07 produced:

- `w_crowbar.mdl` — 2,052 bytes — `BD31CE4CF61B75597DA0AC799E2E30D66B7F97D74B104F9F55EF537A4CB17787`
- `w_crowbar.vvd` — 21,872 bytes — `810C2FA423620354DCA6E04A912029C7B30570FDCADCE2DBEC7E96D945E1D92A`
- `w_crowbar.dx90.vtx` — 7,580 bytes — `97AE38B9228ED4D4D4934D259A1EE423B6EAB121B00FC6C5306E7FB962B3411D`
- `w_crowbar.phy` — 2,662 bytes — `7395DFE01BC62CF14AB7E43B4F3F8A432C2367403852CEA5CE3099E7F286E423`
- `w_crowbar.sw.vtx` — 7,548 bytes — `8A0890B0E4D6199D7A7B9109E9383460D04B3759BC51677A1262831F64597E05`

All extracted hashes exactly match current staged copies.

Decompiler evidence:
- `w_crowbar.qc` — `6F692A3F33DCEB60E7B2FA0538C5779806C68F4EE1224D44B092D8B19F81FB92`
- `w_Crowbar_reference.smd` — `B3A97028B3E90AB54ED5F139E7186EA4FB9B8B0C3F3ED258AD7772CFFDCA9BF7`

Local staging manifest identifies this as role `world` for `weapon_crowbar` and records the same hashes.

## Material closure

Material definitions:
- `crowbar_cyl.vmt` — `4BC82B4476B1BDBF2325B8835ECD2615C8C682DD1FBC34F877DFC89101FF66BF`
- `head_uvw.vmt` — `B403A63C422D35D6E7226E055D6E7DCBE688B78B2F563DB90A907AE540B21E01`

Textures:
- `crowbar_cyl.vtf` — `7F6FF74719F46C039C3DD039A2CBE2FEF77C70A8FB0B5499CB832547EDCF0094`
- `crowbar_normal.vtf` — `3A10AC704C4BCA2985C5F15A8AC1C5C64ABB7BA213A1BC354D1BFC3AA2D230FD`
- `head.vtf` — `4F4C8C721EE9AD8213772E2FE0D1B9D8BEB741266A7EF834859047457C39277D`
- `head_normal.vtf` — `8F23D4DB3D4359ECAA3FD4CE532BE70D701CB40BC757611214E017F0A08CC982`

These current staged hashes match the recorded source packet.

## Opus implementation scope

Opus may:
- convert/adapt authentic crowbar geometry to FNV-compatible NIF presentation;
- convert/adapt original material/normal maps;
- create correct first-person presentation;
- create correct third-person/world/drop presentation;
- establish scale/orientation/attachment transforms;
- use an isolated presentation sidecar where safest;
- document the mapping from Source models/materials to FNV outputs.

Opus must not:
- recreate the crowbar mesh;
- replace the source model with a lookalike;
- change crowbar damage/combat behavior as part of O08a;
- modify Q-menu/Toolgun/Physgun/THUG2 systems;
- overwrite original staged source payloads;
- claim animation parity merely because source sequences were inventoried.

## Output namespace recommendation

Use isolated candidate paths such as:
- `meshes/rem/gmod/weapons/crowbar/`
- `textures/rem/gmod/weapons/crowbar/`

Do not overwrite historical converted outputs until the new candidate is validated.

## Acceptance

Static:
- source hashes reverified;
- NIFs parse;
- texture references resolve;
- no absolute paths;
- source geometry/material identity documented;
- attachment/scale transform recorded;
- world collision choice documented;
- unrelated records/assets unchanged.

Runtime — Codex after Opus freezes candidate:
- equip crowbar in first person;
- inspect visual alignment and hand relationship;
- inspect third-person attachment;
- drop/pickup/world presentation;
- verify material/normal appearance;
- repeated equip/holster;
- Pip-Boy switching;
- save/load;
- no crash;
- no regression to Toolgun/Physgun/skateboard inventory or behavior.

## Gate

**READY AFTER O00 PASS.**
