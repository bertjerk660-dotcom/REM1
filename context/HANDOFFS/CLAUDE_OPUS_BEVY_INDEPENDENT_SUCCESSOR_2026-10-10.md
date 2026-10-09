# Paste into Claude Code / Opus: REM1 Bevy successor kickoff and continuation
Date: 2026-10-10. Primary engineering track: REM1 Bevy (Rust standalone game). Legacy REM1 Fallout NV/xNVSE remains preserved.

You are Claude Code running Claude Opus, the sole implementation and visual/gameplay integration engineer on REM1. Operate on my connected Windows PC when available, with the authorized remote terminal/Desktop Commander and the connected GitHub repository. Continue the work I discussed with you earlier in regular Claude chat, but do NOT take anything claimed in that chat as compiled, installed or verified until you reconcile it with the newest repository commits and actual on-disk files.

## 1. Repository: durable authoritative truth
Canonical GitHub repository: https://github.com/bertjerk660-dotcom/REM1
Main repository tree: https://github.com/bertjerk660-dotcom/REM1/tree/main
Latest reviewed Opus legacy implementation branch: https://github.com/bertjerk660-dotcom/REM1/tree/implementation/opus-o00-golden-bench-20261009
Bevy project decision and your handoff branch: https://github.com/bertjerk660-dotcom/REM1/tree/prep/bevy-opus-handoff-20261009
Start with the newest of these branches after inspection and compare actual SHAs; do not assume main contains the newest source. At the 2026-10-10 review the Opus implementation branch was 194 commits ahead of main and zero commits behind. Do not reset, force push, merge legacy runtime candidates, or overwrite anybody else's work.

Read AGENTS.md; context/BOOTSTRAP.md; context/GOAL.md; context/CURRENT_STATE.md; context/ARCHITECTURE.md; context/DECISIONS.md; context/FAILURE_KNOWLEDGE.md; context/OPEN_WORK.md; context/AGENT_OWNERSHIP.md; context/PROVENANCE_INDEX.md; context/BEVY_PARALLEL_TRACK_DECISION_2026-10-10.md; relevant Opus launch and Q-menu, Physics Gun, Tool Gun, THUG2 and input packets; the 2026-10-09 preparation cover note; builds/O00_golden_bench_candidate_20261009.json and builds/O01_toolgun_candidate_v86_20261009.json; and current commits, issues and branch differences. If a named document does not exist on main, look on the source branch, not an old snapshot ZIP. Read relevant source files, manifests, dependency graphs and failure ledgers before designing or changing systems.

## 2. Explicit new owner decision: TWO VERSIONS, not an in-place rewrite
- REM1 LEGACY is the existing Fallout New Vegas host mod: FalloutNV.exe, ESP, NVSE plugin DLL, existing game installs and save files. Leave it operational, backed up, with known hashes and rollback. It will likely stop receiving major new development, but it is not deleted or declared retired. Keep its old releases and evidence.
- REM1 BEVY is a completely independent standalone game made using Rust and Bevy; it is the PRIMARY development track from here onward. Bevy is the actual engine/runtime replacing Fallout NV as host only in the NEW version. It is NOT merely a Bevy tool, plugin inside NVSE, or graphical overlay over the old Fallout executable.
- The two versions coexist within REM1 GitHub with distinct source trees, branches, dependency graphs, build identifiers, validation reports and release outputs. Prefer a new bevy/ Rust Cargo workspace; do not move or overwrite the legacy source tree to make room. Create an isolated implementation/bevy-* branch from a verified preparation ref.
- Existing legacy source and converted evidence remain valuable references for world data, system behavior, asset pipelines and acceptance tests. Their successful static conversion does NOT mean Bevy compatibility or gameplay equivalence. No legacy implementation claim should silently become a Bevy acceptance result.

## 3. Previous regular Claude conversation: validate and CONTINUE
I have already fed you project instructions, architecture, proposed Rust engine roadmap and reverse-engineering research in a prior non-Claude-Code chat. First locate any accessible previous Claude conversation, artifacts, plans or local Claude Code sessions on this authorized account/PC and gather the material relevant to REM1. If the earlier chat is not accessible through your connected environment, state that limitation in a documented reconciliation report and proceed using GitHub and local evidence rather than inventing chat content.

Build a previous-work reconciliation table: earlier proposal or claim; exact file/branch/commit/input; what was actually completed; reproducible test evidence; conflict with current repository; decision to reuse, revise or abandon. Prioritize preventing duplicated work, preserving the proven original-game research, and continuing any legitimate already-started Bevy work rather than starting from scratch. Do not block meaningful Bevy bootstrap because prior chat data cannot be recovered.

## 4. Verified local Windows tooling / original game locations
Project local research and legacy build workspace:
C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2
This directory was observed to NOT be a Git checkout. Reconcile any project-authored source files missing from GitHub, review licensing and secrets, then put permissible source/tooling/manifests in the correct REM1 branch, never raw copyrighted game binary dumps.

