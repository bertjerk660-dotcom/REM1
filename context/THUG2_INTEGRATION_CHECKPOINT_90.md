# Checkpoint 90 — board material repair and scene adapter
Date: 2026-10-06. Branch: feature/thug2-native-ui-g6.

## Deployed asset repair (DLL unchanged)
Inspected live held/ride board NIFs. They contained NiMaterialProperty alpha=0, black diffuse defaults, empty BSShaderTextureSet paths and disabled depth test/write. This is a concrete conversion defect and a likely visibility contributor, not yet a proven sole runtime cause.
Restored opaque material alpha and diffuse multiplier, depth test/write, and four original texture bindings from the source-derived board_default.glb in build/prepared/thug2_prop_catalog/standalone_glb/models/board_default/board_default.
- Each shape's original material association checked against source triangle count and unique positions after the observed (x,y,z)->(x,-z,y) coordinate conversion.
- Initial equal-vertex-count assertion failed because NIF export splits seam vertices. Geometry comparison was corrected to compare unique positions and triangle counts; all four shapes match.
- Extracted embedded PNGs and saved lossless DDS; pixel equality verified after reopening.
- Reopened all three repaired NIFs; geometry positions unchanged, material alpha=1 and all texture paths resolve.
- Installed skateheldx.nif, skateboard.nif and skateboard_visual.nif plus four textures. FalloutNV was not running.
- Original files backed up at local project backups/board_material90. Deployment checked original hashes before writing and installed hashes afterward.
- Held NIF now SHA256 1fb3ce190cc0e32d2f06eec144605ce3e2eb84be4e3a90a33b227b9639c6d852.
- Both generic/ride NIFs now e6aad886d1ca8a2044f185051ab2f411c61806ecf7a74372d83b5b6203fc5568.
- Live plugin is still v85, hash bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41.
- No in-game visibility/placement test yet. No ESP change, no vertex-position or attachment-transform change, no runtime animation enable.
- Rollback: with Fallout closed, restore the three named NIFs from backups/board_material90 to Data/meshes/rem/thug2. New board90 textures can remain unused.

## v90 isolated code candidate
Parent v89. Release Win32 build PASS; not deployed/playtested.
Candidate DLL hash 04d93fcbcd3429b01c526292573568eac198b58e6d752f2e80cc758a1b925375.
Implemented research/fnv_scene_adapter90.inc:
- Verify known NiNode search/update vtable slots before use.
- Search slot 0x27 accepts an interned handle address, with original constructor/destructor at 0x438170 / 0x4381B0. Replaced retarget's obsolete GetObject declaration call.
- Explicit local transform includes scale, size0x34, local at0x34. Save/restore now includes scale.
- Replaced retarget's wrong UpdateTransform(void) calls with explicit downward-pass slot0x29 / two arguments.
- Update context zeroed; controller-enable byte offset4 left false. Full subtype/update-context semantics and runtime scheduling require further validation.
- Animation and raw-camera quarantines REMAIN. This candidate does not yet make THUG2 animations run.

## IDA Pro 6.8 evidence
Used isolated C:/IDA68WORK/FNV_attachment90.idb copied from FNV_skeleton87.idb.
0xA5E560 recursive name search, vtable offset0x9C, interned-string reference.
0xA5DD70 downward pass accepts context and flags, retn8; recursively calls child slot0x29, world-data slot0x2E.
0xA68C60 world-data dispatch handles collision object or calls 0xA68BF0.
0xA68BF0 composes parent world + local or copies local to world: local0x34, world0x68, 13 dwords each. The old SDK dat0064 is NOT the world transform; it starts at local scale.
Do not re-enable old camera routines or use SDK world-layout declarations.
Evidence saved in builds/ida68_fnv_{attachment,transform,local}90.json.

## Still required to finish user request
Full THUG2 mechanics and animated board placement are NOT complete.
- Verify repaired board visible in first/third person and skate mode; confirm actual ESP paths and grip/deck alignment.
- Implement shared original clip clock, control-root/board-root translation+rotation+scale, original attachment events and mesh-bind transform. Current ride reference still follows fixed player offset.
- Repair original animation retarget math/translation/scale, host update ordering and actor-root lifecycle; validate adapter in a bounded runtime diagnostic before enabling writes.
- Original THUG2 physics/trick transitions/camera/collision, controller adapter and complete animation set (including 51 failed exports) remain.
- v89 lifecycle fixes and v88 HUD are candidate-only, not installed in live v85.
Do not call this a full skating merge or a completed visibility/placement fix until gameplay evidence supports it.

## Reproduction
research/repair_board_material90.py, research/deploy_board_material90.py,
research/fnv_scene_adapter90.inc, research/prepare_attachment90.py,
builds/attachment90_main.patch, builds/attachment90_manifest.json,
builds/board_material_deployment90.json.
Original assets remain local; GitHub stores tooling and provenance.
