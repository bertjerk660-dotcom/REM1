# Provenance and Staging Index — 2026-10-07

Purpose: reconcile useful source/asset provenance from divergent support branches without promoting their runtime claims. Historical GPT-6/Astra wording inside source documents is obsolete; current ownership is defined by `context/AGENT_OWNERSHIP.md`.

## THUG2 executable and skeleton provenance

Source: `prep/code-preservation-20:context/THUG2_INTEGRATION_PROVENANCE.json`

- THUG2 executable platform/region: PS2, `SLES_526.21`.
- Recorded executable SHA256: `91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1`.
- Reverse-engineering requirement: IDA Pro 6.8.
- Recorded native function evidence includes:
  - `GetSkaterVelocity` VA `0x0027DC08`
  - `SetSkaterVelocity` VA `0x0027E040`
  - `AutoRail` VA `0x002752A8`
- FNV skeleton source: `Fallout - Meshes.bsa :: meshes/characters/_male/skeleton.nif`.
- Recorded skeleton SHA256: `C6667DD94FD10392F851F748438B7C69C0D2CB407448BECAE6431D5ED1994C4C`.
- A validated THUG2 -> FNV target-name map exists with zero missing target names, but transform/scale/animation quality remains an Opus implementation + Codex runtime-validation gate.

Status: **useful provenance evidence; selectively promote only after hash/source re-check against the current local workspace.**

## Installed Garry's Mod source provenance

Source: `prep/code-preservation-20:context/GMOD_INTERFACE_PRESERVATION.md` and `builds/gmod_qmenu_source_inventory_20261006.json`

Recorded installation evidence:
- Steam build ID: `25375506`
- appmanifest SHA256: `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`
- `garrysmod_dir.vpk` SHA256: `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`
- 105 relevant Lua files inventoried
- 40 stool files
- 46 VGUI classes
- 29 direct asset references, all 29 resolved in that snapshot

Interpretation:
- real Q/spawn menu is substantially Lua/Derma-defined;
- Toolgun is script-rich and should preserve SWEP/stool selection flow;
- Physgun core manipulation remains partly engine-native;
- GMod notification Lua is the correct source for GMod-owned feedback.

Status: **high-value Codex input, not implementation proof.**

## GMod/Half-Life weapon model staging

Source: `prep/code-preservation-20:builds/gmod_hl_weapon_staging_audit_20261006.json`

Recorded:
- 52 weapon classes
- 73 unique model refs
- 71 concrete model refs
- 71/71 concrete refs staged
- two unstaged references belong to abstract base classes only
- runtime integration performed: false

Status: **staging coverage strong; Opus still owns FNV model/attachment integration, Codex later validates presentation.**

## Opus feed bundle

Source: `prep/opus-feed-bundle-20261006:build/handoffs/gpt6_opus/feed_bundle/FEED_MANIFEST.json`

Despite the legacy path name `gpt6_opus`, this package is an **Opus implementation feed bundle** under the current ownership model.

Recorded source snapshot:
- active source SHA256: `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`
- feed bundle reports `ready_for_opus_visual_work: true`
- bundle contains Opus visual queue, code context, asset reference index, start prompt and handoff index
- proprietary assets embedded: false

Obsolete field:
- `deep_runtime_reserved_for_astra: true` is no longer authoritative.
- Current rule: **Opus implements; Codex performs subsequent runtime validation/debugging.**

Status: **usable as Opus input after current branch/hash reconciliation.**

## Physics Gun provenance gap

Sources:
- main `build/handoffs/gpt6_opus/PREFLIGHT_RESULT.json`
- `prep/opus-feed-bundle-20261006:build/prepared/pre_opus_20261006/physgun_provenance_gap.json`

Unresolved source-declared assets:
- `models/weapons/v_physics.mdl`
- `models/weapons/v_physics.vvd`
- `models/weapons/v_physics.dx90.vtx`

Recorded policy: `do_not_substitute: true`.

Status: **BLOCKED — Codex C03 must resolve provenance or prove the actual source-faithful presentation path before Opus finalizes the Physgun view model.**

## Skateboard asset provenance

