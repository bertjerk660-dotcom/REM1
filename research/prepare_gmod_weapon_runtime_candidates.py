from __future__ import annotations
from pathlib import Path
import json, re, shutil, hashlib, math

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
GMOD=Path(r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod")
FNV_DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
MAN=json.loads((ROOT/"research/gmod_weapon_manifest.json").read_text(encoding="utf-8"))
MODELS=json.loads((ROOT/"build/prepared/gmod_hl_weapon_models/manifest.json").read_text(encoding="utf-8"))
OUT=ROOT/"build/prepared/gmod_weapon_runtime_candidates"
VIEW=OUT/"view_nifs"
WORLD=OUT/"world_nifs"
TEX=OUT/"textures"
for p in (VIEW,WORLD,TEX):p.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

# Source model -> staged package/worker metadata.
model_map={r["model"].replace("\\","/").lower():r for r in MODELS["records"]}

# Index mounted sound payload paths from the already-built VPK listing.
vpk_index=set()
idxfile=OUT/"sound_vpk_index.txt"
if idxfile.exists():
    for line in idxfile.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
        s=line.strip().replace("\\","/").lower()
        if s and not s.startswith("### "):vpk_index.add(s)

# Parse loose Source sound-script definitions.
def top_blocks(text):
    # Tokenize quoted strings and braces. Return root-name -> body tokens/strings
    toks=re.findall(r'"((?:\\.|[^"])*)"|([{}])',text)
    flat=[]
    for q,b in toks:flat.append(q if q!="" else b)
    out={}
    i=0
    while i<len(flat)-1:
        name=flat[i]
        if flat[i+1]!="{":i+=1;continue
        i+=2;depth=1;body=[]
        while i<len(flat) and depth:
            t=flat[i]
            if t=="{":depth+=1
            elif t=="}":depth-=1
            if depth:body.append(t)
            i+=1
        out.setdefault(name.lower(),[]).append(body)
    return out

sound_defs={}
sound_script_files=[]
scripts=GMOD/"sourceengine/scripts"
for p in sorted(scripts.glob("*.txt")):
    if "sound" not in p.name.lower():continue
    try:text=p.read_text(encoding="cp1252",errors="ignore")
    except Exception:continue
    blocks=top_blocks(text)
    added=0
    for name,bodies in blocks.items():
        for body in bodies:
            waves=[]
            for j,t in enumerate(body[:-1]):
                if t.lower() in ("wave","wave1","wave2","wave3","wave4") and body[j+1] not in ("{","}"):
                    w=body[j+1].lstrip("*#@<>^)}$!").replace("\\","/")
                    if w.lower().endswith((".wav",".mp3")):waves.append(w)
            if waves:
                sound_defs.setdefault(name,[])
                for w in waves:
                    if w not in sound_defs[name]:sound_defs[name].append(w)
                added+=1
    if added:
        sound_script_files.append({"path":str(p),"sha256":sha(p),"definitions_with_waves":added})

def resolve_sound(ref):
    r=ref.strip().replace("\\","/")
    waves=[]
    named=False
    if r.lower().endswith((".wav",".mp3")):
        waves=[r.lstrip("*#@<>^)}$!")]
    else:
        named=True
        waves=sound_defs.get(r.lower(),[])
    resolved=[]
    for w in waves:
        q=w.replace("\\","/").lstrip("/")
        if q.lower().startswith("sound/"):q=q[6:]
        key=("sound/"+q).lower()
        loose_candidates=[
            GMOD/"garrysmod/sound"/Path(q),
            GMOD/"sourceengine/sound"/Path(q),
        ]
        loose=[p for p in loose_candidates if p.exists()]
        packed=key in vpk_index
        resolved.append({
            "wave":q,"packed":packed,
            "loose":[{"path":str(p),"sha256":sha(p),"bytes":p.stat().st_size} for p in loose],
            "resolved":packed or bool(loose),
        })
    return {"ref":ref,"named_event":named,"definition_found":bool(waves) if named else None,"waves":resolved,
            "resolved_any":any(x["resolved"] for x in resolved)}

def lua_sound_refs(files):
    refs=set()
    evidence=[]
    for f in files:
        p=Path(f)
        if not p.exists():continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        found=set()
        pats=[
            r'\bSound\s*\(\s*["\']([^"\']+)["\']',
            r'\bEmitSound\s*\(\s*["\']([^"\']+)["\']',
            r'\b(?:Primary|Secondary)\.Sound\s*=\s*(?:Sound\s*\(\s*)?["\']([^"\']+)["\']',
            r'\bsound\s*=\s*["\']([^"\']+\.(?:wav|mp3))["\']',
            r'["\']([^"\']+\.(?:wav|mp3))["\']',
        ]
        for pat in pats:
            for x in re.findall(pat,text,re.I):
                x=x.strip()
                if x:found.add(x)
        for x in sorted(found):
            refs.add(x); evidence.append({"file":str(p),"ref":x})
    return sorted(refs),evidence

def model_info(model,role):
    if not model:return None
    key=model.replace("\\","/").lower()
    rec=model_map.get(key)
    if not rec or not rec.get("staged"):
        return {"source_model":model,"staged":False}
    wm=rec["worker_matches"][0] if rec["worker_matches"] else None
    worker_json=None
    package=None
    if wm:
        package=Path(wm["staged_package"])
        wjp=package/"worker.json"
        if wjp.exists():worker_json=json.loads(wjp.read_text(encoding="utf-8"))
    output=Path(worker_json.get("output_nif")) if worker_json and worker_json.get("output_nif") else None
    dest=None
    if output and output.exists():
        safe=re.sub(r"[^A-Za-z0-9_.-]+","__",model.rsplit(".",1)[0])+".nif"
        dest=(VIEW if role=="view" else WORLD)/safe
        shutil.copy2(output,dest)
    materials=[]
    if worker_json:
        for mat in worker_json.get("materials",[]):
            mm=dict(mat)
            for field in ("base","normal"):
                v=mat.get(field)
                if v:
                    fp=Path(v)
                    mm[field+"_exists"]=fp.exists()
                    if fp.exists():
                        try:rel=fp.relative_to(FNV_DATA/"textures")
                        except:rel=Path(fp.name)
                        td=TEX/rel
                        td.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copy2(fp,td)
                        mm[field+"_sha256"]=sha(fp)
                        mm[field+"_staged"]=str(td)
            materials.append(mm)
    qc_files=list(package.rglob("*.qc")) if package else []
    smd_files=list(package.rglob("*.smd")) if package else []
    anim_smd=[p for p in smd_files if "_anims" in str(p).replace("\\","/")]
    sequences=[]
    for q in qc_files:
        txt=q.read_text(encoding="utf-8",errors="ignore")
        sequences+=re.findall(r'(?im)^\s*\$sequence\s+(?:"([^"]+)"|([^\s{]+))',txt)
    seq_names=sorted(set(a or b for a,b in sequences))
    return {
        "source_model":model,"staged":True,
        "package":str(package) if package else None,
        "converted_nif":str(output) if output else None,
        "converted_nif_exists":bool(output and output.exists()),
        "candidate_copy":str(dest) if dest else None,
        "converted_nif_sha256":sha(output) if output and output.exists() else None,
        "raw_package_file_count":wm.get("file_count") if wm else None,
        "qc_files":[str(x) for x in qc_files],
        "smd_file_count":len(smd_files),
        "animation_smd_count":len(anim_smd),
        "animation_smd_names":[x.name for x in anim_smd],
        "qc_sequence_names":seq_names,
        "materials":materials,
        "worker_mass":worker_json.get("mass") if worker_json else None,
        "worker_havok_material":worker_json.get("havok_material") if worker_json else None,
        "source_surfaceprop":worker_json.get("source_surfaceprop") if worker_json else None,
    }

weapons=[]
for w in MAN["weapons"]:
    if w.get("abstract_base"):continue
    view=model_info(w.get("view_model"),"view")
    world=model_info(w.get("world_model"),"world")
    refs,evidence=lua_sound_refs(w.get("files",[]))
    sound_rows=[resolve_sound(x) for x in refs]
    weapons.append({
        "class":w["class"],"kind":w.get("kind"),"display_name":w.get("display_name"),
        "engine_native":w.get("engine_native"),"source_files":w.get("files",[]),
        "view":view,"world":world,
        "sound_refs":sound_rows,"sound_evidence":evidence,
        "converted_nif":w.get("converted_nif"),
    })

# Aggregate checks.
missing_models=[]
missing_textures=[]
unresolved_sounds=[]
for w in weapons:
    for role in ("view","world"):
        m=w.get(role)
        if m and not m.get("staged"):missing_models.append({"class":w["class"],"role":role,"model":m["source_model"]})
        if m and m.get("staged"):
            for mat in m.get("materials",[]):
                for field in ("base","normal"):
                    if mat.get(field) and not mat.get(field+"_exists"):
                        missing_textures.append({"class":w["class"],"role":role,"field":field,"path":mat[field]})
    for s in w["sound_refs"]:
        if not s["resolved_any"]:
            unresolved_sounds.append({"class":w["class"],"ref":s["ref"],"definition_found":s["definition_found"]})

result={
    "purpose":"Support-stage first/third-person model, material, animation-source and sound dependency handoff for concrete GMod/HL weapons. No weapon mechanics/animation runtime is implemented.",
    "concrete_weapon_classes":len(weapons),
    "missing_models":missing_models,
    "missing_textures":missing_textures,
    "unresolved_sound_refs":unresolved_sounds,
    "sound_script_files":sound_script_files,
    "vpk_sound_index_entries":len(vpk_index),
    "weapons":weapons,
    "status":"pass_with_sound_review" if not missing_models and not missing_textures else "fail",
    "handoff_boundary":[
        "Converted view NIFs are geometry/material candidates only; they are not claimed to be FNV first-person animation-ready.",
        "Decompiled QC/SMD sequence/animation data is preserved for Astra to use when implementing source-faithful animation behavior.",
        "World candidates are prepared separately from view candidates.",
        "Unresolved named sound events require Source sound-script/native resolution; do not substitute Fallout sounds."
    ]
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
(OUT/"summary.json").write_text(json.dumps({
    "concrete_weapon_classes":len(weapons),
    "view_candidates":sum(bool(w.get("view") and w["view"].get("converted_nif_exists")) for w in weapons),
    "world_candidates":sum(bool(w.get("world") and w["world"].get("converted_nif_exists")) for w in weapons),
    "missing_models":missing_models,
    "missing_textures_count":len(missing_textures),
    "sound_refs_total":sum(len(w["sound_refs"]) for w in weapons),
    "unresolved_sound_refs_count":len(unresolved_sounds),
    "unresolved_sound_refs":unresolved_sounds,
    "status":result["status"],
},indent=2),encoding="utf-8")
print((OUT/"summary.json").read_text())