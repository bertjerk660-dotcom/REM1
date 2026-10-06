from pathlib import Path
import json,re
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
B=ROOT/"build/prepared/prop_support_phase4"
SUM=json.loads((B/"summary.json").read_text())
VAL=json.loads((ROOT/"build/validation/prop_support_phase4.json").read_text())
SUP=json.loads((ROOT/"build/validation/support_lane_state.json").read_text())
REL=json.loads((ROOT/"build/prepared/release_install_manifest/summary.json").read_text())
MAT=json.loads((B/"thug2_material_collision_plan.json").read_text())
BAL=json.loads((B/"category_balance_target310.json").read_text())
FB=json.loads((B/"reserve_fallback_map.json").read_text())
TFB=json.loads((B/"runtime_test_batches_with_fallbacks.json").read_text())
SID=json.loads((ROOT/"build/prepared/thug2_prop_catalog_sidecar/build_report.json").read_text())

plan=ROOT/"context/PROP_SUPPORT_PHASE4_NEXT20.md"
lines=[
"# Prop-focused next 20 — phase 4","",
"Purpose: continue useful prop/environment work without touching Astra/Opus-owned THUG2 runtime, animation, camera, real GMod Q-menu runtime or native Tool Gun/Physgun mechanics.","",
"Status legend: COMPLETE = reproducible support work finished; COMPLETE PREP = support side is finished but a human/Astra gate remains; HUMAN GATE = requires visual/in-game confirmation; ASTRA GATE = reserved model/runtime integration.","",
"1. **Reconcile prop source truth — COMPLETE.** Phase 4 is based on the verified phase-3 set: 290 ready props (170 FNV + 120 GMod/Source), plus the 106 THUG2 target archive.",
"2. **Protect runtime/Astra state — COMPLETE.** Installed v85, main ESP and isolated v88 hashes remain unchanged; no runtime code was modified.",
"3. **Diversify the THUG2 first-wave review set — COMPLETE.** 20 candidates: 6 rails, 5 ramps, 4 ledges, 2 benches/tables, 2 fences/pipes and 1 stairs/platform target.",
"4. **Render actual THUG2 candidate-leaf previews — COMPLETE.** All 20 diversified candidates have converted-level GLB geometry previews and leaf metrics.",
f"5. **Score THUG2 leaf isolation/complexity — COMPLETE.** {SUM['leaf_review_status_counts']['high_review_priority']} high-priority + {SUM['leaf_review_status_counts']['medium_review_priority']} medium-priority, 0 complex; none are auto-promoted.",
f"6. **Build a compact GMod reserve pool — COMPLETE.** {SUM['gmod_reserve_selected']} reserve props selected from {SUM['gmod_reserve_eligible']} eligible converted/collision-bearing candidates, balanced across 8 useful categories.",
"7. **Unify the cross-game prop taxonomy — COMPLETE.** Current 290 + hidden future THUG2 entries map to source-neutral skate/physics/environment/street buckets for the future real GMod Q-menu adapter.",
"8. **Reserve future THUG2 form metadata safely — COMPLETE PREP.** 20 future local IDs/EDIDs are reserved; no live ESP records were created.",
f"9. **Build THUG2 material provenance — COMPLETE.** Material/image references are recorded for all {MAT['with_materials']}/{MAT['count']} diversified leaf candidates.",
f"10. **Assign collision strategy per THUG2 candidate — COMPLETE PREP.** {MAT['collision_roles'].get('static_skate_obstacle',0)} are planned as static skate obstacles and {MAT['collision_roles'].get('static_environment_prop',0)} as static environment props; Physgun mobility is not inferred from level geometry.",
"11. **Split visually confirmed THUG2 objects from level geometry — HUMAN GATE.** Preview identity must be confirmed first; no split is considered validated yet.",
"12. **Convert confirmed THUG2 standalone objects to FNV NIF — ASTRA/MODEL GATE.** Preserve original geometry/material identity and independently validate scale/collision.",
f"13. **Build the 310-entry category balance plan — COMPLETE.** Deficits are {[(x['bucket'],x['delta']) for x in BAL['deficits']]}; excesses are {[(x['bucket'],x['delta']) for x in BAL['excesses']]}.",
f"14. **Map every default prop to reserve replacements — COMPLETE.** All {FB['ready_count']} ready props have 3 ranked GMod reserve fallbacks.",
"15. **Generate final thumbnails for promoted THUG2 standalone props — PENDING BY DESIGN.** This begins only after a validated standalone NIF exists; current leaf previews are review evidence only.",
f"16. **Expand runtime test batches with reserve fallbacks — COMPLETE PREP.** {TFB['selected_count']} representative test props in {TFB['batch_count']} batches now carry two reserve fallbacks each.",
f"17. **Prepare the THUG2 prop sidecar builder — COMPLETE PREP / SAFELY BLOCKED.** Builder status is {SID['status']} with {SID['ready']} ready / {SID['blocked']} blocked; it refuses to create an ESP until promotion gates pass.",
f"18. **Run prop phase-4 validation — COMPLETE.** {VAL['check_count']} checks pass with zero errors. This is static/preflight evidence, not gameplay validation.",
f"19. **Integrate prop phase 4 into release/support metadata — COMPLETE.** Release index now tracks {REL['support_manifests']} support manifests; unified support validator passes {len(SUP['checks'])} checks with zero errors.",
"20. **Push and verify the phase-4 GitHub branch — READY FOR FINAL SYNC.** Upload the latest scripts/docs/build manifests to prep/prop-content-phase4, verify the diff against phase 3, then mark this complete.","",
"## Current prop numbers",
f"- Ready player-facing catalog: {SUM['current_ready_props']}.",
f"- Planned first-wave total if all 20 THUG2 candidates eventually pass: {SUM['planned_first_wave']}.",
f"- GMod reserve: {SUM['gmod_reserve_selected']} selected from {SUM['gmod_reserve_eligible']} eligible filtered candidates.",
f"- THUG2 diversified wave: {SUM['thug2_diversified_selected']} ({SUM['thug2_diversified_categories']}).",
f"- Leaf-review status: {SUM['leaf_review_status_counts']}.",
f"- Prop phase-4 validator: {VAL['check_count']} / zero errors.",
f"- Unified support validator: {len(SUP['checks'])} / zero errors.",
"- Runtime playtest: NOT RUN for phase 4.","",
"## Remaining gates that cannot be honestly marked complete here",
"- Human visual confirmation that each chosen GLB leaf is the intended THUG2 object.",
"- Standalone object splitting and source-faithful model conversion for confirmed THUG2 candidates.",
"- In-game prop scale/material/collision/contact/cleanup testing.",
"- Real GMod Q-menu runtime and native Tool Gun/Physgun behavior remain Astra-owned.",
]
plan.write_text("\n".join(lines)+"\n",encoding="utf-8")

