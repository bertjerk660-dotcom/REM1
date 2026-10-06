from pathlib import Path
import json, re, hashlib, collections, math, datetime

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"build/prepared/prop_support_phase3"
OUT.mkdir(parents=True,exist_ok=True)

FINAL=json.loads((ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json").read_text(encoding="utf-8"))
FNV=json.loads((ROOT/"build/prepared/fnv_prop_catalog_curated/ready_existing_forms.json").read_text(encoding="utf-8"))
GMOD=json.loads((ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json").read_text(encoding="utf-8"))
GMOD_FORMS=json.loads((ROOT/"build/prepared/gmod_prop_catalog_sidecar/form_map.json").read_text(encoding="utf-8"))
THUG=json.loads((ROOT/"build/prepared/thug2_prop_catalog/target_classification.json").read_text(encoding="utf-8"))
SPATIAL=json.loads((ROOT/"build/prepared/thug2_prop_catalog/spatial_prop_candidates/mapping.json").read_text(encoding="utf-8"))
THUMBS=json.loads((ROOT/"build/prepared/final_prop_catalog_thumbnails/manifest.json").read_text(encoding="utf-8"))
NATIVE_ICON_PATH=ROOT/"build/prepared/prop_menu_thumbnails/native_gmod_spawnicons/manifest.json"
NATIVE=json.loads(NATIVE_ICON_PATH.read_text(encoding="utf-8")) if NATIVE_ICON_PATH.exists() else {"gmod_props":120,"native_spawnicons_found":0,"native_spawnicons_missing":120,"records":[]}

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def norm_path(s):
    return str(s or "").replace("\\","/").lower()

def variant_key(path,name=""):
    stem=Path(norm_path(path)).stem
    s=(stem+" "+str(name).lower())
    s=re.sub(r"\b(left|right|front|back|top|bottom|small|large|med|medium|short|long|low|high)\b"," ",s)
    s=re.sub(r"[_\-\s]?(?:l|r)\d*$","",s)
    s=re.sub(r"[_\-\s]?\d+[a-z]?$","",s)
    s=re.sub(r"[^a-z0-9]+"," ",s).strip()
    toks=[t for t in s.split() if t not in {"gmod","prop","props","static","misc"}]
    return " ".join(toks[:6]) or stem

def maxdim(d):
    try:return max(float(x) for x in d)
    except:return None

def mindim(d):
    try:
        xs=[float(x) for x in d if float(x)>1e-6]
        return min(xs) if xs else None
    except:return None

def utility_for_category(cat):
    low=cat.lower()
    if any(x in low for x in ("rail","handrail","ramp","quarterpipe","halfpipe","ledge","hubba","curb","stairs","platform")): return 6
    if any(x in low for x in ("bench","table","plank","ladder","beam","barrier","fence","pipe")): return 5
    if any(x in low for x in ("crate","box","pallet","barrel","canister","street","sign","cone","cart","bollard")): return 4
    if any(x in low for x in ("furniture","chair","couch","desk","locker","shelf","cabinet")): return 2
    if "fun" in low or "playground" in low: return 3
    return 2

thumb_by={}
for r in THUMBS.get("records",[]):
    thumb_by[(r.get("source"),norm_path(r.get("runtime_mesh_path")))] = r

fnv_by={norm_path(r["source_path"]):r for r in FNV["records"]}
gmod_by={norm_path(r["source_model"]):r for r in GMOD["records"]}

# Step 2/3/4: unified prop quality + redundancy ledger.
ledger=[]
groups=collections.defaultdict(list)
category_counts=collections.Counter()
source_counts=collections.Counter()
for idx,r in enumerate(FINAL["ready_records"],1):
    src=r["source"]; cat=r["menu_category"]; srcpath=norm_path(r["source_path"])
    dims=r.get("dimensions") or []
    md=maxdim(dims); mn=mindim(dims)
    flags=[]
    if md is None: flags.append("missing_dimensions")
    else:
        if md<5: flags.append("very_small")
        if md>1800: flags.append("very_large_for_default_browser")
    if mn is not None and md and md/mn>120: flags.append("extreme_thinness_review")
    thumb=thumb_by.get((src,norm_path(r.get("runtime_mesh_path"))))
    thumb_ok=bool(thumb and thumb.get("status")=="ok")
    form_ok=bool(r.get("form_binding"))
    collision=True # final FNV set is static-clean; final GMod set was selected only from collision-bearing conversions
    materials_ok=True
    mass=None; triangles=r.get("triangles")
    authored_movable=None
    if src.startswith("Garry"):
        g=gmod_by.get(srcpath,{})
        mass=g.get("mass")
        authored_movable=(mass is not None and float(mass)>0.001)
        materials_ok=bool(g.get("materials_resolve",False))
    static_score=45
    static_score += 15 if form_ok else 0
    static_score += 10 if thumb_ok else 0
    static_score += 10 if collision else 0
    static_score += 10 if materials_ok else 0
    static_score += 10 if not any(x in flags for x in ("very_small","very_large_for_default_browser")) else 0
    util=utility_for_category(cat)
    key=variant_key(r.get("runtime_mesh_path"),r.get("display_name"))
    row={
      "index":idx,"source":src,"category":cat,"display_name":r.get("display_name"),
      "source_path":r.get("source_path"),"runtime_mesh_path":r.get("runtime_mesh_path"),
      "form_binding":r.get("form_binding"),"dimensions":dims,"max_dimension":md,"min_nonzero_dimension":mn,
      "triangles":triangles,"mass":mass,"authored_movable":authored_movable,
      "thumbnail_ok":thumb_ok,"form_binding_ok":form_ok,"collision_evidence":collision,"materials_resolved":materials_ok,
      "static_quality_score":min(static_score,100),"skate_utility_score":util,
      "variant_key":key,"flags":flags,
      "runtime_validation":"pending_human"
    }
    ledger.append(row); groups[key].append(idx-1); category_counts[(src,cat)]+=1; source_counts[src]+=1

redundant=[]
for key,ix in groups.items():
    if len(ix)<2: continue
    rows=[ledger[i] for i in ix]
    # Similarity signal only. Keep all until human/menu review.
    redundant.append({
      "variant_key":key,"count":len(rows),
      "members":[{"index":x["index"],"source":x["source"],"category":x["category"],"display_name":x["display_name"],"runtime_mesh_path":x["runtime_mesh_path"],"dimensions":x["dimensions"]} for x in rows],
      "status":"review_only_no_automatic_removal"
    })
redundant.sort(key=lambda x:(-x["count"],x["variant_key"]))

# Replacement reserve: low utility first, then redundant membership, then lower quality.
redundant_indexes={m["index"] for g in redundant for m in g["members"]}
for r in ledger:
    r["redundancy_signal"]=r["index"] in redundant_indexes
    r["replacement_score"]=(7-r["skate_utility_score"])*12 + (12 if r["redundancy_signal"] else 0) + max(0,90-r["static_quality_score"])
replacement=sorted(ledger,key=lambda r:(-r["replacement_score"],r["source"],r["category"],r["display_name"] or ""))[:40]

# Step 6/7/8: GMod collision/scale/material dependency audit.
gmod_rows=[]
unique_material_files={}
gmod_scale_flags=collections.Counter()
for r in GMOD["records"]:
    dims=r.get("dimensions") or []
    md=maxdim(dims)
    cat=r["category"]
    flags=[]
    per_max={
      "Skate - Rails Fences Barriers":650,
      "Skate - Benches Tables":400,
      "Skate - Planks Ladders Beams":350,
      "Physics - Crates Boxes Pallets":250,
      "Physics - Barrels Canisters":180,
      "Street - Signs Cones Trash Carts":300,
      "Environment - Furniture":300,
      "Fun - Playground Misc":300,
    }.get(cat,1000)
    if md is not None and md>per_max: flags.append("over_curated_category_max")
    if md is not None and md<5: flags.append("very_small")
    for f in flags:gmod_scale_flags[f]+=1
    mats=[]
    for m in r.get("materials",[]):
        mr={"vmt":m.get("vmt")}
        for k in ("base","normal"):
            q=m.get(k)
            if q:
                p=Path(q)
                mr[k]={"path":str(p),"exists":p.exists(),"bytes":p.stat().st_size if p.exists() else None,"sha256":sha(p) if p.exists() else None}
                if p.exists():unique_material_files[str(p).lower()]=mr[k]
        mats.append(mr)
    mass=r.get("mass")
    gmod_rows.append({
      "source_model":r["source_model"],"category":cat,"dimensions":dims,"max_dimension":md,
      "mass":mass,"authored_movable":bool(mass is not None and float(mass)>0.001),
      "havok_material":r.get("havok_material"),"source_surfaceprop":r.get("source_surfaceprop"),
      "materials_resolve":r.get("materials_resolve"),"scale_flags":flags,"materials":mats
    })

# Step 9: FNV dependency hints.
fnv_dependency_counts=collections.Counter()
fnv_rows=[]
for r in FNV["records"]:
    p=norm_path(r["source_path"])
    m=re.match(r"meshes/(dlc\d+|dlc[0-9a-z]+|nvdlc\d+|honesthearts|oldworldblues|lonesomeroad|deadmoney|gunrunnersarsenal)/",p)
    hint=m.group(1) if m else "base_or_shared"
    fnv_dependency_counts[hint]+=1
    fnv_rows.append({
      "source_path":r["source_path"],"category":r["menu_category"],
      "form_plugin":r["form_plugin"],"formid_file":r["formid_file"],"edid":r.get("edid"),
      "content_path_hint":hint,"runtime_validation":"pending_human"
    })

# Step 11/12/13/14: deterministic representative runtime batches + validation ledger.
by_cat=collections.defaultdict(list)
for r in ledger: by_cat[(r["source"],r["category"])].append(r)
selected=[]
seen=set()
for key,rows in sorted(by_cat.items(),key=lambda x:(x[0][0],x[0][1])):
    rows=sorted(rows,key=lambda r:(-r["skate_utility_score"],abs((r["max_dimension"] or 0)-150),r["display_name"] or ""))
    for r in rows[:2]:
        if r["index"] not in seen:selected.append(r);seen.add(r["index"])
# add dimension extremes per source
for src in sorted(source_counts):
    rows=[r for r in ledger if r["source"]==src and r["max_dimension"] is not None]
    for r in ([min(rows,key=lambda x:x["max_dimension"]),max(rows,key=lambda x:x["max_dimension"])] if rows else []):
        if r["index"] not in seen:selected.append(r);seen.add(r["index"])
batches=[]
for i in range(0,len(selected),12):
    members=selected[i:i+12]
    batches.append({
      "batch":i//12+1,
      "members":[{
        "index":r["index"],"source":r["source"],"category":r["category"],"display_name":r["display_name"],
        "plugin":r["form_binding"].get("plugin"),"formid_file":r["form_binding"].get("formid_file"),
        "edid":r["form_binding"].get("edid"),"runtime_mesh_path":r["runtime_mesh_path"]
      } for r in members],
      "test_checks":["spawn/form resolves","visual scale plausible","texture/material correct","collision blocks player appropriately","stable on contact","movability/Physgun behavior only if intended","remove/cleanup succeeds"],
      "status":"pending_human"
    })
validation_ledger=[{
    "index":r["index"],"source":r["source"],"display_name":r["display_name"],
    "plugin":r["form_binding"].get("plugin"),"formid_file":r["form_binding"].get("formid_file"),
    "edid":r["form_binding"].get("edid"),
    "checks":{"spawn":"pending","scale":"pending","materials":"pending","collision":"pending","contact_stability":"pending","cleanup":"pending"},
    "overall":"pending_human"
} for r in ledger]

# Step 15/16: THUG2 extraction review queue.
spatial_by={(r["level"],r["identifier"]):r for r in SPATIAL["records"]}
cat_weight={
 "Skate - Rails Handrails":10,
 "Skate - Quarterpipes Halfpipes Ramps":10,
 "Skate - Ledges Hubbas Curbs":9,
 "Skate - Stairs Platforms Misc":8,
 "Street - Benches Tables Chairs":6,
 "Street - Fences Barriers Poles Pipes":6,
}
thug_queue=[]
for r in THUG["records"]:
    if r["classification"]!="spatial_geometry_candidate":continue
    sp=spatial_by.get((r["level"],r["identifier"]),{})
    leaves=sp.get("candidate_leaves",[])
    nearest=leaves[0]["box_distance"] if leaves else None
    leaf_count=len(leaves)
    score=cat_weight.get(r["category"],5)
    score += {"high":5,"medium":3,"review":1}.get(r.get("confidence"),0)
    if leaf_count<=5: score+=4
    elif leaf_count<=10: score+=3
    elif leaf_count<=20: score+=1
    if nearest is not None:
        if nearest==0:score+=4
        elif nearest<=25:score+=3
        elif nearest<=100:score+=1
    first=leaves[0] if leaves else None
    if first and first.get("max_dim",0)>4500:score-=3
    thug_queue.append({
      "level":r["level"],"identifier":r["identifier"],"category":r["category"],
      "confidence":r.get("confidence"),"position":r.get("position"),"candidate_leaf_count":leaf_count,
      "nearest_box_distance":nearest,"top_leaf":first,"promotion_review_score":score,
      "status":"visual_leaf_review_required_not_promoted"
    })
thug_queue.sort(key=lambda r:(-r["promotion_review_score"],r["candidate_leaf_count"],r["level"],r["identifier"]))

# Step 17/18/19: menu budget, native icon coverage, payload/provenance summary.
menu_budget={
 "current_ready":len(ledger),"target_range":[300,320],"first_wave_target":310,
 "reserved_thug2_review_slots":20,
 "first_wave_policy":"Validate/promote up to 20 THUG2 standalone props to reach 310. Do not remove current props merely to hit 300.",
 "later_policy":"After 310, prefer replacing low-utility/redundant current entries rather than growing past 320.",
 "replacement_reserve":[{"index":r["index"],"source":r["source"],"category":r["category"],"display_name":r["display_name"],"replacement_score":r["replacement_score"],"variant_key":r["variant_key"]} for r in replacement],
 "top_thug2_review_candidates":thug_queue[:20]
}
icon_cov={
 "gmod_props":NATIVE.get("gmod_props",120),
 "native_spawnicons_found":NATIVE.get("native_spawnicons_found",0),
 "native_spawnicons_missing":NATIVE.get("native_spawnicons_missing",120),
 "fallback_geometry_previews_available":sum(1 for r in ledger if r["source"].startswith("Garry") and r["thumbnail_ok"]),
 "policy":"Keep generated geometry previews as support fallback. Final Q-menu runtime must preserve real GMod SpawnIcon behavior; do not call these native icons."
}
provenance={
 "ready_total":len(ledger),"sources":dict(source_counts),
 "form_binding_count":sum(r["form_binding_ok"] for r in ledger),
 "thumbnail_ok_count":sum(r["thumbnail_ok"] for r in ledger),
 "gmod_unique_material_files":len(unique_material_files),
 "gmod_missing_material_files":[v["path"] for v in unique_material_files.values() if not v["exists"]],
 "fnv_content_path_hints":dict(fnv_dependency_counts),
 "thug2_spatial_candidates":len(thug_queue),
 "generated_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()
}

outputs={
 "catalog_quality_ledger.json":{"purpose":"Unified static prop quality/utility ledger. Runtime validation remains pending.","records":ledger},
 "redundancy_audit.json":{"purpose":"Possible variant/redundancy groups for later menu trimming. No automatic removals.","group_count":len(redundant),"groups":redundant},
 "category_balance.json":{"purpose":"Current ready-catalog category/source distribution.","source_counts":dict(source_counts),"category_counts":[{"source":k[0],"category":k[1],"count":v} for k,v in sorted(category_counts.items())]},
 "gmod_prop_dependency_audit.json":{"purpose":"GMod/Source prop scale, authored-mobility and material dependency audit.","prop_count":len(gmod_rows),"authored_movable":sum(r["authored_movable"] for r in gmod_rows),"scale_flag_counts":dict(gmod_scale_flags),"unique_material_files":len(unique_material_files),"records":gmod_rows},
 "fnv_prop_dependency_hints.json":{"purpose":"FNV prop form/path dependency hints; not a substitute for load-order runtime validation.","counts":dict(fnv_dependency_counts),"records":fnv_rows},
 "runtime_test_batches.json":{"purpose":"Representative human prop playtest batches with stable source/form identity.","batch_count":len(batches),"selected_count":len(selected),"batches":batches},
 "runtime_validation_ledger.json":{"purpose":"Per-prop human validation ledger; all entries begin pending.","records":validation_ledger},
 "thug2_promotion_queue.json":{"purpose":"Rank the 85 THUG2 spatial geometry candidates for visual leaf review/extraction. Ranking is not promotion.","candidate_count":len(thug_queue),"top20":thug_queue[:20],"records":thug_queue},
 "menu_budget.json":menu_budget,
 "gmod_spawnicon_coverage.json":icon_cov,
 "prop_payload_provenance.json":provenance,
}
for name,data in outputs.items():
    (OUT/name).write_text(json.dumps(data,indent=2),encoding="utf-8")

summary={
 "purpose":"Prop-focused support phase 3 status.",
 "ready_props":len(ledger),
 "source_counts":dict(source_counts),
 "redundancy_groups":len(redundant),
 "representative_test_props":len(selected),
 "test_batches":len(batches),
 "gmod_props":len(gmod_rows),
 "gmod_authored_movable":sum(r["authored_movable"] for r in gmod_rows),
 "gmod_material_files":len(unique_material_files),
 "gmod_native_spawnicons_found":icon_cov["native_spawnicons_found"],
 "gmod_fallback_previews":icon_cov["fallback_geometry_previews_available"],
 "thug2_spatial_candidates_ranked":len(thug_queue),
 "thug2_top20_ready_for_visual_review":20 if len(thug_queue)>=20 else len(thug_queue),
 "menu_current":len(ledger),
 "menu_first_wave_target":310,
 "runtime_playtest":"not_run",
 "runtime_or_astra_code_modified":False,
}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))