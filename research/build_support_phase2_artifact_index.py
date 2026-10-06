from pathlib import Path
import json,hashlib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"builds/support_phase2_artifacts_20261006.json"

paths=[
 "build/validation/support_lane_state.json",
 "build/prepared/final_prop_catalog_handoff/manifest.json",
 "build/prepared/final_prop_catalog_thumbnails/manifest.json",
 "build/prepared/final_prop_catalog_thumbnails/quality_audit.json",
 "build/prepared/qmenu_content_adapter/manifest.json",
 "build/prepared/gmod_prop_catalog_sidecar/validation.json",
 "build/prepared/gmod_qmenu_source_inventory/manifest.json",
 "build/prepared/gmod_weapon_runtime_candidates/manifest.json",
 "build/prepared/gmod_weapon_runtime_candidates/model_presentation_audit.json",
 "build/prepared/gmod_weapon_runtime_candidates/weapon_sound_handoff.json",
 "build/prepared/gmod_weapon_runtime_candidates/resolved_sound_events/manifest.json",
 "build/prepared/gmod_tool_physgun_asset_handoff/manifest.json",
 "build/prepared/weapon_inventory_qa_matrix.json",
 "build/prepared/thug2_skateboard_asset_handoff/manifest.json",
 "build/prepared/thug2_skateboard_asset_handoff/scale_attachment_analysis.json",
 "build/prepared/thug2_ui_asset_handoff/manifest.json",
 "build/prepared/input_control_matrix/manifest.json",
 "build/prepared/thug2_prop_catalog/embedded_prop_handoff/manifest.json",
 "build/prepared/thug2_prop_catalog/component_evidence.json",
 "build/prepared/thug2_prop_catalog/spatial_prop_candidates/mapping.json",
 "build/prepared/thug2_prop_catalog/target_classification.json",
 "build/prepared/support_sidecars/manifest.json",
 "build/prepared/regression_test_packs/manifest.json",
 "build/prepared/historical_artifact_registry/manifest.json",
 "build/prepared/release_install_manifest/manifest.json",
 "build/prepared/release_install_manifest/summary.json",
 "build/combine_armor/validation.json",
]

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

summary_keys=(
 "status","error_count","ready_count","entry_count","candidate_count","generated","failed",
 "weapon_count","unresolved_count","asset_count","asset_resolved_count","target_count",
 "mapped","no_position","all_disabled","artifact_count","pack_count","requested","resolved",
 "ready_for_geometry_review","not_ready_or_semantic","lua_file_count","tool_stool_files"
)
rows=[]
for rel in paths:
    p=ROOT/rel
    row={"path":rel,"exists":p.exists()}
    if p.exists():
        row.update({"bytes":p.stat().st_size,"sha256":sha(p)})
        try:
            j=json.loads(p.read_text(encoding="utf-8"))
            sm={k:j[k] for k in summary_keys if k in j}
            if "summary" in j and isinstance(j["summary"],dict):sm["summary"]=j["summary"]
            if "classification_counts" in j:sm["classification_counts"]=j["classification_counts"]
            if "missing" in j and isinstance(j["missing"],list):sm["missing"]=j["missing"]
            row["summary"]=sm
        except Exception as e:
            row["json_error"]=repr(e)
    rows.append(row)

res={
 "purpose":"Canonical GitHub-safe index of support-phase-2 local manifests. Proprietary assets are represented by hashes/provenance, not committed binaries.",
 "artifact_count":len(rows),
 "all_present":all(r["exists"] for r in rows),
 "artifacts":rows,
 "canonical_rules":[
   "Prefer gmod_tool_physgun_asset_handoff over the earlier smaller gmod_tool_physgun_assets duplicate.",
   "Prefer input_control_matrix over the earlier controller-map-only summary for authoritative control mapping.",
   "Prefer regression_test_packs over the earlier seven-pack regression_packs duplicate.",
   "Prefer historical_artifact_registry over the earlier smaller versioned_artifact_inventory duplicate.",
   "Prefer release_install_manifest/manifest.json and summary.json over the earlier flat release_install_manifest.json."
 ]
}
OUT.write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({
 "artifact_count":res["artifact_count"],
 "all_present":res["all_present"],
 "missing":[r["path"] for r in rows if not r["exists"]]
},indent=2))