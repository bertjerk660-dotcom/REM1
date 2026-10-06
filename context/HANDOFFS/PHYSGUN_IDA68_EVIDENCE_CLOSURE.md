# Physics Gun IDA Pro 6.8 evidence closure — 2026-10-06

Status: EVIDENCE COMPLETE FOR HANDOFF. This is a reverse-engineering behavior contract, not a claim that the behavior is already integrated into Fallout: New Vegas.

## Inputs verified
- IDA Pro 6.8 analysis exports:
  - C:\IDA68WORK\GMOD_GMODCLIENT_dll_physgun_ida68.txt
  - C:\IDA68WORK\GMOD_GMODSERVER_dll_physgun_ida68.txt
- Inputs correspond to the installed 32-bit Garry's Mod client.dll/server.dll previously copied into C:\IDA68WORK.
- Original GMod Lua/hooks/material/sound/model inventories remain in the existing ASTRA_PHYSGUN and weapon asset handoffs.

## Native behavior evidence map

### Weapon identity / network state
- Client registers weapon_physgun / CWeaponPhysGun.
- Server contains CWeaponPhysGun and DT_WeaponPhysGun evidence.
- Server network/state registration exposes m_hGrabbedEntity and m_vHitPosLocal. These are the durable held-entity and local hit/attachment state that the FNV bridge must represent.

### Target acquisition / range
- Server CWeaponPhysGun path references physgun_minrange and physgun_maxrange.
- physgun_minrange default evidence is 40.
- Server and client both reference physgun_maxrange.
- Handoff requirement: perform an aim trace from the player/view origin, enforce source min/max range semantics, reject invalid/non-physical targets, and preserve the hit position in target-local coordinates rather than repeatedly using only world-space center position.

### Pickup / held state / release
- Server exposes m_OnPhysGunPickup / OnPhysGunPickup, m_OnPhysGunOnlyPickup / OnPhysGunOnlyPickup, m_OnPhysGunDrop / OnPhysGunDrop and m_OnPhysGunPunt / OnPhysGunPunt event fields.
- m_hGrabbedEntity is explicit state, not inferred from beam visuals.
- Handoff requirement: pickup establishes grabbed entity + local hit position + hold controller; release tears down the controller and emits the drop/release semantic. Punt/launch is a distinct transition/event, not ordinary drop.

### Hold controller / damping
Server configuration evidence:
- physgun_maxAngular
- physgun_maxAngularDamping
- physgun_maxSpeed
- physgun_maxSpeedDamping
- physgun_DampingFactor
- physgun_teleportDistance
- physgun_timeToArrive
- physgun_timeToArriveRagdoll
These prove the native hold path is a damped target-follow controller with separate ragdoll arrival timing and teleport-distance handling, not a simple hard position lock.
Handoff requirement: reproduce the controller semantics in FNV physics rather than directly teleporting an object every frame except where the original teleport-distance safeguard applies.

### Rotation / distance adjustment
- Server exposes phys_spinspeed with description: Physics Gun rotation sensitivity using movement keys, server-side; default evidence 200.
- Server function 10104A50-10105038 references physgun_rotation_sensitivity and physgun_wheelspeed and branches on player input flags while a valid physgun/held state exists.
- Client also contains physgun_rotation_sensitivity and physgun_wheelspeed.
Handoff requirement: held-object rotation is an input-driven state transition with configurable sensitivity; mouse wheel changes hold distance using physgun_wheelspeed. Preserve the grabbed local hit offset while rotating.

### Beam / endpoint
- Server registers/creates physgun_beam and CPhysBeam.
- Client has physgun_drawbeams and physgun_beam.
- Beam endpoint must follow the trace/held hit state: idle beam terminates at current trace endpoint; grabbed beam terminates at the held target/local-hit transformed endpoint.
- Existing asset handoff contains the original beam/glow material dependencies. Do not replace this with a generic FNV projectile effect.

### Physics interactions / actors
- Server contains a physgun_interactions dispatch family and entity outputs for pickup, physgun-only pickup, punt and drop.
- Native configuration has physgun_timeToArriveRagdoll, proving ragdoll handling is a distinct hold-controller case.
- For FNV actors, the bridge must never treat a live actor transform as a generic static prop. Enter the project's ragdoll/unconscious compatibility path, manipulate the physical/ragdoll representation, then restore/resolve actor state on release according to the integration agent's validated actor bridge.

### Freeze / unfreeze
- The recovered evidence distinguishes motion-enabled entity outputs and physgun interaction dispatch from the grab controller. Freeze must therefore be modeled as a physics motion-state operation on the targeted/held physical object, not as deleting/replacing the object.
- Exact GMod input binding/lifecycle should be preserved from the original SWEP/hooks already staged; this evidence report does not invent a new Fallout binding.

### Launch / punt
- OnPhysGunPunt and m_OnPhysGunPunt are explicit native event semantics.
- Handoff requirement: launch/punt is a separate action from release: detach hold controller, apply the source-faithful impulse along aim/beam direction, emit corresponding sound/effect/event, and leave the object simulated.

## FNV implementation contract
The integration agent should implement one explicit state machine:
IDLE_TRACE -> ACQUIRE -> HOLD -> {ROTATE / DISTANCE_ADJUST / FREEZE} -> {DROP / PUNT}; invalid entity, weapon unequip, cell transition or actor-state failure must force a safe DROP/CLEANUP.

Required state:
- grabbed reference/entity handle
- target-local hit offset
- target hold distance
- target orientation / rotation delta
- actor/ragdoll compatibility state
- beam active + beam endpoint
- hold-controller/damping state

Required validation:
1. pickup ordinary movable prop
2. beam endpoint remains attached to grabbed point
3. walk/turn while holding without jitter/explosion
4. wheel distance adjustment
5. rotation controls
6. freeze and reacquire
7. normal release
8. punt/launch
9. invalid/static target rejection
10. NPC/ragdoll path
11. weapon switch while holding cleans up
12. cell/load/save cleanup does not leave phantom constraints
13. original GMod sounds/beam assets fire at correct state transitions

## Evidence boundary
Function names beyond literal recovered symbols remain provisional until the integration agent labels the IDA database. This report deliberately records behavior evidence and addresses/strings rather than pretending every sub_* routine has a proven semantic name.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]