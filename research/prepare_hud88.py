from pathlib import Path
import json,hashlib,shutil,subprocess,re
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SDK=ROOT/"third_party/NVSE-6.4.9"
BASE=SDK/"fnv_gmod_thug2_g6_candidate"
DST=SDK/"fnv_gmod_thug2_hud88_candidate"
LIVE=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\NVSE\Plugins\FNVGModTHUG2.dll")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(BASE/"main.cpp")=="52ba85fa1d6968d0868ccc58ab7d73fbb23ec1cbd6623ca44021b1d4cd87a1fa"
assert sha(LIVE)=="bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41"
assert not DST.exists(),"Refusing to overwrite an existing candidate"
shutil.copytree(BASE,DST)
fontdir=ROOT/"build/hud88/fonts"
lines=["// Generated from original local font metrics. Do not edit."]
for fname,prefix in [("testtitle","Title"),("newtrickfont","Trick")]:
    j=json.loads((fontdir/(fname+".json")).read_text())
    table=[[0,0,0,0,0,False] for _ in range(256)]
    for g in j["glyphs"]:
        for c in g["codes"]:
            assert 0<=c<256
            table[c]=[g["x"],g["y"],g["width"],g["height"],g["vertical_metric"],True]
    for c in b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":assert table[c][-1],(fname,c)
    lines.append("static const float kTHUG%sBaseline88 = %s.0f;"%(prefix,j["baseline"]))
    lines.append("static const THUGGlyph88 kTHUG%sGlyphs88[256] = {"%prefix)
    lines.extend("{%s},"%",".join(str(v).lower() for v in row) for row in table)
    lines.append("};")
(DST/"thug2_font_metrics88.inc").write_text("\n".join(lines))
shutil.copy2(ROOT/"research/thug2_bitmap_hud88.inc",DST/"thug2_bitmap_hud88.inc")
overlay=(DST/"gmod_overlay.inc").read_text()
a=overlay.index("static void PaintTHUGHud(HWND hwnd, HDC dc)")
b=overlay.index("static LRESULT CALLBACK THUGHudOverlayWndProc",a)
overlay=overlay[:a]+'#include "thug2_bitmap_hud88.inc"\nstatic void PaintTHUGHud(HWND hwnd,HDC dc) { PaintTHUGHud88(hwnd,dc); }\n\n'+overlay[b:]
(DST/"gmod_overlay.inc").write_text(overlay)
main=(DST/"main.cpp").read_text().replace("info->version = 86;","info->version = 88;").replace("version 86 (G6 HUD candidate; not THUG2 parity)","version 88 (original bitmap HUD candidate; incomplete THUG2 runtime)")
(DST/"main.cpp").write_text(main)
project=DST/"FNVGModTHUG2.vcxproj"
proj=project.read_text(); assert "<PostBuildEvent>" not in proj
stage=ROOT/"build/hud88/package/Data/NVSE/Plugins/FNVGModTHUG2_UI/thug2"
(stage/"fonts").mkdir(parents=True,exist_ok=True)
for name in ("testtitle","newtrickfont"):shutil.copy2(fontdir/(name+".png"),stage/"fonts"/(name+".png"))
for name in ("score_small","special","specialbar","balancemeter","balancearrow"):
    shutil.copy2(ROOT/"build/hud87/sprites"/name/"00000000.png",stage/(name+".png"))
ms=r"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\MSBuild\Current\Bin\MSBuild.exe"
out=ROOT/"build/hud88/bin"
base=[ms,"","/t:Rebuild","/p:Configuration=Release","/p:Platform=Win32","/p:OutDir="+out.as_posix()+"/","/v:minimal","/nologo"]
with (ROOT/"build/hud88/build.log").open("w") as log:
    for path,kind in [(SDK/"common/common_vc9.vcxproj","common"),(project,"plugin")]:
        args=base.copy();args[1]=str(path);args+=["/p:IntDir="+(ROOT/("build/hud88/obj/"+kind)).as_posix()+"/"]
        if kind=="plugin":args+=["/p:BuildProjectReferences=false"]
        r=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
        assert r.returncode==0,"Build failed: inspect build/hud88/build.log"
assert sha(LIVE)=="bc24e9b15bca28b33569bc9ff7fd59db66e962150fd00a9350ce3367dcf06f41"
dll=out/"FNVGModTHUG2.dll"
report={"candidate":88,"parent_candidate":86,"compile":"pass","deployment":"not_deployed","runtime_playtest":"not_run","dll_sha256":sha(dll),"main_sha256":sha(DST/"main.cpp"),"overlay_sha256":sha(DST/"gmod_overlay.inc"),"live_dll_sha256":sha(LIVE),"fonts":"original PS2 testtitle/newtrickfont decoded using IDA 6.8 loader","limitations":["GDI host overlay, not complete QB runtime","combo position temporary; original morph/timing/theme port pending","scoring is existing bridge state","camera/animation quarantines retained","no Xbox adapter yet"]}
(ROOT/"build/hud88/build_manifest.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report))
