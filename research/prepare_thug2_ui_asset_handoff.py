from pathlib import Path
import hashlib, json, subprocess, shutil

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=ROOT/"build/thug2_ui_original"
TOOL=ROOT/"third_party/tools/neversoft-multitool-main/src/NeversoftMultitool/bin/Release/net10.0/NeversoftMultitool.exe"
OUT=ROOT/"build/prepared/thug2_ui_asset_handoff"
PNG=OUT/"png_previews"
PNG.mkdir(parents=True,exist_ok=True)

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

groups={
    "controller_fonts":[
        "fonts/buttonsngc.fnt.ps2",
        "fonts/buttonsps2.fnt.ps2",
        "fonts/buttonsxbox.fnt.ps2",
        "fonts/buttons/buttonsngc.img.ps2",
        "fonts/buttons/buttonsps2.img.ps2",
        "fonts/buttons/buttonsxbox.img.ps2",
    ],
    "hud_fonts":[
        "fonts/newtimerfont.fnt.ps2",
        "fonts/newtrickfont.fnt.ps2",
        "fonts/timerfont/newtimerfont.img.ps2",
        "fonts/trickfont/newtrickfont.img.ps2",
    ],
    "hud_panels":[
        "images/panelsprites/balancearrow.img.ps2",
        "images/panelsprites/balancearrow_glow.img.ps2",
        "images/panelsprites/balancemeter.img.ps2",
        "images/panelsprites/highscore.img.ps2",
        "images/panelsprites/mini_score_hud.img.ps2",
        "images/panelsprites/score_small.img.ps2",
        "images/panelsprites/special.img.ps2",
        "images/panelsprites/specialbar.img.ps2",
        "images/panelsprites/specialbar_end.img.ps2",
    ],
    "controller_and_menu_sprites":[
        "images/mainmenusprites/control_icon.img.ps2",
        "images/mainmenusprites/n_dpad.img.ps2",
        "images/mainmenusprites/p_dpad.img.ps2",
        "images/mainmenusprites/x_dpad.img.ps2",
        "images/mainmenusprites/tricks_icon.img.ps2",
        "images/mainmenusprites/mainicon_score.img.ps2",
        "images/mainmenusprites/menu_sign.img.ps2",
        "images/mainmenusprites/sharedsprites/menu_bottom.img.ps2",
    ],
    "ui_scripts":[
        "scripts/engine/buttonscripts.qb",
        "scripts/engine/buttonscripts.qb.ps2",
        "scripts/engine/controller_pulling.qb",
        "scripts/engine/controller_pulling.qb.ps2",
        "scripts/engine/menu/menubuttonremap.qb",
        "scripts/engine/menu/menubuttonremap.qb.ps2",
        "scripts/game/skater/walking_control.qb",
        "scripts/game/skater/walking_control.qb.ps2",
        "scripts/game/menu/gamemenu_pause.qb",
        "scripts/game/menu/gamemenu_pause.qb.ps2",
        "scripts/game/menu/menusounds.qb",
        "scripts/game/menu/menusounds.qb.ps2",
    ],
    "hud_audio":[
        "sounds/vag/shared/goals/hudspecial1.vag",
        "sounds/vag/shared/goals/hudtrickperfect.vag",
        "sounds/vag/shared/goals/hudtrickslopc.vag",
        "sounds/vag/shared/goals/hud_jumpgap.vag",
        "sounds/vag/shared/goals/hud_specialtrickaa.vag",
        "sounds/vag/shared/goals/landcombo01.vag",
        "sounds/vag/shared/menu/sk6_menu_back.vag",
        "sounds/vag/shared/menu/sk6_menu_fly_in.vag",
        "sounds/vag/shared/menu/sk6_menu_move.vag",
        "sounds/vag/shared/menu/sk6_menu_select.vag",
    ]
}

records=[]
for group,rels in groups.items():
    for rel in rels:
        p=SRC/rel
        row={"group":group,"relative":rel,"exists":p.exists()}
        if p.exists():
            row.update({"bytes":p.stat().st_size,"sha256":sha(p)})
        records.append(row)

# Convert selected PS2 IMG sprite/font-atlas sources to PNG previews.
conversions=[]
for row in records:
    if not row["exists"] or not row["relative"].lower().endswith(".img.ps2"):
        continue
    src=SRC/row["relative"]
    sub=PNG/Path(row["relative"]).parent
    sub.mkdir(parents=True,exist_ok=True)
    cp=subprocess.run([str(TOOL),"ps2tex",str(src),"-o",str(sub)],
                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
    outputs=[]
    for p in sorted(sub.rglob("*.png")):
        outputs.append({
            "path":str(p.relative_to(ROOT)).replace("\\","/"),
            "bytes":p.stat().st_size,
            "sha256":sha(p)
        })
    conversions.append({
        "source":row["relative"],"returncode":cp.returncode,
        "outputs":outputs,"log_tail":"\n".join(cp.stdout.splitlines()[-8:])
    })

# Source-FNT parser currently identifies these runtime font descriptor files as
# a different/non-standalone font container; retain hashes alongside their IMG atlases.
fnt_probe=[]
for rel in [x for x in groups["controller_fonts"]+groups["hud_fonts"] if x.endswith(".fnt.ps2")]:
    p=SRC/rel
    if not p.exists():continue
    cp=subprocess.run([str(TOOL),"fnt",str(p),"-o",str(OUT/"fnt_probe")],
                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
    fnt_probe.append({"source":rel,"returncode":cp.returncode,
                      "log_tail":"\n".join(cp.stdout.splitlines()[-4:])})

missing=[r["relative"] for r in records if not r["exists"]]
result={
    "purpose":"Source-grounded THUG2 HUD/font/controller-glyph/audio asset handoff for Astra. No HUD runtime or v88 files are modified.",
    "source_root":str(SRC),
    "asset_count":len(records),
    "missing":missing,
    "group_counts":{g:sum(r["group"]==g and r["exists"] for r in records) for g in groups},
    "records":records,
    "image_conversions":conversions,
    "image_conversions_success":sum(bool(c["returncode"]==0 and c["outputs"]) for c in conversions),
    "fnt_probe":fnt_probe,
    "findings":[
        "Original Xbox/PS2/NGC controller-button font descriptors and paired IMG atlases are preserved and hashed.",
        "Original timer/trick font descriptors and image atlases are preserved and hashed.",
        "Original balance, score and SPECIAL panel sprites are preserved and converted to local PNG previews for inspection.",
        "Controller/menu scripts and original HUD/menu sounds are indexed for later source-faithful runtime work.",
        "The current multitool fnt parser reports these PS2 runtime FNT descriptors as not its standalone bitmap-font format, so the support lane does not invent metrics; Astra should use the original descriptors/QB behavior."
    ],
    "handoff_boundary":"Astra owns the actual THUG2 HUD/controller-glyph renderer and runtime behavior. Support lane only preserves/hash-converts source assets and dependencies."
}
OUT.mkdir(parents=True,exist_ok=True)
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
(OUT/"summary.json").write_text(json.dumps({
    "asset_count":result["asset_count"],"missing":missing,
    "group_counts":result["group_counts"],
    "image_conversions":len(conversions),
    "image_conversions_success":result["image_conversions_success"],
    "findings":result["findings"]
},indent=2),encoding="utf-8")
print((OUT/"summary.json").read_text())

