# 02 — THUG2 evidence inventory

Status: inventory of local-only evidence. Proprietary extracted assets stay local per `context/ASSET_POLICY.md`. Only counts, fingerprints and paths are recorded here.
Full per-file hashes: `thug2_file_hashes.txt`. Folder fingerprints: `thug2_folder_fingerprints.txt`. Both are in this folder.

## Folder fingerprints (SHA-256 over sorted per-file hashes)

| Folder under `build/prepared/` | Files | Fingerprint |
|---|---|---|
| `thug2_evidence_20261007` | 19 | `455DD57CA6C01511ACA5A4170775D82D486F7A84C50FA89467A3E7E880A46CA2` |
| `thug2_controller_map` | 18 | `D7AA3C9ABE0D998A1DD6CB16380D606F0CD6D5F80902894DECCFC93104E92B4A` |
| `thug2_skateboard_asset_handoff` | 4 | `223656A0BFBC51E74C853BB11E0BF5FEBEE9AA737E960F0FA4FFFBAEBFE0936E` |
| `thug2_ui_asset_handoff` | 24 | `DE88F705A1FA235E7EBB25EA6565098F106C3C51C9AD193DBD79D6AE0FD1D313` |
| `input_control_matrix` | 2 | `830F8B4CA7C783D62713898F195C2ED19F0D94CA1285A522BC478E5D75A965A0` |
| `regression_test_packs` | 2 | `6E16650B66029E6AF23A1F8F1268C677DFB09115A5ED7240C2D0B410C3844D12` |
| `thug2_prop_catalog_sidecar` | 1 | `85FA2642C9DEA189C344CF84AE8EB27CA90BE63A73FA57A5A7C6DDD9D740B291` |
| `thug2_prop_catalog` | 1,403 | Not fingerprinted in this pass. Hash it before handoff. |

## Handoff documents (`context/HANDOFFS/`)

All four THUG2 handoffs exist locally:
- `ASTRA_THUG2_SKATE_RUNTIME.md`
- `ASTRA_SKATEBOARD_ATTACHMENT.md`
- `ASTRA_THUG2_HUD_INPUT.md`
- `ASTRA_PROP_CONTENT.md`

**Correction to my earlier statement:** these four are missing from the uploaded `REM1-main.zip`, not from the local workspace. The earlier conclusion that they were absent was based only on the zip.

## What the GitHub snapshot is missing

The `REM1-main.zip` snapshot (95 files) is behind the local workspace. It lacks:
- the `build/prepared/` folders, including all THUG2 evidence folders above;
- the `OPUS_*` handoffs, `OPUS_READINESS_BOARD.md`, `OPUS_LAUNCH_SEQUENCE_2026-10-07.md`, and `LOCAL_OPUS_PREFLIGHT_SNAPSHOT_2026-10-07.md`;
- the four `ASTRA_THUG2_*` / `ASTRA_SKATEBOARD_*` / `ASTRA_PROP_CONTENT` handoffs;
- the `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json`;
- the GMod bundle is present in the snapshot. Whether the local copy is newer has not been checked.

Action: commit the local context and `build/prepared` manifests (not the proprietary payloads) to the canonical repo before handing off, so Opus reads one consistent source. The readiness board says Opus must not receive anything that is not in the repo.

## Local-only proprietary content (do not commit)

- Extracted THUG2 board SKA files (20 parsed), UI/HUD images and previews (22/22), level GLBs (16/16), and the 85 prop targets.
- Recorded by hash and provenance only.

## Stated gaps in the THUG2 evidence chain

- The `ASTRA_THUG2_SKATE_RUNTIME` / input chain feeds O05 and waits on Codex C04 and C08 per the readiness board.
- O05b camera waits on C05; O06 animation/attachment waits on C06; O07 HUD waits on C07 and C04; O07b audio waits on C04/C06/C07.
- These are marked WAITING FOR CODEX on the readiness board. They have not been completed.

