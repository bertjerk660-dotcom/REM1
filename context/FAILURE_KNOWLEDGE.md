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
Status: still under isolation; v85 disables the entire retarget subsystem to prove or clear it.

## F004 - Held skateboard invisible
Original converted skateboard NIF was a visual NiNode hierarchy without a proper Fallout held-weapon attachment container. A later skateheldx added Prn=Weapon but retained NiNode root. Stock LeadPipe uses BSFadeNode + Prn=Weapon. v82 deploys authentic board geometry in that container and passes structural validation.
Status: structural cause strongly supported; live visibility still requires human confirmation.

## F005 - v80/v81 skate activation crash
v80 reached Fight suppression -> camera switch -> camera profile -> retarget bank load -> ride-board reference -> board-roll -> speed -> HUD complete, then c0000005. v81 still crashed. Instrumentation was expanded rather than applying further multi-system guesses.

## F006 - Stale documentation
Older status/context can lag actual implementation. Reconcile against source, deployed hashes, manifests and logs before modifying.

## F007 - Concurrent state changes
Another active engineering session may modify the workspace. Immediately before modification/deploy, re-check source version/hash, mtimes and deployed hashes. Do not overwrite newer state based on stale reads.

## F008 - Raw Camera3rd transform writes
v83 showed a visible upward camera pan immediately before crash while raw Camera3rd translation/rotation was being overwritten every frame. v84 quarantined Save/Apply/Restore raw camera-node transforms.
v84 result: crash persisted. Therefore raw camera writes are not the sole cause, but remain unsafe/unverified and must stay disabled until the correct object/layout and mutation path are re-verified in IDA Pro 6.8.

## F009 - Crash after a complete first skate frame
v84 completed the entire first active UpdateSkateMode frame, including timing/input, coast injection, speed application, steering, jump/state branch, ride-board update, retarget delay no-op and HUD, then later crashed with c0000005/StackHash_2beb.
Implication: current fault is delayed/asynchronous or appears only on a later frame.
v85 isolates the delayed THUG2 retarget subsystem completely and adds frame heartbeats.

## F010 - Do not misclassify a playtest against the wrong DLL
A DLL copied while FalloutNV.exe is already running does not replace the code loaded in that process. Confirm FNVGModTHUG2.log begins with the expected "bridge loaded, version N" before attributing a crash to that build.
The latest user crash after v85 deployment was actually from a v84-loaded process: log version 84, log mtime 18:08:29, v85 DLL deploy mtime 18:11:46.

## F009 follow-up — matched v85 activation test, 2026-10-05
User reported no crash. Installed DLL hash matches recorded v85; runtime log identifies version 85 and completes skate frame 180 with retarget skipped. This supports investigation of the quarantined retarget path, but does not prove its precise failure mechanism. Keep raw camera transforms and retarget writes quarantined pending evidence-driven repair. One successful activation is not sustained-playability validation.

## F011 — Obsolete scene-graph ABI declarations
IDA 6.8 audit confirms the SDK's UNMODIFIED OBSE NiObjects.h declares GetObject at slot 0x26 and UpdateTransform(void) at 0x2D, while the inspected FNV NiNode vtable has retn-4 null stubs at those slots. Actual name search is slot 0x27 and accepts an interned-string handle reference, not an ordinary C string. Confirmed ABI mismatch; exact runtime crash causality remains unproven. Keep animation/camera quarantine until corrected bindings and update semantics are verified. Evidence: builds/ida68_fnv_skeleton87.json; context/THUG2_INTEGRATION_CHECKPOINT_87.md.
