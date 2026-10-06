from pathlib import Path
import hashlib,json,collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
FNV=ROOT/"build/prepared/fnv_prop_catalog_curated/static_audit.json"
GMOD=ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json"
THUG=ROOT/"build/prepared/thug2_prop_catalog/embedded_prop_targets_curated.json"
OUTDIR=ROOT/"build/prepared/prop_menu_content_handoff"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"manifest.json"
SUMMARY=OUTDIR/"summary.json"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

f=json.loads(FNV.read_text())
g=json.loads(GMOD.read_text())
t=json.loads(THUG.read_text())

# Keep the default ready-to-spawn menu near ~300 items, not hundreds/thousands per source.
FNV_QUOTAS={
    "Skate - Rails & Railings":20,
    "Skate - Benches":14,
    "Skate - Ramps & Stairs":20,
    "Skate - Ledges & Barriers":12,
    "Skate - Tables & Counters":12,
    "Skate - Crates & Large Boxes":10,
    "Skate - Pipes":7,
    "Street - Fences":8,
    "Street - Signs":8,
    "Street - Lamps & Poles":6,
    "Street - Small Props":12,
    "Furniture - Chairs & Couches":8,
    "Furniture - Storage":8,
    "Furniture - Desks":5,
    "Utility - Vending & Terminals":5,
    "Nature - Rocks":5,
    "Nature - Trees & Plants":5,
    "Misc Environment":5,
}
assert sum(FNV_QUOTAS.values())==170

fnv_selected=[]
fnv_shortfalls={}
for cat,quota in FNV_QUOTAS.items():
    pool=[r for r in f["records"] if r["spawn_category"]==cat and r["static_candidate_ok"]]
    take=pool[:quota]
    if len(take)<quota:fnv_shortfalls[cat]=quota-len(take)
    for r in take:
        fnv_selected.append({
            "source":"Fallout New Vegas",
            "menu_category":cat,
            "source_path":r["path"],
            "runtime_mesh_path":r["path"].replace("meshes/","",1).replace("/","\\"),
            "dimensions":r.get("dimensions"),
            "triangles":r.get("triangles"),
            "collision_types":r.get("collision_types",{}),
            "authored_identity":"native FNV NIF",
            "validation_state":"static_clean_runtime_pending",
        })

# Fill any FNV shortfall from other static-clean records without duplicating paths.
used={x["source_path"].lower() for x in fnv_selected}
if len(fnv_selected)<170:
    for r in f["records"]:
        if len(fnv_selected)>=170:break
        if not r["static_candidate_ok"] or r["path"].lower() in used:continue
        used.add(r["path"].lower())
        fnv_selected.append({
            "source":"Fallout New Vegas","menu_category":r["spawn_category"],
            "source_path":r["path"],
            "runtime_mesh_path":r["path"].replace("meshes/","",1).replace("/","\\"),
            "dimensions":r.get("dimensions"),"triangles":r.get("triangles"),
            "collision_types":r.get("collision_types",{}),
            "authored_identity":"native FNV NIF",
            "validation_state":"static_clean_runtime_pending",
        })

gmod_selected=[]
for r in g["records"]:
    gmod_selected.append({
        "source":"Garry's Mod / mounted Source content",
        "menu_category":r["category"],
        "source_path":r["source_model"],
        "runtime_mesh_path":r["output_nif_relative"].replace("meshes/","",1).replace("/","\\"),
        "dimensions":r["dimensions"],
        "mass":r.get("mass"),
        "havok_material":r.get("havok_material"),
        "source_surfaceprop":r.get("source_surfaceprop"),
        "authored_identity":"converted from installed Source/GMod model with collision",
        "validation_state":"converted_collision_materials_resolved_runtime_pending",
    })

ready=fnv_selected+gmod_selected
ready_counts=collections.Counter(x["source"] for x in ready)
cat_counts=collections.Counter((x["source"],x["menu_category"]) for x in ready)

# THUG2 targets are not yet ready-to-spawn and are deliberately kept out of the ready count.
thug_queue=[{
    "source":"THUG2",
    "menu_category":r["category"],
    "identifier":r["identifier"],
    "level":r["level"],
    "family":r["family"],
    "priority_score":r["priority_score"],
    "validation_state":"embedded_scene_target_requires_split_conversion_collision_validation",
} for r in t["records"]]

result={
    "purpose":"Data-only content handoff for the future source-faithful GMod Q menu port. This does not implement or alter the menu runtime.",
    "default_ready_target":"about 300 spawnable environment/skate props",
    "ready_candidate_count":len(ready),
    "ready_by_source":dict(ready_counts),
    "fnv_requested":170,
    "fnv_selected":len(fnv_selected),
    "fnv_quota_shortfalls_before_fill":fnv_shortfalls,
    "gmod_selected":len(gmod_selected),
    "thug2_embedded_queue_count":len(thug_queue),
    "policy":[
        "Keep the player-facing prop browser compact and useful instead of exposing the full 13k FNV or 7.5k converted Source registries.",
        "Favor skate obstacles and practical environment/physics objects.",
        "THUG2 embedded props do not enter the ready menu until separated from level geometry and independently converted/validated.",
        "When THUG2 props are promoted, prefer replacing redundant lower-priority ready props so the default menu remains near 300-320 items.",
        "Runtime spawn/Physgun/skating playtests are still required before final promotion."
    ],
    "source_manifests":{
        "fnv_static_audit":{"path":str(FNV.relative_to(ROOT)).replace("\\","/"),"sha256":sha(FNV)},
        "gmod_curated":{"path":str(GMOD.relative_to(ROOT)).replace("\\","/"),"sha256":sha(GMOD)},
        "thug2_embedded_targets":{"path":str(THUG.relative_to(ROOT)).replace("\\","/"),"sha256":sha(THUG)},
    },
    "ready_categories":[{"source":s,"category":c,"count":n} for (s,c),n in sorted(cat_counts.items())],
    "ready_records":ready,
    "thug2_future_queue":thug_queue,
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
summary={
    "ready_candidate_count":len(ready),
    "ready_by_source":dict(ready_counts),
    "fnv_selected":len(fnv_selected),
    "gmod_selected":len(gmod_selected),
    "thug2_future_queue_count":len(thug_queue),
    "ready_categories":result["ready_categories"],
    "policy":result["policy"],
}
SUMMARY.write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))