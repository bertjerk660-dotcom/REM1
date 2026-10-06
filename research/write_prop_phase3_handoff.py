from pathlib import Path
import json,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/prop_support_phase3"
summary=json.loads((BASE/"summary.json").read_text())
budget=json.loads((BASE/"menu_budget.json").read_text())
batches=json.loads((BASE/"runtime_test_batches.json").read_text())
thug=json.loads((BASE/"thug2_promotion_queue.json").read_text())
icons=json.loads((BASE/"gmod_spawnicon_coverage.json").read_text())
gmod=json.loads((BASE/"gmod_prop_dependency_audit.json").read_text())
fnv=json.loads((BASE/"fnv_prop_dependency_hints.json").read_text())

plan=ROOT/"context/PROP_SUPPORT_NEXT_20.md"
lines=[
"# Prop-focused non-Astra / non-Opus next 20","",
"Purpose: keep progressing the mashup through safe, reproducible prop/content work without modifying Astra v88, THUG2 runtime code, the real Q-menu runtime or native Tool Gun/Physgun mechanics.","",
"Status legend: COMPLETE = support/static preparation finished; IN PROGRESS = useful prep exists but human or model-review work remains; PENDING = not started or intentionally waits for earlier gates.","",
"1. **Reconcile prop source truth — COMPLETE.** Canonical working set is 290 ready props (170 FNV + 120 GMod/Source) plus 106 THUG2 targets, of which 85 are spatial geometry candidates.",
"2. **Build a unified per-prop quality ledger — COMPLETE.** Form binding, dimensions, thumbnail coverage, collision/material evidence, utility and runtime-pending state are recorded for all 290.",
"3. **Detect likely duplicate/variant clutter — COMPLETE.** Variant groups are flagged for review only; nothing is auto-removed.",
"4. **Score props for skate usefulness — COMPLETE.** Rails/ramps/ledges/stairs receive highest utility, then benches/beams/barriers/physics clutter.",
"5. **Set the compact-menu growth budget — COMPLETE.** Keep the player-facing browser at 300–320; first target is 310 by promoting up to 20 validated THUG2 props.",
"6. **Audit GMod prop collision/mobility evidence — COMPLETE STATIC.** All 120 curated GMod props retain conversion collision evidence; source mass is recorded for mobility review.",
"7. **Audit GMod prop scale outliers — COMPLETE STATIC.** Category-specific size limits are rechecked; flagged entries require human in-game scale confirmation rather than automatic rescaling.",
"8. **Audit GMod material dependencies — COMPLETE STATIC.** Unique referenced material payloads are hashed and missing paths are recorded.",
"9. **Audit FNV form/content dependencies — COMPLETE STATIC.** Each native prop keeps plugin/FormID/EDID plus a path-based content hint for later load-order testing.",
"10. **Check category balance and weak spots — COMPLETE.** Current ready counts and source/category distribution are machine-recorded for future swaps.",
"11. **Build representative human prop test batches — COMPLETE PREP.** 56 representative props are split into 5 batches covering all source/category groups plus size extremes.",
"12. **Preserve stable spawn identity for testing — COMPLETE PREP.** Every test row carries plugin, file FormID and EDID; final console load-order prefix must be resolved at test time.",
"13. **Keep support sidecars isolated — COMPLETE PREP.** Prop catalog sidecar stays disabled outside its dedicated test pack.",
"14. **Create the 290-prop runtime validation ledger — COMPLETE PREP.** Spawn/scale/material/collision/contact/cleanup fields all begin pending human validation.",
"15. **Rank THUG2 geometry candidates for extraction review — COMPLETE.** All 85 spatial candidates are ranked by category usefulness, confidence, leaf count and spatial distance.",
"16. **Prepare the first THUG2 prop visual-review packet — COMPLETE PREP.** Top 20 candidates are listed with source level, position, candidate leaf IDs, bounds and triangle evidence. Actual splitting/conversion remains model work.",
"17. **Build a replacement reserve for later THUG2 promotion — COMPLETE PREP.** 40 lower-utility/redundancy candidates are ranked; no existing prop is removed yet.",
f"18. **Audit native GMod SpawnIcon coverage — COMPLETE.** Native mounted spawnicons found for the curated set: {icons['native_spawnicons_found']}/{icons['gmod_props']}; all {icons['fallback_geometry_previews_available']} GMod entries retain generated geometry-preview fallback.",
"19. **Build prop release/provenance metadata — IN PROGRESS.** Current prop payloads/manifests are indexed; phase-3 outputs still need to be folded into the release/support validator.",
"20. **Validate, record and push this prop phase to GitHub — IN PROGRESS.** Add phase-3 validation, build manifest and update CURRENT_STATE/OPEN_WORK on prep/prop-content-phase3.","",
"## Immediate human gates",
"- Run the five representative prop batches with preflight/postflight capture.",
"- Do not call scale/collision/playability verified until observed in Fallout.",
"- Do not enable REM_GModProps_Catalog.esp except for its isolated test.",
"- THUG2 top-20 entries are review targets only, not yet standalone spawnable props.","",
"## Machine-readable outputs",
"- build/prepared/prop_support_phase3/catalog_quality_ledger.json",
"- build/prepared/prop_support_phase3/redundancy_audit.json",
"- build/prepared/prop_support_phase3/category_balance.json",
"- build/prepared/prop_support_phase3/gmod_prop_dependency_audit.json",
"- build/prepared/prop_support_phase3/fnv_prop_dependency_hints.json",
"- build/prepared/prop_support_phase3/runtime_test_batches.json",
"- build/prepared/prop_support_phase3/runtime_validation_ledger.json",
"- build/prepared/prop_support_phase3/thug2_promotion_queue.json",
"- build/prepared/prop_support_phase3/menu_budget.json",
"- build/prepared/prop_support_phase3/gmod_spawnicon_coverage.json",
"- build/prepared/prop_support_phase3/prop_payload_provenance.json",
]
plan.write_text("\n".join(lines)+"\n",encoding="utf-8")

