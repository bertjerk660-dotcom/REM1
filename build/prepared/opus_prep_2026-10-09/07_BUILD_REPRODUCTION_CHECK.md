# 07 — Build reproduction check (2026-10-09)

Question: was the deployed `FNVGModTHUG2.dll` built from the current `main.cpp`?
Answer: **not confirmed.** The feature set matches, but the compiled code does not reproduce byte-for-byte with this toolchain and configuration. The baseline stays unproven for byte identity.

## Setup
- Project: `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/FNVGModTHUG2.vcxproj`
- Compiler: MSBuild from Visual Studio 2022 Community (toolset v180), Windows SDK 10.0.
- Outputs redirected to temp folders. Deployed DLL not targeted.

## Release|Win32 — compiles
- Output: `rem_rebuild_check_2026-10-09\out\FNVGModTHUG2.dll`, 908,800 bytes
- SHA-256 `EFBB0D13FB8ABC219517F7FE7F2BDFB8601721D7B09EB1F54AC727AEBF8DB03E`
- Deployed: `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206` (same size, different hash)

Byte comparison: 6,094 bytes differ. The PE timestamp differs, as expected. Most of the rest falls in the code region (approximately 0xCC104 to 0xDDD4E), so this is not a timestamp-only difference.

Marker strings (count in binary):

| Marker | Deployed | Rebuilt | Source |
|---|---|---|---|
| `THUG2-DIAG` | 27 | 27 | 31 |
| `retarget` | 3 | 3 | 11 |
| `v84` | 1 | 1 | 3 |
| `v85` | 1 | 1 | 2 |
| `heartbeat` | 0 | 0 | 4 |
| `Camera3rd` | 0 | 0 | 4 |
| `camera profile update complete` | 0 | 0 | 0 |

The source contains `heartbeat` and `Camera3rd`, but neither binary does, so those code paths are compiled out in both. The strings that do appear agree, which supports the feature-set match.

## Debug GECK|Win32 — does not compile
Errors: `main.cpp(769)`: `QueueUIMessage` undeclared. `main.cpp(1250)`: `CloneForm` is not a member of `TESSound`.
So this configuration did not produce the deployed DLL, and the current source is not clean under it.

## Post-build side effect
The project's post-build step copies to `$(FalloutNVPath)\Data\NVSE\Plugins` if that path exists. The deployed DLL was unchanged after both builds (hash and mtime checked). Before any future build, confirm `FalloutNVPath` is not set, or remove the copy step, so a build can't overwrite the deployed plugin.

## Conclusion and what would close it
- Feature set: consistent with `main.cpp` (v84/v85 markers, retarget logging).
- Byte identity: not reproduced. Possible causes, untested: a different compiler version, optimisation or link flags than this Release build; or a source revision with the same strings but different code.
- To confirm byte identity, the builder needs to supply the exact toolchain and command used for the deployed DLL. Record it in the manifest.

## Source-availability finding (blocking for Opus)
No commit on any branch of `bertjerk660-dotcom/REM1` contains `main.cpp` or the plugin project. The source exists only on the local machine. Opus cannot read the implementation from GitHub. Committing it needs an owner decision: the project-authored files are in scope under `AGENTS.md`, but some `.inc` files (for example `thug2_anim_data.inc`, about 470 KB, and `gmod_prop_defs.inc`, about 840 KB) may contain data derived from proprietary game assets, so they need an asset-policy review first.
