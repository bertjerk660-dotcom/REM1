from pathlib import Path
import json
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
B=ROOT/"build/prepared/prop_support_phase4"
SUM=json.loads((B/"summary.json").read_text())
VAL=json.loads((ROOT/"build/validation/prop_support_phase4.json").read_text())
WAVE=json.loads((B/"thug2_diversified_first_wave.json").read_text())
LEAF=json.loads((B/"thug2_diversified_leaf_review.json").read_text())
RES=json.loads((B/"gmod_reserve_pool.json").read_text())
TAX=json.loads((B/"menu_taxonomy_v2.json").read_text())

plan=ROOT/"context/PROP_SUPPORT_PHASE4_NEXT20.md"
lines=[
"# Prop-focused next 20 — phase 4","",
"Purpose: continue useful prop/environment work without touching Astra/Opus-owned THUG2 runtime, animation, camera, real GMod Q-menu runtime or native Tool Gun/Physgun mechanics.","",
"Status legend: COMPLETE = reproducible support work finished; IN PROGRESS = useful evidence exists but more support work remains; HUMAN GATE = requires in-game/visual confirmation; ASTRA GATE = reserved high-risk runtime/model integration.","",
"1. Reconcile the prop source of truth from GitHub and local manifests — COMPLETE. Phase 3 remains 290 ready props + 106 THUG2 targets; phase 4 branches from prep/prop-content-phase3.",
"2. Protect the active runtime before prop work — COMPLETE. v85, the main ESP and isolated v88 hashes were rechecked; no runtime/Astra code was modified.",
"3. Replace the rail-heavy THUG2 top-20 with a diversified first-wave review set — COMPLETE. New quota: 6 rails, 5 ramps, 4 ledges, 2 benches/tables, 2 fences/pipes and 1 stairs/platform target.",
"4. Render actual candidate-leaf previews for the diversified THUG2 wave — COMPLETE. 20 review previews generated from converted level GLB leaf geometry.",
f"5. Score THUG2 leaf isolation/complexity — COMPLETE. {LEAF['status_counts']['high_review_priority']} high-priority and {LEAF['status_counts']['medium_review_priority']} medium-priority candidates; none are auto-promoted.",
f"6. Build a practical GMod reserve library — COMPLETE. {RES['selected_reserve']} extra converted/collision-bearing props selected from {RES['eligible_after_filters']} eligible non-default candidates, balanced 10 per category.",
"7. Unify the cross-game prop taxonomy for the real Q-menu adapter — COMPLETE. Current 290 entries and the planned THUG2 first wave map into source-neutral skate/physics/environment/street buckets.",
"8. Reserve THUG2 prop form metadata without creating live records — COMPLETE. 20 future REM_THUG2Props_Catalog.esp IDs/EDIDs are reserved only; no ESP records were written.",
"9. Build per-candidate THUG2 material provenance — PENDING. Record material slots/texture references from each selected GLB leaf before extraction.",
"10. Assign collision strategy per THUG2 candidate — PENDING. Rails/ramps/ledges normally remain static skate obstacles; movable treatment requires explicit evidence and separate testing.",
"11. Create standalone extraction packages for the visually confirmed THUG2 leaves — HUMAN GATE. Do not split geometry until the preview is confirmed to match the named source object.",
"12. Convert confirmed THUG2 standalone props to FNV NIF — ASTRA/MODEL GATE. Keep original source geometry/material identity and validate scale/collision independently.",
"13. Build a category deficit/excess report for the 310-entry target — IN PROGRESS. Taxonomy counts exist; convert them into explicit swap/add targets before promotion.",
"14. Map each failed/default prop to a reserve replacement — PENDING. Use the 80-item GMod reserve instead of returning to the full 7,507/13,003-model archives.",
"15. Generate final thumbnails for promoted THUG2 props — PENDING. Only after a standalone NIF exists; support previews are not native GMod SpawnIcons.",
"16. Expand runtime prop test batches with reserve fallbacks — PENDING. Add one reserve candidate behind every representative default item that fails scale/material/collision tests.",
"17. Prepare the THUG2 sidecar schema/build script — IN PROGRESS. Form IDs/EDIDs are reserved; actual sidecar generation waits for validated NIFs.",
f"18. Run phase-4 static/preflight validation — COMPLETE. {VAL['check_count']} checks pass with zero errors; this is not gameplay validation.",
"19. Record phase-4 manifests/docs and integrate with release/support metadata — IN PROGRESS. Local phase-4 summary, review packet, reserve pool and promotion ledgers exist; GitHub artifact index/update is next.",
"20. Push and verify the prop phase-4 branch — IN PROGRESS. Upload tooling/docs/manifests to prep/prop-content-phase4, verify branch diff, and leave Astra/runtime branches untouched.","",
"Current prop numbers:",
f"- Ready player-facing catalog: {SUM['current_ready_props']}.",
f"- Planned first-wave catalog if all 20 THUG2 candidates eventually pass: {SUM['planned_first_wave']}.",
f"- GMod reserve: {SUM['gmod_reserve_selected']} selected from {SUM['gmod_reserve_eligible']} eligible filtered candidates.",
f"- THUG2 diversified review set: {SUM['thug2_diversified_selected']} ({SUM['thug2_diversified_categories']}).",
f"- THUG2 leaf review: {SUM['leaf_review_status_counts']}.",
"- Runtime playtest: NOT RUN for phase 4.",
"",
"Immediate safe work after this checkpoint:",
"- Material provenance for the 20 THUG2 leaves.",
"- Collision-strategy ledger for the 20 THUG2 leaves.",
"- 310-entry category deficit/excess plan.",
"- Default-to-reserve fallback mapping.",
"- Phase-4 GitHub artifact index and branch verification.",
]
plan.write_text("\n".join(lines)+"\n",encoding="utf-8")

