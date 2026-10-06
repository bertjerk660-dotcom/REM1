from pathlib import Path
import hashlib,json,re

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"build/prepared/historical_artifact_registry"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

files=[]
for base in [ROOT/"build/manifests",ROOT/"backups"]:
    if base.exists():
        for p in sorted(x for x in base.rglob("*") if x.is_file()):
            files.append(p)
bad_patch=ROOT/"research/patch_v74_advdupe_physgun.py"
if bad_patch.exists():files.append(bad_patch)

rows=[]
for p in files:
    rel=str(p.relative_to(ROOT)).replace("\\","/")
    low=rel.lower()
    category="historical_evidence"
    status="preserve"
    warning=None
    if rel=="build/manifests/v85.json":
        category="current_baseline_manifest"
    elif "main_v65_stable" in low or "rem_gmodthug2_v65_stable" in low:
        category="known_historical_stable_baseline"
    elif "crash" in low or "pre_v79_persistent_board" in low or "pre_v80_no_ride_clone" in low or "pre_v81_retarget_stability" in low:
        category="historical_failure_or_fix_evidence"
    elif rel=="research/patch_v74_advdupe_physgun.py":
        category="known_bad_do_not_run"
        warning="Never rerun/reapply: prior v74 patch is recorded as a failed/crashing path."
    elif "/v80.json" in low or "/v81.json" in low or "/v82.json" in low or "/v83.json" in low or "/v84.json" in low:
        category="historical_iteration_manifest"
    elif "quick_assets_" in low:
        category="historical_asset_deployment_snapshot"
    elif "pre_runtime_test" in low:
        category="historical_pretest_backup"
    rows.append({
        "path":rel,"category":category,"status":status,"warning":warning,
        "bytes":p.stat().st_size,"sha256":sha(p)
    })

result={
    "purpose":"Non-destructive registry of historical project artifacts so old crash experiments are not confused with active candidates.",
    "artifact_count":len(rows),
    "categories":{},
    "records":rows,
    "rules":[
        "Nothing is deleted or overwritten by this registry.",
        "Known-bad scripts must remain preserved as failure evidence but must not be executed.",
        "Historical backups are evidence, not automatically valid deployment candidates.",
        "Current installed runtime remains v85; Astra v88 is tracked separately as a protected candidate."
    ]
}
for r in rows:result["categories"][r["category"]]=result["categories"].get(r["category"],0)+1
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"artifact_count":result["artifact_count"],"categories":result["categories"],
                  "known_bad":[r["path"] for r in rows if r["category"]=="known_bad_do_not_run"]},indent=2))