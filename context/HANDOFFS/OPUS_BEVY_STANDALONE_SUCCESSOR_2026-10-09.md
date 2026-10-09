# Claude Opus Code handoff — REM1 standalone Bevy/Rust successor (2026-10-09)

**Owner instruction (supersedes host-engine goal for the NEW edition only):** Build a new **standalone Bevy/Rust version** of the Fallout: New Vegas + Garry's Mod + THUG2 mashup. It must coexist with the legacy Fallout/NVSE edition during migration. **Prioritize Bevy going forward; legacy may later be discontinued after acceptance, not deleted or overwritten now.** The legacy edition, its installed files, v85 protected identity, v86 candidate, rollback evidence, saves and branch history must remain intact.

## Canonical repository and reading order

- https://github.com/bertjerk660-dotcom/REM1
- https://github.com/bertjerk660-dotcom/REM1/blob/main/AGENTS.md
- https://github.com/bertjerk660-dotcom/REM1/blob/main/context/BOOTSTRAP.md
- https://github.com/bertjerk660-dotcom/REM1/blob/main/context/GOAL.md — **historical Fallout-host target, not the new engine architecture**
- https://github.com/bertjerk660-dotcom/REM1/blob/main/context/ARCHITECTURE.md — **historical Fallout-host target**
- https://github.com/bertjerk660-dotcom/REM1/blob/main/context/CURRENT_STATE.md
- https://github.com/bertjerk660-dotcom/REM1/tree/implementation/opus-o00-golden-bench-20261009
- https://github.com/bertjerk660-dotcom/REM1/tree/prep/opus-ready-20261007
- https://github.com/bertjerk660-dotcom/REM1/tree/research/gmod-ui-physgun-20261008
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/context/AGENT_OWNERSHIP.md
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/context/FAILURE_KNOWLEDGE.md
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/context/PROVENANCE_INDEX.md
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/builds/O00_golden_bench_candidate_20261009.json
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/builds/O01_toolgun_candidate_v86_20261009.json
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/context/HANDOFFS/CODEX_O00_CANDIDATE_READY_2026-10-09.md
- https://github.com/bertjerk660-dotcom/REM1/blob/implementation/opus-o00-golden-bench-20261009/build/prepared/opus_prep_2026-10-09/00_README_OPUS_START_HERE.md

Additionally read context/DECISIONS.md, context/OPEN_WORK.md, context/GMOD_2026-10-07/README.md, all matching context/HANDOFFS/OPUS_* and CODEX_* handoffs, manifests, reports, accepted dependencies and remaining issue #5. Branch presence is not evidence of in-game success.

## Current evidence as of handoff

- **Old host-engine branch is not finished.** The main branch describes Fallout as the host; that remains true only for legacy.
- New Bevy work is **not yet a validated playable Bevy game**.
- O00 Source bench conversion has a recorded successful **Opus self-test** but not independent Codex confirmation. O01 Toolgun visual + v86 DLL has static and Opus self-test evidence, but the manifest still marks independent runtime/playability tests NOT RUN. Neither is Bevy engine porting.
- Opus implementation branch named `implementation/opus-o00-golden-bench-20261009` is 194 commits ahead of main at the initial handoff inspection; recheck its current tip and compare before touching any file.
- Preparation readiness 81/100 on pre-existing scoring; do not carry it into a Bevy success percentage. Codex C01-C08 still track old-engine evidence gaps where reusable.
- Protected legacy hashes are in build manifests; do not overwrite/modify the deployed FNVGModTHUG2.dll, REM_GModTHUG2.esp, original save files or active Data files.
- Local machine has Rust 1.99.0 MSVC toolchain; Cargo 1.99.0; Bevy 0.20.0 dependency in an **isolated local installation probe** at `C:\Users\BRAD\Documents\------\Engineer Station\rem1_bevy_install_probe`. This is a toolchain/dependency probe, **not** a checked-in Bevy game.
- IDA Pro 6.8 installation is present at `C:\Program Files (x86)\IDA 6.8`; do not use IDA 9.3. The THUG2 disc binary analyzed in existing research is **PS2 SLES_526.21, 32-bit little-endian MIPS ELF**, not a PC executable.

