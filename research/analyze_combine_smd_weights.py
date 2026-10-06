from pathlib import Path
from collections import Counter, defaultdict

p=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\gmod_batch\Combine_Soldier\decompiled\Soldier_reference.smd")
lines=p.read_text(errors="ignore").splitlines()
names={}
i=lines.index("nodes")+1
while lines[i].strip()!="end":
    s=lines[i].strip(); i+=1
    parts=s.split('"')
    names[int(parts[0].strip())]=parts[1]
i=lines.index("triangles")+1
counts=Counter()
zs=defaultdict(list)
tri_classes=Counter()
while lines[i].strip()!="end":
    i+=1
    tri=[]
    for _ in range(3):
        parts=lines[i].split(); i+=1
        base=int(parts[0]); z=float(parts[3])
        links=[]
        if len(parts)>=10:
            n=int(parts[9]); j=10
            for k in range(n):
                links.append((int(parts[j]),float(parts[j+1]))); j+=2
        if not links:
            links=[(base,1.0)]
        dom=max(links,key=lambda x:x[1])[0]
        nm=names[dom]
        counts[nm]+=1
        zs[nm].append(z)
        tri.append((nm,z))
    doms=[x[0] for x in tri]
    avgz=sum(x[1] for x in tri)/3.0
    if all(("Head1" in x or "Neck1" in x) for x in doms):
        tri_classes["head_all"]+=1
    elif any("Head1" in x for x in doms):
        tri_classes["head_any"]+=1
    elif avgz>60:
        tri_classes["z60"]+=1
    else:
        tri_classes["body"]+=1
print("BONES")
for nm,n in counts.most_common():
    vals=zs[nm]
    print(nm,n,min(vals),max(vals),sum(vals)/len(vals))
print("TRI_CLASSES",dict(tri_classes))