from pathlib import Path
import json,hashlib

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
CAT=ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json"
TH=ROOT/"build/prepared/final_prop_catalog_thumbnails/manifest.json"
cat=json.loads(CAT.read_text(encoding="utf-8"))
th=json.loads(TH.read_text(encoding="utf-8"))

# Thumbnail renderer preserves ready-record order and records source_path.
thumb_by_key={(r["source"],r["source_path"].lower()):r for r in th["records"] if r.get("status")=="ok"}
missing=[]
for r in cat["ready_records"]:
    t=thumb_by_key.get((r["source"],r["source_path"].lower()))
    if not t:
        missing.append({"source":r["source"],"source_path":r["source_path"]})
        continue
    r["support_thumbnail"]={
        "path":t["thumbnail"],
        "sha256":t["thumbnail_sha256"],
        "bytes":t["thumbnail_bytes"],
        "size":[128,128],
        "role":"support/fallback preview only; final source-faithful GMod SpawnIcon behavior remains Astra-owned"
    }
cat["thumbnail_coverage"]={
    "ready":len(cat["ready_records"]),
    "attached":len(cat["ready_records"])-len(missing),
    "missing":missing,
    "renderer_manifest":str(TH.relative_to(ROOT)).replace("\\","/")
}
CAT.write_text(json.dumps(cat,indent=2),encoding="utf-8")
summary=json.loads((CAT.parent/"summary.json").read_text(encoding="utf-8"))
summary["thumbnail_coverage"]=cat["thumbnail_coverage"]
(CAT.parent/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(cat["thumbnail_coverage"],indent=2))