review=ROOT/"context/THUG2_PROP_TOP20_REVIEW.md"
rl=["# THUG2 prop top-20 extraction review packet","",
    "These are the highest-ranked support candidates for visual leaf verification. Ranking is not proof that a leaf is the intended standalone prop.",""]
for i,r in enumerate(thug["top20"],1):
    leaf=r.get("top_leaf") or {}
    rl += [
      f"## {i}. {r['identifier']} ({r['level']})",
      f"- Category: {r['category']}",
      f"- Review score: {r['promotion_review_score']}; confidence: {r['confidence']}",
      f"- Source position: {r['position']}",
      f"- Candidate leaves: {r['candidate_leaf_count']}; nearest box distance: {r['nearest_box_distance']}",
      f"- Top leaf node/mesh: {leaf.get('node')} / {leaf.get('mesh')}",
      f"- Top leaf triangles: {leaf.get('triangles')}; max dimension: {leaf.get('max_dim')}",
      f"- Top leaf bounds: min {leaf.get('min')} / max {leaf.get('max')}",
      "- Next gate: visually confirm isolated geometry before split/conversion/collision work.",
      ""
    ]
review.write_text("\n".join(rl),encoding="utf-8")

testdoc=ROOT/"context/PROP_RUNTIME_TEST_BATCHES.md"
tl=["# Prop runtime test batches","",
    "Prepared human-validation batches. Do not infer runtime correctness from static checks.",""]
for b in batches["batches"]:
    tl += [f"## Batch {b['batch']}",""]
    for m in b["members"]:
        tl.append(f"- {m['source']} | {m['category']} | {m['display_name']} | {m['plugin']}:{m['formid_file']} | {m.get('edid')}")
    tl += ["","Checks: "+", ".join(b["test_checks"]),""]
testdoc.write_text("\n".join(tl),encoding="utf-8")

status=ROOT/"context/PROP_PHASE3_STATUS.md"
sl=[
"# Prop support phase 3 status","",
f"- Ready catalog: {summary['ready_props']} ({summary['source_counts']}).",
f"- Representative test set: {summary['representative_test_props']} props in {summary['test_batches']} batches.",
f"- GMod authored-mobility evidence: {summary['gmod_authored_movable']}/{summary['gmod_props']} curated entries.",
f"- Unique GMod material files indexed: {summary['gmod_material_files']}.",
f"- Native GMod spawnicons found: {summary['gmod_native_spawnicons_found']}; generated fallback previews available: {summary['gmod_fallback_previews']}.",
f"- THUG2 spatial candidates ranked: {summary['thug2_spatial_candidates_ranked']}; top review packet: {summary['thug2_top20_ready_for_visual_review']}.",
f"- Menu plan: {summary['menu_current']} now; first target {summary['menu_first_wave_target']}; stay within 300–320.",
"- Runtime playtest remains NOT RUN for phase-3 prop outputs.",
"- Astra/runtime code modified: false.",
"",
"Human gameplay validation is still required before prop promotion."
]
status.write_text("\n".join(sl)+"\n",encoding="utf-8")
print(json.dumps({"plan":str(plan),"top20":str(review),"batches":str(testdoc),"status":str(status)},indent=2))