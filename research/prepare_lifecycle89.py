from pathlib import Path
import hashlib,shutil,json,subprocess,difflib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SDK=ROOT/"third_party/NVSE-6.4.9"
SRC=SDK/"fnv_gmod_thug2_hud88_candidate"
DST=SDK/"fnv_gmod_thug2_lifecycle89_candidate"
OUT=ROOT/"build/lifecycle89"
LIVE=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\NVSE\Plugins\FNVGModTHUG2.dll")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC/"main.cpp")=="71dae8690a30aae7aaa3e92ec78eea43a2be7c2318ccc9750da0bcbb78c5fe91"
live_before=sha(LIVE)
assert not DST.exists(),"Do not overwrite another candidate"
shutil.copytree(SRC,DST);OUT.mkdir(parents=True,exist_ok=True)
old=(SRC/"main.cpp").read_text();s=old
def replace(a,b):
    global s
    assert s.count(a)==1,(a[:80],s.count(a))
    s=s.replace(a,b)
replace("static void ExitSkateMode()\n","static void ExitSkateMode(bool notifyUser = true)\n")
replace("    if (!player || !g_skate.active) return;\n\n    g_skate.active = false;", """    if (!g_skate.active) return;
    if (!player)
    {
        // World may already be gone: invalidate caches without touching old references.
        if (g_skate.forwardHoldInjected)
            Script::RunScriptLine2("releasekey 17", nullptr, true);
        ClearTHUG2RetargetCacheNoRestore();
        g_skate = SkateState{};
        g_skateboardRideRef = nullptr;
        g_skateboardRideStatic = nullptr;
        g_skateboardRidePendingForm = nullptr;
        g_skateboardRidePendingTick = 0;
        UpdateFalloutHudOwnership(false);
        UpdateTHUGHudOverlay();
        return;
    }

    g_skate.active = false;""")
replace("    RestoreTHUG2RetargetBones(player);\n", """    if (kTHUG2RetargetDiagnosticEnabled)
        RestoreTHUG2RetargetBones(player);
    else
        ClearTHUG2RetargetCacheNoRestore();
""")
replace('    Notify("[THUG2] Skate mode OFF - Fallout movement restored");','    if (notifyUser) Notify("[THUG2] Skate mode OFF - Fallout movement restored");')
replace("""    case NVSEMessagingInterface::kMessage_ExitToMainMenu:
        UpdateFalloutHudOwnership(false);""","""    case NVSEMessagingInterface::kMessage_ExitToMainMenu:
        // PreLoad is dispatched before the old save/world is replaced.
        // Release our input/camera/board ownership before dropping readiness.
        ExitSkateMode(false);
        UpdateSkateboardCombatSuppression(PlayerCharacter::GetSingleton(), false);
        ClearTHUG2RetargetCacheNoRestore();
        g_skateboardRideRef = nullptr;
        g_skateboardRideStatic = nullptr;
        g_skateboardRidePendingForm = nullptr;
        g_skateboardRidePendingTick = 0;
        g_skateboardAttackWasDown = true; // require release before reactivation
        UpdateFalloutHudOwnership(false);""")
replace("""    case NVSEMessagingInterface::kMessage_PostLoadGame:
        g_gameplayReady = true;""","""    case NVSEMessagingInterface::kMessage_PostLoadGame:
        // NVSE Serialization.cpp passes the bool as the pointer VALUE, not bool*.
        // Failed loads can leave the previous world resident; remain in Fallout mode.
        _MESSAGE("[THUG2] load attempt completed: success=%u", msg->data != nullptr);
        ClearTHUG2RetargetCacheNoRestore();
        g_skateboardRideRef = nullptr;
        g_skateboardRideStatic = nullptr;
        g_skateboardRidePendingForm = nullptr;
        g_skateboardRidePendingTick = 0;
        g_gameplayReady = true;""")
replace("info->version = 88;","info->version = 89;")
replace("version 88 (original bitmap HUD candidate; incomplete THUG2 runtime)","version 89 (v88 HUD plus lifecycle cleanup; incomplete THUG2 runtime)")
(DST/"main.cpp").write_text(s)
(OUT/"main.patch").write_text("".join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile="v88/main.cpp",tofile="v89/main.cpp")))
assert "<PostBuildEvent>" not in (DST/"FNVGModTHUG2.vcxproj").read_text()
ms=r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
with (OUT/"build.log").open("w") as log:
    for project,kind in [(SDK/"common/common_vc9.vcxproj","common"),(DST/"FNVGModTHUG2.vcxproj","plugin")]:
        args=[ms,str(project),"/t:Rebuild","/p:Configuration=Release","/p:Platform=Win32","/p:OutDir="+(OUT/"bin").as_posix()+"/","/p:IntDir="+(OUT/"obj"/kind).as_posix()+"/","/v:minimal","/nologo"]
        if kind=="plugin":args+=["/p:BuildProjectReferences=false"]
        assert subprocess.run(args,stdout=log,stderr=subprocess.STDOUT).returncode==0,"build failed"
assert sha(LIVE)==live_before
report=dict(candidate=89,parent=88,compile="pass",runtime="not_tested",deployed=False,main_sha256=sha(DST/"main.cpp"),dll_sha256=sha(OUT/"bin/FNVGModTHUG2.dll"),live_sha256=sha(LIVE),limitations=["Not a THUG2 mechanics port","Original physics/animation/camera integration still pending","Lifecycle dispatch cleanup needs in-game save/load/main-menu regression","No board alignment fix yet"])
(OUT/"manifest.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
