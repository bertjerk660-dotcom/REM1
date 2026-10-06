from pathlib import Path
import json, re, collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/thug2_prop_catalog"
SRC=BASE/"qb_prop_keyword_index.json"
OUT=BASE/"embedded_prop_targets.json"
SUMMARY=BASE/"embedded_prop_targets_summary.json"

m=json.loads(SRC.read_text(encoding="utf-8"))
TARGET_TERMS=(
    "bench","rail","fence","ledge","ramp","barrier","table","chair","stair",
    "pole","pipe","crate","box","sign","curb","planter","block","wall","platform",
    "quarterpipe","halfpipe","kicker","hubba","handrail","bollard"
)
# Engine/script/state names that are evidence about gameplay but not separable art names.
REJECT_PREFIX=(
    "ncomp_","terrain_","gap_","checksum","script","spawn","goal","combo",
    "create","destroy","trigger","nodearray","array_","level","global",
)
REJECT_EXACT={
    "railnode","rail_node","ledge","boundingbox","boxdimsstart","boxdimsmid",
    "boxdimsend","boxdims","climbingnode","noclimbing","metal_pole",
    "rail","fence","bench","table","chair","stairs","stair","pipe","pole",
}
REJECT_PARTS=(
    "railnode","boxdims","boundingbox","climbingnode","grindtype","terrain_",
    "exclude","script","goal_","score","combo","camera","skater","ped_","veh_",
    "particle","lightmap","checksum","debug","test_","spawnpoint","restart",
)

# Names which look like actual scene/mesh object identifiers tend to contain a
# descriptive noun plus a qualifier (location/material/number/direction).
def classify(identifier):
    low=identifier.lower()
    terms=sorted({t for t in TARGET_TERMS if t in low})
    if not terms:return None
    if low in REJECT_EXACT:return None
    if low.startswith(REJECT_PREFIX):return None
    if any(x in low for x in REJECT_PARTS):return None
    if len(identifier)<6 or len(identifier)>90:return None
    if re.fullmatch(r"[0-9a-fA-F]+",identifier):return None
    # Reject names that are mostly generic parameter/property vocabulary.
    generic=("position","rotation","matrix","offset","height","width","length",
             "radius","angle","index","count","flag","type","class","param",
             "min","max","start","end","mid","name","id")
    tokens=[x.lower() for x in re.split(r"[_\-\s]+",identifier) if x]
    if tokens and sum(t in generic for t in tokens)>=max(2,len(tokens)-1):
        return None
    return terms

targets=[]
for x in m["identifiers"]:
    ident=x["identifier"]
    terms=classify(ident)
    if not terms:continue
    files=[f for f in x.get("files",[]) if "_sky/" not in f and not f.startswith("mainmenu/")]
    if not files:continue
    # Score for useful environment/skate nouns and human-readable specificity.
    low=ident.lower()
    score=0
    weights={
        "bench":12,"handrail":12,"rail":9,"fence":8,"ledge":10,"ramp":10,
        "barrier":8,"table":7,"chair":7,"stair":8,"curb":9,"planter":6,
        "crate":6,"box":2,"pipe":6,"pole":5,"platform":8,"quarterpipe":14,
        "halfpipe":14,"kicker":12,"hubba":12,"bollard":8,"sign":4,"wall":2,
    }
    score+=sum(weights.get(t,1) for t in terms)
    if "_" in ident:score+=2
    if re.search(r"[A-Z].*[a-z]|[a-z].*[A-Z]",ident):score+=2
    if re.search(r"\d",ident):score+=1
    if any(k in low for k in ("park","street","plaza","school","hotel","shop","bridge","concrete","metal","wood")):score+=3
    # Very high repetition tends to be a class/semantic label rather than a unique scene object.
    count=int(x.get("count",0))
    if count>80:score-=5
    elif count<=10:score+=2
    targets.append({
        "identifier":ident,"count":count,"terms":terms,"files":files,
        "levels":sorted({f.split("/",1)[0] for f in files}),
        "priority_score":score
    })

# De-duplicate case-insensitively, keeping the stronger evidence row.
best={}
for x in targets:
    k=x["identifier"].lower()
    prev=best.get(k)
    if prev is None or (x["priority_score"],x["count"])>(prev["priority_score"],prev["count"]):
        best[k]=x
targets=list(best.values())
targets.sort(key=lambda x:(-x["priority_score"],-x["count"],x["identifier"].lower()))

# Keep a bounded handoff set. It is a scene-correlation queue, not a player menu.
MAX_TOTAL=5000
selected=targets[:MAX_TOTAL]

by_level=collections.defaultdict(list)
for x in selected:
    for level in x["levels"]:
        by_level[level].append(x["identifier"])
for level in by_level:
    by_level[level]=sorted(set(by_level[level]))

# Connect each level to the converted whole-level GLB(s), if present.
level_sources={}
for level in sorted(by_level):
    glbdir=BASE/"level_glb"/level
    glbs=sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in glbdir.rglob("*.glb")) if glbdir.exists() else []
    qdir=BASE/"qb_decompiled"/level
    qfiles=sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in qdir.rglob("*.q")) if qdir.exists() else []
    level_sources[level]={"whole_level_glbs":glbs,"decompiled_q_files":qfiles}

result={
    "purpose":"Filtered THUG2 embedded environment/skatability identifiers for later scene-to-GEOM correlation. These are extraction targets, not yet standalone spawnable props.",
    "source_keyword_identifier_count":len(m["identifiers"]),
    "filtered_candidates_before_cap":len(targets),
    "selected_target_count":len(selected),
    "max_targets":MAX_TOTAL,
    "targets":selected,
    "by_level":dict(sorted(by_level.items())),
    "level_sources":level_sources,
    "rules":{
        "include_terms":list(TARGET_TERMS),
        "reject_prefixes":list(REJECT_PREFIX),
        "reject_exact":sorted(REJECT_EXACT),
        "reject_parts":list(REJECT_PARTS)
    },
    "handoff":"Astra/model-extraction work should correlate these names against the matching level QB/scene data and whole-level GLBs, then split only useful geometry such as benches, rails, ledges and ramps. Do not import THUG2 maps."
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
terms=collections.Counter(t for x in selected for t in x["terms"])
summary={
    "filtered_candidates_before_cap":len(targets),
    "selected_target_count":len(selected),
    "levels":{k:len(v) for k,v in sorted(by_level.items())},
    "term_counts":dict(terms.most_common()),
    "top_targets":selected[:60],
    "note":"Targets require GEOM/QB correlation and splitting before they can become independent FNV/GMod-menu props."
}
SUMMARY.write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
