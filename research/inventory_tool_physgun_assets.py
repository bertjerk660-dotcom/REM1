from pathlib import Path
import json,hashlib,collections,re,vpk

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
GMOD=Path(r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod")
IDX=ROOT/"build/prepared/gmod_weapon_runtime_candidates/sound_vpk_index.txt"
OUT=ROOT/"build/prepared/gmod_tool_physgun_asset_handoff"
OUT.mkdir(parents=True,exist_ok=True)

def sha_bytes(b): return hashlib.sha256(b).hexdigest().upper()
def sha_file(p): return sha_bytes(p.read_bytes())

pa=collections.defaultdict(list); arc=None
for line in IDX.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
    s=line.strip()
    if s.startswith("### "): arc=Path(s[4:].strip()); continue
    if arc and s: pa[s.replace("\\","/").lower()].append(arc)

archives={}
def vpk_bytes(rel):
    key=rel.replace("\\","/").lower()
    for a in pa.get(key,[]):
        ak=str(a)
        if ak not in archives: archives[ak]=vpk.open(ak)
        for candidate in (rel,key):
            try:return archives[ak][candidate].read(),a
            except Exception:pass
    return None,None

targets=[
 "models/weapons/c_toolgun.mdl","models/weapons/c_toolgun.vvd","models/weapons/c_toolgun.dx90.vtx",
 "models/weapons/w_toolgun.mdl","models/weapons/w_toolgun.vvd","models/weapons/w_toolgun.dx90.vtx","models/weapons/w_toolgun.phy",
 "models/weapons/v_physics.mdl","models/weapons/v_physics.vvd","models/weapons/v_physics.dx90.vtx",
 "models/weapons/w_physics.mdl","models/weapons/w_physics.vvd","models/weapons/w_physics.dx90.vtx","models/weapons/w_physics.phy",
 "materials/entities/gmod_tool.png","materials/entities/weapon_physgun.png",
 "materials/models/weapons/v_toolgun/screen.vmt","materials/models/weapons/v_toolgun/screen_bg.vmt","materials/models/weapons/v_toolgun/screen_bg.vtf",
 "materials/models/weapons/v_toolgun/toolgun.vmt","materials/models/weapons/v_toolgun/toolgun.vtf","materials/models/weapons/v_toolgun/toolgun_mask.vtf","materials/models/weapons/v_toolgun/toolgun_exp.vtf",
 "materials/effects/tool_tracer.vmt","materials/effects/tool_tracer.vtf",
 "materials/cable/physbeam.vmt","materials/sprites/physbeam.vmt","materials/sprites/physbeam_white.vtf",
 "materials/sprites/physbeam_active_white.vtf","materials/sprites/physbeama.vmt",
 "materials/sprites/physg_glow1.vmt","materials/sprites/physg_glow2.vmt","materials/sprites/physgbeamb.vmt","materials/sprites/physgun_glow.vtf",
 "materials/models/weapons/w_physics/w_physics_sheet2.vmt","materials/models/weapons/w_physics/w_physics_sheet2.vtf"
]
rows=[]
for rel in targets:
    loose=None
    for base in (GMOD/"garrysmod",GMOD/"sourceengine"):
        p=base/rel
        if p.exists(): loose=p; break
    if loose:
        rows.append({"path":rel,"resolved":True,"container":"loose","origin":str(loose),"bytes":loose.stat().st_size,"sha256":sha_file(loose)})
    else:
        b,a=vpk_bytes(rel)
        rows.append({"path":rel,"resolved":b is not None,"container":"vpk" if b else None,
                     "origin":str(a) if a else None,"bytes":len(b) if b else None,"sha256":sha_bytes(b) if b else None})

scripts=[]
for p in [
 GMOD/"garrysmod/gamemodes/sandbox/entities/weapons/gmod_tool/shared.lua",
 GMOD/"garrysmod/gamemodes/sandbox/entities/weapons/gmod_tool/stool.lua",
 GMOD/"sourceengine/scripts/weapon_physgun.txt",
 GMOD/"sourceengine/scripts/weapon_physcannon.txt"
]:
    scripts.append({"path":str(p),"exists":p.exists(),"bytes":p.stat().st_size if p.exists() else None,"sha256":sha_file(p) if p.exists() else None})

res={
 "purpose":"Path/hash dependency handoff for original GMod Tool Gun and Physics Gun visual/model source assets.",
 "requested":len(rows),"resolved":sum(x["resolved"] for x in rows),
 "missing":[x["path"] for x in rows if not x["resolved"]],
 "assets":rows,"source_scripts":scripts,
 "known_source_behavior":{
   "toolgun_view_model":"models/weapons/c_toolgun.mdl",
   "toolgun_world_model":"models/weapons/w_toolgun.mdl",
   "toolgun_sound_event":"Toolgun.Single",
   "toolgun_effects":["selection_indicator","ToolTracer"],
   "physgun_source_script":"sourceengine/scripts/weapon_physgun.txt",
   "physgun_sound_events":["Weapon_Physgun.On","Weapon_Physgun.Off","Weapon_Physgun.Special1"]
 },
 "boundary":[
   "These assets are original installed source dependencies, not Fallout substitutes.",
   "Core Physgun target/hold/freeze/launch runtime remains Astra/IDA Pro 6.8 work.",
   "Tool Gun mode comes from the real Q-menu gmod_toolmode workflow; no Fallout prompt selector."
 ]
}
(OUT/"manifest.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({"requested":res["requested"],"resolved":res["resolved"],"missing":res["missing"]},indent=2))