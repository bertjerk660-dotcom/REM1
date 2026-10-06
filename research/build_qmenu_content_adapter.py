from pathlib import Path
import json,re,hashlib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json"
OUT=ROOT/"build/prepared/qmenu_content_adapter"
OUT.mkdir(parents=True,exist_ok=True)
m=json.loads(SRC.read_text(encoding="utf-8"))

def toks(*xs):
    s=" ".join(str(x or "") for x in xs).lower()
    return sorted(set(x for x in re.split(r"[^a-z0-9]+",s) if len(x)>=2))

rows=[]
for i,r in enumerate(m["ready_records"],1):
    rows.append({
        "id":f"rem_prop_{i:03d}",
        "content_type":"model",
        "category":r["menu_category"],
        "display_name":r["display_name"],
        "model":r["runtime_mesh_path"].replace("\\","/"),
        "source_game":r["source"],
        "form_binding":r["form_binding"],
        "thumbnail":r.get("support_thumbnail"),
        "search_tokens":toks(r["display_name"],r["menu_category"],r["source_path"],r["source"]),
        "validation_state":r["validation_state"]
    })

cats={}
for r in rows:
    cats.setdefault(r["category"],[]).append(r["id"])
result={
 "purpose":"Data-only adapter for feeding the curated catalog into Astra's future source-faithful GMod spawnmenu compatibility layer.",
 "entry_count":len(rows),
 "categories":[{"name":k,"count":len(v),"entry_ids":v} for k,v in sorted(cats.items())],
 "entries":rows,
 "runtime_contract":{
   "menu_owns_selection":"The real/ported GMod Q menu owns browsing/search/tool selection.",
   "adapter_role":"Map model selection to an FNV base form plus model path; do not implement a Fallout imitation menu.",
   "notifications":"Use GMod notification system, not Fallout top-left prompts."
 }
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"entries":len(rows),"categories":{k:len(v) for k,v in cats.items()}},indent=2))