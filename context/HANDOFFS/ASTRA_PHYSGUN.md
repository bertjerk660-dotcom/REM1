# Astra handoff — real GMod Physics Gun

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Installed Source weapon_physgun.txt and GMod physgun hooks are inventoried and hashed.
- Physgun/Toolgun visual/audio asset inventory: 27 / 28 direct refs resolve.
- Source script declares models/weapons/v_Physics.mdl, but that legacy view path is not mounted in this install; this discrepancy is recorded rather than silently recreated.
- Project currently stages c_superphyscannon as the visual view candidate and w_physics as world candidate. Treat this as a candidate requiring source/runtime verification, not proof of exact final GMod presentation.
- Original physbeam/physgun glow materials and Weapon_Physgun.On/Off/Special1 event definitions are indexed.
- Native target acquisition, held-object transform, rotation, freeze/unfreeze, drop/release and launch behavior remain Astra/IDA Pro 6.8 work.
- User-required input semantics remain RMB pickup/hold and LMB launch after integration.