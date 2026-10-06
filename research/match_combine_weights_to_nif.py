import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
from collections import defaultdict
from pyffi.formats.nif import NifFormat

smd=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\gmod_batch\Combine_Soldier\decompiled\Soldier_reference.smd")
nif=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\meshes\rem\gmod\Combine_Soldier.nif")
lines=smd.read_text(errors="ignore").splitlines()
i=lines.index("triangles")+1
bypos=defaultdict(list)
while lines[i].strip()!="end":
 i+=1
 for _ in range(3):
  parts=lines[i].split(); i+=1
  base=int(parts[0]); xyz=tuple(map(float,parts[1:4])); normal=tuple(map(float,parts[4:7])); uv=tuple(map(float,parts[7:9]))
  links=[]
  if len(parts)>=10:
   n=int(parts[9]); j=10
   for k in range(n):
    links.append((int(parts[j]),float(parts[j+1]))); j+=2
  if not links: links=[(base,1.0)]
  bypos[tuple(round(x,4) for x in xyz)].append((xyz,normal,uv,links))
d=NifFormat.Data()
with nif.open("rb") as f:d.read(f)
shape=next(b for b in d.get_global_iterator() if isinstance(b,NifFormat.NiTriShape))
unmatched=[]; ambiguity=0; weight_variants=0
for idx,v in enumerate(shape.data.vertices):
 key=(round(v.x,4),round(v.y,4),round(v.z,4))
 cand=bypos.get(key,[])
 if not cand:
  unmatched.append((idx,(v.x,v.y,v.z))); continue
 if len(cand)>1:
  ambiguity+=1
  sets={tuple((a,round(b,6)) for a,b in x[3]) for x in cand}
  if len(sets)>1: weight_variants+=1
print("verts",shape.data.num_vertices,"unmatched",len(unmatched),"ambiguous",ambiguity,"weight_variants",weight_variants)
print("first_unmatched",unmatched[:20])
# appended nearest-neighbor analysis
src_positions=[]
for vals in bypos.values():
    if vals: src_positions.append(vals[0][0])
nearest=[]
for idx,pos in unmatched:
    best=min((sum((pos[k]-q[k])**2 for k in range(3)),q) for q in src_positions)
    nearest.append((best[0]**0.5,idx,pos,best[1]))
nearest.sort(reverse=True)
print("nearest max",nearest[:20])