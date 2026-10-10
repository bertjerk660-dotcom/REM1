# Previous-work reconciliation (Bevy kickoff, 2026-10-10)

Required by `context/HANDOFFS/CLAUDE_OPUS_BEVY_INDEPENDENT_SUCCESSOR_2026-10-10.md` §2.

## Source availability
- **The earlier regular-Claude chat** (Bevy plans, research summaries) is **not accessible** from this Claude Code session. There is no conversation or export tool for it, and the project memory holds no Bevy plan content. Nothing from it is treated as fact. REM1 GitHub and on-disk files are the only sources used below. If the owner exports that chat into `context/`, re-run this reconciliation.
- REM1 GitHub was read at `origin/prep/bevy-opus-handoff-20261009` @ `dbe836a`, along with the legacy implementation branch `implementation/opus-o00-golden-bench-20261009`.

## Reconciliation table

| Earlier claim / work | Where | What is actually complete | Evidence | Decision |
|---|---|---|---|---|
| "Rust 1.99 / Cargo 1.99 / Bevy 0.20 installed and tested" | `Engineer Station\rem1_bevy_install_probe` | Confirmed. The toolchain compiled all of Bevy 0.20.0 for B001. | B001 build log, `rustc -V` in manifest | **Reuse** |
| Bevy physics via a plugin (avian/bevy_rapier) | handoff assumptions | Not possible: no plugin supports Bevy 0.20 | crates.io dependency ranges, checked 2026-10-10 | **Revise**, see D-B001 |
| Second Claude session's Bevy slice (`game.rs`, `lib.rs`, `modes.rs`, `save.rs`) | `REM1-handoff\bevy`, branch `implementation/bevy-vertical-slice-20261010` | **Uncommitted** and mixed with files from this session (F-B001). Never built successfully in its mixed state. | backup + hashes in `rem1_bevy_conflict_backup_20261010\snapshot_0418` | **Owner decision needed:** keep one slice as primary. B001 is the one with a passing build and test. The other session's `modes.rs` (game-mode state) and `save.rs` may hold ideas worth merging. |
| O00 Golden Bench (Source → FNV NIF pipeline) | `implementation/opus-o00-golden-bench-20261009` (3617fcf, 9404b96) | Static/reproducible pipeline plus Opus runtime self-test. No independent Codex verdict. | `builds/O00_golden_bench_candidate_20261009.json` | **Partially reuse.** Parsing Source SMD/QC/VMT/VTF, frame rotation (F013), the VTF alpha decoder (F017) and scale rules carry over to a Source→glTF path. The NIF/Havok writer is legacy-only. |
| O01 Tool Gun visuals + v86 DLL identity fix | same branch (e5f526c, 9deecc8) | World and first-person model in FNV and the identity fix are in the runtime self-test. Human playtest is incomplete. | `builds/O01_toolgun_candidate_v86_20261009.json` | Legacy-only. **Port lessons:** source-faithful model frames and material handling. |
| O08 Crowbar/Pistol/SMG1 conversions | same branch (1737f63 tooling) | Static validation 12/12 per weapon. Manifests and runtime record **not committed**. Owner playtest: pistol OK, SMG invisible. | local O08 files, owner report | Legacy task left open. The Bevy track reuses only the source analysis. |
| Physics Gun / Gravity Gun visuals in FNV | legacy | Invisible world models (owner playtest). Not fixed. | owner report | Legacy, deferred. Bevy will implement the Physics Gun natively (B002). |
| GMod Q-menu (IDA 6.8 research) | legacy research + Codex C01 packet | Research exists. No working menu in FNV. | `NEXT_CODEX_GMOD_C01_C03_KICKOFF_2026-10-09.md` | **Reuse research** for the Bevy Q-menu (B003) once C01 is reviewed |
| THUG2 skate mode in FNV | legacy DLL | Equip, LMB to activate and R to exit work. HUD, animations, camera and grinds are broken. | owner playtests | **Superseded** by native Bevy skate mode (B004). Source evidence (SLES_526.21 MIPS ELF, C04–C08) is still the basis for constants. |

## Legacy preserved unchanged by this work
- This branch adds files only under `bevy/`. No legacy source, DLL, ESP, NIF, plugin list or save was modified by the Bevy work.
- The deployed legacy runtime stays as last recorded: v86 DLL `787F46B0…6EC6`, `plugins.txt` = `FalloutNV.esm, REM_GModTHUG2.esp`.
