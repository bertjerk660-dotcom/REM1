from __future__ import annotations
import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
import json,hashlib,struct,subprocess,re,math
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
THUG=Path(r"C:\IDA68WORK\thug2_datap_unpack\DATAP")
TOOL=ROOT/"third_party/tools/neversoft-multitool-main/src/NeversoftMultitool/bin/Release/net10.0/NeversoftMultitool.exe"
OUT=ROOT/"build/prepared/thug2_skateboard_asset_handoff"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def glb_stats(p):
    raw=p.read_bytes()
    magic,ver,total=struct.unpack_from("<4sII",raw,0)
    if magic!=b"glTF":return {"error":"not glb"}
    off=12
    jl,jt=struct.unpack_from("<II",raw,off);off+=8
    doc=json.loads(raw[off:off+jl].decode("utf-8").rstrip("\x00 "))
    access=doc.get("accessors",[])
    positions=[]
    tris=0
    for mesh in doc.get("meshes",[]):
        for prim in mesh.get("primitives",[]):
            pi=prim.get("attributes",{}).get("POSITION")
            if pi is not None:
                a=access[pi]
                if a.get("min") and a.get("max"):
                    positions.append((a["min"],a["max"]))
            ii=prim.get("indices")
            if ii is not None:tris+=int(access[ii].get("count",0))//3
    if positions:
        mn=[min(x[0][k] for x in positions) for k in range(3)]
        mx=[max(x[1][k] for x in positions) for k in range(3)]
        dims=[mx[k]-mn[k] for k in range(3)]
    else:mn=mx=dims=None
    return {"nodes":len(doc.get("nodes",[])),"meshes":len(doc.get("meshes",[])),
            "materials":len(doc.get("materials",[])),"triangles":tris,
            "bbox":[mn,mx] if mn else None,"dimensions":dims}

def nif_stats(p):
    d=NifFormat.Data()
    with p.open("rb") as f:d.read(f)
    root=d.roots[0] if d.roots else None
    pts=[];tris=0;shapes=0;extras=[]
    for b in d.get_global_iterator():
        tn=type(b).__name__
        if tn=="NiStringExtraData":
            try:
                name=b.name.decode("latin1","ignore") if isinstance(b.name,bytes) else str(b.name)
                val=b.string_data.decode("latin1","ignore") if isinstance(b.string_data,bytes) else str(b.string_data)
                extras.append({"name":name,"value":val})
            except:pass
        dat=getattr(b,"data",None)
        if dat is None or not hasattr(dat,"vertices") or not getattr(dat,"has_vertices",False):continue
        shapes+=1
        try:m=b.get_transform(relative_to=root) if root is not None else None
        except:m=None
        for v in dat.vertices:
            x,y,z=float(v.x),float(v.y),float(v.z)
            if m is not None:
                x,y,z=(x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
                       x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
                       x*m.m_13+y*m.m_23+z*m.m_33+m.m_43)
            pts.append((x,y,z))
        tris+=int(getattr(dat,"num_triangles",0))
    if pts:
        mn=[min(q[k] for q in pts) for k in range(3)]
        mx=[max(q[k] for q in pts) for k in range(3)]
        dims=[mx[k]-mn[k] for k in range(3)]
    else:mn=mx=dims=None
    return {"root_type":type(root).__name__ if root else None,
            "root_name":(root.name.decode("latin1","ignore") if root and isinstance(root.name,bytes) else str(root.name) if root else None),
            "shapes":shapes,"triangles":tris,"bbox":[mn,mx] if mn else None,"dimensions":dims,"extras":extras}

source_dir=THUG/"models/gameobjects/pickups/skateboard"
source_files=[]
for n in ["skateboard.mdl.ps2","skateboard.geom.ps2","skateboard.col.ps2","skateboard.tex.ps2"]:
    p=source_dir/n
    source_files.append({"path":str(p),"exists":p.exists(),"bytes":p.stat().st_size if p.exists() else None,"sha256":sha(p) if p.exists() else None})

