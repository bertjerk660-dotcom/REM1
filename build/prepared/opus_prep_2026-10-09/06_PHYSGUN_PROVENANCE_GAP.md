# 06 — Physics Gun first-person provenance gap

Status: unresolved. This document records the gap and the search done. It does not supply a substitute.

## The gap

`models/weapons/v_physics.mdl`, `.vvd` and `.dx90.vtx` are declared by the installed GMod Physics Gun script but are absent from the mounted install. Per `build/prepared/pre_opus_20261006/physgun_provenance_gap.json` and `context/HANDOFFS/ASTRA_PHYSGUN.md`, the source path is `models/weapons/v_Physics.mdl` (note the capitalisation in the source script). The gap is recorded as "do not silently substitute".

## Searches done

| Search | Scope | Result | Date |
|---|---|---|---|
| Filename `v_physics*` | `C:\Program Files (x86)\Steam\steamapps\common\GarrysMod` (recursive) and the project workspace (recursive) | No matches | 2026-10-09 |
| Text references in `context/*.md` and `context/HANDOFFS/*.md` | Repo context | Four documents record the absence (`CURRENT_STATE.md`, `EVIDENCE_INDEX.md` E003/E020, `GPT6_OPUS_READINESS_2026-10-06.md`, `ASTRA_PHYSGUN.md`) | 2026-10-09 |

Caution: the filename search covered the GarrysMod install folder, not the Steam library's other mounts, the Half-Life 2 or base content VPKs, or any other Source install. Those were not checked in this pass. Searching the VPK indexes would need a dedicated tool; a plain filename search does not see inside them.

## What not to do

- Do not use `c_superphyscannon` or any other model as a stand-in for `v_physics`. The readiness docs prohibit this, and it would make parity claims unprovable.
- Do not recreate the model from the world model.

## Options to close the gap (none executed)

1. Search the VPK indexes of every Source content package the installed GMod mounts (CRC-check against the source-referenced path).
2. Confirm whether the current GMod build uses a different first-person Physics Gun path. The IDA 6.8 evidence may show this.
3. If neither resolves it, record the first-person model as an explicit, approved stand-in with its own provenance and a playtest sign-off, decided by the project owner, not Opus.

Owner: Codex (C03) per the readiness board.
