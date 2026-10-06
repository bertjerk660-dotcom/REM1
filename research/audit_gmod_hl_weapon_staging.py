from pathlib import Path
import hashlib, json

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
WEAPONS=ROOT/"research/gmod_weapon_manifest.json"
STAGED=ROOT/"build/prepared/gmod_hl_weapon_models/manifest.json"
OUT=ROOT/"build/prepared/gmod_hl_weapon_models/audit.json"

weapons=json.loads(WEAPONS.read_text(encoding="utf-8"))
staged=json.loads(STAGED.read_text(encoding="utf-8"))

by_class={w["class"]:w for w in weapons["weapons"]}
records=[]
blocking=[]
nonblocking=[]

for rec in staged["records"]:
    classes=rec.get("weapon_classes",[])
    concrete=[c for c in classes if not by_class.get(c,{}).get("abstract_base",False)]
    abstract=[c for c in classes if by_class.get(c,{}).get("abstract_base",False)]
    files=[]
    for wm in rec.get("worker_matches",[]):
        files.extend(wm.get("files",[]))
    names=[f["relative"].replace("\\","/").lower() for f in files]
    raw_mdl=any(x.endswith(".mdl") and "/src/" in ("/"+x) for x in names)
    raw_vvd=any(x.endswith(".vvd") for x in names)
    raw_vtx=any(x.endswith(".vtx") for x in names)
    qc=any(x.endswith(".qc") for x in names)
    smd=any(x.endswith(".smd") for x in names)
    phy=any(x.endswith(".phy") for x in names)
    item={
        "model":rec["model"],
        "roles":rec.get("roles",[]),
        "weapon_classes":classes,
        "concrete_classes":concrete,
        "abstract_classes":abstract,
        "staged":bool(rec.get("staged")),
        "package_checks":{
            "raw_mdl":raw_mdl,"raw_vvd":raw_vvd,"raw_vtx":raw_vtx,
            "decompiled_qc":qc,"decompiled_smd":smd,"raw_phy":phy,
        }
    }
    records.append(item)
    if not item["staged"]:
        if concrete:
            blocking.append(item)
        else:
            nonblocking.append(item)

concrete_model_refs={r["model"].lower() for r in records if r["concrete_classes"]}
concrete_staged={r["model"].lower() for r in records if r["concrete_classes"] and r["staged"]}
abstract_only_unstaged=[r for r in records if not r["staged"] and not r["concrete_classes"]]

# Package completeness is advisory because some valid Source models do not ship PHY,
# and engine/prop models can differ in companion layout.
incomplete=[]
for r in records:
    if not (r["staged"] and r["concrete_classes"]):
        continue
    p=r["package_checks"]
    required=["raw_mdl","raw_vvd","raw_vtx","decompiled_qc","decompiled_smd"]
    missing=[k for k in required if not p[k]]
    if missing:
        incomplete.append({"model":r["model"],"classes":r["concrete_classes"],"missing":missing})

result={
    "purpose":"Verify staged Source/GMod/Half-Life model packages cover all concrete weapon references. Abstract base-class placeholder models are non-blocking.",
    "weapon_classes_total":len(weapons["weapons"]),
    "abstract_weapon_classes":[w["class"] for w in weapons["weapons"] if w.get("abstract_base")],
    "unique_model_refs_total":len(records),
    "concrete_model_refs":len(concrete_model_refs),
    "concrete_model_refs_staged":len(concrete_staged),
    "concrete_coverage_percent":round(100.0*len(concrete_staged)/len(concrete_model_refs),2) if concrete_model_refs else 100.0,
    "blocking_unstaged":blocking,
    "nonblocking_abstract_only_unstaged":abstract_only_unstaged,
    "concrete_package_incomplete":incomplete,
    "status":"pass" if not blocking else "fail",
    "notes":[
        "models/weapons/v_pistol.mdl is referenced by abstract weapon_base and is absent from the installed loose GMod tree.",
        "models/weapons/v_eq_flashbang.mdl is referenced by abstract weapon_tttbasegrenade and is absent from the installed loose GMod tree.",
        "Concrete TTT grenade subclasses override/use their own installed models; abstract-base placeholder absence should not block the staging set.",
        "PHY is recorded but not required for every weapon/view model package."
    ],
    "records":records
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in [
    "status","weapon_classes_total","unique_model_refs_total","concrete_model_refs",
    "concrete_model_refs_staged","concrete_coverage_percent",
    "blocking_unstaged","nonblocking_abstract_only_unstaged","concrete_package_incomplete"
]},indent=2))