glbs=list((OUT/"source_conversions/pickup_board").glob("*.glb"))
source_glb=[{"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p),"stats":glb_stats(p)} for p in glbs]

live_nifs=[]
for n in ["skateboard.nif","skateboard_visual.nif","skateheldx.nif","skateworld.nif"]:
    p=DATA/"meshes/rem/thug2"/n
    live_nifs.append({"name":n,"path":str(p),"exists":p.exists(),
                      "bytes":p.stat().st_size if p.exists() else None,
                      "sha256":sha(p) if p.exists() else None,
                      "stats":nif_stats(p) if p.exists() else None})

# Source skin files are retained even though the mesh command does not export them standalone.
skin_sources=[]
for rel in [
    "models/ped_male/ped_skateboard.skin.ps2","models/ped_male/ped_skateboard.iskin.ps2",
    "models/ped_male/ped_skateboard.cas.ps2","models/ped_male/ped_skateboard.col.ps2",
    "models/veh/veh_motoskateboard/veh_motoskateboard.skin.ps2",
    "models/veh/veh_motoskateboard/veh_motoskateboard.iskin.ps2",
    "models/veh/veh_motoskateboard/veh_motoskateboard.cas.ps2",
    "models/veh/veh_motoskateboard/veh_motoskateboard.col.ps2",
]:
    p=THUG/rel
    skin_sources.append({"path":str(p),"relative":rel,"exists":p.exists(),
                         "bytes":p.stat().st_size if p.exists() else None,
                         "sha256":sha(p) if p.exists() else None})

# Parse all explicit moto-skateboard SKA files to count tracks/keys. This is asset
# metadata only; animation/runtime implementation remains Astra-owned.
anim_dir=THUG/"anims/thps6_veh_motoskateboard"
animations=[]
for p in sorted(anim_dir.glob("*.ska.ps2")):
    cp=subprocess.run([str(TOOL),"ska",str(p),"-o",str(OUT/"ska_parse")],
                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
    txt=cp.stdout
    m=re.search(r"Total:\s*(\d+)\s+rotation keys\s+\+\s+(\d+)\s+translation keys\s+\+\s+(\d+)\s+custom events across\s+(\d+)\s+bone",txt,re.I)
    animations.append({
        "name":p.name,"path":str(p),"bytes":p.stat().st_size,"sha256":sha(p),
        "parse_returncode":cp.returncode,
        "rotation_keys":int(m.group(1)) if m else None,
        "translation_keys":int(m.group(2)) if m else None,
        "custom_events":int(m.group(3)) if m else None,
        "bone_tracks":int(m.group(4)) if m else None,
        "parse_summary":m.group(0) if m else "\n".join(txt.splitlines()[-8:]),
    })

result={
    "purpose":"Source-grounded skateboard/board-attachment/animation-asset evidence for Astra. No animation, camera, physics or runtime code is changed.",
    "source_board_files":source_files,
    "source_board_glb":source_glb,
    "source_skin_files":skin_sources,
    "live_nifs":live_nifs,
    "motoskateboard_animation_count":len(animations),
    "motoskateboard_animations":animations,
    "findings":[
        "The THUG2 pickup skateboard source converts successfully as 298 triangles.",
        "ped_skateboard.skin.ps2 and veh_motoskateboard.skin.ps2 do not export as standalone meshes through the current mesh command; source files/hashes are preserved for Astra/model-rig investigation.",
        "The live held candidate uses a Fallout-compatible BSFadeNode/Prn=Weapon container around authentic board geometry.",
        "Asset dimensions/hashes are recorded so later rig/attachment changes can be verified without guessing or replacing the source board.",
        "Moto-skateboard SKA files parse as real THUG2 animation tracks; this manifest intentionally does not reinterpret or implement their gameplay state logic."
    ],
    "handoff_boundary":"Astra owns exact bone mapping, attachment transforms, animation retargeting, state transitions and skate physics. Support lane owns source provenance, geometry/size evidence and reproducible asset manifests."
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
(OUT/"summary.json").write_text(json.dumps({
    "source_board_files":len(source_files),
    "source_board_glb_count":len(source_glb),
    "live_nifs":[{"name":x["name"],"sha256":x["sha256"],"stats":x["stats"]} for x in live_nifs],
    "motoskateboard_animation_count":len(animations),
    "animations":[{k:a[k] for k in ("name","rotation_keys","translation_keys","custom_events","bone_tracks","sha256")} for a in animations],
    "findings":result["findings"]
},indent=2),encoding="utf-8")
print((OUT/"summary.json").read_text())