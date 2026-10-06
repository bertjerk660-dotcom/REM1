from __future__ import annotations
import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
import json, math, hashlib, re
from PIL import Image, ImageDraw
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
HANDOFF=json.loads((ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json").read_text(encoding="utf-8"))
FNV_AUDIT=json.loads((ROOT/"build/prepared/fnv_prop_catalog_curated/static_audit.json").read_text(encoding="utf-8"))
FNV_STAGED={r["path"].replace("\\","/").lower():Path(r["staged_path"]) for r in FNV_AUDIT["records"]}
OUTDIR=ROOT/"build/prepared/final_prop_catalog_thumbnails"
PNGDIR=OUTDIR/"png"
PNGDIR.mkdir(parents=True,exist_ok=True)

SIZE=128
PAD=8
MAX_TRIS=8000

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def clean_name(i,r):
    stem=Path(r["runtime_mesh_path"].replace("\\","/")).stem
    stem=re.sub(r"[^A-Za-z0-9_.-]+","_",stem)
    src="fnv" if r["source"]=="Fallout New Vegas" else "gmod"
    return f"{i:03d}_{src}_{stem}.png"

def transform_point(m,v):
    x,y,z=v
    if m is None:return (x,y,z)
    return (
        x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
        x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
        x*m.m_13+y*m.m_23+z*m.m_33+m.m_43,
    )

def load_mesh(path:Path):
    d=NifFormat.Data()
    with path.open("rb") as f:d.read(f)
    root=d.roots[0] if d.roots else None
    verts=[]
    tris=[]
    for b in d.get_global_iterator():
        dat=getattr(b,"data",None)
        if dat is None or not hasattr(dat,"vertices") or not getattr(dat,"has_vertices",False):
            continue
        try:m=b.get_transform(relative_to=root) if root is not None else None
        except Exception:m=None
        base=len(verts)
        local=[transform_point(m,(float(v.x),float(v.y),float(v.z))) for v in dat.vertices]
        verts.extend(local)
        try:
            ts=dat.get_triangles()
        except Exception:
            ts=[]
        for t in ts:
            try:
                a,b2,c=int(t[0])+base,int(t[1])+base,int(t[2])+base
                if a!=b2 and b2!=c and a!=c:tris.append((a,b2,c))
            except Exception:pass
    return verts,tris

def rotate(p):
    x,y,z=p
    yaw=math.radians(35.0)
    pitch=math.radians(25.0)
    cy,sy=math.cos(yaw),math.sin(yaw)
    cp,sp=math.cos(pitch),math.sin(pitch)
    x1=cy*x-sy*y
    y1=sy*x+cy*y
    z1=z
    y2=cp*y1-sp*z1
    z2=sp*y1+cp*z1
    return (x1,y2,z2)

def render(path:Path,out:Path):
    verts,tris=load_mesh(path)
    if not verts or not tris:
        raise RuntimeError("no renderable triangles")
    mins=[min(v[k] for v in verts) for k in range(3)]
    maxs=[max(v[k] for v in verts) for k in range(3)]
    cen=[(mins[k]+maxs[k])*0.5 for k in range(3)]
    rv=[rotate((v[0]-cen[0],v[1]-cen[1],v[2]-cen[2])) for v in verts]
    xs=[v[0] for v in rv];ys=[v[1] for v in rv]
    w=max(xs)-min(xs);h=max(ys)-min(ys)
    scale=(SIZE-2*PAD)/max(w,h,1e-6)
    sx=(SIZE-(w*scale))*0.5-min(xs)*scale
    sy=(SIZE-(h*scale))*0.5+max(ys)*scale
    pts=[(x*scale+sx, sy-y*scale,z) for x,y,z in rv]
    if len(tris)>MAX_TRIS:
        step=max(1,math.ceil(len(tris)/MAX_TRIS))
        tris=tris[::step]
    light=(0.3,-0.4,0.85)
    faces=[]
    for a,b,c in tris:
        pa,pb,pc=rv[a],rv[b],rv[c]
        ux,uy,uz=pb[0]-pa[0],pb[1]-pa[1],pb[2]-pa[2]
        vx,vy,vz=pc[0]-pa[0],pc[1]-pa[1],pc[2]-pa[2]
        nx,ny,nz=uy*vz-uz*vy,uz*vx-ux*vz,ux*vy-uy*vx
        nl=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        dot=(nx*light[0]+ny*light[1]+nz*light[2])/nl
        shade=int(95+125*max(0.0,min(1.0,0.5+0.5*dot)))
        depth=(pa[2]+pb[2]+pc[2])/3.0
        faces.append((depth,shade,(pts[a][:2],pts[b][:2],pts[c][:2])))
    faces.sort(key=lambda x:x[0])
    im=Image.new("RGBA",(SIZE,SIZE),(0,0,0,0))
    dr=ImageDraw.Draw(im,"RGBA")
    for _z,shade,poly in faces:
        dr.polygon(poly,fill=(shade,shade,shade,245))
    # Subtle silhouette outline from alpha edge.
    alpha=im.getchannel("A")
    # Normalize thumbnail around actual occupied bbox.
    bbox=alpha.getbbox()
    if not bbox:raise RuntimeError("empty render")
    im.save(out,optimize=True)
    return {"vertices":len(verts),"triangles_total":len(load_mesh(path)[1]),"triangles_drawn":len(faces),"bbox":bbox}

records=[]
fail=[]
for i,r in enumerate(HANDOFF["ready_records"],1):
    rel=r["runtime_mesh_path"].replace("\\","/").lstrip("/")
    if r["source"]=="Fallout New Vegas":
        key=r["source_path"].replace("\\","/").lower()
        nif=FNV_STAGED.get(key, DATA/"meshes"/Path(rel))
    else:
        nif=DATA/"meshes"/Path(rel)
    name=clean_name(i,r)
    out=PNGDIR/name
    item={
        "index":i,"source":r["source"],"menu_category":r["menu_category"],
        "source_path":r["source_path"],"runtime_mesh_path":r["runtime_mesh_path"],
        "thumbnail":str(out.relative_to(ROOT)).replace("\\","/")
    }
    try:
        stats=render(nif,out)
        item.update({"status":"ok","thumbnail_sha256":sha(out),"thumbnail_bytes":out.stat().st_size,**stats})
    except Exception as exc:
        item.update({"status":"fail","error":repr(exc)})
        fail.append(item)
    records.append(item)
    if i%25==0:print(f"{i}/{len(HANDOFF['ready_records'])}",flush=True)

result={
    "purpose":"Local model-preview thumbnails rendered directly from the actual prepared NIF geometry. These are support/audit assets, not a replacement for GMod's final native SpawnIcon behavior.",
    "size":[SIZE,SIZE],"candidate_count":len(records),
    "generated":sum(r["status"]=="ok" for r in records),
    "failed":len(fail),
    "failures":fail,
    "records":records,
    "final_ui_note":"Astra's source-faithful GMod Q-menu port should preserve original SpawnIcon/model-icon behavior. These previews can be used for audit/fallback/catalog data only."
}
OUTDIR.mkdir(parents=True,exist_ok=True)
(OUTDIR/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("candidate_count","generated","failed")},indent=2))
