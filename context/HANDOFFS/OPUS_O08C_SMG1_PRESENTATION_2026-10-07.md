# O08c — GMod / HL SMG1 Presentation — 2026-10-07

**Status: READY AFTER O00 PASS**

Scope: authentic Source/GMod SMG1 first-person and third-person/world visual presentation only.

## Mandatory prerequisite
O00 Golden Source Bench must pass before this package is implemented.

## Direct installed-archive model provenance

Model archive:
`GarrysMod\garrysmod\garrysmod_dir.vpk`

Direct extraction hashes exactly match the current staged packages.

### First person
- `c_smg1.mdl` — 81,776 bytes — `E7B386DC6222849CB1ECA0768BA1A7975E6C02AC325B664164923EBF5ADEE5CA`
- `c_smg1.vvd` — 86,272 bytes — `266DD7166BC458125D51B693353E0BE2F180D6FAB181F1375ABC661EEE407F48`
- `c_smg1.dx90.vtx` — 21,060 bytes — `6F233766F7CEEFA062A69C7825F29FAD7DF01BA88BC7A94C5F9A202C1212278D`
- `c_smg1.qc` — `5CA67FDFEB4DC69C8E68702B18E44AA1E02135ECEDCD10220A6896023A596A99`
- `Smg1_ref.smd` — `1CDEB19838584F4F28EBFA5C13C7283E892569ECF852F029CE6F1D2C473D7AE4`
- `Smg1_ironsight.smd` — `69D0D694A2B98303EE4EBE7CD91767FD825AF63E0E1A9704B4626C2406FCF18B`

### Third person / world
- `w_smg1.mdl` — 4,048 bytes — `7E228BB32E2BDFAC835FCA69D83B220E7F10C9172BFB750DF2311BCDA9D6A50B`
- `w_smg1.vvd` — 53,936 bytes — `D1781A391DF9669B701B40084C33051ED566098A3D20CCB597693C9E3E3C7F51`
- `w_smg1.dx90.vtx` — 16,478 bytes — `E0AD514BDB104B59823BA1B45DEA5D852D9F10710E63A986E85AD20E72A29972`
- `w_smg1.phy` — 1,070 bytes — `F53C8EFF110C243D3D40703D27B978E7064A7A0B172611C8B74C15FE29566BDB`
- `w_smg1.qc` — `0C2FBAA13C5A5C06F16EC6D8958278F21F2332C557EC159198F855318F0FB3C7`
- `smg1_reference.smd` — `73D90709888856959B4C934053EEE007452D0B98411E88ADDDE69EB481F402A9`
- `w_smg1_physics.smd` — `3F9ECEAA8060A5BD63B9C2AC112446EC8648C174CB23ABC59175D3945B8A17C3`

## Material closure

Original VMTs from `sourceengine\hl2_misc_dir.vpk`:
- `v_smg1/texture4.vmt` — `0B513D553EBD14F94B8B0936F21FBE21A5F7772DA771FEE1159E957432710312`
- `v_smg1/v_smg1_sheet.vmt` — `CA573EBD3408ECB6B6EADAEB1CCA21202D701E1D79EBB6959F3E8B048AB71FA6`
- `w_smg1/smg_crosshair.vmt` — `B4485D41E594570B1D461601D951F0C7BDA5F3FCF74FACF973860D51A58F58C0`
- `w_smg1/w_smg2.vmt` — `907BBCC24DA30A3665A607089B2450042E17E3A6E912ABD982EAD6FAD666A88E`

Original textures from `sourceengine\hl2_textures_dir.vpk`:
- `v_smg1/smg1_normal.vtf` — `820B763E6ED56AFF3C6E83C5C63647B39FC322E8BF95EB127437DD3515EB795E`
- `v_smg1/v_smg1_sheet.vtf` — `D1154A2CA62653C0D0A672852E82C14D57328C0F2258CB0DDB0E61C30A7CEEFD`
- `v_smg2/texture4.vtf` — `E398A566592E833FD9A696C3117B5BD913046E4EFC038DF99115F70B2DB6B7B6`
- `w_smg1/smg_crosshair.vtf` — `A76792C9975892EA1F740472A3E0C75ABCB37002C8267DCCB87B68B94CEDEB92`
- `w_smg1/w_smg2.vtf` — `3023609FE242755861E8BBB87148E10052E73817E14C9F91EFA5BA46CF787453`
- `w_smg1/w_smg2specularmask.vtf` — `AB6122A949F82F986EF88E269B2B72F468CB1D731193BDD026527A8F2DE392D3`

### Staging dependency repair

The original `w_smg2.vmt` explicitly references:
`Models/weapons/w_smg1/w_smg2specularmask`

The old staged `w_smg1` package omitted this VTF.

Normal-GPT preparation copied the **exact original archive file** into the staging package:
`models__weapons__w_smg1/materials/materials/models/weapons/w_smg1/w_smg2specularmask.vtf`

Resulting staged SHA256:
`AB6122A949F82F986EF88E269B2B72F468CB1D731193BDD026527A8F2DE392D3`

This matches the installed source archive exactly. No recreated texture was used.

## Opus scope
Authorized:
- source-faithful visual conversion/adaptation;
- first-person SMG presentation;
- third-person/world/drop presentation;
- shader/material translation;
- scale/orientation/attachment;
- isolated candidate files/records;
- manifest.

Not authorized:
- weapon firing/damage/reload/input behavior;
- replacement geometry;
- unrelated GMod/THUG2 changes.

## Validation
After O00 PASS and candidate freeze, Codex checks:
- first-person model;
- third-person/world/drop model;
- correct material and specular-mask use;
- crosshair/material submesh appearance where applicable;
- scale/orientation/attachment;
- equip/holster/switch/save-load;
- no unrelated regressions.

**READY AFTER O00 PASS.**
