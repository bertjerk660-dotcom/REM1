from pathlib import Path
import json,hashlib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"builds/prop_support_phase3_artifacts_20261006.json"
paths=[
 "build/prepared/prop_support_phase3/summary.json",
 "build/prepared/prop_support_phase3/catalog_quality_ledger.json",
 "build/prepared/prop_support_phase3/redundancy_audit.json",
 "build/prepared/prop_support_phase3/category_balance.json",
 "build/prepared/prop_support_phase3/gmod_prop_dependency_audit.json",
 "build/prepared/prop_support_phase3/fnv_prop_dependency_hints.json",
 "build/prepared/prop_support_phase3/runtime_test_batches.json",
 "build/prepared/prop_support_phase3/runtime_validation_ledger.json",
 "build/prepared/prop_support_phase3/thug2_promotion_queue.json",
 "build/prepared/prop_support_phase3/menu_budget.json",
 "build/prepared/prop_support_phase3/gmod_spawnicon_coverage.json",
 "build/prepared/prop_support_phase3/prop_payload_provenance.json",
 "build/prepared/prop_menu_thumbnails/native_gmod_spawnicons/manifest.json",
 "build/validation/prop_support_phase3.json",
 "build/validation/support_lane_state.json",
 "build/prepared/release_install_manifest/manifest.json",
 "build/prepared/release_install_manifest/summary.json",
]
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()
rows=[]
for rel in paths:
    p=ROOT/rel
    row={"path":rel,"exists":p.exists()}
    if p.exists():
        row["bytes"]=p.stat().st_size; row["sha256"]=sha(p)
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            sm={}
            for k in ("status","error_count","check_count","ready_props","redundancy_groups","representative_test_props","test_batches","prop_count","authored_movable","candidate_count","batch_count","selected_count","current_ready","first_wave_target","native_spawnicons_found","native_spawnicons_missing","artifact_count"):
                if k in j:sm[k]=j[k]
            if "summary" in j and isinstance(j["summary"],dict):sm["summary"]=j["summary"]
            row["summary"]=sm
        except Exception as e:
            row["json_error"]=repr(e)
    rows.append(row)
result={
 "purpose":"GitHub-safe artifact index for prop support phase 3. Proprietary meshes/textures are represented only by derived metadata, paths and hashes.",
 "artifact_count":len(rows),
 "all_present":all(x["exists"] for x in rows),
 "artifacts":rows,
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"artifact_count":result["artifact_count"],"all_present":result["all_present"]},indent=2))