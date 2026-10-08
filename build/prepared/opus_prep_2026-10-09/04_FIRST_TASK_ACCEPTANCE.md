# 04 — First-task acceptance

Status: acceptance criteria only. These do not authorise implementation. Each package is gated by `context/HANDOFFS/OPUS_LAUNCH_SEQUENCE_2026-10-07.md`.

## Gate that applies to every Opus package (from `build/handoffs/gpt6_opus/ACCEPTANCE_GATES.json`)

A subsystem is not complete merely because it compiles or deploys. All nine must pass:
1. build_pass
2. asset_reference_pass
3. boot_pass
4. feature_reachable
5. behavior_pass
6. cleanup_pass
7. save_load_pass
8. regression_pass
9. human_playability_check

Promotion: only from an isolated sidecar, after every applicable gate passes.

## Package O00 — Golden Source bench proof (first package, READY)

This is the first Opus package. The launch sequence says no weapon conversion starts until it passes its human/runtime gate.

Input: `models/props_c17/bench01a.mdl` with `.vvd`, `.dx90.vtx`, `.phy`, `.vmt`, `.vtf`, `.mask.vtf`, and reference hashes, all in `OPUS_O00_GOLDEN_BENCH_2026-10-07.md`.

Pass conditions:
- Mesh, textures and collision are written only to candidate paths: `meshes/rem/golden_bench/bench01a.nif` and `textures/rem/golden_bench/*`.
- The sidecar is disabled by default: `REM_GoldenBench_Test.esp` (EDID `REM_GoldenBench01a`).
- `bench01a_mask.vtf` is used where the material needs it.
- `Wood_Furniture` surface is **not** mapped to Fallout metal Havok material.
- The STAT vs MSTT choice is recorded with a reason.
- In game, the bench renders with correct texture, scale and collision. This is the external-asset proof gate from `OPUS_5_5_EXCLUSIVE_INTEGRATION_2026-10-06.md`. Records or successful conversion alone do not count.
- `REM_GModTHUG2.esp`, the main DLL and any runtime candidate are unchanged.

## Package O01 — Toolgun presentation (READY AFTER O00 PASS)

Pass conditions: c_toolgun first-person and w_toolgun world models visible, scale and attachment valid, no crash. Does not authorise Q-menu, dispatch, Duplicator/Remover, notifications or Physgun behaviour.

## Packages O05 to O07 — THUG2 skate runtime (WAITING FOR CODEX, do not start)

The readiness board lists these as waiting on Codex evidence C04 to C08. They are not ready for Opus, even though the skate failures are the most visible ones.

If the project owner decides to override this gate, these are the pass conditions that must be met, and they are the criteria for the skate-fix candidate:

| ID | Condition | Failure addressed |
|---|---|---|
| S1 | Entering skate mode hides the Fallout HUD and top-left alerts; exit restores them | F008 |
| S2 | Only one skateboard is visible while mounted. Held copy hidden or moved. Exit restores held copy. | F011 |
| S3 | Board is attached to feet in the riding pose during skate mode | F011 |
| S4 | At least one THUG2 riding animation plays from the original SKA data, with the imported transition | F011 |
| S5 | G does not start a grind unless the recovered eligibility check passes | F010 |
| S6 | Enter/exit cycled 10 times with no crash. Each enter and exit logged. | F005 |
| S7 | Regression matrix R01 to R05 still passes | Preserved positives |

Do not accept an approximation for S3 or S4. The contract requires the original SKA data and original attachment evidence.

## Documentation checks before Opus starts (any package)

- Implementation branch recorded, parent commit recorded (see `01_BASELINE_FREEZE.md`).
- Source hash frozen.
- Installed DLL and ESP hashes recorded.
- Load order recorded with sidecars 3 and 4 disabled, unless the package explicitly needs them.
- Rollback copies of the current DLL and ESP kept.
- `build/templates/OPUS_IMPLEMENTATION_MANIFEST_TEMPLATE.json` copied and filled in as work proceeds.
