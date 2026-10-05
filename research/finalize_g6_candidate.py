from pathlib import Path
import re, json, hashlib, subprocess, difflib
root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
nvse=root/"third_party/NVSE-6.4.9"
candidate=nvse/"fnv_gmod_thug2_g6_candidate"
project=candidate/"FNVGModTHUG2.vcxproj"
text=project.read_text(encoding="utf-8")
text=re.sub(r"\s*<PostBuildEvent>.*?</PostBuildEvent>","",text,flags=re.S)
project.write_text(text,encoding="utf-8")
(root/"research/thug2_hud_visibility.inc").write_text((candidate/"thug2_hud_visibility.inc").read_text(),encoding="utf-8")
# Distinct intermediate folders for the plugin and the referenced common library.
cmd=[r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\MSBuild\Current\Bin\MSBuild.exe",
    str(project),"/t:Rebuild","/p:Configuration=Release","/p:Platform=Win32",
    "/p:OutDir="+(root/"build/g6_candidate").as_posix()+"/",
    "/p:IntDir="+(root/"build/g6_candidate_obj/plugin").as_posix()+"/",
    "/p:BuildProjectReferences=false","/v:minimal","/nologo"]
common_cmd=[cmd[0],str(nvse/"common/common_vc9.vcxproj"),"/t:Rebuild",
    "/p:Configuration=Release","/p:Platform=Win32",cmd[5],
    "/p:IntDir="+(root/"build/g6_candidate_obj/common").as_posix()+"/","/v:minimal","/nologo"]
with (root/"build/g6_candidate_build.log").open("w") as f:
    result=subprocess.run(common_cmd,stdout=f,stderr=subprocess.STDOUT)
    assert result.returncode==0,"Common library build failed"
    result=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
assert result.returncode==0,"Build failed; inspect build/g6_candidate_build.log"
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
dll=root/"build/g6_candidate/FNVGModTHUG2.dll"
live=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\NVSE\Plugins\FNVGModTHUG2.dll")
assert sha(live)=="bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41","Live deployment changed"
baseline=nvse/"fnv_gmod_thug2_plugin/main.cpp"
assert sha(baseline)=="ce3628ae131f42424459f5441051817ec132a7ae53414765047eba6a9a4727a5","Live source changed"
diff="".join(difflib.unified_diff(baseline.read_text().splitlines(True),
    (candidate/"main.cpp").read_text().splitlines(True),
    fromfile="a/src/plugin/main.cpp",tofile="b/src/plugin/main.cpp"))
(root/"research/g6_hud_main.patch").write_text(diff,encoding="utf-8")
report={"candidate":"v86-g6-hud","baseline_version":85,"baseline_source_sha256":sha(baseline),
    "candidate_source_sha256":sha(candidate/"main.cpp"),"candidate_dll_sha256":sha(dll),
    "live_dll_sha256":sha(live),"compile":"pass","deployment":"not_deployed",
    "runtime_playtest":"not_run","exact_thug2_parity":False,
    "changes":["FNV HUD root visibility ownership with restoration","SDK GameUI.cpp linked",
        "lifecycle HUD cleanup","post-build auto-install removed from candidate"],
    "known_gaps":["Original THUG2 UI runtime not implemented","v85 crash isolation not playtested",
        "Camera and retarget quarantine retained","No model/animation replacement completed"]}
(root/"build/manifests/g6_hud_candidate.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report))