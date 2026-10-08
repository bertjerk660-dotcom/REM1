# 05 — Regression matrix

Purpose: a standard, repeatable set of checks so Opus does not break behaviour that already works. Each row says what was last observed. "Observed" means a human playtest, not an automated test.

| ID | Behaviour | Steps | Last observed | Status |
|---|---|---|---|---|
| R01 | Held skateboard visible, correct position in hand, correct name | Equip skateboard in Fallout, view from first and third person | 2026-10-06 playtest; 2026-10-09 playtest | Positive |
| R02 | Left-click with skateboard equipped enters skate mode | Equip, left-click | 2026-10-06; 2026-10-09 | Positive |
| R03 | Holster key (R) exits skate mode back to Fallout | Enter skate mode, press R | 2026-10-06; 2026-10-09 | Positive |
| R04 | Enter and exit without crash | Cycle enter/exit 10 times | Single cycle on 2026-10-09. Not yet cycled 10 times. | Partial |
| R05 | THUG2 sounds play in skate mode | Enter skate mode, observe audio | 2026-10-06 (tested path only) | Positive, not audio-parity validated |
| R06 | Skateboard can be dropped and picked up in Fallout | Drop, pick up, check name and inventory | Not recorded in repo | Untested |
| R07 | Save and load with skateboard equipped | Equip, save, reload, check held board and skate mode | Not recorded | Untested |
| R08 | Normal Fallout combat and movement outside skate mode | Fight and move with skateboard unequipped | Not recorded | Untested |
| R09 | Fallout HUD returns after exit | Enter skate mode, exit, check HUD | 2026-10-06 and 2026-10-09: HUD stayed on during skate mode | **Fails** (F008) |
| R10 | Physics Gun range, audio and actor targeting | Physics Gun grab at normal range | 2026-10-06 | **Fails** (F009) |
| R11 | Q-menu opens, categories, icons, selection | Open Q | Placeholder appearance only, not parity | Not parity |

## Rules

- Run R01 to R05 on every candidate. R06 to R08 before any promotion to the main plugin.
- Record the DLL hash, ESP hash and load order used for each run (see `01_BASELINE_FREEZE.md`).
- Keep sidecar mods 3 and 4 (`REM_CombineArmor_Test_TorsoLowered.esp`, `REM_Goodsprings_CombineDeathclawEncounter.esp`) disabled for core-system tests.
- If any positive regresses, stop and record it as a failure before changing anything else.
