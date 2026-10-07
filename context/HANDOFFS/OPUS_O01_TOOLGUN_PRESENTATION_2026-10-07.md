# O01 — Toolgun presentation implementation packet — 2026-10-07

**Status: READY FOR OPUS**

Scope: first-person / world-model / material / attachment / presentation integration for the authentic Garry's Mod Toolgun only.

This packet does **not** authorize final Q-menu behavior, gmod_tool/stool dispatch, Duplicator/Remover behavior, undo/cleanup logic, notification behavior or final input ownership. Those remain gated on Codex C01/C02.

## Player-visible objective

When the player equips the Toolgun from the Fallout inventory:
- the first-person weapon uses the authentic GMod Toolgun source geometry/materials;
- the third-person/world representation uses the authentic GMod Toolgun source geometry/materials;
- the model is correctly scaled, oriented and attached to Fallout-compatible weapon/hand bones;
- the screen/material presentation renders without missing textures, flashing or obvious placeholder materials;
- inventory identity and existing weapon behavior remain intact;
- third-person presentation preserves the project requirement to use the Fallout 10mm-pistol animation family unless a later reviewed package deliberately changes it.

No final GMod Toolgun gameplay semantics are part of O01.

## Provenance

Primary archive:
- `GarrysMod\garrysmod\garrysmod_dir.vpk`
- current machine SHA256: `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`

Source packets:
- `prep/opus-feed-bundle-20261006:build/prepared/pre_opus_20261006/c_toolgun_source_packet.json`
- `prep/opus-feed-bundle-20261006:build/prepared/pre_opus_20261006/w_toolgun_source_packet.json`

Staging audit:
- `prep/pre-opus-thursday:builds/gmod_hl_weapon_staging_audit_20261006.json`
- concrete model-reference staging coverage: 71/71 = 100%;
- no blocking unstaged concrete references;
- runtime integration was not performed by that audit.

## Local hash re-verification — 2026-10-07

### First-person / c_toolgun
- `c_toolgun.mdl` — 64112 bytes — `992ED7A5ED4996B89C59FF656D93981FBA53B06B2E7A478EA52E0D7309E8CC79`
- `c_toolgun.vvd` — 318336 bytes — `D3F469510B6C5B0F1979254B477BA66F228EEA01240FE97DB22AB97D57429580`
- `c_toolgun.dx90.vtx` — 74933 bytes — `9A814D307A9874BBD3B3CF92BEC93069780898203783F80ABD20DEAFA9FAB6DA`
- `c_toolgun.qc` — 12780 bytes — `C6259150D8048F0379B6298A627E2CB7A7D392071992280CBF80AECE50022AD6`
- `toolgun_ref.smd` — 1499143 bytes — `6ECC49B65BB19AB8B4831D3CB318DB353D65C07F1B40BB004E73FC22A8401B98`

### World / w_toolgun
- `w_toolgun.mdl` — 3520 bytes — `19D169CCEF78F358B44E7CAA8CDF3873EEA3FBD21864F70F86E23CE1106B2703`
- `w_toolgun.vvd` — 235456 bytes — `EE8CFAE44FF4BB7A6F83C77DC5F1AA077AA11EDC4ED163B3A715DC8B9CC909C6`
- `w_toolgun.dx90.vtx` — 63222 bytes — `4F43009DCE55EDF1BDBE76EC46E8A0F5FB87EB70CC651E66902B5E051A01A55E`

All above match their recorded source-packet hashes.

