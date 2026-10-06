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


## F011 - THUG2 IDA analysis exists only in a running session
Evidence (2026-10-06): idaq.exe PID 23616 (IDA 6.8, started 01:43, -A -c) is analysing DUMPS\thug2\SLES_526.21 into research\thug2_ida\THUG2_PS2_68.idb. No packed THUG2_PS2_68.idb exists on disk; id0/id1/nam are locked. The only packed THUG2 database found is the older THUG2_skate_batch.idb.
Durable rule: never let an IDA database be the sole holder of reverse-engineering knowledge (PIPELINE.md). Before relying on or closing a session, save/pack the IDB, record its SHA256, and export function names, comments, types and structs to text with an IDA 6.8 script. Do not terminate a running IDA process to get a hash.
Status: open. Owner must save/close IDA when idle, then hash and back up the .idb.

## F012 - Address-only xref exports lose function identity
Evidence: research\thug2_ida\skate_xrefs.txt has 14/14 XREF rows with blank FUNC/NAME. research\thug2_mips_xrefs.txt reports REFS=0 for every target. research\fnv_grab_xrefs.txt has 2/2 blank. The richer C:\IDA68WORK\thug2_skate_table68.txt resolves some name/handler pairs (e.g. GetSkaterVelocity -> sub_27DC08) but shows only name-pointer runs with no adjacent handler for SkaterPhysicsControl_SwitchSkatingToWalking / SwitchWalkingToSkating, DoBalanceTrick and DoNextManualTrick. Name-to-handler mapping for those is unresolved in every export read. Hypothesis (unverified): a separate handler array.
Durable rule: an xref/table export is not accepted as evidence unless function start, name, segment and handler pointer are populated; add a validation check that fails on blank FUNC rows or REFS=0 for gameplay-critical targets.
Status: open. Needs an IDA 6.8 re-export and handler-table resolution.

## F013 - Evidence and dependency trees outside the workspace and inventory
Evidence: C:\IDA68WORK holds 50 scripts, 45 analysis outputs, 5 packed IDBs (including GMODCLIENT/GMODSERVER physgun analysis) and 3 binaries; none of it appears in the 247-row code_preservation inventory, and 102/103 top-level files are absent from research\ by name. Workspace scripts hard-code C:\IDA68WORK, DUMPS\thug2, Steam steamapps and IDA install paths.
Durable rule: any script or output reachable through a hard-coded external root must be inventoried with hash and provenance; scripts should read roots from one paths config. Derived unpack trees (thug2_datap_unpack, thug2_streams_unpack) are recorded by generating command, not archived.
Status: open. See OPEN_WORK.md preservation items.

## FS003 - Derived prop manifests can drift from the selected review wave
Observed 2026-10-06 during prop support phase 4. The diversified THUG2 first-wave selection was generated correctly, but the initial taxonomy/review packet still consumed the older score-only top-20 source. This could have produced valid-looking counts while referring to the wrong prop identities.
Durable rule: whenever a prop selection is replaced or diversified, validate candidate identity across the selection, geometry-review packet, menu taxonomy, form reservations and promotion ledger. Compare set membership where ordering is not semantically meaningful, and do not rely on matching counts alone.
