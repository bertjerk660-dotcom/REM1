from pathlib import Path
import json,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
P3=json.loads((ROOT/"build/prepared/prop_support_phase3/thug2_promotion_queue.json").read_text())
OUT=ROOT/"build/prepared/prop_support_phase4"
OUT.mkdir(parents=True,exist_ok=True)

QUOTAS={
 "Skate - Rails Handrails":6,
 "Skate - Quarterpipes Halfpipes Ramps":5,
 "Skate - Ledges Hubbas Curbs":4,
 "Street - Benches Tables Chairs":2,
 "Street - Fences Barriers Poles Pipes":2,
 "Skate - Stairs Platforms Misc":1,
}
assert sum(QUOTAS.values())==20
by=collections.defaultdict(list)
for r in P3["records"]: by[r["category"]].append(r)
for c in by: by[c].sort(key=lambda r:(-r["promotion_review_score"],r["candidate_leaf_count"],r["nearest_box_distance"] if r["nearest_box_distance"] is not None else 1e9,r["level"],r["identifier"]))
sel=[];short={}
for cat,q in QUOTAS.items():
    take=by.get(cat,[])[:q]
    sel+=take
    if len(take)<q:short[cat]=q-len(take)
if short:
    # backfill from remaining highest-ranked spatial candidates
    used={(r["level"],r["identifier"]) for r in sel}
    pool=[r for r in P3["records"] if (r["level"],r["identifier"]) not in used]
    pool.sort(key=lambda r:(-r["promotion_review_score"],r["candidate_leaf_count"],r["level"],r["identifier"]))
    for r in pool:
        if sum(short.values())<=0:break
        sel.append(r)
        k=next((k for k,v in short.items() if v>0),None)
        if k:short[k]-=1

res={
 "purpose":"Diversified first-wave THUG2 prop review set: preserve high-ranked candidates while avoiding a rail-heavy browser.",
 "target":20,"selected":len(sel),"quotas":QUOTAS,
 "category_counts":dict(collections.Counter(r["category"] for r in sel)),
 "records":sel,
 "policy":[
   "This replaces the purely score-sorted top20 only for first-wave review planning; the full 85-candidate rank remains intact.",
   "No candidate is spawn-ready until visual leaf identity, split, conversion, collision and runtime validation pass."
 ]
}
(OUT/"thug2_diversified_first_wave.json").write_text(json.dumps(res,indent=2),encoding="utf-8")
print(json.dumps({"selected":len(sel),"category_counts":res["category_counts"],"ids":[f"{r['level']}:{r['identifier']}" for r in sel]},indent=2))