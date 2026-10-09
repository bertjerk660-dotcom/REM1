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


## F010 - Grind activation ignores valid surfaces
Human playtest reports that pressing G can trigger grinding anywhere.
Durable rule: grind entry must require the recovered THUG2 grind eligibility logic, including appropriate geometry/contact/state checks. A key press alone must never create a grind state.

## F011 - THUG2 animation/board-to-feet path not functioning
Skate mode can now be entered with left-click and exited with the holster key, but the board does not move into the correct skating position at the feet and the tested THUG2 animation set does not function.
Durable rule: do not equate successful mode switching with successful THUG2 runtime integration. Preserve working enter/exit transitions while repairing source-faithful board attachment, animation selection, retargeting, blending and state transitions.

## F012 - Current GMod prop menu is a placeholder
Human playtest reports the current GMod-style prop menu appears visually correct.
Durable rule: this is explicitly a placeholder and is not evidence that the real GMod Q menu has been ported. Final acceptance still requires the source-faithful GMod Q/spawn-menu implementation, tool-state bridge and associated behavior.

## F013 - Decompiled Source static-prop SMDs are in a rotated frame
Symptom: first O00 conversion put the bench's long axis on FNV +Y (forward) instead of X. The Crowbar SMD long axis was X (+/-37.3) while the QC/`.mdl` hull long axis was Y (+/-38.1).
Cause: studiomdl rotates `$staticprop` geometry 90 deg about +Z when compiling; the decompiled SMD is in the pre-rotation frame. Proven by mapping the physics SMD with model = (-smd_y, smd_x, z) and matching the hull in the `.mdl` header (offset 0x68) to within 0.38 units (studiomdl padding, even on all sides).
Fix: `research/source_to_fnv/convert_source_static.py` applies SMD -> model -> FNV explicitly and refuses to convert if the model-frame check exceeds 0.6 units.
Rule: never infer prop orientation from SMD axes alone; verify against the compiled `.mdl` hull. Weapon models (O01/O08) are not `$staticprop` and must be re-verified, not assumed to share this rotation.

## F014 - pyffi 2.2.3 writes non-reproducible / mis-flagged NIF headers
Symptoms: (a) first NIF failed to read back ("string too long") because the header endian byte was 0 (big) while data was little-endian; (b) two identical runs differed by 20 bytes in the header string table.
Cause: (a) `NifFormat.Data()` defaults the header endian flag to 0; (b) pyffi builds the string table from a set, whose order follows Python's per-process string hash seed.
Fix: set `data.header.endian_type = 1`; converter re-executes itself with `PYTHONHASHSEED=0`; read-back gate and an independent rerun check (validator check 12) now catch both.
Rule: any project tool that writes NIFs with pyffi must set the endian flag, pin the hash seed and read the file back.

## F015 - Legacy GMod prop converter defects (confirmed in source)
`research/convert_gmod_props.py` + `research/blender_prop_worker.py` (local workspace, 2026-10-05):
- `$surfaceprop` not in its table silently becomes `FO_HAV_MAT_METAL` (`Wood_Furniture` -> metal);
- `parse_vmt` reads only `$basetexture`/`$bumpmap`, so `$envmapmask` is dropped;
- one convex hull per prop, which fills open space (bench underside) with invisible collision;
- BSX flags 3 (animated + Havok) on statics, where vanilla uses 2;
- writes straight into the live game `Data` folder;
- ignores the F013 frame rotation.
Status: superseded for golden/weapon work by `research/source_to_fnv`. The legacy tool and its 5,655 earlier outputs are unchanged; outputs from it are not golden evidence.
