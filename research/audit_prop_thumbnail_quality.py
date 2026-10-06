from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
MAN=ROOT/"build/prepared/final_prop_catalog_thumbnails/manifest.json"
OUT=ROOT/"build/prepared/final_prop_catalog_thumbnails/quality_audit.json"
m=json.loads(MAN.read_text(encoding="utf-8"))
rows=[]; bad=[]
for r in m["records"]:
    p=ROOT/r["thumbnail"]
    q={"source":r["source"],"source_path":r["source_path"],"thumbnail":r["thumbnail"],"exists":p.exists()}
    flags=[]
    if p.exists():
        im=Image.open(p).convert("RGBA")
        a=im.getchannel("A")
        bbox=a.getbbox()
        nonzero=sum(1 for v in a.getdata() if v>8)
        occ=nonzero/(im.width*im.height)
        q.update({"size":im.size,"bbox":bbox,"occupancy":round(occ,4),"bytes":p.stat().st_size})
        if im.size!=(128,128):flags.append("wrong_size")
        if not bbox:flags.append("empty")
        else:
            bw=bbox[2]-bbox[0]; bh=bbox[3]-bbox[1]
            if (bw<30 or bh<20) and not (bh>100 and occ>0.025):flags.append("too_small")
            if bw>126 or bh>126:flags.append("touches_edge")
        if occ<0.02:flags.append("low_occupancy")
        if occ>0.82:flags.append("high_occupancy")
    else: flags.append("missing")
    q["flags"]=flags
    rows.append(q)
    if flags:bad.append(q)
res={"purpose":"Quality audit of 290 local prop previews used only as support/fallback thumbnails.",
     "count":len(rows),"clean":len(rows)-len(bad),"flagged":len(bad),
     "flag_counts":{},"records":rows}
for r in bad:
    for f in r["flags"]:res["flag_counts"][f]=res["flag_counts"].get(f,0)+1
OUT.write_text(json.dumps(res,indent=2))
print(json.dumps({k:res[k] for k in ("count","clean","flagged","flag_counts")},indent=2))
