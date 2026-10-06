import time
if not hasattr(time,"clock"):
    time.clock=time.perf_counter

from pathlib import Path
from collections import defaultdict
import math, hashlib, json
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SMD=ROOT/"build/gmod_batch/Combine_Soldier/decompiled/Soldier_reference.smd"
STATIC=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\meshes\rem\gmod\Combine_Soldier.nif")
DONOR=ROOT/"research/armor_donors/AdPowerArmor.NIF"
FNV_SKEL=Path(r"C:\IDA68WORK\THUG2\fnv_skeleton.nif")
OUT=ROOT/"build/combine_armor/CombineSoldierFullBody.nif"
OUT.parent.mkdir(parents=True,exist_ok=True)

# ---------- matrix helpers (column vectors, 4x4) ----------
def ident():
    return [[1.0 if i==j else 0.0 for j in range(4)] for i in range(4)]

def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def mv(a,v):
    return [sum(a[i][k]*v[k] for k in range(4)) for i in range(4)]

def rx(a):
    c=math.cos(a); s=math.sin(a)
    return [[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]

def ry(a):
    c=math.cos(a); s=math.sin(a)
    return [[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]

def rz(a):
    c=math.cos(a); s=math.sin(a)
    return [[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]

def inverse_rigid(m, scale=1.0):
    # Works for uniform scale; translations are in row 0..2 col 3.
    r=[[m[i][j]/scale for j in range(3)] for i in range(3)]
    rt=[[r[j][i] for j in range(3)] for i in range(3)]
    t=[m[i][3] for i in range(3)]
    out=ident()
    invs=1.0/scale
    for i in range(3):
        for j in range(3):
            out[i][j]=rt[i][j]*invs
        out[i][3]=-sum(out[i][j]*t[j] for j in range(3))
    return out

def transform_point(m,p):
    v=mv(m,[p[0],p[1],p[2],1.0])
    return (v[0],v[1],v[2])

def transform_dir(m,p):
    v=[sum(m[i][k]*p[k] for k in range(3)) for i in range(3)]
    ln=math.sqrt(sum(x*x for x in v))
    return tuple(x/ln for x in v) if ln>1e-12 else (0.0,0.0,1.0)

def nif_local_matrix(node):
    r=node.rotation
    m=ident()
    rows=[
        [r.m_11,r.m_12,r.m_13],
        [r.m_21,r.m_22,r.m_23],
        [r.m_31,r.m_32,r.m_33],
    ]
    for i in range(3):
        for j in range(3):
            m[i][j]=rows[i][j]*node.scale
    m[0][3]=node.translation.x
    m[1][3]=node.translation.y
    m[2][3]=node.translation.z
    return m

def set_node_transform(node,m):
    node.scale=1.0
    node.rotation.m_11=m[0][0]; node.rotation.m_12=m[0][1]; node.rotation.m_13=m[0][2]
    node.rotation.m_21=m[1][0]; node.rotation.m_22=m[1][1]; node.rotation.m_23=m[1][2]
    node.rotation.m_31=m[2][0]; node.rotation.m_32=m[2][1]; node.rotation.m_33=m[2][2]
    node.translation.x=m[0][3]; node.translation.y=m[1][3]; node.translation.z=m[2][3]

def set_transform_struct(t,m):
    t.scale=1.0
    t.rotation.m_11=m[0][0]; t.rotation.m_12=m[0][1]; t.rotation.m_13=m[0][2]
    t.rotation.m_21=m[1][0]; t.rotation.m_22=m[1][1]; t.rotation.m_23=m[1][2]
    t.rotation.m_31=m[2][0]; t.rotation.m_32=m[2][1]; t.rotation.m_33=m[2][2]
    t.translation.x=m[0][3]; t.translation.y=m[1][3]; t.translation.z=m[2][3]

# ---------- source SMD skeleton and per-position skin weights ----------
lines=SMD.read_text(errors="ignore").splitlines()
src_name={}; src_parent={}
i=lines.index("nodes")+1
while lines[i].strip()!="end":
    s=lines[i].strip(); i+=1
    q=s.split('"')
    idx=int(q[0].strip())
    src_name[idx]=q[1]
    src_parent[idx]=int(q[2].strip())

i=lines.index("skeleton")+1
while not lines[i].strip().startswith("time "):
    i+=1
i+=1
src_pose={}
while i<len(lines) and lines[i].strip()!="end":
    p=lines[i].split(); i+=1
    src_pose[int(p[0])]=tuple(map(float,p[1:7]))

src_local={}
for bone,v in src_pose.items():
    x,y,z,ax,ay,az=v
    # SMD Euler convention used by Source reference export.
    m=mm(mm(rz(az),ry(ay)),rx(ax))
    m[0][3]=x; m[1][3]=y; m[2][3]=z
    src_local[bone]=m

src_world={}
def src_world_matrix(b):
    if b in src_world:
        return src_world[b]
    m=src_local[b]
    par=src_parent[b]
    src_world[b]=mm(src_world_matrix(par),m) if par>=0 else m
    return src_world[b]
for b in src_name:
    src_world_matrix(b)

weights_by_pos=defaultdict(list)
i=lines.index("triangles")+1
while lines[i].strip()!="end":
    i+=1 # material
    for _ in range(3):
        p=lines[i].split(); i+=1
        base=int(p[0])
        xyz=tuple(map(float,p[1:4]))
        links=[]
        if len(p)>=10:
            n=int(p[9]); j=10
            for k in range(n):
                links.append((int(p[j]),float(p[j+1]))); j+=2
        if not links:
            links=[(base,1.0)]
        key=tuple(round(x,3) for x in xyz)
        if not weights_by_pos[key]:
            weights_by_pos[key]=links

# ---------- target FNV skeleton world matrices ----------
sk=NifFormat.Data()
with FNV_SKEL.open("rb") as f:
    sk.read(f)
sk_root=sk.roots[0]

target_nodes_by_name={}
target_world={}
target_m44={}

def m44_to_col(m):
    # PyFFI Matrix44 uses row-vector convention (translation in the last row).
    # Transpose it into the column-vector convention used by this retarget math.
    return [[getattr(m, f"m_{j+1}{i+1}") for j in range(4)] for i in range(4)]

for node in sk.get_global_iterator():
    if not isinstance(node,NifFormat.NiNode):
        continue
    name=node.name.decode("latin1","ignore")
    if not name:
        continue
    try:
        m=node.get_transform(relative_to=sk_root)
    except Exception:
        continue
    target_nodes_by_name[name]=node
    target_m44[name]=m
    target_world[name]=m44_to_col(m)

# Source ValveBiped -> Fallout Bip01 names.
def map_bone(src):
    n=src_name[src]
    n=n.replace("ValveBiped.","")
    direct={
        "Bip01_Pelvis":"Bip01 Pelvis",
        "Bip01_L_Thigh":"Bip01 L Thigh",
        "Bip01_L_Calf":"Bip01 L Calf",
        "Bip01_L_Foot":"Bip01 L Foot",
        "Bip01_L_Toe0":"Bip01 L Toe0",
        "Bip01_R_Thigh":"Bip01 R Thigh",
        "Bip01_R_Calf":"Bip01 R Calf",
        "Bip01_R_Foot":"Bip01 R Foot",
        "Bip01_R_Toe0":"Bip01 R Toe0",
        "Bip01_Spine":"Bip01 Spine",
        "Bip01_Spine1":"Bip01 Spine1",
        "Bip01_Spine2":"Bip01 Spine2",
        "Bip01_Spine4":"Bip01 Neck",
        "Bip01_Neck1":"Bip01 Neck1",
        "Bip01_Head1":"Bip01 Head",
        "Bip01_L_Clavicle":"Bip01 L Clavicle",
        "Bip01_L_UpperArm":"Bip01 L UpperArm",
        "Bip01_L_Forearm":"Bip01 L Forearm",
        "Bip01_L_Hand":"Bip01 L Hand",
        "Bip01_R_Clavicle":"Bip01 R Clavicle",
        "Bip01_R_UpperArm":"Bip01 R UpperArm",
        "Bip01_R_Forearm":"Bip01 R Forearm",
        "Bip01_R_Hand":"Bip01 R Hand",
        "Bip01_L_Finger0":"Bip01 L Thumb1",
        "Bip01_L_Finger01":"Bip01 L Thumb11",
        "Bip01_L_Finger02":"Bip01 L Thumb12",
        "Bip01_L_Finger1":"Bip01 L Finger1",
        "Bip01_L_Finger11":"Bip01 L Finger11",
        "Bip01_L_Finger12":"Bip01 L Finger12",
        "Bip01_L_Finger2":"Bip01 L Finger2",
        "Bip01_L_Finger21":"Bip01 L Finger21",
        "Bip01_L_Finger22":"Bip01 L Finger22",
        "Bip01_R_Finger0":"Bip01 R Thumb1",
        "Bip01_R_Finger01":"Bip01 R Thumb11",
        "Bip01_R_Finger02":"Bip01 R Thumb12",
        "Bip01_R_Finger1":"Bip01 R Finger1",
        "Bip01_R_Finger11":"Bip01 R Finger11",
        "Bip01_R_Finger12":"Bip01 R Finger12",
        "Bip01_R_Finger2":"Bip01 R Finger2",
        "Bip01_R_Finger21":"Bip01 R Finger21",
        "Bip01_R_Finger22":"Bip01 R Finger22",
        "Cod":"Bip01 Pelvis",
        "Anim_Attachment_LH":"Bip01 L Hand",
        "Anim_Attachment_RH":"Bip01 R Hand",
    }
    if n not in direct:
        raise KeyError("unmapped source bone "+n)
    return direct[n]

# Which source matrix should define local coordinates when special bones collapse.
def source_anchor(src):
    n=src_name[src]
    if n=="ValveBiped.Cod":
        return next(k for k,v in src_name.items() if v=="ValveBiped.Bip01_Pelvis")
    if n=="ValveBiped.Anim_Attachment_LH":
        return next(k for k,v in src_name.items() if v=="ValveBiped.Bip01_L_Hand")
    if n=="ValveBiped.Anim_Attachment_RH":
        return next(k for k,v in src_name.items() if v=="ValveBiped.Bip01_R_Hand")
    return src

# ---------- load visual source and donor root ----------
vis=NifFormat.Data()
with STATIC.open("rb") as f:
    vis.read(f)
vis_shape=next(b for b in vis.get_global_iterator() if isinstance(b,NifFormat.NiTriShape))
if vis_shape.data.num_vertices != 3535:
    raise RuntimeError("unexpected Combine visual vertex count")

don=NifFormat.Data()
with DONOR.open("rb") as f:
    don.read(f)
root=don.roots[0]

# Keep root metadata, but replace all children with our full-body visual + flat skin bones.
root.num_children=0
root.children.update_size()

# Target scale. FNV humanoid bind height is ~1.75x Source Combine bind height.
LOCAL_SCALE=1.75

mapped_vertex_weights=[]
new_positions=[]
new_normals=[]
unmatched=0

# Cache source-position nearest entries for the tiny float differences from conversion.
source_keys=list(weights_by_pos.keys())

def lookup_weights(p):
    key=tuple(round(x,3) for x in p)
    hit=weights_by_pos.get(key)
    if hit:
        return hit
    # Should almost never be needed; static conversion preserves source positions.
    best=None
    for k in source_keys:
        ds=sum((p[j]-k[j])**2 for j in range(3))
        if best is None or ds<best[0]:
            best=(ds,k)
    if best and best[0] < 1e-4:
        return weights_by_pos[best[1]]
    return None

for vi,v in enumerate(vis_shape.data.vertices):
    p=(float(v.x),float(v.y),float(v.z))
    links=lookup_weights(p)
    if not links:
        unmatched+=1
        links=[(next(k for k,vv in src_name.items() if vv=="ValveBiped.Bip01_Pelvis"),1.0)]

    merged=defaultdict(float)
    outp=[0.0,0.0,0.0]
    outn=[0.0,0.0,0.0]
    srcn=vis_shape.data.normals[vi] if vis_shape.data.has_normals else None
    nvec=(float(srcn.x),float(srcn.y),float(srcn.z)) if srcn else (0.0,0.0,1.0)

    for sb,w in links:
        tb=map_bone(sb)
        if tb not in target_world:
            raise RuntimeError("target bone missing "+tb)
        anchor=source_anchor(sb)
        sinv=inverse_rigid(src_world[anchor],1.0)
        local=transform_point(sinv,p)
        local=(local[0]*LOCAL_SCALE,local[1]*LOCAL_SCALE,local[2]*LOCAL_SCALE)
        tp=transform_point(target_world[tb],local)
        for k in range(3):
            outp[k]+=tp[k]*w

        # Normal: source bind -> local orientation -> target bind orientation.
        sninv=inverse_rigid(src_world[anchor],1.0)
        localn=transform_dir(sninv,nvec)
        tn=transform_dir(target_world[tb],localn)
        for k in range(3):
            outn[k]+=tn[k]*w
        merged[tb]+=w

    total=sum(merged.values()) or 1.0
    mapped=sorted(((b,w/total) for b,w in merged.items() if w>1e-5),key=lambda x:-x[1])[:4]
    total=sum(w for _,w in mapped) or 1.0
    mapped=[(b,w/total) for b,w in mapped]
    mapped_vertex_weights.append(mapped)

    new_positions.append(tuple(outp))
    ln=math.sqrt(sum(x*x for x in outn))
    new_normals.append(tuple(x/ln for x in outn) if ln>1e-12 else nvec)

# Apply retargeted geometry to the original converted visual so UV/topology/material stay exact.
for i,p in enumerate(new_positions):
    vis_shape.data.vertices[i].x=p[0]
    vis_shape.data.vertices[i].y=p[1]
    vis_shape.data.vertices[i].z=p[2]
for i,n in enumerate(new_normals):
    vis_shape.data.normals[i].x=n[0]
    vis_shape.data.normals[i].y=n[1]
    vis_shape.data.normals[i].z=n[2]

# Tangent/bitangent arrays are not guaranteed in every converted NIF. If present,
# transform them approximately using the dominant mapped bone.
if len(vis_shape.data.tangents)==vis_shape.data.num_vertices:
    for i,t in enumerate(vis_shape.data.tangents):
        b=max(mapped_vertex_weights[i],key=lambda x:x[1])[0]
        # Use target bone orientation as a safe retarget basis for tangents.
        n=transform_dir(target_world[b],(float(t.x),float(t.y),float(t.z)))
        t.x,t.y,t.z=n
if len(vis_shape.data.bitangents)==vis_shape.data.num_vertices:
    for i,t in enumerate(vis_shape.data.bitangents):
        b=max(mapped_vertex_weights[i],key=lambda x:x[1])[0]
        n=transform_dir(target_world[b],(float(t.x),float(t.y),float(t.z)))
        t.x,t.y,t.z=n

vis_shape.data.update_center_radius()
vis_shape.name=b"REM_CombineSoldierFullBody:0"

# Build flat target bone nodes just like stock Fallout armor NIFs.
used_bones=[]
for vw in mapped_vertex_weights:
    for name,w in vw:
        if name not in used_bones:
            used_bones.append(name)

bone_nodes={}
for name in used_bones:
    node=NifFormat.NiNode()
    node.name=name.encode("ascii")
    node.flags=2
    # Preserve the verified Fallout bind transform exactly in PyFFI's native matrix convention.
    node.set_transform(target_m44[name])
    bone_nodes[name]=node

# Build standard NiSkinInstance. The ARMO BMDT slots own equipment coverage;
# BSDismember partitions are not required for this prototype full-body mesh.
skin=NifFormat.NiSkinInstance()
skin.data=NifFormat.NiSkinData()
skin.skeleton_root=root
skin.num_bones=len(used_bones)
skin.bones.update_size()
for i,name in enumerate(used_bones):
    skin.bones[i]=bone_nodes[name]

sd=skin.data
# identity global skin transform, in PyFFI's native Matrix44 convention
_identity=NifFormat.Matrix44()
_identity.set_identity()
sd.skin_transform.set_transform(_identity)
sd.num_bones=len(used_bones)
sd.bone_list.update_size()

weights_per_bone={name:[] for name in used_bones}
for vi,vw in enumerate(mapped_vertex_weights):
    for name,w in vw:
        weights_per_bone[name].append((vi,w))

for bi,name in enumerate(used_bones):
    bd=sd.bone_list[bi]
    inv=inverse_rigid(target_world[name],1.0)
    # Bone skin transform is the inverse verified Fallout bind transform.
    bd.skin_transform.set_transform(target_m44[name].get_inverse())
    vals=weights_per_bone[name]
    bd.num_vertices=len(vals)
    bd.vertex_weights.update_size()
    local_pts=[]
    for j,(vi,w) in enumerate(vals):
        bd.vertex_weights[j].index=vi
        bd.vertex_weights[j].weight=w
        local_pts.append(transform_point(inv,new_positions[vi]))
    if local_pts and hasattr(bd,"bounding_sphere"):
        cx=sum(x[0] for x in local_pts)/len(local_pts)
        cy=sum(x[1] for x in local_pts)/len(local_pts)
        cz=sum(x[2] for x in local_pts)/len(local_pts)
        bd.bounding_sphere.center.x=cx
        bd.bounding_sphere.center.y=cy
        bd.bounding_sphere.center.z=cz
        bd.bounding_sphere.radius=max(math.sqrt((x[0]-cx)**2+(x[1]-cy)**2+(x[2]-cz)**2) for x in local_pts)

vis_shape.skin_instance=skin

# Add visual first, then the flat bind-pose bone nodes.
root.num_children=1+len(used_bones)
root.children.update_size()
root.children[0]=vis_shape
for i,name in enumerate(used_bones,1):
    root.children[i]=bone_nodes[name]

# Write.
with OUT.open("wb") as f:
    don.write(f)

# Validate re-open.
check=NifFormat.Data()
with OUT.open("rb") as f:
    check.read(f)
shape=next(b for b in check.get_global_iterator() if isinstance(b,NifFormat.NiTriShape))
pts=[(v.x,v.y,v.z) for v in shape.data.vertices]
bbox=tuple((min(p[k] for p in pts),max(p[k] for p in pts)) for k in range(3))
result={
    "output":str(OUT),
    "bytes":OUT.stat().st_size,
    "sha256":hashlib.sha256(OUT.read_bytes()).hexdigest().upper(),
    "vertices":shape.data.num_vertices,
    "triangles":shape.data.num_triangles,
    "skin_type":type(shape.skin_instance).__name__,
    "bones":len(shape.skin_instance.bones),
    "bone_names":[shape.skin_instance.bones[i].name.decode("latin1") for i in range(len(shape.skin_instance.bones))],
    "bbox":bbox,
    "unmatched_source_weights":unmatched,
    "local_scale":LOCAL_SCALE,
}
(ROOT/"build/combine_armor/manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))