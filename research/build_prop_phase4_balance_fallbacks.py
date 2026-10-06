from pathlib import Path
import json,math,collections,re
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
B=ROOT/"build/prepared/prop_support_phase4"
TAX=json.loads((B/"menu_taxonomy_v2.json").read_text())
RES=json.loads((B/"gmod_reserve_pool.json").read_text())
P3B=json.loads((ROOT/"build/prepared/prop_support_phase3/runtime_test_batches.json").read_text())
FINAL=json.loads((ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json").read_text())
OUT=B

RANGES={
 "Skate / Rails & Handrails":[32,42],
 "Skate / Ramps & Stairs":[28,36],
 "Skate / Ledges & Barriers":[24,32],
 "Skate / Benches & Tables":[32,45],
 "Skate / Beams Pipes & Ladders":[24,32],
 "Physics / Crates Boxes & Pallets":[20,30],
 "Physics / Barrels Canisters & Tires":[15,24],
 "Environment / Furniture":[24,36],
 "Street / Signs Lights & Clutter":[20,30],
 "Environment / Nature":[10,18],
 "Environment / Utility":[8,14],
 "Environment / Misc":[10,20],
}

planned=TAX["planned_bucket_counts"]
gaps=[]
for bucket,rng in RANGES.items():
    n=planned.get(bucket,0);lo,hi=rng
    if n<lo:state="deficit";delta=lo-n
    elif n>hi:state="excess";delta=n-hi
    else:state="within_target";delta=0
    gaps.append({"bucket":bucket,"planned_count":n,"target_min":lo,"target_max":hi,"state":state,"delta":delta})
gapres={
 "purpose":"Balance report for the planned 310-entry catalog. Ranges are design targets, not hard runtime constraints.",
 "planned_total":sum(planned.values()),"targets":gaps,
 "deficits":[x for x in gaps if x["state"]=="deficit"],
 "excesses":[x for x in gaps if x["state"]=="excess"],
 "guidance":"Future THUG2/reserve promotions should preferentially fill deficits; excess categories are first candidates for replacement rather than menu growth."
}
(OUT/"category_balance_target310.json").write_text(json.dumps(gapres,indent=2),encoding="utf-8")

def reserve_bucket(cat,path):
    s=(cat+" "+path).lower()
    if "rail" in s or "handrail" in s:return "Skate / Rails & Handrails"
    if any(x in s for x in ("ramp","stair","quarter","halfpipe","platform")):return "Skate / Ramps & Stairs"
    if any(x in s for x in ("barrier","fence","ledge","curb","hubba")):return "Skate / Ledges & Barriers"
    if any(x in s for x in ("bench","table","counter","desk")):return "Skate / Benches & Tables"
    if any(x in s for x in ("beam","plank","ladder","pipe","pole")):return "Skate / Beams Pipes & Ladders"
    if any(x in s for x in ("crate","box","pallet")):return "Physics / Crates Boxes & Pallets"
    if any(x in s for x in ("barrel","canister","drum","tire","wheel")):return "Physics / Barrels Canisters & Tires"
    if any(x in s for x in ("chair","couch","sofa","locker","shelf","cabinet","furniture")):return "Environment / Furniture"
    if any(x in s for x in ("sign","cone","cart","street","trash")):return "Street / Signs Lights & Clutter"
    return "Environment / Misc"

resrows=[]
for r in RES["records"]:
    rr=dict(r);rr["bucket"]=reserve_bucket(r["category"],r["source_model"]);resrows.append(rr)

def ready_bucket(r):
    # reuse taxonomy entries by exact model path
    model=r["runtime_mesh_path"].replace("\\","/").lower()
    t=next((x for x in TAX["current_entries"] if x["model"].lower()==model),None)
    return t["bucket"] if t else "Environment / Misc"

def dimdist(a,b):
    if not a or not b:return 999
    aa=sorted(max(float(x),.01) for x in a);bb=sorted(max(float(x),.01) for x in b)
    return sum(abs(math.log(x)-math.log(y)) for x,y in zip(aa,bb))

fallbacks={}
for i,r in enumerate(FINAL["ready_records"],1):
    b=ready_bucket(r)
    pool=[x for x in resrows if x["bucket"]==b]
    if not pool:pool=resrows
    ranked=sorted(pool,key=lambda x:(dimdist(r.get("dimensions"),x.get("dimensions")),-x.get("score",0),x["source_model"].lower()))
    fallbacks[str(i)]=[{
      "source_model":x["source_model"],"category":x["category"],"bucket":x["bucket"],
      "dimensions":x["dimensions"],"score":x["score"],"output_nif_relative":x["output_nif_relative"],
      "dimension_distance":round(dimdist(r.get("dimensions"),x.get("dimensions")),4)
    } for x in ranked[:3]]

fbres={
 "purpose":"Reserve replacement mapping for every current ready prop. Use only after a current prop fails runtime validation or a category is intentionally rebalanced.",
 "ready_count":len(FINAL["ready_records"]),"reserve_count":len(resrows),"fallbacks_by_ready_index":fallbacks
}
(OUT/"reserve_fallback_map.json").write_text(json.dumps(fbres,indent=2),encoding="utf-8")

# Add fallback alternatives to the 56 representative human test rows.
batches=[]
for batch in P3B["batches"]:
    nb=dict(batch);members=[]
    for m in batch["members"]:
        # resolve ready index by matching model/name/form
        idx=None
        for i,r in enumerate(FINAL["ready_records"],1):
            fb=r.get("form_binding",{})
            if m.get("formid_file")==fb.get("formid_file") and m.get("plugin")==fb.get("plugin"):
                idx=i;break
        mm=dict(m);mm["ready_index"]=idx;mm["reserve_fallbacks"]=fallbacks.get(str(idx),[])[:2] if idx else []
        members.append(mm)
    nb["members"]=members
    batches.append(nb)
testres={
 "purpose":"Representative prop runtime batches with precomputed GMod reserve fallbacks. Fallbacks stay inactive unless the tested default prop fails.",
 "batch_count":len(batches),"selected_count":sum(len(b["members"]) for b in batches),"batches":batches
}
(OUT/"runtime_test_batches_with_fallbacks.json").write_text(json.dumps(testres,indent=2),encoding="utf-8")
print(json.dumps({
 "planned_total":gapres["planned_total"],
 "deficits":gapres["deficits"],
 "excesses":gapres["excesses"],
 "fallback_ready_count":fbres["ready_count"],
 "test_props":testres["selected_count"]
},indent=2))