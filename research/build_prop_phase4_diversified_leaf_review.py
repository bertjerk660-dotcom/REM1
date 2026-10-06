from __future__ import annotations
from pathlib import Path
import json,struct,math,re,hashlib
from PIL import Image,ImageDraw

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
P3=ROOT/"build/prepared/prop_support_phase3/thug2_promotion_queue.json"
BASE=ROOT/"build/prepared/thug2_prop_catalog"
OUT=ROOT/"build/prepared/prop_support_phase4"
PRE=OUT/"diversified_leaf_previews"
PRE.mkdir(parents=True,exist_ok=True)

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def read_glb(p:Path):
    raw=p.read_bytes()
    magic,ver,total=struct.unpack_from("<4sII",raw,0)
    if magic!=b"glTF" or ver!=2: raise ValueError(f"not glTF2: {p}")
    off=12
    jl,jt=struct.unpack_from("<II",raw,off); off+=8
    if jt!=0x4E4F534A: raise ValueError("missing JSON chunk")
    doc=json.loads(raw[off:off+jl].decode("utf-8").rstrip("\x00 ")); off+=jl
    if off+8>len(raw): return doc,b""
    bl,bt=struct.unpack_from("<II",raw,off); off+=8
    if bt!=0x004E4942: raise ValueError("missing BIN chunk")
    return doc,raw[off:off+bl]

COMP_FMT={5120:"b",5121:"B",5122:"h",5123:"H",5125:"I",5126:"f"}
COMP_SIZE={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}
TYPE_N={"SCALAR":1,"VEC2":2,"VEC3":3,"VEC4":4,"MAT2":4,"MAT3":9,"MAT4":16}

def accessor_values(doc,binchunk,idx):
    a=doc["accessors"][idx]
    bv=doc["bufferViews"][a["bufferView"]]
    ct=a["componentType"]; ncomp=TYPE_N[a["type"]]; count=a["count"]
    csize=COMP_SIZE[ct]; fmt="<"+COMP_FMT[ct]*ncomp
    stride=bv.get("byteStride",csize*ncomp)
    start=bv.get("byteOffset",0)+a.get("byteOffset",0)
    out=[]
    for i in range(count):
        pos=start+i*stride
        out.append(struct.unpack_from(fmt,binchunk,pos))
    return out

def node_matrix(node):
    # glTF column-major 4x4 or TRS. Geometry from current converter is generally
    # already in level coordinates, but honor node transforms when present.
    if "matrix" in node and len(node["matrix"])==16:
        return node["matrix"]
    t=node.get("translation",[0,0,0]); s=node.get("scale",[1,1,1]); q=node.get("rotation",[0,0,0,1])
    x,y,z,w=q
    xx,yy,zz=x*x,y*y,z*z; xy,xz,yz=x*y,x*z,y*z; wx,wy,wz=w*x,w*y,w*z
    r=[
      1-2*(yy+zz),2*(xy+wz),2*(xz-wy),0,
      2*(xy-wz),1-2*(xx+zz),2*(yz+wx),0,
      2*(xz+wy),2*(yz-wx),1-2*(xx+yy),0,
      0,0,0,1
    ]
    # scale columns, then translation
    r[0]*=s[0];r[1]*=s[0];r[2]*=s[0]
    r[4]*=s[1];r[5]*=s[1];r[6]*=s[1]
    r[8]*=s[2];r[9]*=s[2];r[10]*=s[2]
    r[12],r[13],r[14]=t
    return r

def xf(m,p):
    x,y,z=p
    return (
      m[0]*x+m[4]*y+m[8]*z+m[12],
      m[1]*x+m[5]*y+m[9]*z+m[13],
      m[2]*x+m[6]*y+m[10]*z+m[14],
    )

def leaf_geometry(doc,binchunk,node_idx):
    node=doc["nodes"][node_idx]
    mi=node.get("mesh")
    if mi is None:return [],[],set()
    mtx=node_matrix(node)
    verts=[]; tris=[]; mats=set()
    for prim in doc["meshes"][mi].get("primitives",[]):
        pi=prim.get("attributes",{}).get("POSITION")
        if pi is None: continue
        pv=accessor_values(doc,binchunk,pi)
        base=len(verts); verts.extend(xf(mtx,v[:3]) for v in pv)
        if "indices" in prim:
            iv=accessor_values(doc,binchunk,prim["indices"])
            flat=[int(x[0]) for x in iv]
        else:
            flat=list(range(len(pv)))
        mode=prim.get("mode",4)
        if mode==4:
            for i in range(0,len(flat)-2,3): tris.append((base+flat[i],base+flat[i+1],base+flat[i+2]))
        if "material" in prim:mats.add(int(prim["material"]))
    return verts,tris,mats

def rot(p):
    x,y,z=p; yaw=math.radians(35); pitch=math.radians(25)
    cy,sy=math.cos(yaw),math.sin(yaw); cp,sp=math.cos(pitch),math.sin(pitch)
    x1=cy*x-sy*y; y1=sy*x+cy*y; z1=z
    return (x1,cp*y1-sp*z1,sp*y1+cp*z1)

