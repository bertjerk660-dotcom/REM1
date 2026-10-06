from pathlib import Path
import json,math
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=json.loads((ROOT/"build/prepared/thug2_skateboard_asset_handoff/manifest.json").read_text())
OUT=ROOT/"build/prepared/thug2_skateboard_asset_handoff/scale_attachment_analysis.json"
glb=SRC["source_board_glb"][0]["stats"]
src_dims=glb["dimensions"]
live={x["name"]:x for x in SRC["live_nifs"] if x.get("stats") and x["stats"].get("dimensions")}
rows=[]
for name,x in live.items():
    dims=x["stats"]["dimensions"]
    ratios=[dims[i]/src_dims[i] if src_dims[i] else None for i in range(3)]
    rows.append({
        "name":name,"source_dimensions":src_dims,"live_dimensions":dims,
        "axis_scale_ratios":ratios,
        "uniform_ratio_mean":sum(ratios)/3,
        "uniform_ratio_spread":max(ratios)-min(ratios),
        "root_type":x["stats"]["root_type"],"root_name":x["stats"]["root_name"],
        "extras":x["stats"]["extras"]
    })
res={
 "purpose":"Compare authentic THUG2 board conversion dimensions with staged FNV board containers; no runtime attachment transforms are changed.",
 "source_glb_dimensions":src_dims,
 "comparisons":rows,
 "findings":[
   "skateboard.nif/skateboard_visual.nif/skateworld.nif preserve the same visual dimensions as each other.",
   "skateheldx.nif is larger because the Fallout held-weapon container applies a transform around the authentic board hierarchy.",
   "This analysis supplies scale evidence only. Hand/foot attachment transforms and animated board placement remain Astra-owned."
 ],
 "handoff_rule":"Do not alter authentic board geometry to solve attachment. Adjust host-container/bone attachment transforms only after Astra validates the correct state/bone mapping."
}
OUT.write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))