## Connection and preservation

Use Claude Code with its connected GitHub integration and an authorized Remote Desktop Commander session (Windows device DESKTOP-6PTSS3D) where available. Do not invent permissions, claim remote access if unavailable, or ask to repeat a confirmed source path. Source workspace: `C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2` is **not a Git checkout**; inspect rather than trying `git commit` in it. Current authored NVSE source reported under `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp` and `gmod_overlay.inc`. Verify local installed Steam GMod/FNV dirs and THUG2 PS2 paths rather than guessing. Keep proprietary source-game content local, with provenance/hash/import scripts recorded to GitHub. Audit project-authored source absent from GitHub and plan source-preservation without committing third-party secrets/binaries.

**Earlier Claude/Opus ordinary chat is relevant but not proven durable state:** if the previous Claude conversation/artifacts are accessible, read its latest handoff, commits, local files and outputs. Compare everything against the **current remote branch**, local hashes and manifests. Keep verified existing work, do not redo O00/O01 discovery or discard it. If prior chat is inaccessible, use repository/history and local files, label missing context explicitly and continue rather than assuming prior actions happened.

## Edition isolation and branch discipline

1. Start from current REM1 GitHub and this handoff. Record exact base SHA. Use a **new isolated `engine/bevy-standalone-20261009` branch** for the edition, or retain an existing newer standalone Bevy branch after checking for concurrent writes. Never force-push, reset or modify legacy branch.
2. Put all new game source and pipelines under `engine/bevy/` (or a documented equivalent); create distinct `Cargo.toml`, `Cargo.lock`, .gitignore, reproducible CLI scripts, configs, tests, engine-specific manifests and docs.
3. Keep old Fallout/NVSE source, DLL/ESP/runtime/historical branches available as reference and rollback. Do not depend on launching Fallout to run Bevy edition.
4. Keep separate version numbers, build artifacts, user saves, file layouts, launcher names and validation for `legacy-fnv` and `bevy-standalone`. Record proposed deprecation criteria, not an immediate deprecation claim.
5. Never merge old runtime candidates just because their branch contains useful docs; selectively port verified evidence and reusable authored tools.

## Required game design and systems

Goal: a coherent **standalone 3D game running on Bevy** using the Fallout: New Vegas world/design as baseline and source-faithful Garry's Mod/THUG2-derived systems. New game must **not require FalloutNV.exe/NVSE**, while preserving the recognizable Fallout-style progression, inventory/Pip-Boy interaction and default movement/combat loop.

- GMod **real Q/spawn-menu behavior**: categories, search, real useful prop thumbnails, curated roughly 290-300 props (not 13,003 raw), tool-selection state, spawn permissions/placement, undo/cleanup, Duplicator, Remover and model changer, proper input ownership.
- GMod Toolgun: script/source-evidenced modes/actions, real GMod-style VGUI/popups/sounds/visuals, Q-driven modes, no fake Fallout top-left prompt. Original GMod Lua/SWEP/stools are evidence; create a justified compatibility/Rust adaptation rather than falsely promising direct Derma execution.
- GMod Physgun: source-evidenced acquisition range, hold/rotate/freeze/unfreeze/launch, beam and highlight, continuous hold audio, NPC ragdoll on TARGET only. Project-owner mapping: **LMB grab/interact, RMB release/launch** as currently specified, with complete keyboard/mouse and Xbox equivalents.
- THUG2: skateboard is an equippable, visible and droppable item in the Fallout-like inventory. LMB toggles **full THUG2-style free-roam skate mode**, holster/exiting returns to Fallout-like controls. When skating the THUG2 HUD replaces Fallout HUD, controls/animations/board hand-to-feet/camera/momentum/trick-combo/SPECIAL/balance/manual/grind/lip/wallride/revert/bail/recovery/audio are source-evidenced. Grinds require genuine grindable collision/contact, not simply G key anywhere. Include Xbox and KBM control switching without double-binding.
- World import: recover Fallout world and relevant metadata from the owner's installed files via deterministic conversion pipeline. Define format/legal/provenance boundaries and coordinate transform, scale, collision, streaming/LOD/materials/lighting/navmesh/spawns, saves and quests. Do not claim full-map parity from an empty test map.
- Cross-system: state ownership (Fallout default/GMod contextual Q/THUG2 exclusive skating HUD), physics stability, common world object identities, save-load persistence, gamepad support, camera/animation transitions and robust error recovery.
- Preserve provenance: only source-backed assets/behaviors where possible, no fabricated 'authentic' code, and avoid uploading proprietary game assets to public GitHub without redistribution rights.

