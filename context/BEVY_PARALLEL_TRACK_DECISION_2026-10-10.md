# D-012 — Independent REM1 Bevy successor track (2026-10-10)

## Owner decision
REM1 Bevy, a standalone Rust/Bevy game, will coexist with the existing Fallout: New Vegas / NVSE REM1 Legacy mod. **Bevy is now the primary future development target.** Legacy is preserved in full and may become maintenance-only/discontinued-development later, but must not be deleted, overwritten, or marked retired without an explicit decision.

This decision supersedes the legacy host-engine assumption **for the Bevy track only**. Existing GOAL.md and ARCHITECTURE.md still describe the legacy runtime and remain true for that historical branch; separate Bevy planning documents describe the successor.

## Independent version rules
- REM1 Legacy: original FalloutNV/xNVSE DLL+ESP, protected v85 baseline, existing save games, candidates O00/O01, tools, manifests, and history. No Bevy work may change legacy runtime or existing enabled plugins.
- REM1 Bevy: independent Rust/Bevy executable, standalone save format, physics, UI, control input, gameplay systems, content loader and build/test pipeline. No assumption that FalloutNV.exe, GMod, or THUG2 runs alongside Bevy.
- Both live in https://github.com/bertjerk660-dotcom/REM1 with separately identifiable branches, folders, release artifacts, manifests and rollback paths. Do not move existing source or history merely to achieve a preferred directory structure.
- Proposed new source folder: bevy/. Legacy folder is a future optional organizational improvement, not an instruction to relocate existing files now.

## Desired playability
Default world gameplay should preserve the intended Fallout-like exploration, combat, inventory and progression. A skateboard weapon/item switches to full source-evidenced THUG2-like free-roam skating, with correct board position, controller/camera/physics, trick state machine, grind eligibility, bails, animations, HUD, combos and exit/restore. Contextual GMod Q/spawn menu, original-style Tool Gun, Physics Gun, prop management and notifications coexist with the world. Keep keyboard/mouse and Xbox controller mappings. Preserve owner's input priorities: skateboard LMB activation and holster to exit; Physgun LMB acquisition/manipulation and RMB launch/release.

## Authorship and safety
Claude Opus is the sole substantive implementation/integration owner; Codex defaults to investigation, IDA 6.8 evidence, runtime debugging and validation; normal GPT owns workflow, documentation and manifests. Opus can conduct narrow investigation when needed to unblock work under D-009A. The user's machine has IDA Pro 6.8 in C:\Program Files (x86)\IDA 6.8; do not use IDA 9.3. The known THUG2 disc executable is PS2 SLES_526.21 (MIPS ELF), not a verified PC executable.

Do not commit or redistribute copyrighted third-party proprietary executables, game models, textures, sounds, decompiled code or other content without permission. Commit original authored code, import/conversion tools, maps, hashes, analysis notes, tests, build manifests and documentation. Validate licensing before any standalone distribution. Any original-content loader must use verified legitimate local game installations or cleared replacement content.

## Engineering and validation
Stages: (0) reconcile GitHub and Windows workspace and prior Claude chat; inventory/provenance/licenses; (1) standalone Bevy launch + world collision + camera + keyboard/Xbox input + save/load + CI/build smoke; (2) one properly imported world region as a playable quality gate; (3) skateboard movement/animations/HUD/full free-roam mechanics; (4) functional GMod Q menu, Tool Gun, Physgun, props and notifications; (5) world integration, AI/progression, audio, systems regression, release packaging. These are migration goals, not claims of completion.

Version all builds and require boots, assets, collision, input, UI mode restoration, save/load, regression, and real gameplay tests. Reuse technical knowledge from legacy O00 and O01, but do not confuse their static or Opus selftests with validation in Bevy.

## Evidence as of 2026-10-10
- GitHub main points to 19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0. The latest inspected implementation/opus-o00-golden-bench-20261009 branch was ahead by 194 commits and behind by 0.
- The branch carries builds/O00_golden_bench_candidate_20261009.json and builds/O01_toolgun_candidate_v86_20261009.json. Runtime/playability gates remain separately tracked.
- Rust and Cargo stable 1.99.0 for Windows MSVC successfully installed from the checksum-verified official rustup installer. Bevy v0.20.0 was resolved as a Cargo dependency inside isolated rem1_bevy_install_probe on this PC; a compiled Bevy smoke result is a separate gate.
- The source workspace C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2 is not itself a git checkout. Project-authored local source not in GitHub must be reconciled before porting.

## Session completion rule
Every Opus iteration updates a Bevy-specific current state, roadmap/open work, failure knowledge, build manifest, validation results and durable GitHub commits. Verify push and hashes. Never assert a playable game exists based on a successful Rust dependency install.