### Toolgun materials/textures
Current local staged hashes match the source packets:
- `screen.vmt` — `CCED67B3CB3B2C569E06B3E647007F3D9B97BD8F1B5A56FD23303621F080B524`
- `toolgun.vmt` — `42B467C7C4780CA0C0644A13ABD460103B54A42FB5ADF483571C345A918C6D51`
- `toolgun2.vmt` — `DC5CAF8D985C6838E789C7367CD52C10F7ECFD81B5F5CC135B5E6373589D4B9D`
- `toolgun3.vmt` — `BA5BE27F9B638A00A02B760A2515C443665C1E85390ADF468EA19C30E503EEF4`
- `screen_bg.vtf` — `6D106B4B9122199B217788A2567A49E29F3B45DEEF5F22EE237578E899346590`
- `toolgun.vtf` — `A485F39B2F6D413A432F92180F14E7F1ED3A28A0D42C3A1FEA387000056D2270`
- `toolgun_mask.vtf` — `DD465F46D3F8D9775ABD19A00998F9A4FA2D79ADA88EB16B0FFB1D3CEB24DB97`
- `toolgun_exp.vtf` — `F34D0F7A842D4AAA3A40AD3E1C74C7F37B0AFC2F8CFBFDDEBC786DB7ECDC68DD`
- `toolgun2.vtf` — `897B1D2FFF6BF58D8FC759852D673327B7A303FCD2E73F7B0F58754069651312`
- `toolgun2_mask.vtf` — `6F9FFFD6A1117A54C4E83D40E98185C6BD45F4790CE470DBBE705274B68FF0E6`
- `toolgun3.vtf` — `55F393A55C9060519FDBB521700BF94A50E152BC7469C235EA54B10A70FFDFBC`
- `toolgun3_mask.vtf` — `B2F6720F3CD1060429D34670309BE5BAF501098B498E008F1431EE713E575B8D`
- `toolgun3_exp.vtf` — `DD32CBA99992442A6CDEF00768827E0BA0163566F5FFCF712B2122FBE612F6DA`

Source-material note:
- Source `env_cubemap` references are engine-generated resources, not missing texture files.
- Opus must adapt Source shader behavior to Fallout-compatible material/shader conventions; do not fabricate substitute textures.

## Current implementation baseline warning

Do not use the old 2026-10-06 feed-bundle `main.cpp` hash as the implementation baseline.

Current local source:
- `main.cpp` SHA256 `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE`

Old feed-bundle source:
- `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`

Before Opus modifies any runtime/presentation source, freeze the selected branch/commit and current source hash.

## Implementation boundaries

Opus owns:
- authentic Source model conversion/adaptation into FNV-compatible visual geometry;
- first-person Toolgun presentation;
- third-person/world Toolgun presentation;
- material/texture conversion;
- scale, axis and attachment transforms;
- Fallout-compatible mesh hierarchy;
- required visual/presentation record changes;
- visual testing assets/candidate sidecar if isolation is preferable.

Opus must not in O01:
- invent or implement final Q-menu behavior;
- implement final Toolgun tool dispatch;
- invent Duplicator/Remover semantics;
- replace authentic GMod source geometry with recreated geometry;
- change skateboard/Physgun/THUG2 systems;
- change persistent inventory identity unnecessarily;
- promote any unrelated runtime candidate.

## Preserved behavior

O01 must preserve:
- Fallout boot/load;
- Pip-Boy inventory availability of existing core weapons;
- persistent ESP-owned identities;
- existing skateboard equip/activation/holster behavior;
- no grenade/type regression;
- existing input ownership;
- Q key behavior must not be newly redefined by O01;
- no change to unrelated support sidecars.

## Candidate output contract

Opus must record:
- source branch + commit;
- candidate branch + commit;
- all source hashes;
- all generated NIF/texture hashes;
- changed ESP/DLL hashes if any;
- exact load order;
- test save/location;
- rollback paths.

Use:
`build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`

Recommended candidate isolation:
- converted assets under a dedicated `meshes/rem/gmod/weapons/toolgun/` namespace;
- converted textures under a dedicated `textures/rem/gmod/weapons/toolgun/` namespace;
- do not overwrite original staged Source payloads.

## Acceptance

Static/presentation acceptance:
- source geometry provenance retained;
- first-person model renders;
- third-person/world model renders;
- no missing textures/materials;
- screen/material regions map correctly;
- correct scale/orientation;
- correct weapon-hand attachment;
- no obvious clipping introduced by conversion;
- no absolute development paths in candidate assets;
- no unrelated forms/assets modified.

Runtime handoff to Codex:
- equip Toolgun first person;
- inspect first-person model from representative angles;
- switch third person and inspect attachment/scale;
- holster/re-equip repeatedly;
- drop/pickup if supported by current record;
- Pip-Boy select/switch regression;
- save/load regression;
- confirm no new Q-menu/tool behavior was introduced as an O01 side effect;
- confirm skateboard and Physgun inventory/presentation are unaffected.

## Unlock state

**READY FOR OPUS.**

C01/C02 are not required to implement this visual-only package, but they remain mandatory before O02/O03 behavior integration.
