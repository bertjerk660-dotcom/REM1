from pathlib import Path
import hashlib, json, re

PROJECT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
GMOD=Path(r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\garrysmod")
STEAM_MANIFEST=Path(r"C:\Program Files (x86)\Steam\steamapps\appmanifest_4000.acf")
OUTDIR=PROJECT/"build/prepared/gmod_qmenu_source_inventory"
OUTDIR.mkdir(parents=True,exist_ok=True)

sandbox=GMOD/"gamemodes/sandbox"
base=GMOD/"gamemodes/base"
lua=GMOD/"lua"
materials=GMOD/"materials"

role_files={}

def add(path,role):
    p=Path(path)
    if p.exists() and p.is_file():
        role_files.setdefault(p,set()).add(role)

def add_tree(path,role):
    p=Path(path)
    if not p.exists(): return
    for f in p.rglob("*.lua"):
        add(f,role)

# Real Q/spawn menu client stack.
add(sandbox/"gamemode/cl_spawnmenu.lua","qmenu_entry")
add(sandbox/"gamemode/cl_search_models.lua","qmenu_search")
add(sandbox/"gamemode/cl_notice.lua","notifications")
add_tree(sandbox/"gamemode/spawnmenu","qmenu_spawnmenu")
# Real Tool Gun SWEP + tool definitions.
add_tree(sandbox/"entities/weapons/gmod_tool","toolgun")
# Physgun Lua-visible hooks and Sandbox policy/notifications. Core weapon remains native.
for p in [
    base/"gamemode/shared.lua",
    base/"gamemode/player.lua",
    sandbox/"gamemode/shared.lua",
    sandbox/"gamemode/init.lua",
    sandbox/"gamemode/cl_init.lua",
]:
    add(p,"physgun_hooks")
# Core GMod modules visibly used by the target systems.
for name in [
    "spawnmenu.lua","controlpanel.lua","duplicator.lua","notification.lua",
    "cleanup.lua","undo.lua","presets.lua","properties.lua","killicon.lua",
    "list.lua","hook.lua","concommand.lua","constraint.lua","numpad.lua",
]:
    add(lua/"includes/modules"/name,"core_module")
# Some stock menu population comes from autorun scripts.
for name in ["utilities_menu.lua","game_hl2.lua"]:
    add(lua/"autorun"/name,"menu_population")

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def rel(p):
    try:return p.relative_to(GMOD).as_posix()
    except:return str(p)

def strings(pattern,text):
    return sorted(set(m.group(1) for m in re.finditer(pattern,text,re.M)))

def parse(p):
    text=p.read_text(encoding="utf-8",errors="ignore")
    inc=strings(r'\b(?:include|AddCSLuaFile)\s*\(\s*["\']([^"\']+)["\']',text)
    funcs=strings(r'\bfunction\s+([A-Za-z0-9_:.]+)\s*\(',text)
    funcs+=strings(r'\b([A-Za-z0-9_:.]+)\s*=\s*function\s*\(',text)
    hooks=[]
    for m in re.finditer(r'hook\.Add\s*\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']',text):
        hooks.append({"event":m.group(1),"id":m.group(2)})
    cons=strings(r'concommand\.Add\s*\(\s*["\']([^"\']+)["\']',text)
    spawn_calls=sorted(set(re.findall(r'\bspawnmenu\.([A-Za-z0-9_]+)',text)))
    notify_calls=sorted(set(re.findall(r'\bnotification\.([A-Za-z0-9_]+)',text)))
    vcreate=strings(r'vgui\.Create\s*\(\s*["\']([^"\']+)["\']',text)
    vreg=[]
    for m in re.finditer(r'vgui\.Register\s*\(\s*["\']([^"\']+)["\']\s*,[^,]+,\s*["\']([^"\']+)["\']',text):
        vreg.append({"class":m.group(1),"base":m.group(2)})
    for m in re.finditer(r'derma\.DefineControl\s*\(\s*["\']([^"\']+)["\']',text):
        vreg.append({"class":m.group(1),"base":"derma"})
    assets=set()
    for pat in [
        r'\bMaterial\s*\(\s*["\']([^"\']+)["\']',
        r'surface\.GetTextureID\s*\(\s*["\']([^"\']+)["\']',
        r':SetImage\s*\(\s*["\']([^"\']+)["\']',
        r'killicon\.[A-Za-z0-9_]+\s*\([^,]+,\s*["\']([^"\']+)["\']',
    ]:
        assets.update(re.findall(pat,text))
    native_prefixes={}
    for prefix in ["gui","input","surface","render","cam","draw","file","util","ents","constraint","duplicator","undo","cleanup","net","player","game","engine"]:
        calls=sorted(set(re.findall(r'\b'+re.escape(prefix)+r'\.([A-Za-z0-9_]+)',text)))
        if calls:native_prefixes[prefix]=calls
    methods=sorted(set(re.findall(r'\b(?:LocalPlayer\(\)|ply|player|ent|phys|tr|wep)\s*:\s*([A-Za-z0-9_]+)',text)))
    return {
        "path":rel(p),"bytes":p.stat().st_size,"sha256":sha(p),
        "roles":sorted(role_files[p]),
        "includes":inc,"functions":sorted(set(funcs)),
        "hooks":hooks,"concommands":cons,
        "spawnmenu_calls":spawn_calls,"notification_calls":notify_calls,
        "vgui_create":vcreate,"vgui_register":vreg,
        "asset_refs":sorted(assets),
        "native_api_namespaces":native_prefixes,
        "object_methods":methods,
    }

records=[parse(p) for p in sorted(role_files,key=lambda x:rel(x).lower())]

# Register all stock VGUI controls so dependencies can be mapped without copying source.
vgui_map={}
for f in sorted((lua/"vgui").glob("*.lua")):
    txt=f.read_text(encoding="utf-8",errors="ignore")
    regs=[]
    for m in re.finditer(r'vgui\.Register\s*\(\s*["\']([^"\']+)["\']\s*,[^,]+,\s*["\']([^"\']+)["\']',txt):
        regs.append((m.group(1),m.group(2)))
    for m in re.finditer(r'derma\.DefineControl\s*\(\s*["\']([^"\']+)["\']',txt):
        regs.append((m.group(1),"derma"))
    for cls,basecls in regs:
        vgui_map[cls]={"source":rel(f),"base":basecls,"sha256":sha(f)}

created=sorted(set(x for r in records for x in r["vgui_create"]))
vgui_dependencies={c:vgui_map.get(c,{"source":None,"base":None,"status":"engine_or_dynamic"}) for c in created}

# Resolve material/image references against loose GMod files and the installed
# garrysmod_dir VPK index. No proprietary payload is copied.
VPK_INDEX=OUTDIR/"garrysmod_vpk_index.txt"
vpk_entries=set()
if VPK_INDEX.exists():
    for line in VPK_INDEX.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
        q=line.strip().replace("\\","/").lower()
        if q:
            vpk_entries.add(q)
VPK_DIR=GMOD/"garrysmod_dir.vpk"
vpk_dir_sha256=sha(VPK_DIR) if VPK_DIR.exists() else None

def asset_candidate_relpaths(ref):
    r=ref.replace("\\","/").lstrip("/")
    if r.startswith("materials/"):
        r=r[len("materials/"):]
    candidates=[]
    suffix=Path(r).suffix.lower()
    if suffix:
        candidates.append("materials/"+r)
    else:
        candidates.extend(["materials/"+r+".vmt","materials/"+r+".png","materials/"+r+".vtf"])
    return [x.replace("//","/") for x in candidates]

asset_refs=sorted(set(x for r in records for x in r["asset_refs"]))
asset_inventory=[]
for a in asset_refs:
    loose_hits=[]
    packed_hits=[]
    for candidate in asset_candidate_relpaths(a):
        lp=GMOD/candidate
        if lp.exists():
            loose_hits.append({"path":rel(lp),"bytes":lp.stat().st_size,"sha256":sha(lp)})
        if candidate.lower() in vpk_entries:
            packed_hits.append({"path":candidate,"archive":"garrysmod_dir.vpk"})
    asset_inventory.append({
        "ref":a,
        "loose":loose_hits,
        "packed":packed_hits,
        "resolved_any":bool(loose_hits or packed_hits)
    })

# Count key systems/symbol evidence.
key_evidence={
    "qmenu_entry_functions":[],
    "toolgun_menu_registration":[],
    "physgun_hooks":[],
    "notification_api":[],
    "duplicator_api":[],
}
for r in records:
    for f in r["functions"]:
        lf=f.lower()
        if "spawnmenu" in lf or "contextmenu" in lf:
            key_evidence["qmenu_entry_functions"].append({"path":r["path"],"symbol":f})
        if "physgun" in lf:
            key_evidence["physgun_hooks"].append({"path":r["path"],"symbol":f})
    if "AddToolMenuOption" in r["spawnmenu_calls"] or "AddToolCategory" in r["spawnmenu_calls"]:
        key_evidence["toolgun_menu_registration"].append(r["path"])
    if r["notification_calls"]:
        key_evidence["notification_api"].append({"path":r["path"],"calls":r["notification_calls"]})
    if "duplicator" in r["native_api_namespaces"]:
        key_evidence["duplicator_api"].append({"path":r["path"],"calls":r["native_api_namespaces"]["duplicator"]})

# Steam app manifest provenance.
steam={}
if STEAM_MANIFEST.exists():
    txt=STEAM_MANIFEST.read_text(errors="ignore")
    for key in ("buildid","LastUpdated","StateFlags","installdir"):
        m=re.search(r'"'+re.escape(key)+r'"\s+"([^"]+)"',txt,re.I)
        if m:steam[key]=m.group(1)
    steam["sha256"]=sha(STEAM_MANIFEST)

role_counts={}
for r in records:
    for role in r["roles"]: role_counts[role]=role_counts.get(role,0)+1

result={
    "purpose":"Inventory/hash/dependency map for the real installed Garry's Mod Q menu, Tool Gun, Physgun-visible Lua hooks and notification stack. No runtime port is performed.",
    "source_root":str(GMOD),
    "steam_appmanifest":steam,
    "lua_file_count":len(records),
    "role_counts":dict(sorted(role_counts.items())),
    "tool_stool_files":sum(1 for r in records if "toolgun" in r["roles"] and "/stools/" in r["path"]),
    "vgui_classes_created":len(created),
    "vgui_dependencies":vgui_dependencies,
    "asset_ref_count":len(asset_inventory),
    "vpk_index":{"entries":len(vpk_entries),"dir_vpk_sha256":vpk_dir_sha256},
    "asset_refs_unresolved":[x for x in asset_inventory if not x["resolved_any"]],
    "key_evidence":key_evidence,
    "files":records,
    "asset_inventory":asset_inventory,
    "handoff_boundary":{
        "support_lane":"Preserve paths/hashes/dependencies, identify script/native boundary, stage assets and tests.",
        "astra_lane":"Implement the actual Lua/Derma/native compatibility runtime in Fallout/xNVSE and use IDA Pro 6.8 for native Source/GMod behavior unavailable in script."
    },
    "important_findings":[
        "The Q/spawn menu has a substantial Lua/Derma implementation under gamemodes/sandbox/gamemode/spawnmenu plus lua/includes/modules/spawnmenu.lua.",
        "The Tool Gun is script-rich: gmod_tool SWEP/stool.lua and the stools tree directly register tool-menu entries with spawnmenu APIs.",
        "Physgun pickup/drop/unfreeze policy is exposed through Lua gamemode hooks, but weapon_physgun itself is engine-native; exact beam/manipulation weapon behavior therefore crosses the native boundary and belongs to Astra/IDA 6.8 work.",
        "GMod notifications are script-visible through lua/includes/modules/notification.lua and Sandbox client notification code; these are the correct source for notification bubbles instead of Fallout HUD prompts."
    ]
}
(OUTDIR/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

summary={
    "lua_file_count":result["lua_file_count"],
    "role_counts":result["role_counts"],
    "tool_stool_files":result["tool_stool_files"],
    "vgui_classes_created":result["vgui_classes_created"],
    "asset_ref_count":result["asset_ref_count"],
    "vpk_index":result["vpk_index"],
    "asset_refs_unresolved_count":len(result["asset_refs_unresolved"]),
    "steam_appmanifest":steam,
    "important_findings":result["important_findings"],
}
(OUTDIR/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))