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
Status: strongly supported cause; live fix not yet proven.

## F005 - v80/v81 skate activation crash
v80 reached Fight suppression -> camera switch -> camera profile -> retarget bank load -> ride-board reference -> board-roll -> speed -> HUD complete, then c0000005. v81 human test still crashed; latest diagnostic checkpoint was camera profile update complete.
Next action if v82 still crashes: narrow instrumentation within the pre-ride-board UpdateSkateMode section rather than speculative multi-system changes.

## F006 - Stale documentation
Older status/context can lag actual implementation. Reconcile against source, deployed hashes, manifests and logs before modifying.

## F007 - Concurrent state changes
Another active engineering session may modify the workspace. Immediately before modification/deploy, re-check source version/hash, mtimes and deployed hashes. Do not overwrite newer state based on stale reads.

## FS001 - FNVScript script selection is stateful/unreliable in this workspace
Observed 2026-10-06 during support automation. Passing a new .pas path to FNVScript.exe did not reliably execute that script; the tool repeatedly loaded/applied a previously remembered script (REM_FixOriginIconFields). This can create false confidence that a requested audit or edit actually ran.
Durable rule: never claim an FNVScript/xEdit automation succeeded without verifying its own expected output/log. For read-only audits, prefer reproducible binary parsers when practical. For simple disabled support sidecars, use validated deterministic generators only when the file format is fully understood, then run structural/reference validation. Complex gameplay/plugin edits remain in xEdit/Astra workflows.

## F008 - Raw Camera3rd transform writes are unsafe and were not the sole crash cause
v83 produced a visible upward camera pan immediately before a repeatable c0000005/StackHash crash. The skate camera path treated global 0x011E07D4 as a NiAVObject pointer without verified RTTI/layout and overwrote transform fields every frame. v84 quarantined SaveTHUG2CameraNode/ApplyTHUG2NativeCameraProfile/RestoreTHUG2CameraNode and used Fallout's normal third-person camera path, but the crash still occurred.
Rule: keep direct raw camera-node writes disabled until the real camera object/layout and supported mutation path are re-verified with IDA Pro 6.8. Do not treat this path as the sole cause of the skate crash.

## F009 - v84 crash occurred after a complete first active skate frame
The v84 diagnostic log completed timing/input, coast injection, speed application, steering, jump/state branch, ride-board update, retarget selection/apply no-op during its delay, and the end-of-frame checkpoint. The process later crashed with c0000005/StackHash_2beb.
Implication: the fault is not an operation that deterministically fails on the first active frame. Delayed/asynchronous or later-frame behavior must be isolated with single-subsystem A/B tests and frame heartbeats rather than broad speculative changes.

## F010 - Do not classify a playtest against the wrong loaded DLL
A reported crash after v85 deployment was initially ambiguous. The live DLL hash was v85, but the existing plugin log began with "bridge loaded, version 84" and had been written before the v85 deployment. The already-running Fallout process had loaded v84 and copying a new DLL did not replace code in that process.
Rule: before attributing any gameplay result to a build, require a fresh process and verify the new plugin log begins with the expected "bridge loaded, version N" line. If the loaded version does not match, do not use that test as evidence for the new build.

## FS002 - Parallel support generators can leave stale duplicate manifests
Observed 2026-10-06 while reconciling the support lane. Parallel work produced smaller duplicate artifacts beside richer canonical outputs: a 28/27 Tool Gun/Physgun inventory beside the canonical 36/33 handoff, a 7-pack regression file beside the canonical 8-pack set, and a 41-item version inventory beside the canonical 63-item historical registry. A stale local 20-point tracker also lagged the GitHub support branch.
Durable rule: before updating support docs or validators, compare local and GitHub support state and prefer the explicitly canonical artifacts named by context/SUPPORT_20_POINT_TRACKER.md. Preserve superseded evidence, but do not overwrite a richer/newer manifest with a smaller duplicate merely because the duplicate was generated later.
