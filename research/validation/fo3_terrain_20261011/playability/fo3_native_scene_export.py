# Build an isolated glTF scene from source Fallout 3 ESM + NIF objects.
# No game assets may be committed/published; local-only owner sourced data.
import time
time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
import pathlib,struct,json,math,hashlib,collections
w=pathlib.Path(r"D:\REM_Dream_validation_20261011")
original=w/"fo3_original_two_cells_6_7_7_7.glb"
base=json.loads((w/"fo3_two_cell_base_models.json").read_text())["base_records"]
placement=json.loads((w/"fo3_placed_objects_two_cells.json").read_text())["all_placed"]
extracts=json.loads((w/"fo3_bsa_model_extract.json").read_text())["extracted"]
byname={e["path"].lower():e for e in extracts}
visual=collections.Counter()
buffer=bytearray(); views=[];access=[];meshes=[];nodes=[];mat=[];materials={}
def matid(tag):
    if tag not in materials:
        colors={"terrain":[0.56,0.5,0.38,1],"rock":[0.52,0.49,0.44,1],"road":[0.35,0.36,0.36,1],
        "monorail":[0.45,0.42,0.38,1],"trees":[0.46,0.40,0.28,1],"clutter":[0.42,0.41,0.37,1],"vegetation-proxy":[0.26,0.35,0.16,1]}
        materials[tag]=len(mat);mat.append({"name":tag,"pbrMetallicRoughness":{"baseColorFactor":colors.get(tag,[0.5,0.5,0.5,1]),"metallicFactor":0,"roughnessFactor":1},"doubleSided":True})
    return materials[tag]
def addbuf(blob,target):
    s=len(buffer);buffer.extend(blob)
    while len(buffer)%4:buffer.append(0)
    views.append({"buffer":0,"byteOffset":s,"byteLength":len(blob),"target":target})
    return len(views)-1
def make_primitive(vertices,faces,material):
    clean=[]
    for a,b,c in faces:
        if 0<=a<len(vertices) and 0<=b<len(vertices) and 0<=c<len(vertices) and a!=b and b!=c and a!=c:clean.extend([a,b,c])
    if not clean:return None
    assert vertices and all(all(math.isfinite(t) for t in v) for v in vertices)
    normals=[[0.0,0.0,0.0] for _ in vertices]
    for i in range(0,len(clean),3):
        a,b,c=[vertices[clean[i+j]] for j in range(3)]
        p=[b[k]-a[k] for k in range(3)];q=[c[k]-a[k] for k in range(3)]
        fn=(p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0])
        for vi in clean[i:i+3]:
            for k in range(3):normals[vi][k]+=fn[k]
    normals=[tuple(v/max(1e-9,math.sqrt(sum(t*t for t in n))) for v in n) for n in normals]
    vb=addbuf(struct.pack("<"+str(len(vertices)*3)+"f",*(t for v in vertices for t in v)),34962)
    nb=addbuf(struct.pack("<"+str(len(normals)*3)+"f",*(t for n in normals for t in n)),34962)
    ib=addbuf(struct.pack("<"+str(len(clean))+"I",*clean),34963)
    lo=[min(v[k] for v in vertices) for k in range(3)];hi=[max(v[k] for v in vertices) for k in range(3)]
    va=len(access);access.append({"bufferView":vb,"componentType":5126,"count":len(vertices),"type":"VEC3","min":lo,"max":hi})
    na=len(access);access.append({"bufferView":nb,"componentType":5126,"count":len(normals),"type":"VEC3"})
    ia=len(access);access.append({"bufferView":ib,"componentType":5125,"count":len(clean),"type":"SCALAR"})
    return {"attributes":{"POSITION":va,"NORMAL":na},"indices":ia,"material":matid(material),"mode":4},len(clean)//3
# First place exact source ESM LAND surface.
raw=original.read_bytes();jslen=struct.unpack_from("<I",raw,12)[0];gj=json.loads(raw[20:20+jslen])
payload=raw[28+jslen:]
def srcview(i):
    a=gj["accessors"][i];v=gj["bufferViews"][a["bufferView"]]
    return payload[v["byteOffset"]+a.get("byteOffset",0):],a["count"]
