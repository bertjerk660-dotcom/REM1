from pathlib import Path
import json,re,collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/thug2_prop_catalog"
SRC=BASE/"embedded_prop_targets.json"
OUT=BASE/"embedded_prop_targets_curated.json"
m=json.loads(SRC.read_text(encoding="utf-8"))

QUOTAS=[
    ("Skate - Quarterpipes Halfpipes Ramps",24,("quarterpipe","halfpipe","ramp","kicker")),
    ("Skate - Rails Handrails",28,("handrail","rail")),
    ("Skate - Ledges Hubbas Curbs",24,("hubba","ledge","curb")),
    ("Street - Benches Tables Chairs",14,("bench","table","chair")),
    ("Street - Fences Barriers Poles Pipes",18,("fence","barrier","pole","pipe")),
    ("Skate - Stairs Platforms Misc",12,("stair","platform","planter","crate")),
]
TARGET=sum(x[1] for x in QUOTAS)

REJECT_PARTS=(
    "shadow","trg_","trigger","bullafter","bullbefore","collision","col_",
    "script","goal","gap_","dummy","lightmap","restart","camera","bounding",
)

def family(name):
    # Collapse numbered scene variants to a single extraction family per level.
    x=re.sub(r'(?i)(?:_?\d+[a-z]?)$', '', name)
    x=re.sub(r'(?i)(?:_0?\d+)(?=_|$)', '_#', x)
    x=re.sub(r'#+','#',x)
    return x.lower()

def category_for(x):
    terms=set(x["terms"])
    low=x["identifier"].lower()
    if any(y in low for y in REJECT_PARTS):return None
    for cat,_quota,tags in QUOTAS:
        if any(t in terms or t in low for t in tags):
            return cat
    return None

# Build one representative per (level, semantic family), favoring score/evidence.
best={}
for x in m["targets"]:
    cat=category_for(x)
    if not cat:continue
    for level in x["levels"]:
        key=(cat,level,family(x["identifier"]))
        candidate=dict(x)
        candidate["category"]=cat
        candidate["level"]=level
        candidate["family"]=key[2]
        prev=best.get(key)
        rank=(candidate["priority_score"],candidate["count"],-len(candidate["identifier"]))
        if prev is None:
            best[key]=candidate
        else:
            prank=(prev["priority_score"],prev["count"],-len(prev["identifier"]))
            if rank>prank:best[key]=candidate

pool=list(best.values())
# Prefer high-scoring, but also diversify levels by penalizing repeated level selections.
selected=[]
used_keys=set()
level_counts=collections.Counter()
cat_counts=collections.Counter()

for cat,quota,_tags in QUOTAS:
    candidates=[x for x in pool if x["category"]==cat]
    while cat_counts[cat]<quota and candidates:
        candidates.sort(key=lambda x:(
            level_counts[x["level"]],
            -x["priority_score"],
            -x["count"],
            x["identifier"].lower()
        ))
        pick=candidates.pop(0)
        key=(pick["level"],pick["family"])
        if key in used_keys:continue
        used_keys.add(key)
        selected.append(pick)
        level_counts[pick["level"]]+=1
        cat_counts[cat]+=1

shortfalls={cat:quota-cat_counts[cat] for cat,quota,_ in QUOTAS if cat_counts[cat]<quota}

# Whole-level GLB/QB references for every selected level.
level_sources={}
for level in sorted({x["level"] for x in selected}):
    glbdir=BASE/"level_glb"/level
    qdir=BASE/"qb_decompiled"/level
    level_sources[level]={
        "whole_level_glbs":sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in glbdir.rglob("*.glb")) if glbdir.exists() else [],
        "decompiled_q_files":sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in qdir.rglob("*.q")) if qdir.exists() else [],
    }

result={
    "purpose":"Balanced THUG2 embedded skate/environment extraction queue. These are named scene targets, not standalone assets and not yet Q-menu entries.",
    "target_count":TARGET,
    "selected_count":len(selected),
    "category_counts":dict(cat_counts),
    "level_counts":dict(sorted(level_counts.items())),
    "shortfalls":shortfalls,
    "records":selected,
    "level_sources":level_sources,
    "handoff_steps":[
        "Use the named identifier and its decompiled level QB/scene records to locate the corresponding mesh leaves in that level's converted whole-level GLB.",
        "Split only the useful object geometry; preserve original THUG2 materials/shape where possible.",
        "Convert the separated object to a Fallout-compatible prop container and validate scale/collision independently.",
        "Only promoted standalone props become Q-menu content. Do not import the THUG2 map."
    ],
    "playtest":"not_applicable_yet"
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({
    "target_count":TARGET,"selected_count":len(selected),
    "category_counts":dict(cat_counts),"level_counts":dict(sorted(level_counts.items())),
    "shortfalls":shortfalls,
    "sample":[{"id":x["identifier"],"level":x["level"],"category":x["category"]} for x in selected[:40]]
},indent=2))