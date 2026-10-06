from pathlib import Path
import json, hashlib, collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
FNV=ROOT/"build/prepared/fnv_prop_catalog_curated/ready_existing_forms.json"
GMOD=ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json"
GMOD_FORMS=ROOT/"build/prepared/gmod_prop_catalog_sidecar/form_map.json"
THUG=ROOT/"build/prepared/thug2_prop_catalog/embedded_prop_targets_curated.json"
OUTDIR=ROOT/"build/prepared/final_prop_catalog_handoff"
OUTDIR.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

f=json.loads(FNV.read_text(encoding="utf-8"))
g=json.loads(GMOD.read_text(encoding="utf-8"))
fm=json.loads(GMOD_FORMS.read_text(encoding="utf-8"))
t=json.loads(THUG.read_text(encoding="utf-8"))

# source model -> sidecar form row
form_by_source={x["source_model"].replace("\\","/").lower():x for x in fm["records"]}

records=[]
for r in f["records"]:
    records.append({
        "source":"Fallout New Vegas",
        "menu_category":r["menu_category"],
        "display_name":r.get("full") or r.get("edid") or Path(r["source_path"]).stem,
        "source_path":r["source_path"],
        "runtime_mesh_path":r["runtime_mesh_path"],
        "dimensions":r.get("dimensions"),
        "triangles":r.get("triangles"),
        "form_binding":{
            "plugin":r["form_plugin"],
            "signature":r["form_signature"],
            "formid_file":r["formid_file"],
            "edid":r.get("edid")
        },
        "provenance":"native FNV model + existing native base form",
        "validation_state":"static_clean_existing_form_runtime_pending",
    })

missing_gmod_forms=[]
for r in g["records"]:
    source_key=r["source_model"].replace("\\","/").lower()
    form=form_by_source.get(source_key)
    if not form:
        missing_gmod_forms.append(r["source_model"])
        continue
    mesh=r["output_nif_relative"].replace("/","\\")
    if mesh.lower().startswith("meshes\\"):mesh=mesh[7:]
    records.append({
        "source":"Garry's Mod / mounted Source content",
        "menu_category":r["category"],
        "display_name":form["full"],
        "source_path":r["source_model"],
        "runtime_mesh_path":mesh,
        "dimensions":r.get("dimensions"),
        "mass":r.get("mass"),
        "havok_material":r.get("havok_material"),
        "source_surfaceprop":r.get("source_surfaceprop"),
        "form_binding":{
            "plugin":"REM_GModProps_Catalog.esp",
            "signature":"MSTT",
            "local_id":form["local_id"],
            "formid_file":form["formid_file"],
            "edid":form["edid"]
        },
        "provenance":"installed Source/GMod model -> existing project conversion -> disabled catalog sidecar",
        "validation_state":"converted_collision_materials_resolved_sidecar_static_pass_runtime_pending",
    })

by_source=collections.Counter(r["source"] for r in records)
by_category=collections.Counter((r["source"],r["menu_category"]) for r in records)
thug_queue=[{
    "identifier":r["identifier"],"level":r["level"],"category":r["category"],
    "family":r["family"],"priority_score":r["priority_score"],
    "state":"embedded_source_target_requires_split_conversion_collision_validation"
} for r in t["records"]]

result={
    "purpose":"Final support-lane data catalog for Astra's later source-faithful GMod Q-menu adapter. No Q-menu runtime is implemented here.",
    "ready_count":len(records),
    "ready_by_source":dict(by_source),
    "missing_gmod_sidecar_forms":missing_gmod_forms,
    "all_ready_have_form_binding":all(bool(r.get("form_binding")) for r in records),
    "ready_records":records,
    "future_thug2_queue_count":len(thug_queue),
    "future_thug2_queue":thug_queue,
    "source_manifests":{
        "fnv_ready_existing_forms":{"path":str(FNV.relative_to(ROOT)).replace("\\","/"),"sha256":sha(FNV)},
        "gmod_curated":{"path":str(GMOD.relative_to(ROOT)).replace("\\","/"),"sha256":sha(GMOD)},
        "gmod_sidecar_form_map":{"path":str(GMOD_FORMS.relative_to(ROOT)).replace("\\","/"),"sha256":sha(GMOD_FORMS)},
        "thug2_future_targets":{"path":str(THUG.relative_to(ROOT)).replace("\\","/"),"sha256":sha(THUG)}
    },
    "category_counts":[{"source":s,"category":c,"count":n} for (s,c),n in sorted(by_category.items())],
    "policy":[
        "Default ready catalog stays at 290: 170 FNV existing-form props + 120 GMod/Source sidecar props.",
        "No default FNV ready entry requires a newly invented custom form.",
        "THUG2 props remain outside the ready catalog until their source level geometry is split and independently validated.",
        "When THUG2 props are promoted, replace redundant lower-priority entries to keep the default browser near 300-320."
    ]
}
(OUTDIR/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
(OUTDIR/"summary.json").write_text(json.dumps({
    "ready_count":result["ready_count"],
    "ready_by_source":result["ready_by_source"],
    "all_ready_have_form_binding":result["all_ready_have_form_binding"],
    "missing_gmod_sidecar_forms":missing_gmod_forms,
    "future_thug2_queue_count":len(thug_queue),
    "category_counts":result["category_counts"],
    "policy":result["policy"]
},indent=2),encoding="utf-8")
print((OUTDIR/"summary.json").read_text())