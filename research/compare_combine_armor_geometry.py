import time
if not hasattr(time,'clock'): time.clock=time.perf_counter
from pathlib import Path
from pyffi.formats.nif import NifFormat

root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
smd=root/"build/gmod_batch/Combine_Soldier/decompiled/Soldier_reference.smd"
static=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\meshes\rem\gmod\Combine_Soldier.nif")
donor=root/"research/armor_donors/AdPowerArmor.NIF"
helm=root/"research/armor_donors/AdPowerArmorHelm.NIF"

def smd_vertices(p):
    lines=p.read_text(errors='ignore').splitlines()
    i=lines.index('triangles')+1
    vs=[]
    bones={}
    while i<len(lines) and lines[i].strip()!='end':
        mat=lines[i].strip(); i+=1
        for _ in range(3):
            parts=lines[i].split(); i+=1
            bone=int(parts[0]); xyz=tuple(map(float,parts[1:4])); normal=tuple(map(float,parts[4:7])); uv=tuple(map(float,parts[7:9]))
            links=[]
            if len(parts)>=10:
                n=int(parts[9]); j=10
                for k in range(n):
                    links.append((int(parts[j]),float(parts[j+1]))); j+=2
            if not links: links=[(bone,1.0)]
            vs.append((xyz,normal,uv,links,mat))
    return vs
sv=smd_vertices(smd)
xyz=[x[0] for x in sv]
print("SMD verts",len(xyz),"bbox",tuple((min(v[k] for v in xyz),max(v[k] for v in xyz)) for k in range(3)))

def read(p):
 d=NifFormat.Data()
 with p.open('rb') as f:d.read(f)
 return d
for label,p in [('STATIC',static),('DONOR',donor),('HELM',helm)]:
 d=read(p); allv=[]
 print('\n',label,p)
 for block in d.get_global_iterator():
  if isinstance(block,NifFormat.NiTriShape):
   dat=block.data
   pts=[(v.x,v.y,v.z) for v in dat.vertices] if dat and dat.has_vertices else []
   if pts:
    allv+=pts
    print("shape",block.name,"verts",len(pts),"tris",dat.num_triangles,"bbox",tuple((min(v[k] for v in pts),max(v[k] for v in pts)) for k in range(3)),"skin",type(block.skin_instance).__name__ if block.skin_instance else None)
    if block.skin_instance:
      print(" bones",[getattr(b,'name',b'') for b in block.skin_instance.bones])
      sd=block.skin_instance.data
      print(" skin transform",sd.skin_transform.scale,sd.skin_transform.translation)
      print(" bone_data",sd.num_bones,len(sd.bone_list))
 if allv: print("ALL bbox",tuple((min(v[k] for v in allv),max(v[k] for v in allv)) for k in range(3)))