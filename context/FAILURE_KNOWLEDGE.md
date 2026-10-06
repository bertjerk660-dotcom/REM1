# Failure Knowledge

## F001 - Runtime skateboard WEAP cloning / serialized runtime forms
Symptoms across v73-v78 included startup/load crashes and access violations in Fallout inventory/extra-data paths. Runtime CloneForm-based skateboard forms were repeatedly implicated.
Durable rule: use an ESP-owned persistent WEAP for skateboard identity; avoid recreating/rebinding serialized runtime weapon forms during load.

## F002 - Direct PlayerCharacter::playerNode dereference
v76 skate activation crashed at plugin RVA 0x2B77. The path used PlayerCharacter::playerNode directly during camera transition.
Fix: use TESObjectREFR::GetNiNode() and defer animation binding until an active 3D root exists.
Rule: never assume conditional playerNode fields are valid across camera/3D transitions.

## F003 - Unsafe retarget bone caching
Earlier retarget code reinterpreted NiObjectNET* as NiAVObject* and cached bone pointers across camera/3D root rebuilds.
v81 mitigation: RTTI-cast every target to NiAVObject, require a sufficiently complete skeleton, track owning NiNode root, discard caches when root changes, validate clip bounds/finite quaternions, and delay first retarget application 900 ms after skate camera transition.
Playtest status: pending.

## F004 - Held skateboard invisible
Original converted skateboard NIF was a visual NiNode hierarchy without a proper Fallout held-weapon attachment container. A later skateheldx added Prn=Weapon but retained NiNode root. Stock LeadPipe uses BSFadeNode + Prn=Weapon. v82 deploys authentic board geometry in that container and passes structural validation.
Status: held-weapon visibility/placement is now human-verified on 2026-10-06: the skateboard appears and is correctly positioned in the player's hand. This does not yet prove board-to-feet attachment or skate-state transition correctness.

## F005 - v80/v81 skate activation crash
v80 reached Fight suppression -> camera switch -> camera profile -> retarget bank load -> ride-board reference -> board-roll -> speed -> HUD complete, then c0000005. v81 human test still crashed; latest diagnostic checkpoint was camera profile update complete.
Next action if v82 still crashes: narrow instrumentation within the pre-ride-board UpdateSkateMode section rather than speculative multi-system changes.

## F006 - Stale documentation
Older status/context can lag actual implementation. Reconcile against source, deployed hashes, manifests and logs before modifying.

## F007 - Concurrent state changes
Another active engineering session may modify the workspace. Immediately before modification/deploy, re-check source version/hash, mtimes and deployed hashes. Do not overwrite newer state based on stale reads.


## F008 - Skate mode UI remains Fallout-hosted
Human playtest on 2026-10-06 shows skate mode still uses a simple text overlay, Fallout-style top-left alerts, and the Fallout HUD remains visible.
Durable rule: active skate mode must suppress the Fallout HUD and replace fallback text/alerts with the source-faithful THUG2 HUD/UI/notification/scoring path required by the recovered skating system. Fallout HUD/UI should return only when skate mode exits.

## F009 - Physics Gun range/audio/actor target regressions
Human playtest on 2026-10-06 reports three linked Physics Gun problems: acquisition/manipulation range is extremely short, the wrong sound plays while a target is held instead of the correct continuous beam/hold loop, and final actor grab/lock applies the unconscious effect to the player rather than the acquired target.
Durable rule: derive range and held-state audio from the preserved GMod/Source behavior; keep the active acquired target reference distinct from PlayerCharacter; apply actor ragdoll/unconscious handling only to the acquired target; add regression checks for range, loop start/stop, release, and target identity.
