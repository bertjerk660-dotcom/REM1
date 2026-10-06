# Astra Handoff — Real GMod Physics Gun

## Original installed source evidence
- sourceengine/scripts/weapon_physgun.txt SHA256: B5E61291AB5A0296EC6FA48E9E9F8A5712D2C350D3831411D4F3DD61E0BFC354
- sourceengine/scripts/weapon_physcannon.txt SHA256: F8FC6038845B3484C5D6AC03891AFE13D7934D2DE87DE239AE31062470F9D0D2
- weapon_physgun.txt names the original events Weapon_Physgun.On, Weapon_Physgun.Off and Weapon_Physgun.Special1.
- Real GMod/Source beam/glow/material paths are inventoried, including physbeam/physg/physgun_glow resources.
- The installed source script references models/weapons/v_Physics.mdl, but that exact view-model file is absent from the current mounted GMod/Source VPK set. Do not silently replace it with a Fallout model; treat this as an explicit source dependency question.
- models/weapons/w_physics.* is present.

## Product control override
The integrated project requirement is RMB pickup/hold and LMB launch.

## Astra runtime work
Use IDA Pro 6.8 for native Source/GMod behavior not represented in Lua: target acquisition, held-body transform, rotation, freeze/unfreeze, drop/launch, actor/ragdoll interaction and beam/highlight coupling. Reuse the original assets/sounds rather than Fallout approximations.

## Validation gate
Acquire valid target -> correct beam/highlight -> hold/move/rotate -> freeze/unfreeze -> release -> launch -> actor/ragdoll case -> repeated use without crash.
