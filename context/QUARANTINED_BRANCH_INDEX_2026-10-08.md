# Quarantined Branch Index — 2026-10-08

Purpose: provide one current branch-head registry so historical runtime/preparation branches cannot be mistaken for canonical implementation merely because their names or version numbers look newer.

Canonical `main`: `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`

Current clean preparation base:
`prep/opus-ready-20261007` @ `2c3f72c69475b2e842b5cbb3532f4946781b0fff`

Machine-readable index:
`build/prepared/quarantined_branch_index_20261008.json`

| Branch | Pinned head | Relation to current main | Classification | Allowed use |
|---|---|---:|---|---|
| `prep/pre-opus-thursday` | `862a5160...` | +184 / -47 | QUARANTINED mixed prep/runtime evidence | selective manifests/provenance/source packets |
| `feature/thug2-native-ui-g6` | `df2e4ff9...` | +53 / -59 | QUARANTINED runtime implementation evidence | historical implementation/provenance/failure evidence |
| `runtime/astra-phase1-input92` | `63836011...` | +63 / -59 | QUARANTINED runtime candidate | historical input/candidate evidence only |
| `diag/v85-retarget-quarantine` | `603d4047...` | +4 / -59 | historical failure evidence | crash/retarget regression design |
| `prep/opus-feed-bundle-20261006` | `bf0d8590...` | +34 / -17 | stale preparation snapshot | old asset/source metadata only after current re-check |
| `prep/prop-content-phase4` | `153ec39d...` | +183 / -47 | branch-only support evidence | catalog/provenance/static evidence |
| `prep/support-workflow` | `492c3dc7...` | +127 / -47 | branch-only support evidence | support documentation/provenance |

## Hard rules

- Never wholesale-merge a quarantined branch merely to obtain a few manifests.
- Never promote v84-v92 or any later label by version number alone.
- Never treat legacy `ASTRA`, `GPT6`, `*-g6` names as current ownership.
- If historical implementation is reused, Opus must integrate/freeze a current candidate and Codex must validate the exact candidate.
- Historical provenance may be cited without promoting historical runtime claims.
- `prep/opus-feed-bundle-20261006` is explicitly stale as a current implementation baseline.

## Haiku findings branch

`prep/haiku-findings-20261007` @ `3299b5d7a84b0bf8089b19f5ae06664f91834bf5` is **documentation findings only**, not a runtime candidate.

Its factual repository/hash/environment findings may be reconciled selectively. Its broader proposed reassignment of reverse engineering to Opus is not current dispatch authority; current ownership remains defined by `context/AGENT_OWNERSHIP.md` and `context/DECISIONS.md`.

## Promotion requirements

A historical candidate may influence canonical runtime state only after:
1. exact branch + commit are pinned;
2. exact source/build/artifact hashes are recorded;
3. candidate load order and manifest are frozen;
4. Codex runs the applicable runtime/regression validation;
5. Opus fixes any implementation failures;
6. workflow review deliberately promotes the result.

Until then, quarantine is intentional project truth.