def draw_geom(geoms,out,size=(960,320)):
    im=Image.new("RGBA",size,(24,24,24,255))
    dr=ImageDraw.Draw(im,"RGBA")
    panel_w=size[0]//max(1,len(geoms))
    for gi,g in enumerate(geoms):
        verts,tris,label=g
        x0=gi*panel_w
        dr.rectangle((x0,0,x0+panel_w-1,size[1]-1),outline=(80,80,80,255))
        if not verts:
            dr.text((x0+10,10),label+" NO GEOMETRY",fill=(255,180,180,255));continue
        mn=[min(v[k] for v in verts) for k in range(3)]; mx=[max(v[k] for v in verts) for k in range(3)]
        c=[(mn[k]+mx[k])*0.5 for k in range(3)]
        rv=[rot((v[0]-c[0],v[1]-c[1],v[2]-c[2])) for v in verts]
        xs=[p[0] for p in rv]; ys=[p[1] for p in rv]
        w=max(xs)-min(xs);h=max(ys)-min(ys);scale=min((panel_w-20)/max(w,1e-6),(size[1]-55)/max(h,1e-6))
        sx=x0+panel_w/2-(min(xs)+max(xs))*0.5*scale
        sy=(size[1]+20)/2+(min(ys)+max(ys))*0.5*scale
        pts=[(p[0]*scale+sx,sy-p[1]*scale,p[2]) for p in rv]
        faces=[]
        step=max(1,math.ceil(len(tris)/6000))
        for a,b,cx in tris[::step]:
            if a>=len(pts) or b>=len(pts) or cx>=len(pts):continue
            z=(pts[a][2]+pts[b][2]+pts[cx][2])/3
            faces.append((z,(pts[a][:2],pts[b][:2],pts[cx][:2])))
        faces.sort(key=lambda x:x[0])
        for _,poly in faces: dr.polygon(poly,fill=(150,150,150,230))
        dr.text((x0+8,8),label,fill=(245,245,245,255))
        dr.text((x0+8,size[1]-32),f"{len(verts)}v {len(tris)}t",fill=(220,220,220,255))
    im.save(out,optimize=True)

def dims(verts):
    if not verts:return None
    mn=[min(v[k] for v in verts) for k in range(3)];mx=[max(v[k] for v in verts) for k in range(3)]
    return [mx[k]-mn[k] for k in range(3)],mn,mx

allq=json.loads(P3.read_text(encoding="utf-8"))
wave=json.loads((OUT/"thug2_diversified_first_wave.json").read_text(encoding="utf-8"))
queue={"top20":wave["records"],"records":allq["records"]}
records=[]
for rank,t in enumerate(queue["top20"],1):
    level=t["level"]; ident=t["identifier"]
    bundle=json.loads((BASE/f"embedded_prop_handoff/{level}/targets.json").read_text(encoding="utf-8"))
    if not bundle.get("whole_level_glbs"):
        records.append({"rank":rank,**t,"status":"missing_level_glb"});continue
    glb=ROOT/Path(bundle["whole_level_glbs"][0])
    doc,binchunk=read_glb(glb)
    sp=next((x for x in queue["records"] if x["level"]==level and x["identifier"]==ident),t)
    leaves=[]
    for cand in (json.loads((BASE/"spatial_prop_candidates/mapping.json").read_text())["records"]):
        if cand["level"]==level and cand["identifier"]==ident:
            leaves=cand.get("candidate_leaves",[]);break
    leaf_rows=[]; render=[]
    for ci,cand in enumerate(leaves[:3],1):
        ni=cand["node"]; vv,tt,mm=leaf_geometry(doc,binchunk,ni)
        dd=dims(vv)
        leaf_rows.append({
          "candidate_rank":ci,"node":ni,"mesh":cand.get("mesh"),
          "box_distance":cand.get("box_distance"),"vertices":len(vv),"triangles":len(tt),
          "material_count":len(mm),"dimensions":dd[0] if dd else None,
          "bbox_min":dd[1] if dd else None,"bbox_max":dd[2] if dd else None
        })
        render.append((vv,tt,f"#{ci} node {ni}"))
    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",f"{rank:02d}_{level}_{ident}")[:110]
    png=PRE/(safe+".png")
    draw_geom(render,png)
    # isolation heuristic only; human visual confirmation still required
    first=leaf_rows[0] if leaf_rows else {}
    maxd=max(first.get("dimensions") or [0])
    isolate_score=0
    if first:
        isolate_score+=3 if (first.get("box_distance") or 0)==0 else 2 if (first.get("box_distance") or 999)<=25 else 1
        isolate_score+=3 if len(leaves)<=5 else 2 if len(leaves)<=10 else 1
        isolate_score+=2 if 5<=maxd<=1200 else 0
        isolate_score+=1 if first.get("triangles",0)<=20000 else 0
    status="high_review_priority" if isolate_score>=7 else "medium_review_priority" if isolate_score>=5 else "complex_review"
    records.append({
      "rank":rank,"level":level,"identifier":ident,"category":t["category"],
      "source_position":t.get("position"),"phase3_score":t.get("promotion_review_score"),
      "source_glb":str(glb.relative_to(ROOT)).replace("\\","/"),
      "source_glb_sha256":sha(glb),"candidate_leaf_count":len(leaves),
      "leaf_metrics":leaf_rows,"isolation_score":isolate_score,
      "review_status":status,
      "preview":str(png.relative_to(ROOT)).replace("\\","/"),
      "preview_sha256":sha(png),
      "promotion_state":"not_promoted_visual_confirmation_required"
    })
result={
 "purpose":"Top-20 THUG2 prop geometry review packet with actual converted-level leaf geometry metrics and local previews. This does not promote or convert a standalone prop.",
 "count":len(records),
 "status_counts":{k:sum(r.get("review_status")==k for r in records) for k in ("high_review_priority","medium_review_priority","complex_review")},
 "records":records,
 "rule":"Preview/heuristics narrow review only. Confirm object identity/leaf isolation visually before splitting or FNV conversion."
}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"thug2_diversified_leaf_review.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"count":result["count"],"status_counts":result["status_counts"],"preview_dir":str(PRE)},indent=2))