status=ROOT/"context/PROP_PHASE4_STATUS.md"
sl=[
"# Prop support phase 4 status","",
f"- Current ready catalog: {SUM['current_ready_props']}.",
f"- Planned first wave: {SUM['planned_first_wave']}.",
f"- GMod reserve: {SUM['gmod_reserve_selected']} of {SUM['gmod_reserve_eligible']} eligible filtered candidates.",
f"- THUG2 diversified first-wave categories: {SUM['thug2_diversified_categories']}.",
f"- THUG2 leaf review status: {SUM['leaf_review_status_counts']}.",
f"- Form reservations: {SUM['form_reservations']}; no live records created.",
f"- Phase-4 validator: {VAL['status']} / {VAL['check_count']} checks / {VAL['error_count']} errors.",
"- Runtime/Astra code modified: false.",
"- Human visual/runtime gates remain open.",
]
status.write_text("\n".join(sl)+"\n",encoding="utf-8")

state=ROOT/"context/CURRENT_STATE.md"
s=state.read_text(encoding="utf-8")
marker="## Prop support phase 4 — 2026-10-06"
block=f"""
{marker}
- Phase-4 prop work is isolated from Astra/runtime code and tracked in context/PROP_SUPPORT_PHASE4_NEXT20.md.
- Ready catalog remains 290. The planned first-wave target is 310 only if individually validated THUG2 props pass promotion gates.
- A diversified THUG2 review wave now contains 20 candidates: {SUM['thug2_diversified_categories']}.
- Actual converted-level geometry previews exist for all 20; review scoring finds {LEAF['status_counts']['high_review_priority']} high and {LEAF['status_counts']['medium_review_priority']} medium candidates, with no automatic promotion.
- An 80-item GMod/Source reserve pool was selected from {RES['eligible_after_filters']} eligible converted/collision-bearing non-default props, balanced across 8 practical categories.
- Source-neutral menu taxonomy metadata now covers current ready props plus hidden future THUG2 entries.
- Twenty future THUG2 form IDs/EDIDs are reserved as metadata only; no new THUG2 prop ESP records were created.
- Dedicated phase-4 validator passes {VAL['check_count']} checks with zero errors. Runtime/visual playability validation remains pending.
"""
if marker in s:s=s.split(marker)[0].rstrip()+"\n\n"+block.strip()+"\n"
else:s=s.rstrip()+"\n\n"+block.strip()+"\n"
state.write_text(s,encoding="utf-8")

openp=ROOT/"context/OPEN_WORK.md"
o=openp.read_text(encoding="utf-8")
marker2="## Prop support phase 4 remaining gates"
block2=f"""
{marker2}
- Add material/texture provenance for each of the 20 diversified THUG2 leaf candidates.
- Assign and document collision strategy for each THUG2 candidate before conversion.
- Visually confirm candidate leaf identity before any geometry split or NIF conversion.
- Build a category deficit/excess plan for the 310 target and map failed/default props to the 80-item GMod reserve.
- Generate THUG2 sidecar records only after standalone NIF conversion plus scale/collision/material validation.
- Keep all support sidecars disabled outside isolated tests.
- Do not treat phase-4 static validation ({VAL['check_count']} checks) as gameplay validation.
"""
if marker2 in o:o=o.split(marker2)[0].rstrip()+"\n\n"+block2.strip()+"\n"
else:o=o.rstrip()+"\n\n"+block2.strip()+"\n"
openp.write_text(o,encoding="utf-8")

build=ROOT/"builds/prop_support_phase4_20261006.json"
obj={
 "build":"prop_support_phase4_20261006","branch":"prep/prop-content-phase4","parent":"prep/prop-content-phase3",
 "goal":"Advance the merged game's prop side with a diversified THUG2 review wave and practical GMod reserve, without runtime changes.",
 "changes":[
   "diversified 20-item THUG2 review wave",
   "actual converted-level candidate-leaf previews and isolation metrics",
   "80-item balanced GMod reserve pool",
   "source-neutral menu taxonomy v2",
   "future THUG2 form-ID/EDID reservations and promotion ledger",
   "phase-4 static validator"
 ],
 "validation":{"status":VAL["status"],"checks":VAL["check_count"],"errors":VAL["error_count"]},
 "playtest":"not_run","runtime_changes":False,
 "protected_hashes":{
   "installed_v85":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
   "astra_v88":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
   "main_esp":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7"
 },
 "summary":SUM,
 "known_gates":[
   "visual identity confirmation for THUG2 leaves",
   "standalone split/conversion/material/collision/scale validation",
   "human prop runtime batches",
   "real GMod Q-menu runtime remains Astra-owned"
 ]
}
build.write_text(json.dumps(obj,indent=2),encoding="utf-8")
print(json.dumps({"plan":str(plan),"status":str(status),"build":str(build)},indent=2))