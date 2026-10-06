from pathlib import Path
import json, math, collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/fnv_prop_catalog_curated"
COV=json.loads((BASE/"form_coverage_static_clean.json").read_text(encoding="utf-8"))
OLD=json.loads((ROOT/"build/prepared/prop_menu_content_handoff/form_coverage_audit.json").read_text(encoding="utf-8"))
OUT=BASE/"ready_existing_forms.json"
REPL=BASE/"missing_form_replacements.json"

QUOTAS={
    "Skate - Rails & Railings":14,
    "Skate - Benches":14,
    "Skate - Ramps & Stairs":18,
    "Skate - Ledges & Barriers":10,
    "Skate - Tables & Counters":12,
    "Skate - Crates & Large Boxes":10,
    "Skate - Pipes":7,
    "Street - Fences":8,
    "Street - Signs":8,
    "Street - Lamps & Poles":7,
    "Street - Small Props":12,
    "Furniture - Chairs & Couches":8,
    "Furniture - Storage":8,
    "Furniture - Desks":5,
    "Utility - Vending & Terminals":7,
    "Nature - Rocks":8,
    "Nature - Trees & Plants":6,
    "Misc Environment":8,
}
assert sum(QUOTAS.values())==170

# Favor compact/practical objects, while retaining the curated source ordering as tie-break.
def quality(r,idx):
    dims=r.get("dimensions") or [9999,9999,9999]
    md=max(dims)
    tri=r.get("triangles") or 0
    # Moderate-size independent objects first; don't over-penalize larger ramps/rails.
    extreme=max(0,md-1200)/100.0 + max(0,4-md)*10
    complexity=max(0,tri-12000)/2000.0
    return (extreme+complexity,idx)

selected=[]
shortfalls={}
for cat,q in QUOTAS.items():
    pool=[(i,r) for i,r in enumerate(COV["records"]) if r["spawn_category"]==cat and r["has_existing_form"]]
    pool.sort(key=lambda x:quality(x[1],x[0]))
    take=[r for _,r in pool[:q]]
    if len(take)<q:shortfalls[cat]=q-len(take)
    for r in take:
        form=r["existing_forms"][0]
        selected.append({
            "source":"Fallout New Vegas",
            "menu_category":cat,
            "source_path":r["path"],
            "runtime_mesh_path":r["path"].replace("meshes/","",1).replace("/","\\"),
            "dimensions":r.get("dimensions"),
            "triangles":r.get("triangles"),
            "form_plugin":form["plugin"],
            "form_signature":form["signature"],
            "formid_file":form["formid"],
            "edid":form.get("edid"),
            "full":form.get("full"),
            "validation_state":"static_clean_existing_form_runtime_pending",
        })
if shortfalls:
    raise SystemExit(f"quota shortfall: {shortfalls}")

# Replacement suggestions for missing-form FNV entries used in the earlier 170-item handoff.
def dim_distance(a,b):
    if not a or not b:return 9999.0
    aa=sorted(max(float(x),0.01) for x in a)
    bb=sorted(max(float(x),0.01) for x in b)
    return sum(abs(math.log(x)-math.log(y)) for x,y in zip(aa,bb))

new_by_cat=collections.defaultdict(list)
for r in selected:new_by_cat[r["menu_category"]].append(r)
replacements=[]
for old in OLD["records"]:
    if old["source"]!="Fallout New Vegas" or old["has_existing_form"]:
        continue
    candidates=new_by_cat.get(old["menu_category"],[])
    ranked=sorted(candidates,key=lambda x:dim_distance(old.get("dimensions"),x.get("dimensions")))
    best=ranked[0] if ranked else None
    p=old["source_path"].lower()
    if "/scol/" in p:
        reason="SCOL/static-collection candidate has no ready base form; prefer an existing-form standalone object."
    elif "/architecture/" in p or "/dlc03/" in p:
        reason="Architecture/kit-piece candidate has no ready base form; avoid creating an arbitrary standalone record."
    else:
        reason="No existing base form in installed runtime; compact-menu policy prefers an existing-form substitute."
    replacements.append({
        "removed_path":old["source_path"],
        "category":old["menu_category"],
        "reason":reason,
        "suggested_replacement":best,
        "dimension_distance":dim_distance(old.get("dimensions"),best.get("dimensions")) if best else None
    })

result={
    "purpose":"170-item FNV ready subset using only statically-clean models that already have real Fallout base forms.",
    "count":len(selected),
    "quotas":QUOTAS,
    "shortfalls":shortfalls,
    "records":selected,
    "policy":[
        "Do not create custom forms for the 17 missing-form FNV entries from the earlier ready handoff.",
        "Prefer existing Fallout records to preserve native behavior and avoid arbitrary form definitions.",
        "Missing-form SCOL/architecture/kit candidates remain searchable research assets but are removed from the default ready set."
    ]
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
REPL.write_text(json.dumps({
    "previous_missing_count":len(replacements),
    "replacements":replacements
},indent=2),encoding="utf-8")
print(json.dumps({
    "ready_count":len(selected),
    "category_counts":dict(collections.Counter(r["menu_category"] for r in selected)),
    "previous_missing_replacements":len(replacements)
},indent=2))