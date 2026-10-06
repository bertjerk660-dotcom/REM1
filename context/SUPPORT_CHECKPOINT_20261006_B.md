# Support Checkpoint B — 2026-10-06

This checkpoint completes the requested non-Astra preparation pass. It does not change or deploy Astra's v88 runtime candidate.

## Runtime isolation
- Installed runtime remains v85: `FNVGModTHUG2.dll` SHA256 `BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41`.
- Active `REM_GModTHUG2.esp` remains SHA256 `0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7`.
- Astra v88 candidate remains isolated/undeployed: SHA256 `6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439`.
- Unified support validator passes 61 static/preflight checks with zero errors.
- Static validation is not a gameplay pass.

## Final compact prop-content handoff
- Ready catalog remains 290 items: 170 Fallout New Vegas + 120 converted GMod/Source.
- The 170 FNV entries are now selected only from statically-clean assets that already have real existing base forms.
- Full static-clean FNV pool: 278. Existing-form coverage: 246. Missing-form research candidates: 32.
- The earlier 17 missing-form entries from the ready 170 were replaced by existing-form candidates; no arbitrary custom FNV forms are required by the final ready set.
- 120 GMod/Source entries have dedicated disabled sidecar `MSTT` records.
- Every final ready entry has a form binding.
- Final catalog local manifest SHA256: `BC7AC41C96A4F5D12C10D4A480D604262BAB6C320067D4CA0E78489D98A9A77F`.

## Disabled GMod prop catalog sidecar
- `REM_GModProps_Catalog.esp` contains 120 curated GMod/Source `MSTT` records.
- SHA256: `55E0758D4E96DC0C3B5F591002AD3C2C630CC76BE281DEDA0DAF2D2F91A4423E`.
- It is not enabled in `plugins.txt`.
- Static validator passes record count, unique IDs/EDIDs, model references, bounds, data fields, hash and disabled-state checks.
- Runtime spawning/playability has not been tested.

## Prop thumbnails
- 290/290 final ready entries have 128x128 local geometry previews generated directly from the actual prepared NIFs.
- Final thumbnail manifest SHA256: `4A90D8E60BC86C57D655F6AB876D9A1144D13ECB5E6FDF46DC68D65FFA7378EC`.
- These are support/fallback previews only. Astra's real GMod Q-menu port should preserve source-faithful SpawnIcon behavior.
- The selected 120 GMod props do not currently have matching prepacked native spawnicons in the indexed mounted content.

## GMod / Half-Life weapon staging
- Concrete Source model coverage remains 71/71 referenced model paths.
- 49 concrete weapon classes have separated view/world candidate packages.
- 48 view NIF candidates and 48 world NIF candidates exist; no concrete model or texture dependency is missing.
- QC/SMD animation sources and sequence names are preserved for Astra.
- 40 sound references were inventoried. Fifteen unique named Source/GMod events remained unresolved by direct loose-script lookup; fourteen have evidence-only candidate packed wave groups. `Toolgun.Single` remains unresolved.
- Candidate wave matches are not substitutes; Astra/native Source behavior must resolve exact named sound-event behavior.
- Runtime-candidate manifest SHA256: `AABE583D91313F938DCDFAC3F432F129B515D61297F2E95E92BA28468E106D49`.

## Weapon inventory presentation
- Read-only audit covers all 49 GMod weapon records plus THUG2 Skateboard.
- 47 GMod records are clean against the prepared presentation data.
- THUG2 Skateboard origin icon/name/model references pass the audit.
- GMod Camera has an intentional/review-only view-model discrepancy and was not auto-modified.
- GMod RPG had a clear missing world-model and origin-icon defect.
- Disabled `REM_WeaponPresentation_Fixes.esp` fixes only the RPG presentation:
  - world model `rem\gmod\weapons\w_rocket_launcher.nif`
  - GMod large/small Pip-Boy origin icons.
- Fix sidecar SHA256: `15380779823DA61F0F7A536E317FFB2489F35A156EFDF348348BB61D7BCA7723`.
- Static validation passes; sidecar remains disabled.

## THUG2 embedded environment props
- 106 named skate/environment targets remain queued across 16 THUG2 levels.
- Per-level handoff bundles now include QB context for 106/106 targets plus matching whole-level GLB/QB references.
- These are source extraction targets, not standalone props.
- Astra/model-extraction work should split only the named object from source level geometry; no THUG2 map import is intended.

## THUG2 board and source animation assets
- Original THUG2 pickup-board model/geometry/collision/texture sources are hashed and recorded.
- Pickup board converts successfully as source geometry.
- Live board/held/world NIF hashes, dimensions and container structure are recorded.
- Held NIF remains the BSFadeNode + `Prn=Weapon` candidate using authentic board geometry.
- Twenty explicit moto-skateboard THUG2 SKA files parse successfully as 50-track animation assets; key counts/hashes are recorded.
- This is asset evidence only. Astra owns exact animation/state/physics integration.
- Board handoff manifest SHA256: `5ED16EA52A6C5C14C475BDBE3335FF71474CAAF5D846022FFC4184307387E7C5`.

## THUG2 HUD/controller asset handoff
- 49 source UI/font/controller/audio/script assets are indexed with zero missing.
- Includes Xbox/PS2/NGC button font descriptors + atlases, timer/trick font sources, balance/score/SPECIAL sprites, controller/menu scripts and HUD/menu sounds.
- 22/22 IMG sources convert successfully to local PNG previews.
- The original PS2 FNT descriptors are preserved rather than inventing unsupported metrics.
- Manifest SHA256: `BBA25C2BBFFEA48B85070D6EE40867AB5A8DAF7627C9A7041B382BFA2E0E9312`.
- Astra still owns the source-faithful HUD renderer/runtime.

## Test infrastructure
- Added preflight/postflight playtest capture scripts.
- They snapshot runtime/candidate hashes, sidecar enablement, plugin logs and Windows Application events without launching the game or changing saves/plugins.
- Tooling smoke test produced no hash changes and no relevant Application event.
- Added a staged support playtest checklist for baseline Fallout, inventory/drop/pickup, board, prop catalog, Combine armor and later Q-menu/Tool Gun/Physgun validation.

## Remaining gates
- Human gameplay tests are still required for staged sidecars, inventory drop/pickup, prop spawning/physics, Combine armor and skateboard visibility/activation.
- Astra/Claude still owns the difficult runtime layer: THUG2 gameplay/physics/animations/camera, real GMod Q-menu compatibility runtime, Tool Gun behavior and native Physgun behavior.
