from pathlib import Path
import json,hashlib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"builds/prop_support_phase4_artifacts_20261006.json"
paths=[
 "build/prepared/prop_support_phase4/summary.json",
 "build/prepared/prop_support_phase4/thug2_diversified_first_wave.json",
 "build/prepared/prop_support_phase4/thug2_diversified_leaf_review.json",
 "build/prepared/prop_support_phase4/thug2_material_collision_plan.json",
 "build/prepared/prop_support_phase4/gmod_reserve_pool.json",
 "build/prepared/prop_support_phase4/menu_taxonomy_v2.json",
 "build/prepared/prop_support_phase4/category_balance_target310.json",
 "build/prepared/prop_support_phase4/reserve_fallback_map.json",
 "build/prepared/prop_support_phase4/runtime_test_batches_with_fallbacks.json",
 "build/prepared/prop_support_phase4/promotion_plan.json",
 "build/prepared/prop_support_phase4/thug2_promotion_validation_ledger.json",
 "build/prepared/prop_support_phase4/review_packet.json",
 "build/prepared/thug2_prop_catalog_sidecar/build_report.json",
 "build/validation/prop_support_phase4.json",
 "build/validation/support_lane_state.json",
 "build/prepared/release_install_manifest/summary.json",
]
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest().upper()
rows=[]
keys=("status","error_count","check_count","current_ready_props","planned_first_wave","gmod_reserve_selected",
      "gmod_reserve_eligible","thug2_diversified_selected","selected","count","candidate_count","current_ready_count",
      "planned_first_wave_count","ready","blocked","batch_count","selected_count","ready_count","reserve_count",
      "with_materials","artifact_count","support_manifests")
for rel in paths:
 p=ROOT/rel
 row={"path":rel,"exists":p.exists()}
 if p.exists():
  row.update({"bytes":p.stat().st_size,"sha256":sha(p)})
  try:
   j=json.loads(p.read_text(encoding="utf-8"))
   sm={k:j[k] for k in keys if k in j}
   if "status_counts" in j:sm["status_counts"]=j["status_counts"]
   if "category_counts" in j:sm["category_counts"]=j["category_counts"]
   if "collision_roles" in j:sm["collision_roles"]=j["collision_roles"]
   row["summary"]=sm
  except Exception as e:row["json_error"]=repr(e)
 rows.append(row)
res={
 "purpose":"GitHub-safe artifact index for prop support phase 4. Binary previews and proprietary assets remain local; GitHub stores scripts/docs/hashes/provenance.",
 "artifact_count":len(rows),"all_present":all(r["exists"] for r in rows),"artifacts":rows,
 "local_binary_evidence":[
   "build/prepared/prop_support_phase4/diversified_leaf_previews/*.png",
   "build/prepared/prop_support_phase4/thug2_top20_contact_sheet.png"
 ]
}
OUT.write_text(json.dumps(res,indent=2))
print(json.dumps({"artifact_count":res["artifact_count"],"all_present":res["all_present"],"missing":[r["path"] for r in rows if not r["exists"]]},indent=2))