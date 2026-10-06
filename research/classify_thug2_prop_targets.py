from pathlib import Path
import json, re, collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/thug2_prop_catalog"
MAPPING=json.loads((BASE/"spatial_prop_candidates/mapping.json").read_text(encoding="utf-8"))
OUT=BASE/"target_classification.json"

semantic_markers=("gap","hit","transfer","script","bouncy")
rows=[]
for r in MAPPING["records"]:
    ident=r["identifier"]
    low=ident.lower()
    if r["status"]=="mapped":
        leafs=r.get("candidate_leaves",[])
        nearest=leafs[0]["box_distance"] if leafs else None
        confidence="review"
        if nearest is not None:
            rad=max(float(r.get("radius",400)),1)
            ratio=nearest/rad
            if ratio<=0.05 and len(leafs)<=8: confidence="high"
            elif ratio<=0.25: confidence="medium"
            else: confidence="review"
        cls="spatial_geometry_candidate"
        reason="Original QB position is available and has nearby converted level geometry leaves."
    else:
        if any(x in low for x in semantic_markers):
            cls="semantic_or_gap_identifier"
            reason="Identifier appears to describe a gap/trigger/hit/transfer semantic and has no object position binding."
        else:
            cls="unresolved_named_target"
            reason="No reliable Name-block/nearby QB position was recovered; keep as research only."
        confidence="not_ready"
    rows.append({
        "level":r["level"],"identifier":ident,"category":r["category"],
        "classification":cls,"confidence":confidence,"reason":reason,
        "position":r.get("pos"),
        "candidate_leaf_count":len(r.get("candidate_leaves",[])),
        "nearest_box_distance":(r.get("candidate_leaves") or [{}])[0].get("box_distance")
    })

counts=collections.Counter(x["classification"] for x in rows)
conf=collections.Counter(x["confidence"] for x in rows)
result={
    "purpose":"Classify all 106 THUG2 environment/skate targets for support-lane extraction planning.",
    "target_count":len(rows),
    "classification_counts":dict(counts),
    "confidence_counts":dict(conf),
    "ready_for_geometry_review":sum(x["classification"]=="spatial_geometry_candidate" for x in rows),
    "not_ready_or_semantic":sum(x["classification"]!="spatial_geometry_candidate" for x in rows),
    "records":rows,
    "policy":[
        "Do not force script/gap/semantic identifiers into standalone prop conversion.",
        "Spatial candidates still require visual/geometry sanity review before splitting/conversion.",
        "Only independently validated THUG2 objects may replace lower-priority entries in the compact Q-menu catalog."
    ]
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("target_count","classification_counts","confidence_counts","ready_for_geometry_review","not_ready_or_semantic")},indent=2))