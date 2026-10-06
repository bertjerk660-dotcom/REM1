from pathlib import Path
import json,hashlib,math,re
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/prop_support_phase4"
LEAF=json.loads((BASE/"thug2_diversified_leaf_review.json").read_text())
OUT=BASE
PRE=BASE/"leaf_previews"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

# Review queue: all high priority first, then medium. This is not a conversion pass.
q=[]
for r in LEAF["records"]:
    first=(r.get("leaf_metrics") or [{}])[0]
    q.append({
      "rank":r["rank"],"level":r["level"],"identifier":r["identifier"],"category":r["category"],
      "review_status":r["review_status"],"isolation_score":r["isolation_score"],
      "candidate_leaf_count":r["candidate_leaf_count"],
      "top_leaf_node":first.get("node"),"top_leaf_mesh":first.get("mesh"),
      "top_leaf_triangles":first.get("triangles"),"top_leaf_dimensions":first.get("dimensions"),
      "box_distance":first.get("box_distance"),
      "preview":r["preview"],"source_glb":r["source_glb"],
      "next_action":"human/model visual confirmation of object identity and isolation",
      "conversion_state":"blocked_pending_visual_confirmation"
    })
q.sort(key=lambda x:(0 if x["review_status"]=="high_review_priority" else 1,-x["isolation_score"],x["rank"]))
(OUT/"thug2_conversion_review_queue.json").write_text(json.dumps({
  "purpose":"Ordered THUG2 prop review queue. No candidate is conversion-approved until visual identity/isolation is confirmed.",
  "count":len(q),
  "high_priority":sum(x["review_status"]=="high_review_priority" for x in q),
  "records":q
},indent=2),encoding="utf-8")

# Make a single local contact sheet for quick human/Astra visual review.
thumb_w,thumb_h=480,180
cols=2; rows=math.ceil(len(q)/cols)
sheet=Image.new("RGB",(cols*thumb_w,rows*(thumb_h+36)),(18,18,18))
dr=ImageDraw.Draw(sheet)
for i,item in enumerate(q):
    x=(i%cols)*thumb_w; y=(i//cols)*(thumb_h+36)
    p=ROOT/item["preview"]
    if p.exists():
        im=Image.open(p).convert("RGB")
        # crop first panel because source preview contains top 3 leaf candidates;
        # keep all panels by fitting full source horizontally.
        im.thumbnail((thumb_w-8,thumb_h-8))
        px=x+(thumb_w-im.width)//2; py=y+4+(thumb_h-im.height)//2
        sheet.paste(im,(px,py))
    label=f"{item['rank']:02d} {item['level']} {item['identifier']} | {item['review_status']} score={item['isolation_score']}"
    dr.text((x+6,y+thumb_h+4),label[:78],fill=(235,235,235))
sheet_path=OUT/"thug2_top20_contact_sheet.png"
sheet.save(sheet_path,optimize=True)

manifest={
 "purpose":"Visual review packet for top-20 THUG2 prop candidates.",
 "contact_sheet":str(sheet_path.relative_to(ROOT)).replace("\\","/"),
 "contact_sheet_sha256":sha(sheet_path),
 "contact_sheet_size":sheet.size,
 "review_queue":"build/prepared/prop_support_phase4/thug2_conversion_review_queue.json",
 "rule":"Visual confirmation is still required before geometry splitting/conversion. This packet is evidence, not promotion."
}
(OUT/"review_packet.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps({"queue":len(q),"high_priority":sum(x["review_status"]=="high_review_priority" for x in q),"contact_sheet":str(sheet_path),"sha256":manifest["contact_sheet_sha256"]},indent=2))