Fallout New Vegas local install:
C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas
Garry's Mod local install:
C:\Program Files (x86)\Steam\steamapps\common\GarrysMod
Fallout 3 GOTY reference install:
C:\Program Files (x86)\Steam\steamapps\common\Fallout 3 goty
IDA PRO 6.8 (EXACT REQUIRED VERSION):
C:\Program Files (x86)\IDA 6.8\idaq.exe
and its ida/idaq64/idaw tools as appropriate to the specific input. The PC also has IDA Professional 9.3 installed, but it is NOT approved for this project. Before native research, confirm IDA Pro 6.8 is launched and preserve the input binary hashes, image base, architecture, function evidence, dataflow, reproducible notes and source attribution.

THUG2 original source identity in REM1 is PS2 SLES_526.21, 32-bit little-endian MIPS ELF, recorded SHA256 91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1. Discover its current physical path and re-hash it. Do not invent a PC THUG2 executable or treat decompiled pseudocode as compiled Rust. Use original installed GMod Lua/Derma/SWEP/stool and verified Source scripts where applicable; IDA 6.8 for native behavior not exposed by scripts. Codex is the default investigator and independent runtime validator; Opus may perform narrowly necessary investigation to unblock Opus implementation under D-009A, documenting it to the same standard.

Rust stable MSVC x86_64 was installed and checked locally on 2026-10-10:
rustc 1.99.0 and cargo 1.99.0. Bevy 0.20.0 is registered through crates.io in isolated local probe:
C:\Users\BRAD\Documents\------\Engineer Station\rem1_bevy_install_probe
Treat this as an installation/smoke-test probe, not as the real REM1 Bevy codebase. Create the new authoritative Bevy source in the GitHub-backed working tree. Validate Visual Studio C++ build tools and Windows SDK if a renderer/native build requires them. Refer to https://bevy.org and https://bevy.org/learn/quick-start/getting-started/ for official engine setup.

## 5. Product vision: one coherent crossover, not an asset museum
Construct an independently running Fallout-world-inspired game that hosts the GMod building/physics interaction systems and a switchable THUG2 free-roam skating subsystem. First retain essential exploration/world interaction, combat, inventory, collision, AI/navigation, loading/saving and player identity. On skateboard equip and left-click, switch player-facing movement physics, camera, input, animation, board state and full HUD to THUG2-derived skating. On holster/exit, restore default gameplay and HUD, without corruption, permanent bindings or lost world state. THUG2 story, missions, levels, narrative population and campaign are OUT OF SCOPE; the Fallout world remains the traversable setting.

THUG2 movement requirements: precise state transition evidence for carrying/holding board, mounting, pushing, coasting, turning/carving, crouch, ollie, air/landing, manuals, lip tricks, wallrides/wallplants, grinds, reverts, flip/grab tricks, specials, combos/scoring/special meter, bails/falls/recovery/board break and animations/retargeting. The board must migrate correctly between hands and feet and collision eligibility must be geometry-aware: pressing G cannot trigger grinding anywhere. Source-faithful HUD/UI/popups and audio should replace legacy Fallout text fallback in skating mode.

GMod requirements: source-faithful working Q/spawn menu with genuine tab/category/search/icon semantics, curated relevant prop browser, model changer if viable, selected Tool Gun modes, Duplicator/Remover and tool/cleanup lifecycle. Use actual GMod Lua/Derma definitions/logic as behavior references and only necessary Bevy-adapted functionality, not the legacy placeholder custom Q-menu. Physgun must use accurate acquisition, beam/highlight, continuous hold sounds, held-object rotate/move/freeze/unfreeze/release/launch, actor-target identity (ragdoll target, NEVER the player), adequate range and proper entity cleanup. Preserve user requested Physgun controls: LMB acquire/interact and RMB launch/release, then define secondary actions through explicit mapping. Avoid using Fallout top-left prompts for GMod tools. Curate props useful for skating and construction, not the full thousands-entry archive.

Keyboard/mouse and Xbox controller are both mandatory. Build a shared action-input adapter with explicit control ownership and mode/focus switching. Do not copy physical input-event plumbing from FNV directly into Bevy as an assumed runtime dependency.

## 6. Implementation architecture and phases
Design a modular Bevy ECS/gameplay architecture in Rust with separate modules/plugins for application bootstrap, content provenance/loading, streaming world/scene graph, physics and collision, player state, AI/NPCs, inventory/equipment/combat, game modes and transitions, keyboard/controller input, camera, THUG2-style skating, GMod tools/props/Q menu/notifications, UI/audio, save/load, diagnostics and tests. Use a fixed timestep for physics and deterministic playback/replay tests where useful; separate coordinate systems, animation rigs and content units through well-documented converters. Choose Bevy-compatible physics and animation libraries after checking actual current API/version compatibility rather than assuming historical packages will compile.

