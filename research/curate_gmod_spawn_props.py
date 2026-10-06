import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
import hashlib, json, math, re
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
REG=ROOT/"research/gmod_converted_registry.json"
OUTDIR=ROOT/"build/prepared/gmod_prop_menu_curated"
OUTDIR.mkdir(parents=True,exist_ok=True)

registry=json.loads(REG.read_text(encoding="utf-8"))

SPECS=[
    ("Skate - Rails Fences Barriers",15,("rail","fence","barrier","barricade")),
    ("Skate - Benches Tables",15,("bench","table","counter")),
    ("Skate - Planks Ladders Beams",15,("plank","ladder","ibeam","beam","ramp","slide")),
    ("Physics - Crates Boxes Pallets",18,("crate","box","pallet")),
    ("Physics - Barrels Canisters",12,("barrel","drum","canister","propane")),
    ("Street - Signs Cones Trash Carts",15,("sign","cone","trash","dumpster","cart","bollard")),
    ("Environment - Furniture",20,("chair","couch","sofa","desk","locker","shelf","cabinet","dresser")),
    ("Fun - Playground Misc",10,("playground","swingset","carousel","teeter","basket","tire")),
]
TARGET=sum(x[1] for x in SPECS)

REJECT=(
    "/gibs/","/gib","_gib","damage","damaged","chunk","shard","debris","broken",
    "player/","models/weapons/","hostage","ragdoll","explosive","wrecked",
    "door_wheel","windowbreak","bodygroup","lod","_p0","_p1","_p2","_p3","_p4",
    "boxcar","props/de_nuke/ibeams_","cluster",
)

def norm(s):return s.replace("\\","/").lower()

def valid_record(model,rec):
    p=norm(model)
    if rec.get("status")!="ok" or not rec.get("has_collision"):return False
    if any(x in p for x in REJECT):return False
    out=Path(rec.get("output_nif") or rec.get("output") or "")
    if not out.exists():return False
    return True

def bounds(p:Path):
    d=NifFormat.Data()
    with p.open("rb") as f:d.read(f)
    root=d.roots[0] if d.roots else None
    pts=[]
    for b in d.get_global_iterator():
        dat=getattr(b,"data",None)
        if dat is None or not hasattr(dat,"vertices") or not getattr(dat,"has_vertices",False):continue
        try:m=b.get_transform(relative_to=root) if root is not None else None
        except Exception:m=None
        for v in dat.vertices:
            x,y,z=float(v.x),float(v.y),float(v.z)
            if m is not None:
                # PyFFI row-vector matrix
                x,y,z=(x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
                       x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
                       x*m.m_13+y*m.m_23+z*m.m_33+m.m_43)
            pts.append((x,y,z))
    if not pts:return None
    mins=[min(q[k] for q in pts) for k in range(3)]
    maxs=[max(q[k] for q in pts) for k in range(3)]
    dims=[maxs[k]-mins[k] for k in range(3)]
    return dims

def score(model,rec,tags,dims):
    p=norm(model); name=Path(p).name
    s=0
    for tag in tags:
        if tag in name:s-=20
        elif tag in p:s-=5
    for fav in ("props_c17","props_junk","props_wasteland","props_trainstation","props_interiors","props_urban"):
        if fav in p:s-=3
    if "static" in p:s+=5
    if rec.get("mass",0)>0:s-=4
    md=max(dims) if dims else 99999
    # Prefer practical prop scale; skating pieces can be larger.
    if md<8:s+=30
    elif md>1500:s+=30
    elif md>800:s+=10
    return (s,len(p),p)

# Cache bounds only for plausible keyword candidates to keep this pass cheap.
candidate_models=set()
for model,rec in registry.items():
    if not valid_record(model,rec):continue
    low=norm(model)
    if any(tag in low for _,_,tags in SPECS for tag in tags):
        candidate_models.add(model)

bboxes={}
errors={}
for i,model in enumerate(sorted(candidate_models),1):
    rec=registry[model]
    try:bboxes[model]=bounds(Path(rec.get("output_nif") or rec.get("output")))
    except Exception as exc:errors[model]=repr(exc)
    if i%100==0:print(f"bounds {i}/{len(candidate_models)}",flush=True)

chosen=[]
used=set()
category_paths={}
shortfalls={}
for cat,quota,tags in SPECS:
    pool=[]
    for model in candidate_models:
        if model in used:continue
        p=norm(model)
        if not any(tag in p for tag in tags):continue
        dims=bboxes.get(model)
        if not dims:continue
        md=max(dims)
        per_category_max={
            "Skate - Rails Fences Barriers":650,
            "Skate - Benches Tables":400,
            "Skate - Planks Ladders Beams":350,
            "Physics - Crates Boxes Pallets":250,
            "Physics - Barrels Canisters":180,
            "Street - Signs Cones Trash Carts":300,
            "Environment - Furniture":300,
            "Fun - Playground Misc":300,
        }.get(cat,1000)
        if md>per_category_max or md<5:continue
        pool.append((model,registry[model],dims))
    pool.sort(key=lambda x:score(x[0],x[1],tags,x[2]))
    take=pool[:quota]
    category_paths[cat]=[]
    for model,rec,dims in take:
        used.add(model)
        mats=rec.get("materials",[])
        material_ok=all((not m.get("base")) or Path(m["base"]).exists() for m in mats)
        item={
            "category":cat,
            "source_model":model,
            "output_nif":rec.get("output_nif") or rec.get("output"),
            "output_nif_relative":str(Path(rec.get("output_nif") or rec.get("output")).relative_to(Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data"))).replace("\\","/"),
            "mass":rec.get("mass"),
            "havok_material":rec.get("havok_material"),
            "source_surfaceprop":rec.get("source_surfaceprop"),
            "dimensions":dims,
            "materials":mats,
            "materials_resolve":material_ok,
        }
        chosen.append(item);category_paths[cat].append(model)
    if len(take)<quota:shortfalls[cat]=quota-len(take)

# Keep the curated list category-pure. If a quota cannot be filled, report it
# rather than backfilling with unrelated models.
category_counts={}
for x in chosen:category_counts[x["category"]]=category_counts.get(x["category"],0)+1
result={
    "purpose":"Compact curated GMod/Source prop library for later use by the real GMod Q menu port; no runtime menu integration performed.",
    "registry_entries":len(registry),
    "target":TARGET,
    "selected":len(chosen),
    "category_counts":category_counts,
    "shortfalls_before_backfill":shortfalls,
    "bounds_parse_errors":errors,
    "materials_unresolved":[x["source_model"] for x in chosen if not x["materials_resolve"]],
    "records":chosen,
    "selection_rules":[
        "Only previously converted registry entries with status=ok, collision and existing output NIFs.",
        "Favor practical environment/skate/physics props; exclude obvious gibs, damage fragments, player/weapon models and wreckage.",
        "Reject extreme static bounds for this initial menu set.",
        "Source model identity and converted NIF/material provenance are retained for every item."
    ],
    "playtest":"not_run"
}
(OUTDIR/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("registry_entries","target","selected","category_counts","shortfalls_before_backfill","materials_unresolved")},indent=2))