Source: `prep/opus-feed-bundle-20261006:ASSET_REFERENCE_INDEX.json`

Recorded live/staged assets include:
- `skateboard.nif` SHA256 `C13CC1ABB997D85E0C5A4860410A7EF14E8DFDCA5EA14D29983EBDAAA7843E4C`
- `skateboard_visual.nif` same SHA256
- `skateheldx.nif` SHA256 `4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A`
- `skateworld.nif` SHA256 `2DE82089C42543963FEE7419FF0E2B9E21E731BF6AFBF93CAAD1EF72C2C396D2`
- 20 board animation assets recorded
- held board uses `BSFadeNode` + `Prn=Weapon`

Current human evidence confirms held-board visibility/placement only; it does not validate board-to-feet, animation, trick or full skate runtime.

## Release/install branch evidence

Source: `prep/code-preservation-20:context/RELEASE_MANIFEST.md`

That branch records an installed v85 baseline and an isolated v88 candidate, but these are **branch-only claims that conflict with main's older verified-state documentation**. Do not promote them by version number alone.

Any future use requires Codex to reconcile:
- exact local source;
- branch/commit;
- installed DLL/ESP hashes;
- enabled load order;
- build manifest;
- human/runtime evidence.


## Cross-branch corroboration — GMod source/staging manifests

The following project-authored manifests were observed with the same Git blob SHA on multiple later preparation branches:

- `builds/gmod_qmenu_source_inventory_20261006.json` — Git blob `b1234b17745f1de0b28be81b987d7a56ae3d7478` on at least `prep/pre-opus-thursday` and `prep/prop-content-phase4`.
- `builds/gmod_hl_weapon_staging_audit_20261006.json` — Git blob `52c364e6125cef4729177ef462a326d1bd9140a7` on at least those same branches.

This corroborates that later support work reused the same inventory/audit rather than silently changing its recorded source snapshot.

Recorded Q-menu inventory details:
- GMod build ID `25375506`;
- appmanifest SHA256 `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`;
- `garrysmod_dir.vpk` SHA256 `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`;
- 105 relevant Lua files;
- 40 stool files;
- 46 VGUI classes;
- 29 direct asset refs, zero unresolved;
- local manifest SHA256 `A499117503C53710B91AE27C401DBFCF53F23C4B741B3AF29FD0A43C06B0774B`;
- runtime port performed: false.

Recorded weapon staging audit:
- 52 weapon classes;
- 73 unique model refs;
- 71 concrete refs;
- 71/71 concrete refs staged;
- two abstract-only unstaged references: `models/weapons/v_eq_flashbang.mdl` and `models/weapons/v_pistol.mdl`;
- local audit SHA256 `D8435F3482CB32E6EC5A21D40C394B55B4E7E2C89247C918E79E065D3AE659FF`;
- runtime integration performed: false.

**Promotion status:** provenance/index evidence is accepted for coordination use. Before Codex or Opus relies on the installed-game hashes as current local truth, re-check the current installation. This does not promote any runtime implementation.

## Quarantined v85/v88 install snapshot

Branch-only `context/RELEASE_MANIFEST.md` on `prep/prop-content-phase4` and `prep/support-workflow` records:
- installed runtime label v85;
- DLL SHA256 `BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41`;
- active `REM_GModTHUG2.esp` SHA256 `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7`;
- isolated/not-installed v88 candidate SHA256 `6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439`;
- 290-entry catalog (170 native FNV + 120 custom GMod/Source);
- 205 unique converted GMod prop payload files;
- disabled support plugins for Combine armor, GMod prop catalog and weapon presentation.

The two branch manifests differ in support-validator count (110 versus 111 checks) while sharing the same local release-manifest SHA256 `0CD126920013F0766F80F3579A704C50235D81102659AC2BC765A99E87046377`. That inconsistency is itself evidence that prose branch ledgers must not define canonical runtime state.

**Quarantine status:** RUNTIME CANDIDATE / INSTALL-SNAPSHOT EVIDENCE ONLY. Do not update CURRENT_STATE to v85 or v88 from these documents. Codex must identify the actual installed files/hashes and run the required baseline/runtime gates before promotion.

## Provenance policy

