# GMod weapon prop preparation handoff

Prepared on 2026-10-05 for later GPT-6 Astra integration. This work does not alter the active NVSE plugin, ESP, THUG2 HUD candidate, animations, weapon code or live Fallout Data.

## Local staging
- Root: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\prepared\gmod_weapon_props
- Manifest with full local paths/hashes: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\prepared\gmod_weapon_props\manifest.json
- Staged converted NIF copies: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\prepared\gmod_weapon_props\meshes
- Staged NIF texture dependencies: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\prepared\gmod_weapon_props\textures
- Staging README: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\prepared\gmod_weapon_props\README.md

## Prepared inventory
- Weapon definitions mapped: 49
- Unique converted world/prop NIFs copied: 38
- Weapon definitions with an available converted NIF: 49
- Missing mapped converted NIFs: 0
- Staged texture dependency files: 48

## Scope boundary
- These are prepared world/prop assets and mappings, not completed first-person weapon integrations.
- No animation binding, attack/firing behavior, reload logic, ammo mapping, Pip-Boy records, ESP edits, balance changes, controller work or runtime code changes were performed.
- Original GMod Lua/source references are recorded in the JSON manifest for later behavior reconstruction.
- Do not commit the staged proprietary NIF/DDS binaries to GitHub; keep only this text handoff and hash/mapping manifest in the repository.

## Weapon families prepared
- Automatic: AR2, H.U.G.E-249, M16, MAC10, SMG1, Stun Gun
- Camera: GMod Camera
- Flechette: Flechette Gun
- Grenade: Discombobulator, Frag Grenade, Molotov, Smoke Grenade
- Launcher: RPG
- Medkit: Medkit
- Melee: Crowbar, Crowbar, Fists, Knife, Magneto-stick, Stunstick, Unarmed
- Physcannon: Gravity Gun
- Physgun: Physics Gun
- Pistol: .357 Magnum, Desert Eagle, Five-Seven, Flare Gun, Glock, Pistol, Silenced USP
- Rifle: Crossbow, Newton Launcher, Poltergeist, Scout Rifle
- Shotgun: Shotgun, XM1014 Shotgun
- Toolgun: Tool Gun
- Utility: Beacon, Binoculars, C4, DNA Scanner, Decoy, Defuser, Health Station, Manhack Welder, Radio, S.L.A.M., Teleporter, Visualizer

## Later Astra handoff
Use build/manifests/gmod_weapon_prop_prep.json to choose weapon classes, then consume the corresponding local staged NIF/texture set. Re-validate each candidate as a Fallout held/view/world model before wiring code or ESP records; several definitions deliberately share a world model and are not proof of behavior parity.
