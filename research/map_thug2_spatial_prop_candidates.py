from pathlib import Path
import json,struct,re,math
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/thug2_prop_catalog"
HAND=json.loads((BASE/"embedded_prop_handoff/manifest.json").read_text())
OUT=BASE/"spatial_prop_candidates"
OUT.mkdir(parents=True,exist_ok=True)

def read_doc(p):
    b=p.read_bytes(); o=12
    jl,jt=struct.unpack_from("<II",b,o); o+=8
    return json.loads(b[o:o+jl].decode("utf-8").rstrip("\x00 "))

def pose(t):
    ident=t["identifier"]
    for f in t.get("files",[]):
        p=BASE/"qb_decompiled"/f
        if not p.exists(): continue
        lines=p.read_text(encoding="utf-8",errors="ignore").splitlines()
        for i,line in enumerate(lines):
            if re.search(r'^\s*Name\s*=\s*'+re.escape(ident)+r'\s*$',line,re.I):
                for j in range(i-1,max(-1,i-16),-1):
                    m=re.search(r'Pos\s*=\s*\(([-+0-9.eE]+),\s*([-+0-9.eE]+),\s*([-+0-9.eE]+)\)',lines[j],re.I)
                    if m:
                        return [float(m.group(k)) for k in (1,2,3)]
        for i,line in enumerate(lines):
            if ident.lower() in line.lower():
                for j in range(i-1,max(-1,i-24),-1):
                    m=re.search(r'Pos\s*=\s*\(([-+0-9.eE]+),\s*([-+0-9.eE]+),\s*([-+0-9.eE]+)\)',lines[j],re.I)
                    if m:
                        return [float(m.group(k)) for k in (1,2,3)]
    return None

def dist_point_box(p,mn,mx):
    return math.sqrt(sum((mn[k]-p[k])**2 if p[k]<mn[k] else (p[k]-mx[k])**2 if p[k]>mx[k] else 0 for k in range(3)))

def radius(cat):
    c=cat.lower()
    if "ramp" in c or "halfpipe" in c or "quarterpipe" in c:return 650
    if "rail" in c:return 350
    if "ledge" in c or "curb" in c:return 400
    if "bench" in c or "table" in c or "chair" in c:return 350
    if "fence" in c or "barrier" in c or "pipe" in c:return 450
    if "stair" in c or "platform" in c:return 550
    return 400

records=[]
for lr in HAND["levels"]:
    level=lr["level"]
    b=json.loads((BASE/f"embedded_prop_handoff/{level}/targets.json").read_text())
    glb=ROOT/Path(b["whole_level_glbs"][0])
    doc=read_doc(glb)
    leaves=[]
    for ni,n in enumerate(doc.get("nodes",[])):
        mi=n.get("mesh")
        if mi is None: continue
        mins=[1e30]*3; maxs=[-1e30]*3; tri=0; ok=False
        for pr in doc["meshes"][mi].get("primitives",[]):
            ai=pr.get("attributes",{}).get("POSITION")
            if ai is None: continue
            a=doc["accessors"][ai]
            if "min" not in a or "max" not in a: continue
            ok=True
            for k in range(3):
                mins[k]=min(mins[k],a["min"][k]); maxs[k]=max(maxs[k],a["max"][k])
            if "indices" in pr: tri+=doc["accessors"][pr["indices"]].get("count",0)//3
        if ok:
            leaves.append({"node":ni,"mesh":mi,"min":mins,"max":maxs,"triangles":tri,
                           "max_dim":max(maxs[k]-mins[k] for k in range(3))})
    for t in b["targets"]:
        p=pose(t)
        row={"level":level,"identifier":t["identifier"],"category":t["category"],"pos":p}
        if not p:
            row["status"]="no_position"; records.append(row); continue
        rad=radius(t["category"])
        cand=[]
        for x in leaves:
            if x["max_dim"]>5000: continue
            bd=dist_point_box(p,x["min"],x["max"])
            if bd<=rad:
                cand.append((bd,x))
        cand.sort(key=lambda z:(z[0],z[1]["max_dim"],z[1]["node"]))
        cand=cand[:18] or sorted([(dist_point_box(p,x["min"],x["max"]),x) for x in leaves if x["max_dim"]<=5000],key=lambda z:z[0])[:1]
        row.update({"status":"mapped","radius":rad,"candidate_leaves":[dict(x,box_distance=round(d,3)) for d,x in cand]})
        records.append(row)

res={"purpose":"Spatial mapping of 106 THUG2 named environment targets to converted level GLB leaf candidates using original QB positions.",
     "targets":len(records),"mapped":sum(r["status"]=="mapped" for r in records),"no_position":sum(r["status"]=="no_position" for r in records),
     "records":records,
     "note":"Candidate leaves are not yet promoted standalone props; each requires geometry sanity review before conversion."}
(OUT/"mapping.json").write_text(json.dumps(res,indent=2))
print(json.dumps({k:res[k] for k in ("targets","mapped","no_position")},indent=2))