For every imported or converted asset track:
- source game;
- source archive/package;
- original path;
- source hash where useful;
- extracted/staged path;
- conversion output path;
- intended final destination;
- skeleton/material/sound dependencies;
- state: original / converted / generated metadata / implementation / temporary test;
- Opus implementation status;
- Codex runtime-validation status.

Never treat branch presence, conversion success or an ESP record as proof that an asset works in the running game.


## Prop-content phase 4 reconciliation

Sources:
- `prep/prop-content-phase4:builds/final_prop_catalog_20261006.json`
- `prep/prop-content-phase4:builds/gmod_prop_menu_curated_20261006.json`
- `prep/prop-content-phase4:builds/prop_menu_content_handoff_20261006.json`
- `prep/prop-content-phase4:builds/prop_support_phase4_20261006.json`
- `prep/prop-content-phase4:context/PROP_PHASE4_STATUS.md`

Durable coordination facts:
- ready player-facing catalog remains **290** entries;
- source split is **170 Fallout New Vegas + 120 GMod/mounted Source**;
- the selected GMod pool was curated from **7,507** registry entries;
- the 120 GMod entries report **0 unresolved materials** in that branch snapshot;
- thumbnails were recorded as **290/290** covered for support/fallback use;
- the intended menu policy is to remain near **300-320** useful items rather than grow into a raw archive;
- THUG2 embedded-prop queue records **106** future targets across **16** levels, but none is promoted solely from proximity/leaf evidence;
- diversified THUG2 review wave contains **20** candidates: 13 high-review-priority and 7 medium-review-priority;
- all 20 have recorded material provenance; intended collision roles are 16 static skate obstacles + 4 static environment props;
- the THUG2 sidecar builder correctly remained blocked at **0 ready / 20 blocked** because visual identity, standalone split/conversion, collision and scale were not yet validated;
- phase-4 static validator reported 66 checks / 0 errors and unified support validator 112 checks / 0 errors;
- runtime changes = false and runtime/visual playtest = not run.

Historical ownership wording inside those manifests that says Astra owns runtime is obsolete. Current ownership remains: Opus implements; Codex investigates and runtime-validates.

**Promotion status:** catalog/provenance/taxonomy evidence is accepted for coordination and future Opus content-adapter planning. THUG2 prop candidates remain **NOT PROMOTED** pending visual/conversion/collision evidence and later runtime validation. The disabled GMod sidecar and its branch hash are not runtime proof.


## Current-local provenance refresh — 2026-10-07

Remote Desktop Commander re-hashed the actual current machine.

Exact matches to recorded source provenance:
- GMod appmanifest SHA256 `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`;
- `garrysmod_dir.vpk` SHA256 `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`;
- THUG2 PS2 `SLES_526.21` SHA256 `91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1`;
- FNV skeleton extract SHA256 `C6667DD94FD10392F851F748438B7C69C0D2CB407448BECAE6431D5ED1994C4C`.

Current project identity differs from the old Opus feed snapshot:
- current local `main.cpp` SHA256: `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE`;
- old feed-bundle `main.cpp` SHA256: `CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5`;
- current installed `FNVGModTHUG2.dll` SHA256: `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206`;
- active `REM_GModTHUG2.esp` remains `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7`.

Current enabled support sidecars:
- `REM_CombineArmor_Test_TorsoLowered.esp` SHA256 `99F4B59D498E52A21423869210579609C8DC5B981AF2F3FF7C95247ACE7BBE16`;
- `REM_Goodsprings_CombineDeathclawEncounter.esp` SHA256 `B37B2087B75701AFAAE64FEA62B580774B99965A8B4C37CED32E4161FECB590F`;
- support DLL `REMGoodspringsResponse.dll` SHA256 `2FCEAC8BB4B3AD11B774F9B9B0D9F97A08E9D9372205C9A7E4E34F2BF4F0F13F`.

Interpretation: source-game provenance is current and trustworthy, but the 2026-10-06 Opus feed bundle cannot define the exact current implementation-source baseline. Any Opus task must freeze a new branch/commit/source hash and explicitly decide whether unrelated support sidecars are enabled during validation.

See `context/LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`.
