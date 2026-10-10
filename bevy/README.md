# REM1 Bevy (primary track)

A standalone Rust/Bevy game: a Fallout-style world with Garry's Mod and THUG2 gameplay systems.
It is separate from **REM1 Legacy** (the FNV/NVSE mod in the rest of this repository), which is not modified by anything here.

| | |
|---|---|
| Engine | Bevy `=0.20.0` |
| Physics | rapier3d `=0.36.0`, integrated directly (no Bevy physics plugin supports 0.20 yet; see D-B001) |
| Toolchain | Rust/Cargo 1.99.0 (`%USERPROFILE%\.cargo\bin`, not on PATH by default) |
| Current build | B001, the vertical slice. See `docs/CURRENT_STATE.md` and `builds/B001.json`. |

## Build, play, test (Windows)

```powershell
$env:PATH = "$env:USERPROFILE\.cargo\bin;$env:PATH"
$env:CARGO_TARGET_DIR = 'D:\rem1_bevy_target_chat'   # keep off C: (F-B002)
cd bevy
cargo run                                   # play
powershell -ExecutionPolicy Bypass -File tools\autotest.ps1 -BuildId B00N -Parent B00M -Goal "..."   # build + scripted test + manifest
```

`cargo run -- --autotest --out <dir>` runs the scripted gameplay test directly. It drives the real input path through injected actions, writes `autotest_report.json` and screenshots, and exits with code 0 only if every check passes.

## Controls

| Action | Keyboard / mouse | Xbox controller |
|---|---|---|
| Move | WASD | Left stick |
| Look | Mouse (LMB captures the cursor, Esc releases it) | Right stick |
| Jump | Space | A |
| Sprint | Left Shift | LS click |
| Take item | E | X |
| Drop item | G | B |
| 1st/3rd person | V | RS click |
| Quicksave / quickload | F5 / F9 | View (save) |
| Pause / release cursor | Esc | Menu |

## Source layout

| Module | Responsibility |
|---|---|
| `src/main.rs` | App, window, CLI (`--autotest`, `--out`), cursor capture, autotest script and report |
| `src/input.rs` | Device → **action** layer with **control ownership** (Gameplay / Menu). Gameplay systems read `ActionState` only, never raw devices. |
| `src/physics.rs` | rapier3d world resource, fixed 60 Hz step, body↔entity mapping, kinematic character controller, raycasts |
| `src/gameplay.rs` | Test arena, player capsule, movement / jump / gravity, over-the-shoulder and first-person camera |
| `src/systems.rs` | Look-at targeting, pickup and drop, inventory, versioned JSON save/load, HUD |

Do not commit original game binaries or asset dumps here. Only authored code, tools, manifests, hashes and docs belong in this tree.
