from pathlib import Path
import json,struct,hashlib,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/prop_support_phase4"
LEAF=json.loads((BASE/"thug2_diversified_leaf_review.json").read_text())
OUT=BASE

def read_glb_doc(p:Path):
    raw=p.read_bytes()
    if raw[:4]!=b"glTF":raise ValueError(p)
    off=12
    jl,jt=struct.unpack_from("<II",raw,off);off+=8
    if jt!=0x4E4F534A:raise ValueError("missing JSON")
    return json.loads(raw[off:off+jl].decode("utf-8").rstrip("\x00 "))

def material_info(doc,idx):
    mats=doc.get("materials",[])
    if idx<0 or idx>=len(mats):return {"index":idx,"missing":True}
    m=mats[idx]
    tex_indices=set()
    pbr=m.get("pbrMetallicRoughness",{})
    for k in ("baseColorTexture","metallicRoughnessTexture"):
        if k in pbr and isinstance(pbr[k],dict) and "index" in pbr[k]:tex_indices.add(pbr[k]["index"])
    for k in ("normalTexture","occlusionTexture","emissiveTexture"):
        if k in m and isinstance(m[k],dict) and "index" in m[k]:tex_indices.add(m[k]["index"])
    textures=doc.get("textures",[]);images=doc.get("images",[])
    refs=[]
    for ti in sorted(tex_indices):
        t=textures[ti] if ti<len(textures) else {}
        src=t.get("source")
        im=images[src] if isinstance(src,int) and src<len(images) else {}
        refs.append({
          "texture_index":ti,"image_index":src,
          "image_uri":im.get("uri"),"image_bufferView":im.get("bufferView"),
          "mimeType":im.get("mimeType")
        })
    return {
      "index":idx,"name":m.get("name"),"doubleSided":m.get("doubleSided"),
      "alphaMode":m.get("alphaMode","OPAQUE"),"textures":refs
    }

def collision_strategy(cat,dims,triangles):
    low=cat.lower()
    if any(x in low for x in ("rail","handrail","ledge","hubba","curb","ramp","quarterpipe","halfpipe","stairs","platform")):
        role="static_skate_obstacle"
        method="static mesh/shape collision preserving grindable/skateable silhouette"
    elif any(x in low for x in ("bench","table","chair","fence","barrier","pole","pipe")):
        role="static_environment_prop"
        method="static collision initially; only add dynamic wrapper after explicit Physgun test requirement"
    else:
        role="static_environment_prop";method="static collision initially"
    complexity="low" if (triangles or 0)<=5000 else "medium" if (triangles or 0)<=20000 else "high"
    return {
      "role":role,"recommended_initial_collision":method,
      "collision_complexity":complexity,
      "physgun_mobility":"not_inferred_from_THUG2_level_geometry; runtime dynamic wrapper or separate movable record required if later desired",
      "scale_validation":"required_against_FNV_player_and_known_source_object_dimensions"
    }

records=[]
for r in LEAF["records"]:
    p=ROOT/r["source_glb"];doc=read_glb_doc(p)
    top=(r.get("leaf_metrics") or [{}])[0]
    node_idx=top.get("node");mesh_idx=top.get("mesh")
    material_indices=[]
    if isinstance(mesh_idx,int) and mesh_idx<len(doc.get("meshes",[])):
        for pr in doc["meshes"][mesh_idx].get("primitives",[]):
            if "material" in pr:material_indices.append(int(pr["material"]))
    material_indices=sorted(set(material_indices))
    mats=[material_info(doc,i) for i in material_indices]
    records.append({
      "level":r["level"],"identifier":r["identifier"],"category":r["category"],
      "source_glb":r["source_glb"],"node":node_idx,"mesh":mesh_idx,
      "dimensions":top.get("dimensions"),"triangles":top.get("triangles"),
      "materials":mats,"material_count":len(mats),
      "collision_plan":collision_strategy(r["category"],top.get("dimensions"),top.get("triangles")),
      "state":"provenance_prepared_visual_identity_still_pending"
    })

result={
 "purpose":"Material provenance and collision-strategy handoff for the diversified THUG2 prop wave. No NIF/ESP/runtime changes.",
 "count":len(records),
 "with_materials":sum(r["material_count"]>0 for r in records),
 "collision_roles":dict(collections.Counter(r["collision_plan"]["role"] for r in records)),
 "records":records,
 "rules":[
   "THUG2 level geometry is treated as static source evidence by default.",
   "Do not claim Physgun-movable behavior from static level geometry.",
   "Preserve original material/image references through standalone extraction/conversion.",
   "Human visual identity confirmation remains required before splitting."
 ]
}
(OUT/"thug2_material_collision_plan.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"count":result["count"],"with_materials":result["with_materials"],"collision_roles":result["collision_roles"]},indent=2))