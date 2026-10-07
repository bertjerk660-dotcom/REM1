# GMOD → Fallout compatibility matrix — 2026-10-07

This matrix separates original-system contracts from observed host code. Current-source identity and inspected limits are in [EXISTING_IMPLEMENTATION_AUDIT.md](EXISTING_IMPLEMENTATION_AUDIT.md); machine rows are in [compatibility_matrix.json](../../manifests/gmod_2026-10-07/compatibility_matrix.json). Proposed adapters are requirements, not implemented successes.

| Component | Original implementation/dependency | Required Fallout bridge | Observed current state |
| --- | --- | --- | --- |
| Q input/lifecycle | Original command press/release, persistent SpawnMenu, cursor/focus/hang-open | One input owner; Source bind/command events; cursor and host control restoration | Q/F2 rising-edge toggle; Toolgun R also opens; only Fight/Movement disabled; incomplete |
| VGUI/Derma menu | Original Lua panels, skin/layout/surface/fonts/materials | Implement measured Lua/native panel/render service contract | Win32/GDI fixed grid/Tahoma; recreated placeholder |
| Prop browser/search | CreationMenu/content registry, spawnlists/search/model previews | Curated data adapter preserving original panel/filter behavior | Compiled category/page grid; search and preview not present in inspected path |
| Prop icons | SpawnIcon/ModelImage plus native model rendering/cache | Real model/icon render/cache service; original material resolution | FNV-1a PNG lookup, null-cache and generic fallback; support preview only |
| Spawn/undo | Original content click/concommand, validation/trace/entity/undo | Source entity→FNV reference and trace/spawn/undo translation | SpawnSelectedBuildProp→SpawnConvertedProp or NPC proxy; useful unverified bridge |
| Tool selection | Original tool command/convar/SWEP selected id | Selected id/state dispatch without Fallout dialog | Hover/click index7/29; immediate custom index change; recreated/incomplete |
| Tool Gun fire | Original gmod_tool/stools, trace/prediction/hooks/effects | Realm/prediction semantics and trace/action/effect/audio adapters | Hard-coded custom action dispatcher; unsupported primary says port pending; secondary shows Fallout status |
| Tool screen/HUD | Original render target/material/font and tool HUD | Render-target and draw-service adapter | Not proved in inspected runtime source |
| Duplicator | Original serialization/entities/constraints/undo/cleanup | Reference/constraint persistence with original semantics | Copies NIF/name only; paste fixed-distance model spawn; recreated/incomplete |
| Remover | Original tool permissions/trace/removal/undo | Safe FNV target/removal/undo translation | Disables crosshair ref; undo enables id; original permission/constraint semantics absent |
| Camera tool | Original camera stool/entity; distinct gmod_camera weapon | Separate camera entity/control and screenshot/FOV adapters | Camera weapon calls host JPEG/FOV routines; stool/entity parity unresolved |
| Physgun interaction | Native weapon/hold controller plus original Lua permissions | Trace/ref/body/bone/controller and input translation | Fallout crosshair ref limits acquisition; 4096 only hold clamp; reference-origin controller/teleport fallback; original parity unresolved |
| Physgun beam/color | Native beam state/attachment/hitpoint; original materials | World render/material/color adapter | Fixed screen strip/center glow/cyan; recreated/incomplete |
| Physgun highlight | Original DrawPhysgunBeam target registration/PreDrawHalos/player color | Host target silhouette/outline tied to acquired ref/color | No halo/outline implementation found in full main/overlay; external backend unproved |
| Physgun sound | Original named events/payloads/state transitions | Audio event/loop lifecycle and spatialization | Runtime sounds explicitly nonlooping/2D; no hold-loop lifecycle in main/overlay |
| Actor/ragdoll | Source physical entity/physics object and permission hooks | Acquired target→FNV actor/Havok/ragdoll, distinct player identity | setunconscious targets acquired ref; pushactoraway names player; likely symptom candidate pending command-semantics test; single wake slot and original-unconscious state missing |
| Notifications/hints | Original panels/stack/expiry/fonts/materials/binding localization | Original panel/audio/timer services | Notify directly QueueUIMessage; stale R-cycle hint; original notification execution absent inspected path |
| View/world/inventory models | Original model components/animations/materials | Validated NIF/rig/animation/form/world/drop translation | First14 defs; imported world NIF/form bridge, Fallout donor animations; original first-person parity/human QA pending |
| Shared filesystem | Source mount order/VPK/addon/material/model/sound resolution | Preserve exact original paths and mounted origin precedence | Relative UI PNG path; staging manifests/native package closure needed |

No row authorizes transplanting arbitrary binary regions or proprietary publication. Clean host boundaries must retain the original behavior while providing measured service translations.
