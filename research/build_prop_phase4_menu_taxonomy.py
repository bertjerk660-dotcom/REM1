from pathlib import Path
import json,re,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
CAT=json.loads((ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json").read_text())
WAVE=json.loads((ROOT/"build/prepared/prop_support_phase4/thug2_diversified_first_wave.json").read_text())
OUT=ROOT/"build/prepared/prop_support_phase4"
OUT.mkdir(parents=True,exist_ok=True)

def bucket(cat,path=""):
    s=(cat+" "+path).lower()
    if "rail" in s or "handrail" in s:return "Skate / Rails & Handrails"
    if any(x in s for x in ("ramp","stair","quarterpipe","halfpipe","platform")):return "Skate / Ramps & Stairs"
    if any(x in s for x in ("ledge","hubba","curb","barrier","fence")):return "Skate / Ledges & Barriers"
    if any(x in s for x in ("bench","table","counter","desk")):return "Skate / Benches & Tables"
    if any(x in s for x in ("plank","beam","ladder","pipe","pole")):return "Skate / Beams Pipes & Ladders"
    if any(x in s for x in ("crate","box","pallet")):return "Physics / Crates Boxes & Pallets"
    if any(x in s for x in ("barrel","canister","drum","tire","wheel")):return "Physics / Barrels Canisters & Tires"
    if any(x in s for x in ("chair","couch","sofa","storage","locker","shelf","furniture")):return "Environment / Furniture"
    if any(x in s for x in ("sign","cone","trash","cart","street","lamp")):return "Street / Signs Lights & Clutter"
    if any(x in s for x in ("rock","tree","plant","nature")):return "Environment / Nature"
    if any(x in s for x in ("vending","terminal","utility")):return "Environment / Utility"
    return "Environment / Misc"

def aliases(name,cat,path):
    s=" ".join([str(name or ""),cat,path])
    t=set(x for x in re.split(r"[^a-zA-Z0-9]+",s.lower()) if len(x)>=2)
    syn={
      "rail":{"rail","handrail","grind"},
      "ramp":{"ramp","kicker","quarterpipe","halfpipe"},
      "bench":{"bench","seat"},
      "table":{"table","desk","counter"},
      "crate":{"crate","box"},
      "barrel":{"barrel","drum","canister"},
      "fence":{"fence","barrier"},
    }
    for k,v in syn.items():
        if k in t:t|=v
    return sorted(t)

rows=[];counts=collections.Counter()
for i,r in enumerate(CAT["ready_records"],1):
    b=bucket(r["menu_category"],r["source_path"])
    counts[b]+=1
    rows.append({
      "id":f"ready_{i:03d}","source":r["source"],"display_name":r["display_name"],
      "bucket":b,"original_category":r["menu_category"],
      "model":r["runtime_mesh_path"].replace("\\","/"),"form_binding":r["form_binding"],
      "search_aliases":aliases(r["display_name"],r["menu_category"],r["source_path"]),
      "state":"ready_runtime_validation_pending"
    })

future=[]
for i,r in enumerate(WAVE["records"],1):
    b=bucket(r["category"],r["identifier"])
    counts[b]+=1
    future.append({
      "id":f"thug2_future_{i:02d}","source":"THUG2","display_name":r["identifier"],
      "bucket":b,"original_category":r["category"],"level":r["level"],
      "search_aliases":aliases(r["identifier"],r["category"],r["identifier"]),
      "state":"future_visual_leaf_review_not_spawn_ready"
    })

res={
 "purpose":"Source-neutral prop browser taxonomy for the future real GMod Q-menu adapter. Does not implement the menu.",
 "current_ready_count":len(rows),"planned_first_wave_count":len(rows)+len(future),
 "target_range":[300,320],"current_entries":rows,"planned_thug2_first_wave":future,
 "planned_bucket_counts":dict(sorted(counts.items())),
 "policy":[
   "Keep one practical cross-game taxonomy rather than separate game-specific dumps.",
   "Expose source identity as metadata/filter, not as a requirement to duplicate categories.",
   "THUG2 future entries stay hidden until split/converted/validated.",
   "Search aliases are data for the real/ported GMod search behavior, not a replacement UI."
 ]
}
(OUT/"menu_taxonomy_v2.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({"current":res["current_ready_count"],"first_wave":res["planned_first_wave_count"],"buckets":res["planned_bucket_counts"]},indent=2))