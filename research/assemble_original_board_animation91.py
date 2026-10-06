from pathlib import Path
import json,struct,copy,hashlib,math
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=ROOT/"build/prepared/thug2_prop_catalog/standalone_glb/models/board_default/board_default/board_default.glb"
ANIMS=ROOT/"build/skater87/glb"
OUT=ROOT/"build/board_animation91"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 b=p.read_bytes();magic,version,total=struct.unpack_from("<4sII",b)
 assert magic==b"glTF" and version==2 and total==len(b)
 off=12;j=None;blob=None
 while off<total:
  n,t=struct.unpack_from("<II",b,off);off+=8;c=b[off:off+n];off+=n
  if t==0x4e4f534a:j=json.loads(c)
  elif t==0x004e4942:blob=c
 assert j and blob is not None and len(j["buffers"])==1
 assert j["buffers"][0]["byteLength"]<=len(blob)
 return j,blob
def write(p,j,b):
 j["buffers"]=[{"byteLength":len(b)}]
 js=json.dumps(j,separators=(",",":")).encode();js+=b" "*((-len(js))%4);b+=b"\0"*((-len(b))%4)
 p.write_bytes(struct.pack("<4sII",b"glTF",2,28+len(js)+len(b))+struct.pack("<II",len(js),0x4e4f534a)+js+struct.pack("<II",len(b),0x004e4942)+b)
mesh,mb=read(SRC)
assert not mesh.get("skins") and not mesh.get("animations")
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
clips=["thps6_skater_basics/"+s+".glb" for s in ["idle","push","ollie","land","manual"]]+["thps6_skater_fliptricks/kickflip.glb"]
for rel in clips:
 p=ANIMS/rel;original,ab=read(p);j=copy.deepcopy(original)
 board=[i for i,x in enumerate(j["nodes"]) if x.get("name","").lower()=="bone_board_root"]
 assert len(board)==1
 keys=["bufferViews","accessors","images","samplers","textures","materials","meshes","nodes"]
 offsets={k:len(j.get(k,[])) for k in keys}
 start=len(ab);ab+=b"\0"*((-len(ab))%4);start=len(ab)
 for v0 in mesh.get("bufferViews",[]):
  v=copy.deepcopy(v0);assert v["buffer"]==0;v["byteOffset"]=v.get("byteOffset",0)+start;j.setdefault("bufferViews",[]).append(v)
 for a0 in mesh.get("accessors",[]):
  a=copy.deepcopy(a0);assert "sparse" not in a;a["bufferView"]+=offsets["bufferViews"];j.setdefault("accessors",[]).append(a)
 for im0 in mesh.get("images",[]):
  im=copy.deepcopy(im0);assert "bufferView" in im;im["bufferView"]+=offsets["bufferViews"];j.setdefault("images",[]).append(im)
 j.setdefault("samplers",[]).extend(copy.deepcopy(mesh.get("samplers",[])))
 for t0 in mesh.get("textures",[]):
  t=copy.deepcopy(t0);t["source"]+=offsets["images"]
  if "sampler" in t:t["sampler"]+=offsets["samplers"]
  j.setdefault("textures",[]).append(t)
 for m0 in mesh.get("materials",[]):
  m=copy.deepcopy(m0);pbr=m.get("pbrMetallicRoughness",{})
  for obj,key in [(pbr,"baseColorTexture"),(pbr,"metallicRoughnessTexture"),(m,"normalTexture"),(m,"occlusionTexture"),(m,"emissiveTexture")]:
   if key in obj:obj[key]["index"]+=offsets["textures"]
  assert set(m.get("extensions",{}))<= {"KHR_materials_unlit"}
  j.setdefault("materials",[]).append(m)
 for m0 in mesh["meshes"]:
  m=copy.deepcopy(m0)
  for pr in m["primitives"]:
   pr["attributes"]={k:v+offsets["accessors"] for k,v in pr["attributes"].items()}
   if "indices" in pr:pr["indices"]+=offsets["accessors"]
   if "material" in pr:pr["material"]+=offsets["materials"]
   assert "targets" not in pr and "extensions" not in pr
  j.setdefault("meshes",[]).append(m)
 for n0 in mesh["nodes"]:
  n=copy.deepcopy(n0);assert "skin" not in n
  if "mesh" in n:n["mesh"]+=offsets["meshes"]
  if "children" in n:n["children"]=[v+offsets["nodes"] for v in n["children"]]
  j["nodes"].append(n)
 roots=mesh["scenes"][mesh.get("scene",0)]["nodes"]
 j["nodes"][board[0]].setdefault("children",[]).extend(v+offsets["nodes"] for v in roots)
 for k in ["extensionsUsed","extensionsRequired"]:
  j[k]=sorted(set(j.get(k,[])+mesh.get(k,[])))
 # Animation channels, keyframes and all source node transforms remain unchanged.
 j["asset"]["generator"]="REM1 original THUG2 board/animation assembly 91"
 dst=OUT/(p.stem+".glb");write(dst,j,ab+mb)
 check,cb=read(dst)
 assert check["animations"]==original["animations"]
 assert check["accessors"][:offsets["accessors"]]==original["accessors"]
 assert cb[:len(ab)]==ab and cb[start:start+len(mb)]==mb
 for v in check["bufferViews"]:assert v.get("byteOffset",0)+v["byteLength"]<=len(cb)
 for n in check["nodes"]:
  for child in n.get("children",[]):assert child<len(check["nodes"])
 for a,b in zip(original["nodes"],check["nodes"]):
  for k in ["translation","rotation","scale","matrix"]:assert a.get(k)==b.get(k)
 tracks=[c for a in original["animations"] for c in a["channels"] if c["target"]["node"]==board[0]]
 rows.append({"clip":rel,"output":str(dst),"source_sha256":sha(p),"output_sha256":sha(dst),"board_tracks":len(tracks),"source_animation_and_binary_preserved":True,"mesh_binary_preserved":True,"validation":"pass"})
report={"stage":91,"source_board":str(SRC),"source_board_sha256":sha(SRC),"clips":rows,"deployed":False,"scope":"Original mesh attached to original bone_board_root with complete source animation hierarchy; asset assembly, not a native THUG2 code port","remaining":["Visual bind-origin/scale validation","Source attachment events and transition code","Fallout runtime player/board shared clock and rig integration"]}
(OUT/"manifest.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
