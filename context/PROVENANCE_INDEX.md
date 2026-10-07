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
