from pathlib import Path
import json, collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/thug2_prop_catalog"
CUR=json.loads((BASE/"embedded_prop_targets_curated.json").read_text(encoding="utf-8"))
OUT=BASE/"embedded_prop_handoff"
OUT.mkdir(parents=True,exist_ok=True)

by_level=collections.defaultdict(list)
for r in CUR["records"]:
    by_level[r["level"]].append(r)

summary=[]
for level, targets in sorted(by_level.items()):
    ldir=OUT/level
    ldir.mkdir(parents=True,exist_ok=True)
    rows=[]
    for t in targets:
        snippets=[]
        for f in t.get("files",[]):
            if not (f==level or f.startswith(level+"/")):
                continue
            p=BASE/"qb_decompiled"/f
            if not p.exists():
                continue
            lines=p.read_text(encoding="utf-8",errors="ignore").splitlines()
            needle=t["identifier"].lower()
            for i,line in enumerate(lines):
                if needle in line.lower():
                    a=max(0,i-3); b=min(len(lines),i+4)
                    snippets.append({
                        "file":str(p.relative_to(ROOT)).replace("\\","/"),
                        "line":i+1,
                        "context":[{"line":j+1,"text":lines[j][:500]} for j in range(a,b)]
                    })
                    break
            if snippets:
                break
        x=dict(t)
        x["qb_snippets"]=snippets
        rows.append(x)

    glbdir=BASE/"level_glb"/level
    qdir=BASE/"qb_decompiled"/level
    bundle={
        "level":level,
        "target_count":len(rows),
        "targets":rows,
        "whole_level_glbs":sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in glbdir.rglob("*.glb")) if glbdir.exists() else [],
        "qb_files":sorted(str(p.relative_to(ROOT)).replace("\\","/") for p in qdir.rglob("*.q")) if qdir.exists() else [],
        "instructions":[
            "Resolve each named target against its QB context and matching whole-level GLB.",
            "Split only the target object leaves; do not import the THUG2 map.",
            "Convert the separated object to FNV and validate scale/collision before menu promotion."
        ]
    }
    (ldir/"targets.json").write_text(json.dumps(bundle,indent=2),encoding="utf-8")
    summary.append({
        "level":level,
        "targets":len(rows),
        "with_qb_context":sum(bool(x["qb_snippets"]) for x in rows),
        "whole_level_glbs":len(bundle["whole_level_glbs"]),
        "qb_files":len(bundle["qb_files"])
    })

result={
    "purpose":"Per-level THUG2 embedded-prop handoff bundles for later Astra/model extraction.",
    "target_count":sum(x["targets"] for x in summary),
    "levels":summary
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps(result,indent=2))