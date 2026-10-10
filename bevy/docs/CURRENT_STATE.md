# REM1 Bevy: current state

Updated 2026-10-10 by Claude Opus (Claude Code session).
Branch `implementation/bevy-slice-chat-20261010`, parent `dbe836a` (prep/bevy-opus-handoff-20261009).

## Verified (with evidence)

**B001, the vertical slice.** It builds and runs on DESKTOP-6PTSS3D.
- Toolchain: Rust 1.99.0, Bevy 0.20.0, rapier3d 0.36.0.
- Manifest: `bevy/builds/B001.json`.
- Evidence: `D:\rem1_bevy_runs\B001\`, kept local and not committed. It holds 3 screenshots, the report, the save file and logs.

Scripted autotest `--autotest`: **8/8 PASS**. The same result came from 3 consecutive runs (run1, run2, B001) with identical numbers.

| Check | Result |
|---|---|
| boot_and_ground | Window opens. The player capsule settles on the floor (y 0.92). Physics steps at a fixed 60 Hz. |
| walk_forward | 5.67 m in 1.5 s. Includes acceleration from rest; walk speed is 4.2 m/s. |
| jump_and_land | Peak rise 1.42 m, then lands. |
| wall_collision | Walking into a wall stops at x = -6.13 (face -6.5 plus radius 0.35, plus controller offset). No tunnelling. |
| pickup | The camera ray targets crate_3, then E removes it from the world and puts it in the inventory. |
| quicksave_written | F5 writes versioned JSON (`saves/quicksave.json`). |
| quickload_restores | F9 restores player position (0.000 m error), inventory, and world items. |
| drop_and_physics | G drops the crate in front of the player. It falls and comes to rest under rapier physics at y 0.30. |

I reviewed the screenshots myself:
- The arena renders with shadows: floor, walls, stairs, ramp, rail, shack and crates.
- The HUD shows the active device, 1st/3rd-person view, grounded state, inventory and the interaction prompt.
- run1 found the 3rd-person camera too close and centred, with HUD text unreadable over the sand. Both are fixed in B001: an over-the-shoulder camera, a dark HUD panel and a crosshair.

## Not yet verified / known gaps (do not claim these)

- **Xbox controller:** the code path exists (sticks, buttons, dead zone, device switching), but `gamepads_detected = 0` in every run. It needs a run with a pad connected.
- **Human playtest:** none yet. The checks above are scripted and use injected actions through the real action layer, not physical keypresses.
- Process exit code is verified as 0 for B001 by `tools/autotest.ps1`, which caches the process handle. The earlier ad-hoc runs could not capture it.
- Placeholder content: capsule player, box props, untextured materials. No Fallout, GMod or THUG2 assets are imported yet.
- No menus (the `ControlOwner::Menu` path is unused so far), no audio, no animation, no combat, no NPCs.
- The arena is authored test geometry, not a Fallout world region.
- Release build not yet tested. Only the `dev` profile (deps at opt-level 3) has been run.

## Next milestones (smallest useful first)

1. **B002 physics props and Physics Gun core.**
   - Spawnable dynamic props and a Physics Gun item with grab, hold at distance, rotate, freeze/unfreeze, release and launch, driven by a target-velocity spring on the held body.
   - Use `ControlOwner` so the gun takes over the mouse while rotating.
   - Add autotest checks for grab, carry, freeze persists, and launch speed.
   - Source fidelity: port the documented GMod physgun constants once Codex evidence (C03) is reviewed. Until then, values are marked provisional in code.
2. **B003 Q-menu shell.**
   - A `ControlOwner::Menu` overlay with categories, a prop grid and search, spawning B002 props in front of the player.
   - Visual and behaviour fidelity waits on C01 evidence.
3. **B004 skate mode prototype.** Skateboard item, left-click to enter, holster to exit, push, ride, ollie and simple rail grind on the existing rail, with a 3rd-person skate camera. THUG2 constants come from C04/C05 evidence when reviewed.
4. **Content pipeline:** an asset mount outside the repo (game files stay on the PC). First import is one validated prop through the existing Source→intermediate tooling, converted to glTF for Bevy.
5. A small Fallout-style region, then inventory UI, combat and NPCs.

## Concurrency note

A second Claude session has uncommitted Bevy work in `C:\Users\BRAD\Documents\REM1-handoff\bevy` on branch `implementation/bevy-vertical-slice-20261010`. See `docs/RECONCILIATION_2026-10-10.md`. That folder belongs to that session; this branch lives in its own worktree, `C:\Users\BRAD\Documents\REM1-bevy-chat`.
