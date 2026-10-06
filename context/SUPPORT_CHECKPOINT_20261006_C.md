# Support Checkpoint C — 2026-10-06

This checkpoint closes the requested 20-point non-Astra/non-Opus preparation pass. It does not modify or deploy Astra v88.

## Protected runtime
- Installed runtime stays v85.
- Live DLL SHA256: BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41.
- Active REM_GModTHUG2.esp SHA256: 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7.
- Astra v88 candidate remains isolated/not installed, SHA256 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439.
- Unified support validator: PASS, 94 checks, zero errors.
- Validator report SHA256: 68ABA18984574DB48985953B29402CFA3E216E8439CE7F21554544BC4AA2BBDD.

## Prop/catalog work
- Final ready catalog: 290 entries.
- Fallout: 170 statically-clean props, all using existing real base forms.
- GMod/Source: 120 converted props, all with disabled sidecar MSTT forms.
- Every ready entry has a form binding.
- 290/290 fallback thumbnails generated and quality-audited clean.
- Real-Q-menu data adapter exposes all 290 with category/search/model/form/source metadata.
- THUG2 queue: 106 targets fully classified; 85 are spatial geometry candidates, 14 semantic/gap identifiers and 7 unresolved named targets. None are falsely promoted to standalone props.

## Weapon/source work
- Concrete GMod/HL source model references: 71/71 staged.
- View candidates: 48; world candidates: 48.
- Missing candidate material paths: 0.
- All 15 previously unresolved named Source/GMod sound events were located in original installed sound-script definitions.
- 14/15 have every referenced payload path confirmed in mounted VPKs; the remaining definition stays explicit rather than receiving a Fallout substitute.
- Tool Gun/Physgun model/material/effect dependency audit: 33/36 exact paths resolve.
- The only absent paths are the source-declared models/weapons/v_Physics.mdl, .vvd and .dx90.vtx triplet. No replacement was invented.
- RPG presentation issue is isolated in disabled REM_WeaponPresentation_Fixes.esp and passes static validation.

## THUG2 source handoff
- 49 HUD/font/controller/audio/script assets indexed; no missing source asset.
- 22/22 image previews convert.
- 17 relevant QB files were decompiled locally for controller/trick/physics evidence.
- 22-entry source-backed input/control matrix generated.
- Authentic board source/current NIF hashes and dimension relationships recorded.
- 20 real moto-skateboard SKA files parsed and hashed.
- Current source->FNV board dimensions are non-uniform; attachment must not be “fixed” by recreating/deforming the board.

## Test and project engineering
- Three isolated support sidecars exist and are disabled: Combine armor, GMod prop catalog, RPG presentation.
- Eight regression packs prepared.
- Preflight/postflight evidence scripts capture hashes, sidecar enablement, plugin logs and Windows Application events.
- 63 historical/versioned artifacts classified non-destructively.
- research/patch_v74_advdupe_physgun.py is explicitly known-bad/do-not-run.
- Eventual release/install manifest indexes current baseline, sidecars, icons, board/armor assets and 205 GMod prop payload files.
- Nine focused Astra handoff documents cover Q menu, Tool Gun, Physgun, skate physics, animation/board, camera, HUD/input, weapon presentation and THUG2 embedded props.
- The later main-branch Fallout 3 Combine staging handoff was copied into this support branch so no canonical project knowledge is lost.

## Remaining gates
The remaining work is intentionally outside this support-completion claim:
- human baseline/inventory/prop/armor/skateboard gameplay tests;
- visual verification and final split/conversion of THUG2 embedded geometry;
- complete THUG2 physics/animation/camera/HUD/input runtime;
- real GMod Q-menu compatibility runtime;
- Tool Gun and native Physics Gun behavior;
- final first-person/world weapon animation integration.

A support artifact must not be called gameplay-verified until its corresponding human pack passes.
