# O08b — GMod / HL Pistol Presentation — 2026-10-07

**Status: READY AFTER O00 PASS**

Scope: authentic Source/GMod pistol first-person and third-person/world visual presentation only. No firearm gameplay, damage, firing logic, reload logic or input changes are authorized by this packet.

## Mandatory prerequisite
O00 Golden Source Bench must pass the isolated Source→FNV conversion/material/collision gate first.

## Direct installed-archive provenance

Model archive:
`GarrysMod\garrysmod\garrysmod_dir.vpk`

Direct temporary extraction on 2026-10-07 exactly matches the staged model package:

### First person
- `c_pistol.mdl` — 39,724 bytes — `682220E528FEC38C0BED0FA62F287E12EA07CDFD59B582209BAAC4D62D808DE7`
- `c_pistol.vvd` — 62,848 bytes — `B448AD4683FE5066D4B0D78C740D870EC3DCFCF49582D4E0B81F851AAC0B2B38`
- `c_pistol.dx90.vtx` — 13,864 bytes — `941299832D28DEA485D8F1BF943B2C6EA1F22179AF4D5BDF3A8E062B9B27FACE`
- `c_pistol.qc` — `B6F609E72E631BE691C9E2372246289E94675B17C7A625F001A6EC4D9F8BEA6A`
- `v_pistol_reference.smd` — `2B1994389E0434503AA2AB9387F0D13E93D742A30E7F16E412119EAE9BA1FE6E`

### Third person / world
- `w_pistol.mdl` — 3,840 bytes — `3494567C5217A2CFA7AFC67158B29EFE339B74D880D37E22D5B59926ACA3C902`
- `w_pistol.vvd` — 27,776 bytes — `C044892FA03E73ECD73421E3995667AAE86BA9CF385CE36038CB2000CD096553`
- `w_pistol.dx90.vtx` — 8,036 bytes — `3FB243D570D15C03709B32F8A8EB943F1B80D7CFA1DA8110CC82AB90C63D4B9F`
- `w_pistol.phy` — 1,314 bytes — `360F20B55C24301FD63E1CBE0F61B1079B28E92C2F8BE678862B3B9B17AB9EE7`
- `w_pistol.qc` — `28B789E0014C8F8CA5C23F2F9E5C53E13F9338C40D78EF17BDCA0CBA9D15B7DC`
- `w_pistol_ref.smd` — `61DFF3C05216BD03E5AE6DF1C8B71F9FA445FDA29CBD28366E50FC05037198F2`
- `w_pistol_physics.smd` — `37F657E790ACBBF8D9F4346A20BBEE0770C3C602D411BBA18D24FEB34A5FB9B2`

## Material closure

Original definitions from `sourceengine\hl2_misc_dir.vpk`:
- `materials/models/weapons/v_pistol/v_pistol_sheet.vmt`
  - SHA256 `D5A194F1F708E32E888C414FACBC8E83FB0F487F37BEB3E5E2CF3BB01B9C7121`
- `materials/models/weapons/w_pistol/pistol.vmt`
  - SHA256 `75FA6C8648C5C75A067D435644CF61ED10F1F1139DD8350F208BC97429481B0C`

Original textures from `sourceengine\hl2_textures_dir.vpk`:
- `v_pistol_sheet.vtf` — `F811F31B1C254CC95EA24E86A25CC033C77BF37D825D1C8DD69DCCD4AC06B9EE`
- `v_pistol_sheet_normal.vtf` — `FAFFCB532C4C6FE4D67E5DB7616D77A8ECD4E2EE31FD58C918E36B52C282259E`
- `w_pistol/pistol.vtf` — `275DB63EF4573FF10C8A8264824C98DFD932A3A4788BC0546025CD0CF3A94E09`

Current staged hashes match those archive extracts exactly.

The first-person VMT uses:
- base texture;
- bump map;
- `env_cubemap`;
- normal-map alpha envmap mask;
- self-illumination;
- phong properties.

`env_cubemap` is an engine-generated Source resource, not a missing texture. Opus must translate the material intent to FNV-compatible shaders rather than inventing a substitute texture.

## Opus scope
Authorized:
- authentic model conversion/adaptation;
- materials/textures;
- first-person presentation;
- third-person/world/drop presentation;
- scale/orientation/attachment;
- isolated candidate records/assets;
- implementation manifest.

Not authorized:
- firearm mechanics;
- damage/ammo/reload behavior;
- input changes;
- replacing original geometry/materials;
- changes to Toolgun/Physgun/THUG2.

## Validation
After O00 PASS and Opus candidate freeze, Codex validates:
- first-person visibility/alignment;
- third-person/world/drop visibility;
- material/normal/shader appearance;
- scale/attachment;
- repeated equip/holster/switch;
- save/load;
- no unrelated regressions.

**READY AFTER O00 PASS.**

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.