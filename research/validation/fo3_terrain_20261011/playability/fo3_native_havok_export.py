# Convert actual original Fallout 3 NIF hkPackedNiTriStrips collision vertices
# into local-only Rapier input triangles. Original game data never checked in.
import time
time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
import pathlib,struct,json,math,hashlib,collections
w=pathlib.Path(r"D:\REM_Dream_validation_20261011")
ex=json.loads((w/"fo3_bsa_model_extract.json").read_text())["extracted"]
bases=json.loads((w/"fo3_two_cell_base_models.json").read_text())["base_records"]
placements=json.loads((w/"fo3_placed_objects_two_cells.json").read_text())["all_placed"]
models={};errors=[]
for e in ex:
 d=NifFormat.Data()
 with pathlib.Path(e["local_file"]).open("rb") as f:d.read(f)
 arrays=[g for g in d.blocks if type(g).__name__=="hkPackedNiTriStripsData"]
 if not arrays:continue
 vv=[];tt=[]
 for g in arrays:
  start=len(vv)
  vv.extend([(v.x*7.0,v.y*7.0,v.z*7.0) for v in g.vertices])
  for t in g.triangles:
   tri=t.triangle
   a,b,c=int(tri.v_1),int(tri.v_2),int(tri.v_3)
   if a>=g.num_vertices or b>=g.num_vertices or c>=g.num_vertices:
    errors.append("bad triangle in "+e["path"]);continue
   if len({a,b,c})<3:continue
   tt.append((start+a,start+b,start+c))
 models[e["path"].lower()]=(vv,tt)
def qm(a,b):
 ax,ay,az,aw=a;bx,by,bz,bw=b
 return aw*bx+ax*bw+ay*bz-az*by,aw*by-ax*bz+ay*bw+az*bx,aw*bz+ax*by-ay*bx+az*bw,aw*bw-ax*bx-ay*by-az*bz
def qrot(v,q):
 a,b,c,w=q;x,y,z=v
 tx,ty,tz=2*(b*z-c*y),2*(c*x-a*z),2*(a*y-b*x)
 return (x+w*tx+b*tz-c*ty,y+w*ty+c*tx-a*tz,z+w*tz+a*ty-b*tx)
def quat(rx,ry,rz):
 qx=(math.sin(rx/2),0,0,math.cos(rx/2));qy=(0,math.sin(ry/2),0,math.cos(ry/2));qz=(0,0,math.sin(rz/2),math.cos(rz/2))
 return qm(qm(qz,qy),qx)
verts=[];inds=[];count=0;used_bases=set();instance_samples=[];skip_count=0
for o in placements:
 if o['kind']!="REFR":continue
 base=o['base'];path=bases[base]['model']
 if not path:continue
 path=("meshes\\"+path).lower()
 if path not in models:skip_count+=1;continue
 source_v,source_t=models[path]
 px,py,pz=o['position'];sc=o['scale']
 q=quat(*o['rotation'])
 offset=len(verts)
 for v in source_v:
  x,y,z=qrot((v[0]*sc,v[1]*sc,v[2]*sc),q)
  xyz=(px+x,py+y,pz+z)
  verts.append((xyz[0]/64.0,xyz[2]/64.0,-xyz[1]/64.0))
 for a,b,c in source_t:inds.append((offset+a,offset+b,offset+c))
 count+=1;used_bases.add(base)
 if len(instance_samples)<8:instance_samples.append(dict(id=o['id'],base=base,triangles=len(source_t)))
out=w/"fo3_original_havok_static_collisions.bin"
with out.open('wb') as f:
 f.write(b"FO3COL01"+struct.pack("<II",len(verts),len(inds)))
 packv=struct.Struct("<3f").pack
 packt=struct.Struct("<3I").pack
 for v in verts:f.write(packv(*v))
 for tri in inds:f.write(packt(*tri))
manifest=dict(source_esm_sha256="D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06",
 model_count=len(models),native_shape_instance_count=count,instances_without_native_shape=skip_count,
 native_base_ids=sorted(used_bases),vertices=len(verts),triangles=len(inds),
 file=str(out),file_size=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),errors=errors,
 havok_to_source_ratio=7.0,source_to_bevy_ratio=1/64,
 rotation_assumption="Z*Y*X Euler, not verified against live Fallout 3 state",
 sample=instance_samples)
(w/"fo3_havok_collider_export_manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k not in ("native_base_ids","sample")},indent=2))
