from pathlib import Path
import hashlib,shutil,json,subprocess,difflib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SDK=ROOT/"third_party/NVSE-6.4.9";SRC=SDK/"fnv_gmod_thug2_lifecycle89_candidate";DST=SDK/"fnv_gmod_thug2_attachment90_candidate"
OUT=ROOT/"build/attachment90"
LIVE=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\NVSE\Plugins\FNVGModTHUG2.dll")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC/"main.cpp")=="8a025d885a51daf6594141976eb9daa659f6fb25d76f2d7485794755b33bbbdb"
assert not DST.exists()
before=sha(LIVE);shutil.copytree(SRC,DST);OUT.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/"research/fnv_scene_adapter90.inc",DST/"fnv_scene_adapter90.inc")
old=(SRC/"main.cpp").read_text();s=old
def rep(a,b,count=1):
    global s
    assert s.count(a)==count,(a,s.count(a))
    s=s.replace(a,b)
rep("static NiAVObject::RotAndTranslate g_thug2RetargetSaved", '#include "fnv_scene_adapter90.inc"\nstatic FNVTransform90 g_thug2RetargetSaved')
rep("root->GetObject(kTHUG2RetargetBoneNames[i])","FNVFindNode90(root, kTHUG2RetargetBoneNames[i])")
rep("g_thug2RetargetSaved[i] = bone->dat0034;","g_thug2RetargetSaved[i] = FNVLocal90(bone);")
rep("g_thug2RetargetBones[i]->dat0034 = g_thug2RetargetSaved[i];","FNVLocal90(g_thug2RetargetBones[i]) = g_thug2RetargetSaved[i];")
rep("QuaternionToNiMatrix(q, bone->dat0034.rotate);","QuaternionToNiMatrix(q, FNVLocal90(bone).rotate);")
rep("currentRoot->UpdateTransform();","FNVRefreshPose90(currentRoot);",2)
rep("info->version = 89;","info->version = 90;")
rep("version 89 (v88 HUD plus lifecycle cleanup; incomplete THUG2 runtime)","version 90 (scene adapter candidate; animation remains quarantined)")
assert "kTHUG2RetargetDiagnosticEnabled = false" in s or "kTHUG2RetargetDiagnosticEnabled=false" in s
(DST/"main.cpp").write_text(s)
(OUT/"main.patch").write_text("".join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile="v89/main.cpp",tofile="v90/main.cpp")))
assert "<PostBuildEvent>" not in (DST/"FNVGModTHUG2.vcxproj").read_text()
ms=r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
with (OUT/"build.log").open("w") as log:
    for project,kind in [(SDK/"common/common_vc9.vcxproj","common"),(DST/"FNVGModTHUG2.vcxproj","plugin")]:
        args=[ms,str(project),"/t:Rebuild","/p:Configuration=Release","/p:Platform=Win32","/p:OutDir="+(OUT/"bin").as_posix()+"/","/p:IntDir="+(OUT/"obj"/kind).as_posix()+"/","/v:minimal","/nologo"]
        if kind=="plugin":args+=["/p:BuildProjectReferences=false"]
        assert subprocess.run(args,stdout=log,stderr=subprocess.STDOUT).returncode==0
assert sha(LIVE)==before
r={"candidate":90,"parent":89,"compile":"pass","runtime":"not_tested","deployed":False,"retarget_enabled":False,"main_sha256":sha(DST/"main.cpp"),"dll_sha256":sha(OUT/"bin/FNVGModTHUG2.dll"),"live_sha256":sha(LIVE)}
(OUT/"manifest.json").write_text(json.dumps(r,indent=2));print(json.dumps(r))
