from pathlib import Path
import time,struct,json,hashlib,copy,io
time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
from PIL import Image
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
OUT=ROOT/"build/attachment90/package/Data"
SRC=ROOT/"build/prepared/thug2_prop_catalog/standalone_glb/models/board_default/board_default/board_default.glb"
raw=SRC.read_bytes();n=struct.unpack_from("<I",raw,12)[0];j=json.loads(raw[20:20+n]);blob=raw[28+n:]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
textures=[]
for i,img in enumerate(j["images"]):
 v=j["bufferViews"][img["bufferView"]];png=blob[v.get("byteOffset",0):v.get("byteOffset",0)+v["byteLength"]]
 im=Image.open(io.BytesIO(png)).convert("RGBA")
 rel=Path("textures/rem/thug2/board90")/("source_%d.dds"%i);dst=OUT/rel;dst.parent.mkdir(parents=True,exist_ok=True)
 im.save(dst)
 assert Image.open(dst).convert("RGBA").tobytes()==im.tobytes()
 textures.append({"path":str(rel),"sha256":sha(dst),"pixels_verified":True})
rows=[]
for name in ["skateheldx.nif","skateboard.nif","skateboard_visual.nif"]:
 src=DATA/"meshes/rem/thug2"/name;d=NifFormat.Data()
 with src.open("rb") as f:d.read(f)
 shapes=[x for x in d.get_global_iterator() if isinstance(x,NifFormat.NiTriShape)]
 assert len(shapes)==len(j["meshes"])==4
 before=[]
 for i,shape in enumerate(shapes):
  prim=j["meshes"][i]["primitives"][0];a=j["accessors"][prim["attributes"]["POSITION"]]
  assert len(shape.data.triangles)*3==j["accessors"][prim["indices"]]["count"]
  v=j["bufferViews"][a["bufferView"]];start=v.get("byteOffset",0)+a.get("byteOffset",0)
  xyz=[struct.unpack_from("<3f",blob,start+k*v.get("byteStride",12)) for k in range(a["count"])]
  # Blender splits vertices at seams. Compare positions after its Y-up -> Z-up conversion.
  source_positions={(round(x,4),round(-z,4),round(y,4)) for x,y,z in xyz}
  nif_positions={(round(v.x,4),round(v.y,4),round(v.z,4)) for v in shape.data.vertices}
  assert source_positions==nif_positions,"Source material association requires matching geometry"
  mat=j["materials"][prim["material"]];assert mat.get("alphaMode","OPAQUE")=="OPAQUE"
  imageidx=j["textures"][mat["pbrMetallicRoughness"]["baseColorTexture"]["index"]]["source"]
  for k,prop in enumerate(shape.properties):
   if isinstance(prop,NifFormat.NiMaterialProperty):
    original=prop;prop=NifFormat.NiMaterialProperty();prop.deepcopy(original);shape.properties[k]=prop
    before.append({"shape":i,"old_alpha":prop.alpha,"material":mat["name"],"image":imageidx})
    prop.name=mat["name"].encode();prop.alpha=1.0
    prop.diffuse_color.r=prop.diffuse_color.g=prop.diffuse_color.b=1.0
   if isinstance(prop,NifFormat.BSShaderPPLightingProperty):
    prop.texture_set.num_textures=6;prop.texture_set.textures.update_size()
    prop.texture_set.textures[0]=textures[imageidx]["path"].replace("/","\\").encode()
    prop.shader_flags.sf_z_buffer_test=1;prop.shader_flags_2.sf_2_z_buffer_write=1
  assert len(shape.data.uv_sets)>0
 dst=OUT/"meshes/rem/thug2"/name;dst.parent.mkdir(parents=True,exist_ok=True)
 with dst.open("wb") as f:d.write(f)
 check=NifFormat.Data()
 with dst.open("rb") as f:check.read(f)
 cs=[x for x in check.get_global_iterator() if isinstance(x,NifFormat.NiTriShape)]
 for a,b in zip(shapes,cs):
  assert [(v.x,v.y,v.z) for v in a.data.vertices]==[(v.x,v.y,v.z) for v in b.data.vertices]
  assert all(p.alpha==1 for p in b.properties if isinstance(p,NifFormat.NiMaterialProperty))
  for p in b.properties:
   if isinstance(p,NifFormat.BSShaderPPLightingProperty):assert (OUT/p.texture_set.textures[0].decode()).exists()
 rows.append({"name":name,"before_sha256":sha(src),"after_sha256":sha(dst),"materials":before,"roundtrip":"pass"})
report={"source_glb":str(SRC),"source_sha256":sha(SRC),"textures":textures,"nifs":rows,"deployed":False,"runtime_visibility":"not_tested","scope":"Opaque original board material restoration; geometry and placement unchanged"}
(ROOT/"build/attachment90/board_material_repair.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report))
