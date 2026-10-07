# Repository reconciliation — 2026-10-07

## Canonical state and scope

Canonical repository: `bertjerk660-dotcom/REM1` (private). The session-start main head is `3610b370d62fb0daa86b10f819b7704ab096809b`, containing **52 blobs**, principally documentation and prepared metadata rather than the actual plugin source tree. The session's evidence branch is `prep/gmod-dependency-evidence-20261007`. Exact heads of all 13 observed branches, 20 recent main commits, the complete main blob inventory and open pull requests are preserved in [repository_snapshot.json](../../manifests/gmod_2026-10-07/repository_snapshot.json). Those GitHub facts were collected by the root agent and read by this auditor; this is not a claim of a second independent API fetch.

The latest main commits add/link the GMod overlay contract (`99e49c2`, `83f205c`) and THUG2 overlay contract (`046d992`, `3610b37`), reconcile the exclusive Opus handoff (`7de9700`) and record the latest human playtest failures. Their recency is a reason to preserve their acceptance and ownership boundaries, not evidence that runtime integration is complete.

Open draft PRs: [#1](https://github.com/bertjerk660-dotcom/REM1/pull/1), `prep/support-workflow`, and [#2](https://github.com/bertjerk660-dotcom/REM1/pull/2), `prep/astra-prompt4-workflow`. The issue search returned no entries; that result did not establish absence of open PRs. No issues or PRs were modified by this audit.

The supplied Windows project directory `C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2` is **not a Git working checkout**. `/workspace/REM1` is a fetched evidence workspace, also not a checkout. A separate true Windows Git checkout has not been established. Do not fabricate a branch or claim the Windows runtime files have been reconciled with a local Git HEAD. GitHub branch history remains the canonical comparison layer.

## Required reads and cross-branch recovery

The auditor read `AGENTS.md`, `context/BOOTSTRAP.md`, `GOAL.md`, `ARCHITECTURE.md`, `CURRENT_STATE.md`, `DECISIONS.md`, `FAILURE_KNOWLEDGE.md`, `OPEN_WORK.md`, `SUPPORT_20_POINT_TRACKER.md` and `HANDOFFS/OPUS_5_5_EXCLUSIVE_INTEGRATION_2026-10-06.md`, plus pipeline, asset policy, validation and local-workspace notes. The complete read/hash catalogue is [prior_evidence_catalog.json](../../manifests/gmod_2026-10-07/prior_evidence_catalog.json).

`SUPPORT_20_POINT_TRACKER.md` was absent from session-start main, but present on `prep/support-workflow` at `492c3dc7c23bbcac9eb8c2a52b5e61e32fda775b`. Likewise, `HANDOFFS/ASTRA_GMOD_QMENU.md`, `ASTRA_TOOLGUN.md` and `ASTRA_PHYSGUN.md` were absent from main, **not absent from GitHub**. The root recovered them from that support commit. The earlier main overlay handoff's statement about missing canonical inputs is therefore a branch-local publication gap, not loss of discovery. Recovered aliases now identify their original branch/commit/blob and link this pass's findings.

Additional support documents read: `context/ASTRA_HANDOFF_{QMENU,TOOLGUN,PHYSGUN,WEAPON_PRESENTATION}.md`, `context/HANDOFFS/ASTRA_WEAPON_MODELS.md`, and `builds/gmod_{qmenu_source_inventory,hl_weapon_staging_audit,prop_menu_curated}_20261006.json`. The support tree has 111 blobs according to root reconciliation; this audit does not claim to have reread every unrelated THUG2 payload manifest.

The older physgun handoff specifies RMB pickup/hold and LMB launch. The user's explicit 2026-10-07 requirement supersedes that project mapping: **LMB interacts/grabs; RMB provides the requested launch/release action**. Keep the original GMod native semantics separately evidenced. No runtime control was changed during reconciliation.

## What prior discovery must be preserved

| Subsystem | Existing durable evidence | Preserve / remaining boundary |
|---|---|---|
| Q/spawn menu | Build ID 25375506; 105 relevant Lua files, including 33 spawnmenu files; 46 referenced/created VGUI classes; 29/29 direct UI/material refs resolved | Reuse inventory, hashes and original scripts; tracing and VGUI/input bridge remain required. Inventory counts do not prove runtime parity. |
| Curated browser | 290 ready entries: 170 native FNV + 120 Source/GMod; bindings, search tokens, categories and 128×128 support thumbnails | Preserve compact library and bindings. Thumbnails remain fallback/audit evidence and cannot replace original SpawnIcon behavior. |
| Tool Gun | Original `gmod_tool/shared.lua` and `stool.lua`, 40 stools, c_toolgun/w_toolgun, ToolTracer/selection_indicator, Toolgun.Single | Preserve Q -> `gmod_toolmode` -> selected tool object's LeftClick/RightClick/Reload chain. No Fallout tool selector. |
| Physgun assets | `weapon_physgun.txt` / `weapon_physcannon.txt` hashes; w_physics model/collision, beam/glow materials, On/Off/Special1 events | Exact legacy v_physics MDL/VVD/DX90.VTX unresolved. c_superphyscannon candidate is not proof of exact presentation. |
| Native physgun | Prior IDA 6.8 client/server exports and behavior reports; m_hGrabbedEntity/local hit/controller/range/input evidence | Preserve evidence, revalidate module/function attribution. Prior phrase “evidence complete” does not prove freeze routine, exact native mouse actions or FNV runtime success. |
| Weapon presentation | 71/71 concrete model refs staged; 48 view and 48 world candidates, QC/SMD evidence | Geometry/material conversion is not first-person animation parity. 49 weapon records audited, 47 presentation-clean; RPG fix sidecar remains disabled. |
| Source weapon sounds | All 15 previously unresolved named events found; 14/15 have every payload confirmed | Do not interpret “zero unresolved event refs” as proof every referenced audio payload is present. Do not use old 21-unresolved summary as current truth. |
| Runtime | Central PollControls and established weapon/menu/physgun boundaries documented | Preserve working cleanup and form timing; source hashes have changed since the older integration map. |

Historical asset counts have different scopes: recovered aliases say 27/28 direct visual/audio refs; support tracker later reports 33/36 exact model/material/effect dependencies; the narrower main physgun manifest contains 15/18. These are not contradictory denominators and should not be merged into a single total. Their explicit common gap is the legacy first-person triplet.

Prior inventory provenance: Steam appmanifest SHA-256 `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`; garrysmod_dir.vpk SHA-256 `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`; Q inventory manifest SHA-256 `A499117503C53710B91AE27C401DBFCF53F23C4B741B3AF29FD0A43C06B0774B`. These are prior recorded identities, not fresh file hashes from this auditor.

## Source/runtime divergence and concurrency guard

[runtime_snapshot.json](../../manifests/gmod_2026-10-07/runtime_snapshot.json) records root's read-only current Windows inspection at `2026-10-07T05:16:57Z`:

| File | Current SHA-256 |
|---|---|
| `third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp` | `4517D804A6B61B51B2E0751777949BCAE61AC470E5572BFAD070BF2103DB64CE` |
| `gmod_overlay.inc` | `E6EF0C484AFDDC1A74C02F6BA8A72CD0899D6E80F5BA5459CD61B9C67183250F` |
| Deployed `Data/NVSE/Plugins/FNVGModTHUG2.dll` | `D6C8881699852B6ABBC6FE7D16C758FAD700D1FDF1A73BB40502CCC4B68B5206` |
| Deployed `Data/REM_GModTHUG2.esp` | `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7` |

Current source reports version 85 and the support-patch combine-autogive label. A source label does not prove the deployed DLL build; preserve binary identity by hash. The older canonical CURRENT_STATE v81 DLL/ESP identities and RUNTIME_INTEGRATION_MAP source hash `CE3628...` are stale against these supplied files. Its historical line numbers are navigational hints, not current offsets. Do not replace the current source with an older GitHub map or claim the version85 path has been playtested in this pass.

Failure knowledge F007 requires source/hash/mtime rechecks before modification or deployment. Support tooling and documentation may proceed; the exclusive Opus handoff reserves substantive UI/gameplay/model/runtime integration. This investigation did not modify any runtime source, DLL, ESP, deployed payload or unrelated THUG2 implementation.

## Existing implementation and protected positives

Current main playtest notes classify the visually correct custom prop menu as a **placeholder**. Tool/physgun feedback through Fallout top-left boxes is also temporary. The latest recorded physgun failures are short acquisition range, incorrect held-target loop and actor unconscious handling hitting PlayerCharacter rather than the acquired actor. Preserve these as regression requirements rather than declaring a fix based on static evidence.

Preserve verified held-skateboard visibility/placement, LMB skate entry, holster exit and reported working THUG2 sounds. Preserve ESP-owned skateboard identity, delayed runtime form initialization, root-aware bone caches and safe camera transitions from F001–F005. Do not run historical `research/patch_v74_advdupe_physgun.py`; support tracker marks it known-bad/do-not-run.

## Existing staging and publication policy

Root verified existing Windows `build/prepared` directories: `gmod_qmenu_source_inventory`, `qmenu_content_adapter`, `final_prop_catalog_handoff`, `gmod_prop_menu_curated`, `gmod_prop_catalog_sidecar`, `gmod_hl_weapon_models`, `gmod_tool_physgun_assets`, `gmod_tool_physgun_asset_handoff`, `gmod_weapon_props`, `gmod_weapon_runtime_candidates`, `agent_handoff_2026-10-06`, `prop_menu_content_handoff`, `prop_support_phase3`, `prop_support_phase4`, `input_control_matrix`, `historical_artifact_registry`, `regression_test_packs`, `release_install_manifest`, `support_sidecars` and `weapon_presentation_fix_sidecar`. Other THUG2 stages exist and remain outside this audit's mutation scope.

Use those stages and check their manifest paths/hashes before extraction. Metadata presence does not imply every original staged payload was rehashed. Never bulk-copy the installation or create replacements for unresolved files. Repository privacy alone is not authorization to publish proprietary content: user and AGENTS instructions permit authored tooling, hashes, provenance and evidence; extracted/decompiled game payloads remain local.

## Metadata reproducibility defects

This auditor independently inspected every locally fetched main `build/**/*.json` listed in the catalogue. All ten contained an appended `[executed on device: ...]` marker after the JSON value; nine also had a UTF-8 BOM. This includes the runtime integration map and physgun implementation manifests, not just orchestration files. A strict parser rejects the trailing marker. For this read audit only, the leading JSON value was decoded with UTF-8-sig and JSONDecoder.raw_decode, and the tail was recorded separately. Original files were not repaired or overwritten. New manifests must be strict JSON; any future normalization should preserve original SHA-256 and transformation provenance.

The main physgun implementation manifest lists 15 resolved assets, while the prepared physgun package also includes `materials/sprites/physgbeamb.vmt`. Keep these scopes separate when reconciling dependency completeness.

## Coverage limits and remaining work

The catalogue distinguishes independently read local metadata from root-collected GitHub/Windows facts. It covers every required bootstrap document, every locally fetched main GMOD package, the recovered support handoffs and three targeted support summaries. Full lower-level Windows manifests, every historical branch's runtime source, a true Windows Git checkout, current payload hash comparison and end-of-pass concurrency comparison remain root-owned or explicitly unresolved; this audit does not claim exhaustive lower-level inspection.

The child auditor's GitHub/remote batches hung twice without returning results and were canceled. They provided no independent API or Windows evidence and caused no intentional mutation. The completed report uses bounded local reads and root's recorded snapshots instead. No further remote tool execution is needed for this audit.