src,count=srcview(0);terrain_verts=[struct.unpack_from("<3f",src,i*12) for i in range(count)]
src,nind=srcview(3);terrain_faces=[struct.unpack_from("<3I",src,i*12) for i in range(nind//3)]
p,nt=make_primitive(terrain_verts,terrain_faces,"terrain")
meshes.append({"name":"FO3_Original_ESM_LAND_6_7_7_7","primitives":[p]})
nodes.append({"name":"FO3_Wasteland_LAND","mesh":0})
original_mesh_ids={};hull_problems=[];nif_counts={}
for e in extracts:
    file=pathlib.Path(e["local_file"])
    nf=NifFormat.Data()
    with file.open("rb") as f:nf.read(f)
    root=nf.roots[0];prim=[];tcnt=0;vcnt=0
    for shape in nf.blocks:
        if type(shape).__name__ not in ("NiTriShape","NiTriStrips") or not shape.data:continue
        triangles=list(shape.data.get_triangles())
        local=[]
        m=shape.get_transform(relative_to=root).as_list()
        for vertex in shape.data.vertices:
            x,y,z=vertex.x,vertex.y,vertex.z
            # NIF matrix rows 3D affine; source Z-up -> Bevy Y-up.
            xx=m[0][0]*x+m[0][1]*y+m[0][2]*z+m[0][3]
            yy=m[1][0]*x+m[1][1]*y+m[1][2]*z+m[1][3]
            zz=m[2][0]*x+m[2][1]*y+m[2][2]*z+m[2][3]
            local.append((xx/64.0,zz/64.0,-yy/64.0))
        if "monorail" in e["path"]:cat="monorail"
        elif "\\roads\\" in e["path"]:cat="road"
        elif "\\rocks\\" in e["path"]:cat="rock"
        elif "\\trees\\" in e["path"]:cat="trees"
        else:cat="clutter"
        output=make_primitive(local,triangles,cat)
        if output:
            prim.append(output[0]);tcnt+=output[1];vcnt+=len(local)
    if not prim:hull_problems.append(e["path"]);continue
    meshid=len(meshes)
    meshes.append({"name":e["path"],"primitives":prim})
    original_mesh_ids[e["path"]]=meshid
    nif_counts[e["path"]]=dict(triangles=tcnt,vertices=vcnt,primitives=len(prim))
# Place exact source world references. Source rotation Euler order assumption is noted in manifest.
def mult(a,b):
 ax,ay,az,aw=a;bx,by,bz,bw=b
 return (aw*bx+ax*bw+ay*bz-az*by,aw*by-ax*bz+ay*bw+az*bx,aw*bz+ax*by-ay*bx+az*bw,aw*bw-ax*bx-ay*by-az*bz)
def quat(x,y,z):
 qx=(math.sin(x/2),0,0,math.cos(x/2))
 qy=(0,math.sin(y/2),0,math.cos(y/2))
 qz=(0,0,math.sin(z/2),math.cos(z/2))
 sx,sy,sz,sw=mult(mult(qz,qy),qx)
 return [sx,sz,-sy,sw]
placed=0;speedtrees=0;missing=[]
for o in placement:
    if o["kind"] not in ("REFR",):continue
    baseform=base[o["base"]]
    local=baseform["model"]
    if not local:missing.append(o["id"]);continue
    sourcepath=("meshes\\"+local).lower()
    if sourcepath not in original_mesh_ids:
        if local.lower().endswith(".spt"):
            speedtrees+=1
            continue
        missing.append(o["id"]);continue
    mesh_id=original_mesh_ids[sourcepath]
    x,y,z=o["position"]
    rotx,roty,rotz=o["rotation"];s=o["scale"]
    nodes.append({"name":"FO3_"+o["id"]+"_"+baseform["edid"],"mesh":mesh_id,
                  "translation":[x/64.0,z/64.0,-y/64.0],
                  "rotation":quat(rotx,roty,rotz),
                  "scale":[s,s,s]})
    placed+=1
doc={"asset":{"version":"2.0","generator":"REM Dream isolated original game mesh research; geometry only"},
    "buffers":[{"byteLength":len(buffer)}],"bufferViews":views,"accessors":access,"materials":mat,
    "meshes":meshes,"nodes":nodes,"scenes":[{"nodes":list(range(len(nodes)))}],"scene":0}
js=json.dumps(doc,separators=(",",":")).encode("utf8");js+=b" "*((-len(js))%4)
glb=struct.pack("<III",0x46546C67,2,12+8+len(js)+8+len(buffer))+struct.pack("<I4s",len(js),b"JSON")+js+struct.pack("<I4s",len(buffer),b"BIN\0")+buffer
out=w/"fo3_two_cell_original_nif_scene.glb";out.write_bytes(glb)
result=dict(source_esm_sha256="D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06",
 scene_glb=str(out),bytes=len(glb),sha256=hashlib.sha256(glb).hexdigest(),
 meshes=len(meshes),unique_nif_meshes=len(original_mesh_ids),nif_visual_triangles=sum(x["triangles"] for x in nif_counts.values()),
 original_land_triangles=nt,placed_original_nif_instances=placed,speedtree_unconverted_placements=speedtrees,
 missing_references=missing, geometry_issues=hull_problems,
 orientation_fidelity="PROVISIONAL: original record Euler order ZYX assumed; no runtime parity evidence",
 height_scale_fidelity="PROVISIONAL /64 Fallout units per metre; mesh height decode seams and Rapier contact validated")
(w/"fo3_native_scene_export_manifest.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
