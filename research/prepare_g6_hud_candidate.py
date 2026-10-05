from pathlib import Path
import hashlib, shutil, json
root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
src=root/"third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin"
dst=src.parent/"fnv_gmod_thug2_g6_candidate"
expected="ce3628ae131f42424459f5441051817ec132a7ae53414765047eba6a9a4727a5"
raw=(src/"main.cpp").read_bytes()
assert hashlib.sha256(raw).hexdigest()==expected,"Live source changed; inspect before proceeding"
if dst.exists():
    assert hashlib.sha256((dst/"main.cpp").read_bytes()).hexdigest()==expected,"Candidate changed; refusing overwrite"
else:
    shutil.copytree(src,dst,ignore=shutil.ignore_patterns("Release","Debug",".vs","*.user"))
s=raw.decode("utf-8").replace("\r\n","\n")
def once(old,new):
    global s
    assert s.count(old)==1,("Ambiguous/missing anchor",old[:80],s.count(old))
    s=s.replace(old,new)
once("static void EnterSkateMode()",'#include "thug2_hud_visibility.inc"\n\nstatic void EnterSkateMode()')
once("    g_skate.active = true;\n    g_skate.moveState", "    g_skate.active = true;\n    UpdateFalloutHudOwnership(true);\n    g_skate.moveState")
once("    g_skate.active = false;\n\n    if (!g_skate.fightWasDisabled)", "    g_skate.active = false;\n    UpdateFalloutHudOwnership(false);\n\n    if (!g_skate.fightWasDisabled)")
once("static void PollControls()\n{", "static void PollControls()\n{\n    UpdateFalloutHudOwnership(g_gameplayReady && g_skate.active);")
once("    case NVSEMessagingInterface::kMessage_PostLoad:\n", """    case NVSEMessagingInterface::kMessage_PreLoadGame:
    case NVSEMessagingInterface::kMessage_ExitToMainMenu:
        UpdateFalloutHudOwnership(false);
        g_gameplayReady = false;
        g_skate.active = false;
        UpdateTHUGHudOverlay();
        break;
    case NVSEMessagingInterface::kMessage_PostLoad:
""")
once("    case NVSEMessagingInterface::kMessage_ExitGame:\n", """    case NVSEMessagingInterface::kMessage_ExitGame_Console:
    case NVSEMessagingInterface::kMessage_ExitGame:
        UpdateFalloutHudOwnership(false);
""")
# A newly loaded world must never inherit an ownership record from the old UI.
s=s.replace("        g_skate = SkateState{};","        UpdateFalloutHudOwnership(false);\n        g_skate = SkateState{};")
once("info->version = 85;", "info->version = 86;")
once("bridge loaded, version 85", "bridge loaded, version 86 (G6 HUD candidate; not THUG2 parity)")
(dst/"main.cpp").write_text(s,encoding="utf-8")
shutil.copy2(root/"research/thug2_hud_visibility.inc",dst/"thug2_hud_visibility.inc")
project=dst/"FNVGModTHUG2.vcxproj"
xml=project.read_text(encoding="utf-8")
anchor=r'<ClCompile Include="..\nvse\nvse\GameTiles.cpp">'
assert xml.count(anchor)==1
xml=xml.replace(anchor,r'<ClCompile Include="..\nvse\nvse\GameUI.cpp" />'+'\n    '+anchor)
import re
xml=re.sub(r"\s*<PostBuildEvent>.*?</PostBuildEvent>","",xml,flags=re.S)
project.write_text(xml,encoding="utf-8")
report={"candidate":"v86-g6-hud","baseline_sha256":expected,"path":str(dst),
    "deployment":"not_deployed","exact_thug2_parity":False}
(root/"build/manifests/g6_hud_candidate.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report))