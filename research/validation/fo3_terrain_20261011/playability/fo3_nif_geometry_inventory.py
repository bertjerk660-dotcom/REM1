import time, pathlib,collections,json,inspect
time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
work=pathlib.Path(r"D:\REM_Dream_validation_20261011")
manifest=json.loads((work/"fo3_bsa_model_extract.json").read_text())
rows=[]
for entry in manifest["extracted"]:
 p=pathlib.Path(entry["local_file"]);d=NifFormat.Data()
 try:
  with p.open("rb") as f:d.read(f)
  cls=collections.Counter(type(b).__name__ for b in d.blocks)
  geom=[];collision=[]
  for b in d.blocks:
   typ=type(b).__name__
   if typ in ("NiTriShape","NiTriStrips"):
    g=b.data
    try:tris=list(g.get_triangles()) if hasattr(g,"get_triangles") else [tuple((int(t.v_1),int(t.v_2),int(t.v_3))) for t in g.triangles]
    except Exception as e:tris=[];print("TRIERR",p.name,str(e))
    geom.append(dict(type=typ,vertices=g.num_vertices if g else 0,triangles=len(tris),name=str(b.name)))
   if typ=="hkPackedNiTriStripsData":collision.append(dict(vertices=b.num_vertices,triangles=b.num_triangles))
  rows.append(dict(model=entry["path"],file_bytes=entry["bytes"],root_count=len(d.roots),block_count=len(d.blocks),visual=geom,collision=collision))
 except Exception as e:rows.append(dict(model=entry["path"],error=str(e)))
stat=dict(models=len(rows),parsed=sum("error" not in r for r in rows),has_render_mesh=sum(bool(r.get("visual")) for r in rows),has_havok=sum(bool(r.get("collision")) for r in rows),visual_triangles=sum(sum(g["triangles"] for g in r.get("visual",[])) for r in rows),havok_triangles=sum(sum(g["triangles"] for g in r.get("collision",[])) for r in rows),problems=[r for r in rows if "error" in r or not r.get("visual")])
(work/"fo3_nif_geometry_inventory.json").write_text(json.dumps(dict(summary=stat,models=rows),indent=2))
print(json.dumps(stat,indent=2))
print("EXAMPLES",json.dumps(rows[:8],indent=2)[:9000])
print("get_transform signature",inspect.signature(NifFormat.NiAVObject.get_transform))