## Reverse engineering and design process

Codex remains default investigation/independent validation agent. Opus owns **all implementation and integration**. Opus may do **narrow, specifically recorded** IDA investigations where essential to unblock code (decision D-009A), or hand evidence work to Codex. Use **IDA Pro 6.8 only** on owner-authorized local binaries. GMod Lua/Derma often supplies original tool/menu behavior; use native reversing only for uncovered engine boundaries. THUG2 PS2 executable requires proper MIPS/ELF architecture and verified SHA. Save function signatures, call graphs, provenance, uncertainty, tests, and offsets/hashes in REM1; translate gameplay semantics into testable Rust modules rather than assuming binary code directly links to Bevy.

Propose ECS/plugin boundaries for Fallout core, GMod tools/Q, THUG2 skate state, common interactions, input/camera, renderer/UI, physics and collision, save/asset pipelines. Pick an actively compatible Bevy 0.20 physics/ragdoll solution only after checking versions and APIs, test minimum build and performance first. No silent feature substitutions.

## Immediate ordered tasks for Claude Code

1. Bootstrap/read named repo files and all latest branch/commit/issue evidence; compare local source, the previous Claude conversation if available, and latest Opus outputs. Produce reconciliation report: confirmed / inferred / blocked / needs owner input.
2. Inspect Rust, Cargo, installed MSVC tooling, Bevy probe and IDA 6.8 on the actual machine. Confirm dependencies, MSVC linker and current installed-game source locations and hashes. Report failures honestly.
3. Record Bevy successor decision in context/DECISIONS.md, context/GOAL.md and context/ARCHITECTURE.md **without erasing historical legacy target**; record new per-edition CURRENT_STATE and migration roadmap with exact origin SHA.
4. Create isolated Bevy Cargo workspace with clear crate/component boundaries. Build a **minimal runnable Bevy window** with stable 3D camera, lit test mesh, controllable capsule, solid ground and keyboard + Xbox input probe. Add deterministic tests and a smoke-test log (boot/exit, frames, controls, crash absence); distinguish automated from human tests.
5. Prove first real import path using ONE authorized Fallout-derived static asset through authored conversion script and correct texture, scale and collision. Preserve hashes and source path; no batch import until proof passes.
6. Port shared entity/interaction model; then add a small GMod prop spawn + physics interaction vertical slice and THUG2 state-transition skeleton. Prioritize playability and save-load, not only UI appearance.
7. Create traceable milestone matrix from legacy features/evidence to Bevy components, unit/integration/manual tests, ownership and acceptance gates. Continue incrementally without redoing proven research; do not label unfinished features complete.
8. After each meaningful iteration run formatting, clippy, cargo test, cargo build/check and practical game validation when possible, record output SHA, commit branch, push, re-fetch and confirm remote SHA. Write CHANGELOG, builds/* manifest, context/CURRENT_STATE.md edition-specific status, failure knowledge and next actions.

**Deliver first:** reconciliation, architecture ADR, isolated Bevy source scaffold, runnable smoke build if toolchain works, and complete reproducible instructions. No destructive changes, no unverifiable progress claims. Final report must include remote branch, full commit SHA, Bevy/Rust versions, tested outcome, legacy-protection check and remaining blockers.
