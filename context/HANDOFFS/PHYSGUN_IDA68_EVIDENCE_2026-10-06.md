# Physics Gun IDA Pro 6.8 Evidence Pass - 2026-10-06

Status: evidence lane complete; runtime integration still requires implementation and playtest.

## Provenance
Installed GMod x86 client.dll and server.dll were analyzed by the existing local IDA Pro 6.8 batch evidence pass. Evidence files are GMOD_GMODCLIENT_dll_physgun_ida68.txt and GMOD_GMODSERVER_dll_physgun_ida68.txt under C:\IDA68WORK. Do not substitute IDA 9 output.

## Confirmed native contract
- Weapon: CWeaponPhysGun is registered in server and client evidence.
- Range: physgun_maxrange defaults to 4096; physgun_minrange defaults to 40.
- Beam: server registers physgun_beam, CPhysBeam and DT_PhysBeam.
- Networked weapon state: m_hPhysBeam, m_vHitPosLocal and m_hGrabbedEntity are exposed together.
- Hold controller: CPhysGunControllerPoint creates/attaches a physics controller and retains target-relative state.
- Hold tuning defaults evidenced in server binary: maxAngular 5000, maxAngularDamping 10000, maxSpeed 5000, maxSpeedDamping 10000, DampingFactor 0.8, timeToArrive 0.05, ragdoll timeToArrive 0.1.
- Rotation: phys_spinspeed defaults to 200 and its binary description says movement-key rotation is server-side. The main input routine consumes physgun_rotation_sensitivity and input axes.
- Hold distance: the same native input routine consumes physgun_wheelspeed and updates/clamps held distance.
- Interactions: native outputs include OnPhysGunPickup, OnPhysGunPunt, OnPhysGunOnlyPickup and OnPhysGunDrop plus corresponding stored output fields.
- Entity behavior: physgun_interactions is consulted in native server interaction paths and m_bHasBeenPhysgunned exists.
- Original visuals referenced include sprites/physcannon_bluelight2.vmt and sprites/glow04_noz.vmt.

## Integration state machine
Idle/aim -> Acquire -> Hold -> Rotate or distance-adjust -> Release/drop OR Launch/punt.
Acquire must validate physics/interaction eligibility, capture grabbed entity plus local hit point, then create the hold controller.
Hold updates controller target from aim/distance and resolves the beam endpoint through the stored local hit point.
Release detaches without launch impulse and fires the drop transition.
Launch is a separate detach plus punt/launch transition.
NPC/ragdoll handling must use interaction eligibility and ragdoll-specific arrival timing.

## Evidence boundary
Freeze/unfreeze remains an implementation verification point: current binary evidence establishes the controller/input/interaction machinery but does not label a freeze routine strongly enough to claim an exact function. It must be verified during the integration pass rather than guessed.

## Runtime gates
Target acquisition, moving beam endpoint, pickup, stable hold, distance adjustment, rotation, freeze/unfreeze, release, launch, prop behavior, NPC/ragdoll behavior, beam/highlight, save/load and crash/regression checks. Physics Gun is not complete until these pass in FNV.

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]