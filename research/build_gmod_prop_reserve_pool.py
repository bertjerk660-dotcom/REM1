from pathlib import Path
import json,re,math,hashlib,time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
REG=json.loads((ROOT/"research/gmod_converted_registry.json").read_text(encoding="utf-8"))
CUR=json.loads((ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json").read_text(encoding="utf-8"))
OUT=ROOT/"build/prepared/prop_support_phase4"
OUT.mkdir(parents=True,exist_ok=True)
CURRENT={r["source_model"].replace("\\","/").lower() for r in CUR["records"]}

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def nif_dims(p:Path):
    d=NifFormat.Data()
    with p.open("rb") as f:d.read(f)
    root=d.roots[0] if d.roots else None
    pts=[]
    for b in d.get_global_iterator():
        dat=getattr(b,"data",None)
        if dat is None or not hasattr(dat,"vertices") or not getattr(dat,"has_vertices",False):continue
        try:m=b.get_transform(relative_to=root) if root else None
        except Exception:m=None
        for v in dat.vertices:
            x,y,z=float(v.x),float(v.y),float(v.z)
            if m is not None:
                x,y,z=(x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
                       x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
                       x*m.m_13+y*m.m_23+z*m.m_33+m.m_43)
            pts.append((x,y,z))
    if not pts:return None
    mn=[min(v[k] for v in pts) for k in range(3)]
    mx=[max(v[k] for v in pts) for k in range(3)]
    return [mx[k]-mn[k] for k in range(3)]

CATS=[
 ("Skate - Rails & Barriers",["rail","handrail","barrier","barricade","fence","bollard","parking_bumper"]),
 ("Skate - Benches & Tables",["bench","table","picnic","counter","desk"]),
 ("Skate - Beams Planks Ladders",["beam","plank","ladder","ibeam","scaffold","board"]),
 ("Skate - Ramps Platforms Stairs",["ramp","stair","platform","kicker","quarter","halfpipe","diving_board"]),
 ("Physics - Crates Pallets Boxes",["crate","pallet","box","container"]),
 ("Physics - Barrels Canisters Tires",["barrel","drum","canister","propane","tire","wheel"]),
 ("Street - Signs Cones Carts",["sign","cone","cart","dumpster","trashcan","garbage_can","mailbox","parking"]),
 ("Environment - Furniture Utility",["chair","couch","sofa","locker","shelf","cabinet","vending","fridge","stove","sink"]),
]

BAD=["gib","debris","chunk","damage","brokenpiece","player/","models/weapons/","hostage","zombie","door","window","tree","helicopter","vehicle","subwaycar","train_box","train_tank","building","roof","wall","arch","column","bridge","tower","terrain"]

def category(path):
    low=path.lower()
    if any(x in low for x in BAD):return None
    for cat,keys in CATS:
        if any(k in low for k in keys):return cat
    return None

def materials_ok(rec):
    for m in rec.get("materials",[]):
        for k in ("base","normal"):
            q=m.get(k)
            if q and not Path(q).exists():return False
    return True

rows=[]
errors={}
for model,rec in REG.items():
    key=model.replace("\\","/").lower()
    if key in CURRENT:continue
    if rec.get("status")!="ok" or not rec.get("has_collision"):continue
    cat=category(key)
    if not cat:continue
    p=Path(rec.get("output_nif") or rec.get("output") or "")
    if not p.exists() or not materials_ok(rec):continue
    try:dims=nif_dims(p)
    except Exception as e:
        errors[model]=repr(e);continue
    if not dims:continue
    md=max(dims); positive=[x for x in dims if x>0.01]; mn=min(positive) if positive else 0
    # Keep practical objects, not map-scale or tiny clutter.
    if md<8 or md>850:continue
    ratio=md/max(mn,0.01)
    score=0
    if cat.startswith("Skate - Rails"):score+=10
    elif cat.startswith("Skate - Ramps"):score+=10
    elif cat.startswith("Skate - Beams"):score+=9
    elif cat.startswith("Skate - Benches"):score+=8
    elif cat.startswith("Physics"):score+=6
    else:score+=4
    if 25<=md<=350:score+=5
    elif md<=600:score+=3
    if ratio<80:score+=2
    mass=rec.get("mass")
    if mass is not None and float(mass)>0:score+=2
    rows.append({
      "source_model":model,"category":cat,"score":score,"dimensions":dims,"max_dimension":md,
      "mass":mass,"havok_material":rec.get("havok_material"),"source_surfaceprop":rec.get("source_surfaceprop"),
      "output_nif":str(p),"output_nif_relative":str(p).replace(str(Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data"))+"\\","").replace("\\","/"),
      "output_nif_sha256":sha(p),"materials":rec.get("materials",[]),
      "state":"reserve_only_not_in_default_catalog"
    })

by={}
for r in rows:by.setdefault(r["category"],[]).append(r)
# 10 per category where possible => up to 80.
selected=[]
for cat,_ in CATS:
    pool=sorted(by.get(cat,[]),key=lambda r:(-r["score"],abs(r["max_dimension"]-160),r["source_model"].lower()))
    selected+=pool[:10]
selected=selected[:80]
res={
 "purpose":"Extra converted GMod/Source reserve pool for replacing failed/redundant default props without exposing the full raw registry.",
 "registry_entries":len(REG),"current_default":len(CURRENT),"eligible_after_filters":len(rows),
 "selected_reserve":len(selected),
 "category_counts":{c:sum(r["category"]==c for r in selected) for c,_ in CATS},
 "parse_errors_count":len(errors),
 "records":selected,
 "policy":[
   "Reserve entries are not added to the player-facing catalog yet.",
   "Promote only when an existing default entry fails runtime validation or when a category needs improvement.",
   "Keep the normal browser near 300-320 total entries."
 ]
}
(OUT/"gmod_reserve_pool.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({k:res[k] for k in ("registry_entries","eligible_after_filters","selected_reserve","category_counts","parse_errors_count")},indent=2))