import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
import json, collections
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=ROOT/"build/prepared/fnv_prop_catalog_curated/static_audit.json"
OUT=ROOT/"build/prepared/fnv_prop_catalog_curated/havok_motion_audit.json"
m=json.loads(SRC.read_text())
rows=[]
counts=collections.Counter()
cats={}
for i,r in enumerate(m["records"],1):
    if not r.get("parse_ok") or not r.get("has_collision"):
        continue
    p=Path(r["staged_path"])
    d=NifFormat.Data()
    with p.open("rb") as f:d.read(f)
    bodies=[]
    for b in d.get_global_iterator():
        if type(b).__name__ in ("bhkRigidBody","bhkRigidBodyT"):
            x={
                "type":type(b).__name__,
                "motion_system":int(getattr(b,"motion_system",-1)),
                "quality_type":int(getattr(b,"quality_type",-1)),
                "mass":float(getattr(b,"mass",0.0)),
                "friction":float(getattr(b,"friction",0.0)),
                "restitution":float(getattr(b,"restitution",0.0)),
            }
            bodies.append(x)
            counts[(x["motion_system"],x["quality_type"],round(x["mass"],3))]+=1
    dynamic=any(b["mass"]>0.001 for b in bodies)
    # Some Bethesda fixed/statics report zero mass. For support planning, mass>0 is
    # a conservative signal that an asset was authored for movable rigid-body behavior.
    item={
        "path":r["path"],"spawn_category":r["spawn_category"],
        "bodies":bodies,"authored_movable":dynamic,
        "dimensions":r.get("dimensions"),"static_candidate_ok":r.get("static_candidate_ok")
    }
    rows.append(item)
    c=cats.setdefault(r["spawn_category"],{"collision_props":0,"authored_movable":0,"fixed_or_zero_mass":0})
    c["collision_props"]+=1
    if dynamic:c["authored_movable"]+=1
    else:c["fixed_or_zero_mass"]+=1
    if i%50==0: print(i,flush=True)
result={
    "purpose":"Conservative Havok authored-mobility audit for curated FNV props. mass>0 is treated as movable-authoring evidence; zero mass does not prove the runtime cannot wrap/spawn it dynamically.",
    "body_signature_counts":[{"motion_system":k[0],"quality_type":k[1],"mass":k[2],"count":v} for k,v in counts.most_common()],
    "category_summary":cats,
    "authored_movable_count":sum(1 for x in rows if x["authored_movable"]),
    "collision_props":len(rows),
    "records":rows,
    "notes":[
        "Skate obstacles can be useful even when authored as fixed/static collision.",
        "Physgun parity should not assume a native FNV static NIF is directly movable; Astra/runtime integration may need dynamic wrappers or separately authored physics forms.",
        "This audit does not modify any NIF."
    ]
}
OUT.write_text(json.dumps(result,indent=2))
print(json.dumps({k:result[k] for k in ("collision_props","authored_movable_count","body_signature_counts","category_summary")},indent=2))