# THUG2 Animation / Bone / Camera Preservation Handoff

## Preserved animation evidence
The local `thug2_exact_animation_manifest.json` records a later clean 35-bone THUG2→FNV mapping and four converted animation samples:
- ollie: 0.6333333254 s, 20 keys, 35 mapped bones;
- manual: 0.4333333373 s, 14 keys, 35 mapped bones;
- revertbs: 0.6666666865 s, 21 keys, 35 mapped bones;
- revertfs: 0.6666666865 s, 21 keys, 35 mapped bones.

The manifest states the source is original THUG2 PS2 SKA data exported using `thps6_human.ske.ps2` exact-QbKey binding and the target is the Fallout New Vegas Bip01 skeleton.

## Conversion tooling
`research/thug2_glb_to_fnv_kf.py` is project-authored conversion tooling and should be preserved as AUTHORITATIVE_PROJECT_TOOLING. Generated KF files are outputs, not source truth. The generator, source animation identity/hash, skeleton identity/hash, mapping version and output hash must travel together in promotion manifests.

## Bone-map conflict
The older `thug2_fnv_bone_map.json` contains dirty/suspicious FNV node names and must not silently override the later clean exact-animation mapping. Before promotion:
1. extract/list the actual FNV target skeleton node names;
2. regenerate mapping against that skeleton;
3. reject targets absent from the skeleton;
4. compare the regenerated map with the exact-animation manifest;
5. version and hash the accepted map.

## Board attachment
Board bones preserved by the animation manifest:
`bone_board_root`, `bone_board_nose`, `Bone_Trucks_Nose`, `Bone_Board_Tail`, `Bone_Trucks_Tail`.

The held-board Fallout container is a separate presentation concern. Do not confuse held-weapon attachment (`Prn=Weapon`) with skate-mode board-to-feet animation attachment.

## Camera preservation boundary
Known failure evidence proves raw writes through the previously assumed Camera3rd object/global are unsafe and not the sole crash cause. Therefore:
- preserve camera discoveries as evidence;
- do not promote raw transform writes;
- use IDA Pro 6.8 to identify the real camera object/layout/update path;
- capture signatures/xrefs and host-safe call/update points;
- keep camera ownership isolated behind the runtime ownership contract.

## Required Astra handoff
Astra should receive: source hashes, accepted bone map version, animation manifest, converter version/hash, board-bone semantics, camera IDA evidence, unresolved assumptions, and regression assertions. No claim of 1:1 animation/camera behavior is valid until live playtesting passes.