status=ROOT/"context/PROP_PHASE4_STATUS.md"
status.write_text("\n".join([
"# Prop support phase 4 status","",
f"- Ready catalog remains {SUM['current_ready_props']}; no THUG2 candidate was falsely promoted.",
f"- Planned first wave remains {SUM['planned_first_wave']} only if all 20 diversified THUG2 candidates pass later gates.",
f"- GMod reserve: {SUM['gmod_reserve_selected']} of {SUM['gmod_reserve_eligible']} eligible filtered candidates.",
f"- THUG2 review mix: {SUM['thug2_diversified_categories']}.",
f"- Leaf review: {SUM['leaf_review_status_counts']}.",
f"- THUG2 material provenance: {MAT['with_materials']}/{MAT['count']}; collision roles: {MAT['collision_roles']}.",
f"- Reserve fallback mapping: {FB['ready_count']} ready props x 3 alternatives.",
f"- Representative runtime batches with fallbacks: {TFB['selected_count']} props / {TFB['batch_count']} batches.",
f"- THUG2 sidecar builder: {SID['status']} ({SID['ready']} ready / {SID['blocked']} blocked).",
f"- Phase-4 validator: PASS, {VAL['check_count']} checks / 0 errors.",
f"- Unified support validator: PASS, {len(SUP['checks'])} checks / 0 errors.",
f"- Release/support manifest count: {REL['support_manifests']}.",
"- Runtime/Astra code changed: false.",
"- Runtime/visual playtest for phase 4: not run.",
])+"\n",encoding="utf-8")

bp=ROOT/"builds/prop_support_phase4_20261006.json"
obj=json.loads(bp.read_text())
obj["validation"]={"phase4":{"status":VAL["status"],"checks":VAL["check_count"],"errors":VAL["error_count"]},
                   "unified_support":{"status":SUP["status"],"checks":len(SUP["checks"]),"errors":SUP["error_count"]}}
obj["release_support_manifests"]=REL["support_manifests"]
obj["material_collision"]={"with_materials":MAT["with_materials"],"count":MAT["count"],"collision_roles":MAT["collision_roles"]}
obj["category_balance"]={"deficits":BAL["deficits"],"excesses":BAL["excesses"]}
obj["reserve_fallbacks"]={"ready_count":FB["ready_count"],"reserve_count":FB["reserve_count"],"fallbacks_per_ready":3}
obj["runtime_batches_with_fallbacks"]={"batches":TFB["batch_count"],"selected":TFB["selected_count"],"fallbacks_per_test":2}
obj["thug2_sidecar_builder"]={"status":SID["status"],"ready":SID["ready"],"blocked":SID["blocked"]}
bp.write_text(json.dumps(obj,indent=2),encoding="utf-8")

for rel in ("context/CURRENT_STATE.md","context/OPEN_WORK.md"):
    p=ROOT/rel;s=p.read_text(encoding="utf-8")
    s=re.sub(r"Dedicated phase-4 validator passes \d+ checks","Dedicated phase-4 validator passes %d checks"%VAL["check_count"],s)
    s=re.sub(r"phase-4 static validation \(\d+ checks\)","phase-4 static validation (%d checks)"%VAL["check_count"],s)
    p.write_text(s,encoding="utf-8")

print(json.dumps({"phase4_checks":VAL["check_count"],"support_checks":len(SUP["checks"]),"support_manifests":REL["support_manifests"]},indent=2))