# Runtime Ownership Contract

This is a handoff contract, not proof that the runtime is implemented.

| State | Input owner | Camera owner | HUD/UI owner | Animation owner | Physics/world interaction owner |
|---|---|---|---|---|---|
| Fallout baseline | Fallout/FNV | Fallout | Fallout/Pip-Boy | Fallout | Fallout/Havok |
| Skate transition | compatibility layer gates input | supported FNV camera transition only | transition layer | no unsafe cached retarget pointers | Fallout world remains authoritative |
| THUG2 skate | THUG2-derived control/state layer | THUG2-derived behavior through verified host-safe adapter | THUG2 HUD/state | THUG2 animation selection/transition + validated retarget | THUG2 skate movement logic adapted to Fallout collision/world |
| Skate exit | compatibility layer restores host bindings | restore Fallout camera | restore Fallout HUD | release THUG2 animation ownership/caches | restore Fallout movement |
| GMod Q menu | Q-menu UI consumes menu input | Fallout camera must not be mutated by menu | real/ported GMod Q menu | Fallout unless preview needs isolated presentation | no direct world mutation until an explicit spawn/tool action |
| Tool Gun active | GMod Tool Gun + selected stool | Fallout aiming camera | GMod notifications/tool UI | weapon presentation adapter | selected real/ported GMod tool callback through host adapter |
| Physgun active | GMod Physgun mapping/product override | Fallout aiming camera | GMod feedback | weapon presentation adapter | Physgun acquire/hold/rotate/freeze/release/launch adapter |

## Hard invariants
- Normal Fallout gameplay owns the runtime until an imported mode is explicitly activated.
- Q-menu owns Tool Gun tool selection; Fallout prompts must not substitute for it.
- Do not perform raw Camera3rd transform writes until IDA 6.8 verifies object/layout and a safe mutation path.
- Do not cache retarget bone pointers across player 3D/camera-root rebuilds.
- Skateboard identity remains ESP-owned/persistent; no runtime CloneForm rebinding.
- Every mode transition must have an explicit restore path for input, camera, HUD and animation ownership.
- A source-faithful imported subsystem may adapt at the host boundary, but the adapter must not silently replace source behavior with Fallout behavior.