Phase A — audit and foundation: inspect repo and Windows source, establish branch, map previous Opus claims, protect baseline, define rights/provenance/content mount, record Bevy engine/toolchain versions and migration acceptance matrix. Create bevy/Cargo.toml and Cargo.lock, a minimal executable and reproducible build scripts/tests. The official standalone Bevy window should launch. Commit.
Phase B — playable vertical slice: a small walkable collision-enabled test environment, controllable character, stable camera, keyboard/mouse and Xbox action routing, physics, interaction, basic item/equip state and save/load. Capture real boot/playtest evidence. Do NOT claim the whole Fallout world is ported based on one scene.
Phase C — world/asset pipeline: select one small actual Fallout world region from the user's own installation, inventory references, legally mount local assets, transform/import models, textures, scale, collision, navigation, lighting, audio and world triggers. Verify visible geometry, collision, orientation and performance. Build automated conversion and missing-resource checks; record import hashes and mappings rather than raw commercial game resources in public GitHub.
Phase D — skating: migrate complete THUG2-derived free-roam behavior subsystem-by-subsystem, test each movement/camera/animation/HUD/audio state, board hand/foot transforms, accurate grind eligibility, controller mapping and transition to/from baseline.
Phase E — GMod: implement actual Q-menu interaction semantics, curated prop spawn and physics, Tool Gun selected modes, Duplicator/Remover, Physics Gun beam/hold/throw/freeze/actor targeting, GMod-style feedback and cross-mode input ownership. Verify in-world persistence and cleanup.
Phase F — overall gameplay quality: world-scale traversal, content streaming, Fallout-like inventory/combat/AI/progression, audio and UX, save persistence, performance, accessibility, packaging and complete cross-system regression. Only then recommend a distinct decision to stop active legacy development.

Prioritize the smallest playable vertical slice that proves Bevy's engine, controller/camera, physics, persistence and one imported object before promising a whole-game conversion. Keep source-faithful behavior goals, but do not promise bit-identical physics/animation across radically different host engines without actual evidence/tests. For systems without clear port evidence, mark confidence and gaps explicitly.

## 7. Existing achievements and failure knowledge to preserve
- Legacy player-held skateboard visible and properly located in hand, with LMB skate activation / holster exit observed in prior human tests.
- Legacy Fallout HUD persists during skate mode; no genuine THUG2 runtime HUD; board fails to attach to feet; THUG2 animations broken; G can grind anywhere.
- GMod prop menu looks plausible but is NOT real Q-menu parity. Physgun had extremely short targeting range, incorrect continuous grab audio and misapplied knockout to the player.
- O00 bench Source-to-FNV conversion has a manifest and static/reproducible validation; Opus own runtime selftest exists, not independent Codex validation. O01 Tool Gun visuals and v86 identity changes have a candidate manifest and incomplete independent runtime/human playtest. These are legacy proofs/known hazards, not Bevy completion. Read failures F001–F019, including bad bone-pointer caching, stale DLL/ESP hashes, geometry frame rotation, NIF/endian reproducibility, and material alpha issues. Port lessons, not invalid binaries.
- Last published preparation readiness score was 81/100 under the LEGACY Codex/Opus evidence rubric; do not call Bevy 81% complete or claim that migrated content is ready to ship.

## 8. GitHub storage is mandatory throughout development
Work on an isolated implementation/bevy-* branch. Prefer placing original Rust code, configs, tool scripts, test fixtures that you authored and docs under a bevy/ directory. All important progress must survive this chat and this PC. For every meaningful iteration:
1. Preflight hash check + clean/dirty status + branch SHA + source identity.
2. Plan a small deterministic feature milestone with acceptance criteria.
3. Implement safely, preserving rollback, keeping local third-party binary assets uncommitted.
4. Build, run format/lint/unit/integration checks, boot/gameplay smoke and target acceptance tests.
5. Save dated structured JSON manifests (parent build, branch, source SHA, engine/compiler/tool versions, input hashes, outputs, validations, test outcomes, known issues and rollback).
6. Record exact failures/reproductions and proven prevention in context/FAILURE_KNOWLEDGE.md or a new Bevy-specific failure index.
7. Update Bevy-specific CURRENT_STATE, architecture, goal/open work, decisions, evidence index and migration roadmap. Keep legacy records accurate; never rewrite historical data to make progress look better.
8. Commit, push, verify remote branch and SHA, and give me the precise result/next milestone. If auth/push is blocked, say so plainly and leave local commits plus precise instructions; do not claim they reached REM1.

Keep copyright and trade-secret content out of the repository and distribute only what is lawful. For private testing mount owner-installed content locally; publish only authored, cleared assets/code or a downloader/mount workflow requiring the user's own lawful installations. Do not use pirated sources or bypass DRM.

## 9. Immediate deliverables: BEGIN WORK, do not stop at a proposal
Start by comparing the authoritative latest REM1 work with the earlier Claude plan and actual Windows PC. Create a Bevy-specific implementation roadmap and source-layout; write a clean standalone boot target in Rust, with a smoke test and reproducible Cargo build. Verify the result on the PC. Save the first Bevy build manifest, screenshot/log/evidence as appropriate, and push the branch. Tell me what really runs, which hashes/versions were tested, what the first playable slice still lacks, and which legacy files were preserved unchanged. Continue forward to the next smallest useful implementation milestone without turning the work into generic brainstorming.

The only permissible definition of success is a stable, tested, enjoyable game. A dependency installation, script that converts models, or a compile-only pass is NOT a playable game.
