# GMod Q Menu / Tool Gun / Physics Gun Preservation Contract

Verified from installed-GMod inventory and project support manifests on 2026-10-06.

## Source provenance
Installed GMod inventory records Steam buildid `25375506`; appmanifest SHA256 `55648202F35A9165220C98975F59CDEB0079AE20D0C377FCC5CC83682449EA8A`. The indexed `garrysmod_dir.vpk` SHA256 is `A3237FC7442C6C57AA924525951280F1381BC641D323B6ED4CE52FD5BE09F83E`.

The inventory covers 105 relevant Lua files: 33 Q/spawn-menu-role files, 48 Tool Gun-role files, 5 Physgun-hook files, plus core/menu/notification support. Forty stool files were identified. It records 46 VGUI classes and 29 asset references; the recorded Q-menu asset references are resolved.

## Q-menu compatibility interface
The port must expose enough compatibility behavior for the original Lua/Derma flow to retain:
- Q/spawn-menu open/close lifecycle;
- tabs/categories and content population;
- curated model entries;
- search/filter tokens;
- content icons/thumbnails;
- Tool Gun category/options registration;
- selected `gmod_toolmode` state;
- Duplicator/Remover access;
- source-faithful notification calls.

The existing 290-entry adapter is data-only. It provides model path, category, display name, source game, FNV form binding, thumbnail, search tokens and validation state. It must feed the real/ported menu rather than becoming a replacement Fallout menu.

## Tool Gun host callback contract
Original GMod Tool Gun script behavior is script-rich. Preserve the original SWEP/stool selection flow. The host adapter needs callable boundaries for:
- trace acquisition;
- `LeftClick(trace)`;
- `RightClick(trace)`;
- `Reload(trace)`;
- selected tool-mode read/write;
- spawn/remove/manipulation operations requested by individual stools;
- source-faithful effects/sounds/notifications.

The installed source asset handoff identifies `models/weapons/c_toolgun.mdl`, `models/weapons/w_toolgun.mdl`, `Toolgun.Single`, selection indicator and ToolTracer dependencies.

## Physics Gun native boundary
Lua exposes sandbox pickup/drop/unfreeze policy hooks, but `weapon_physgun` core manipulation is engine-native. Exact target acquisition, beam, hold/rotation, freeze/unfreeze and release/launch behavior therefore requires native reverse engineering/host adaptation rather than invention.

Required host-facing operations:
- acquire target from aim trace;
- establish/release held target;
- update held transform/distance/rotation;
- freeze/unfreeze where Source behavior requires it;
- launch/release;
- actor-specific ragdoll/unconscious handling required by project design;
- beam/glow/highlight presentation synchronized to held/target state;
- original sound-event dispatch.

The asset audit requested 36 Tool/Physgun paths and resolved 33. The unresolved triplet is the source-declared `models/weapons/v_physics.{mdl,vvd,dx90.vtx}`. Do not invent a substitute. The world Physgun model and beam/glow material dependencies are present.

## Input note
The current project requirement overrides the integrated Physgun mouse mapping to RMB acquire/hold and LMB launch. Preserve this explicitly as a product-level compatibility override; do not mislabel it as evidence of original GMod default binding.

## Promotion gate
Astra must verify native interfaces with IDA Pro 6.8, implement adapters, then validate menu/tool/physgun behavior in-game. Static source inventories alone do not prove runtime equivalence.
