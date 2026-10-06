from __future__ import annotations
import hashlib, json, math, time
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
NIF=DATA/"meshes/rem/gmod/armor/CombineSoldierFullBody.nif"
WORLD=DATA/"meshes/rem/gmod/Combine_Soldier.nif"
ESP=DATA/"REM_CombineArmor_Test.esp"
MAIN_DLL=DATA/"NVSE/Plugins/FNVGModTHUG2.dll"
HUD88=ROOT/"build/hud88/bin/FNVGModTHUG2.dll"
REPORT=ROOT/"build/combine_armor/validation.json"

def sha(p:Path):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper() if p.exists() else None

def read_nif(p:Path):
    d=NifFormat.Data()
    with p.open("rb") as f:
        d.read(f)
    return d

checks=[]
def check(name, ok, details=None):
    checks.append({"name":name,"pass":bool(ok),"details":details})
    return bool(ok)

check("biped_nif_exists",NIF.exists(),str(NIF))
check("world_nif_exists",WORLD.exists(),str(WORLD))
check("sidecar_esp_exists",ESP.exists(),str(ESP))
check("live_v85_dll_exists",MAIN_DLL.exists(),str(MAIN_DLL))
check("hud88_candidate_exists",HUD88.exists(),str(HUD88))

nif_info={}
if NIF.exists():
    d=read_nif(NIF)
    roots=d.roots
    shapes=[b for b in d.get_global_iterator() if isinstance(b,NifFormat.NiTriShape)]
    check("single_root",len(roots)==1,len(roots))
    check("has_skinned_shape",any(getattr(s,"skin_instance",None) is not None for s in shapes),len(shapes))
    if shapes:
        s=max(shapes,key=lambda x: x.data.num_vertices if x.data else 0)
        si=s.skin_instance
        data=s.data
        nif_info["root_type"]=type(roots[0]).__name__
        nif_info["shape_name"]=s.name.decode("latin1","ignore") if isinstance(s.name,bytes) else str(s.name)
        nif_info["vertices"]=int(data.num_vertices)
        nif_info["triangles"]=int(data.num_triangles)
        nif_info["skin_type"]=type(si).__name__ if si else None
        nif_info["bones"]=len(si.bones) if si else 0
        check("expected_vertex_count",data.num_vertices==3535,int(data.num_vertices))
        check("expected_triangle_count",data.num_triangles==4682,int(data.num_triangles))
        check("skin_instance_type",type(si).__name__=="NiSkinInstance" if si else False,type(si).__name__ if si else None)
        if si and si.data:
            sums=[0.0]*data.num_vertices
            influences=[0]*data.num_vertices
            bad_indices=[]
            for bd in si.data.bone_list:
                for vw in bd.vertex_weights:
                    idx=int(vw.index); w=float(vw.weight)
                    if idx<0 or idx>=len(sums):
                        bad_indices.append(idx)
                        continue
                    sums[idx]+=w
                    if w>1e-6: influences[idx]+=1
            uncovered=[i for i,v in enumerate(influences) if v==0]
            max_err=max(abs(x-1.0) for x in sums) if sums else 999.0
            max_inf=max(influences) if influences else 0
            nif_info["max_weight_sum_error"]=max_err
            nif_info["max_influences"]=max_inf
            nif_info["uncovered_vertices"]=len(uncovered)
            check("skin_vertex_indices_valid",not bad_indices,bad_indices[:10])
            check("all_vertices_weighted",not uncovered,uncovered[:10])
            check("weights_sum_to_one",max_err<0.002,max_err)
            check("max_four_influences",max_inf<=4,max_inf)
            bone_names=[]
            for b in si.bones:
                if b:
                    bone_names.append(b.name.decode("latin1","ignore") if isinstance(b.name,bytes) else str(b.name))
            nif_info["bone_names"]=bone_names
            check("core_humanoid_bones_present",all(x in bone_names for x in [
                "Bip01 Pelvis","Bip01 Spine","Bip01 Head","Bip01 L Hand","Bip01 R Hand",
                "Bip01 L Foot","Bip01 R Foot"
            ]),bone_names)

    tex=[]
    for b in d.get_global_iterator():
        ts=getattr(b,"texture_set",None)
        if ts:
            for t in ts.textures:
                if t:
                    if isinstance(t,bytes):
                        t=t.decode("latin1","ignore")
                    tex.append(str(t))
    tex=list(dict.fromkeys(tex))
    nif_info["textures"]=tex
    missing=[]
    for t in tex:
        rel=t.replace("\\","/").lower()
        if rel.startswith("textures/"):
            rel=rel[len("textures/"):]
        fp=DATA/"textures"/Path(rel)
        if not fp.exists():
            missing.append(str(fp))
    check("all_nif_textures_resolve",not missing,{"textures":tex,"missing":missing})

esp_strings=[]
if ESP.exists():
    raw=ESP.read_bytes()
    for token in [
        b"REMCombineSoldierFullBodyTest",
        b"Combine Soldier Full-Body Armor (Test)",
        b"rem\\gmod\\armor\\CombineSoldierFullBody.nif",
        b"rem\\gmod\\Combine_Soldier.nif",
        b"rem_gmod_origin.dds",
    ]:
        ok=token in raw
        check("esp_contains_"+token.decode("latin1","ignore").replace("\\","/"),ok)
        if ok: esp_strings.append(token.decode("latin1","ignore"))

plugins=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")
enabled=False
if plugins.exists():
    enabled=any(line.strip().lstrip("*").lower()=="rem_combinearmor_test.esp" for line in plugins.read_text(errors="ignore").splitlines())
check("sidecar_not_enabled",not enabled,enabled)

known={
    "live_v85_dll":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
    "hud88_candidate":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
}
check("live_dll_unchanged",sha(MAIN_DLL)==known["live_v85_dll"],sha(MAIN_DLL))
check("hud88_candidate_unchanged",sha(HUD88)==known["hud88_candidate"],sha(HUD88))

result={
    "purpose":"Separate Combine Soldier full-body armor test package; does not replace Enclave/Remnants records and does not deploy HUD88.",
    "status":"static_validation_pass" if all(c["pass"] for c in checks) else "static_validation_fail",
    "checks":checks,
    "artifacts":{
        "biped_nif":{"path":str(NIF),"sha256":sha(NIF),"bytes":NIF.stat().st_size if NIF.exists() else None},
        "world_nif":{"path":str(WORLD),"sha256":sha(WORLD),"bytes":WORLD.stat().st_size if WORLD.exists() else None},
        "test_esp":{"path":str(ESP),"sha256":sha(ESP),"bytes":ESP.stat().st_size if ESP.exists() else None,"enabled":enabled},
        "live_v85_dll":{"path":str(MAIN_DLL),"sha256":sha(MAIN_DLL)},
        "hud88_candidate":{"path":str(HUD88),"sha256":sha(HUD88)},
    },
    "nif":nif_info,
    "esp_strings":esp_strings,
    "playtest":"not_run",
    "promotion_note":"Use only for later armor-equipping test. Do not replace Enclave/Remnants NPC equipment until deformation, clipping, first/third-person, save/load and NPC tests pass."
}
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))