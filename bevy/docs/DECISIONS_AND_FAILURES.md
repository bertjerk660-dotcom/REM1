# REM1 Bevy: decisions and failure knowledge

These are Bevy-track only. Legacy decisions and failures (D-001…, F001–F019) stay in `context/`.

## Decisions

### D-B001: integrate rapier3d directly (proposed, in use by B001)
- **Context:** the owner pinned Bevy 0.20.0 (D-012). Checked against crates.io on 2026-10-10: avian3d 0.7.0 and bevy_rapier3d 0.36.0 both require `bevy ^0.19`. No physics plugin supports 0.20.
- **Decision:** depend on `rapier3d =0.36.0` (glam-based math, `PhysicsWorld`) and own a thin integration in `src/physics.rs`:
  - fixed 60 Hz step;
  - body↔entity mapping through collider `user_data`;
  - a kinematic character controller;
  - raycasts.
- **Consequences:** about 150 lines of glue that we own. Interpolation, debug rendering and events are not provided yet. Revisit if bevy_rapier3d/avian publish 0.20 support; the module boundary keeps the swap local.

### D-B002: one session owns one working folder
- **Context:** F-B001.
- **Decision:** each agent session works in its own `git worktree` and branch, and its own `CARGO_TARGET_DIR`. Never write into a folder another live session is using. Reconcile through git, not by sharing a working tree.

### D-B003: cargo target dir off C:, reduced debuginfo
- **Context:** F-B002.
- **Decision:** `CARGO_TARGET_DIR=D:\...`, with `profile.dev` `debug = "line-tables-only"` and dependencies `debug = false`. The full dependency build then completes in ~10 min and fits the disk.

### D-B004: actions, not devices
All gameplay reads `input::ActionState`, which `gather_actions` fills from keyboard/mouse **or** the gamepad, gated by `ControlOwner`. The autotest injects at the same layer, so scripted tests exercise the real gameplay path. Future menus (Q-menu, skate HUD) take ownership instead of polling keys. This prevents the legacy F019-class bug, where gameplay keys leaked into the console.

## Failures

### F-B001: concurrent agent sessions clobbered a shared `bevy/` folder
- **Symptom:** the first `cargo build` gave 57 errors referencing modules this session never wrote (`game.rs`, `lib.rs`, `modes.rs`, `save.rs`).
- **Cause:** a second Claude session (desktop app, started 03:51) was writing a different design into the same `REM1-handoff\bevy` folder at the same time. Each session overwrote some of the other's files.
- **Fix:** both sessions' files were backed up with hashes in `C:\Users\BRAD\Documents\rem1_bevy_conflict_backup_20261010\snapshot_0418\README_CONFLICT.md`. This session moved to its own worktree and branch, and the other folder was left untouched.
- **Prevention:** D-B002. Before writing, check for other recent writers (folder timestamps not made by you, other cargo processes) and stop if found.

### F-B002: debug build filled the system drive
- **Symptom:** `failed to build archive ... no space on the disk (os error 112)` and `LLVM ERROR: IO failure on output stream` while compiling `bevy_light`/`bevy_audio`. C: had ~11 GB free after cargo cleaned up.
- **Cause:** a full-debuginfo dev build of Bevy 0.20 plus wgpu reached about 5+ GB before failing, and C: was nearly full (917 GB used).
- **Fix / prevention:** D-B003. `tools/autotest.ps1` defaults the target dir to D:.

### F-B003: Bevy 0.20 / rapier 0.36 API drift from older examples
These were all caught at compile time and fixed in B001. Recorded so future code starts correct:
- `DirectionalLight.shadows_enabled` → `shadow_maps_enabled`.
- rapier `RigidBody::translation()` returns `Vec3` by value (glam), so do not dereference it.
- `QueryFilter::exclude_dynamic()` is a constructor: write `QueryFilter::exclude_dynamic().exclude_rigid_body(h)`.
- `PhysicsWorld::remove_body_with_colliders(handle, remove_attached_colliders: bool)`.
- Also: `AppExit` is a `Message` (`MessageWriter<AppExit>`), cursor grab is the `CursorOptions` component, and text size is `TextFont { font_size: FontSize::Px(..) }`.
