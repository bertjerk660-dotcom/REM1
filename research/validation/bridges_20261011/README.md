# Validation harness — public bridge references (2026-10-11)

Source review: [EXTERNAL_BRIDGES_MW2_LIBERTYCRAFT_2026-10-11.md](../../../bevy/docs/EXTERNAL_BRIDGES_MW2_LIBERTYCRAFT_2026-10-11.md).
Results: [VALIDATION_MW2_LIBERTYCRAFT_2026-10-11.md](../../../bevy/docs/VALIDATION_MW2_LIBERTYCRAFT_2026-10-11.md).

## Scope
This small authored Rust crate executes the **unmodified** upstream MW2 `rails.rs` against Bevy 0.20 `bevy_math` (the principal REM1 Bevy branch pins 0.20.0). It does not compile the IW4L game, run Skate 3, or prove THUG2 parity.

## Reproduce independently
Clone `https://github.com/chasmlol/2010-rust-rewrite-mashup` pinned at `f608f85e407ff1b7689d54a9aafdd16e95711ac4`.
Copy the *unchanged* `crates/render_anim/src/skate/rails.rs` to this crate's untracked `src/rails_external.rs`. Confirm the source hash SHA256 is `B33D1070B69CC0B998C0EC1157C038FEF0CE454A6C0E8C934FC902A1212DD215`.
Then run `cargo test --offline -- --nocapture` if Rust crate cache is populated (otherwise omit `--offline`). Do not commit the upstream file; this harness compiles it by reference.

For LibertyCraft, clone `https://github.com/mrborghini/libertycraft` pinned at `18ccef417a93e29332abb5dfcf8005b2f8928376`, run its portable `asi/tests/drive_test.cpp` in C++17 using the Visual Studio developer command prompt, and run the other listed suites from the report. `collision_test.cpp` requires two `[]` -> `[=]` lambda captures in `asi/src/collision/Geometry.h` lines 914-915 for tested MSVC compatibility; if doing this, document the local-only patch and restore the file afterward.

No executable from this harness should overwrite REM1 Legacy or the B001 Bevy build. All tests here are synthetic static/source-level checks, not source-game runtime parity validation.
