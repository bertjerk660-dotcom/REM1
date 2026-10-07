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


## F013 - Per-bone torso scaling deforms converted Combine armor
Human playtest showed that anisotropic per-bone torso-depth scaling made the Combine torso, back and shoulders worse even though the head correction was successful.
Durable rule: do not correct this armor's fit by scaling individual torso bone-local axes. Preserve the validated head correction and use isolated world-space translation/region fitting for torso placement changes, validating one geometric degree of freedom at a time.


## FS002 - xEdit FNVScript master-confirmation/save state can leave a successful-looking run unsaved
**Symptom:** `FNVScript.exe` reached the script window and showed expected in-memory records, but the output ESP was absent or an earlier report remained on disk because modal master confirmations/save state had not completed.

**Evidence:** The Goodsprings response v2 rebuild paused on separate master-confirmation dialogs for `FalloutNV.esm` and `REM_CombineArmor_Test_TorsoLowered.esp`; checking only the window title/report was insufficient to prove a new ESP was saved.

**Proven handling:**
- verify the actual output file exists and its hash/mtime changed;
- recursively parse all group/record/subrecord sizes before deployment;
- for small, well-understood post-generation edits, prefer the checked-in deterministic binary patcher over repeatedly driving xEdit GUI state;
- keep the original generated ESP as an immutable backup;
- never treat xEdit's in-memory “script done” state as a successful build until the on-disk artifact validates.

**Prevention:** `support/goodsprings_response/patch_goodsprings_response_v2.py` and `validate_goodsprings_response.py` are the reproducible fallback/validation path for this encounter.
