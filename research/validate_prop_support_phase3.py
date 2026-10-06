from pathlib import Path
import json, hashlib, datetime

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
LOCALAPP=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV")
BASE=ROOT/"build/prepared/prop_support_phase3"
OUT=ROOT/"build/validation/prop_support_phase3.json"
OUT.parent.mkdir(parents=True,exist_ok=True)

EXPECTED={
 "runtime":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
 "astra_v88":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
 "main_esp":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7",
}
FILES={
 "runtime":DATA/"NVSE/Plugins/FNVGModTHUG2.dll",
 "astra_v88":ROOT/"build/hud88/bin/FNVGModTHUG2.dll",
 "main_esp":DATA/"REM_GModTHUG2.esp",
}

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

checks=[]
def ck(name,ok,details=None,severity="error"):
    checks.append({"name":name,"pass":bool(ok),"severity":severity,"details":details})

for k,p in FILES.items():
    ck(k+"_exists",p.exists(),str(p))
    if p.exists():ck(k+"_protected_hash",sha(p)==EXPECTED[k],{"actual":sha(p),"expected":EXPECTED[k]})

plugins=(LOCALAPP/"plugins.txt").read_text(errors="ignore").splitlines() if (LOCALAPP/"plugins.txt").exists() else []
enabled={x.strip().lstrip("*").lower() for x in plugins if x.strip()}
for name in ("REM_GModProps_Catalog.esp","REM_CombineArmor_Test.esp","REM_WeaponPresentation_Fixes.esp"):
    ck(name+"_disabled",name.lower() not in enabled,{"enabled":name.lower() in enabled})

def load(name):
    p=BASE/name
    ck(name.replace("/","_")+"_exists",p.exists(),str(p))
    if not p.exists():return None
    try:return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        ck(name.replace("/","_")+"_json",False,repr(e));return None

summary=load("summary.json")
if summary:
    ck("ready_prop_count",summary.get("ready_props")==290,summary.get("ready_props"))
    ck("source_split",summary.get("source_counts")=={"Fallout New Vegas":170,"Garry's Mod / mounted Source content":120},summary.get("source_counts"))
    ck("representative_batches",summary.get("representative_test_props")==56 and summary.get("test_batches")==5,{"selected":summary.get("representative_test_props"),"batches":summary.get("test_batches")})
    ck("thug2_ranked",summary.get("thug2_spatial_candidates_ranked")==85 and summary.get("thug2_top20_ready_for_visual_review")==20,{"ranked":summary.get("thug2_spatial_candidates_ranked"),"top20":summary.get("thug2_top20_ready_for_visual_review")})
    ck("no_runtime_modification",summary.get("runtime_or_astra_code_modified") is False,summary.get("runtime_or_astra_code_modified"))

ledger=load("catalog_quality_ledger.json")
if ledger:
    rec=ledger.get("records",[])
    ck("quality_ledger_290",len(rec)==290,len(rec))
    ck("quality_all_form_bound",all(x.get("form_binding_ok") for x in rec),sum(not x.get("form_binding_ok") for x in rec))
    ck("quality_all_thumbnails",all(x.get("thumbnail_ok") for x in rec),sum(not x.get("thumbnail_ok") for x in rec))
    ck("quality_all_collision_evidence",all(x.get("collision_evidence") for x in rec),sum(not x.get("collision_evidence") for x in rec))

gmod=load("gmod_prop_dependency_audit.json")
if gmod:
    rec=gmod.get("records",[])
    missing_materials=[]
    unresolved=[]
    for x in rec:
        if not x.get("materials_resolve"):unresolved.append(x.get("source_model"))
        for m in x.get("materials",[]):
            for k in ("base","normal"):
                if m.get(k) and not m[k].get("exists"):missing_materials.append(m[k]["path"])
    ck("gmod_dependency_120",gmod.get("prop_count")==120,len(rec))
    ck("gmod_materials_resolve",not unresolved,unresolved)
    ck("gmod_material_files_exist",not missing_materials,missing_materials)
    ck("gmod_authored_mobility_recorded",gmod.get("authored_movable")==120,gmod.get("authored_movable"),severity="info")

batches=load("runtime_test_batches.json")
if batches:
    ck("runtime_batches_5",batches.get("batch_count")==5,batches.get("batch_count"))
    ck("runtime_batch_selected_56",batches.get("selected_count")==56,batches.get("selected_count"))
    ck("runtime_batches_pending_only",all(b.get("status")=="pending_human" for b in batches.get("batches",[])),None)

validation=load("runtime_validation_ledger.json")
if validation:
    rec=validation.get("records",[])
    ck("runtime_validation_ledger_290",len(rec)==290,len(rec))
    ck("runtime_validation_not_falsely_passed",all(r.get("overall")=="pending_human" for r in rec),None)

thug=load("thug2_promotion_queue.json")
if thug:
    ck("thug_queue_85",thug.get("candidate_count")==85,thug.get("candidate_count"))
    ck("thug_top20_exact",len(thug.get("top20",[]))==20,len(thug.get("top20",[])))
    ck("thug_not_promoted",all(r.get("status")=="visual_leaf_review_required_not_promoted" for r in thug.get("records",[])),None)

budget=load("menu_budget.json")
if budget:
    ck("menu_budget_current",budget.get("current_ready")==290,budget.get("current_ready"))
    ck("menu_budget_target",budget.get("target_range")==[300,320] and budget.get("first_wave_target")==310,{"range":budget.get("target_range"),"first":budget.get("first_wave_target")})
    ck("replacement_reserve_40",len(budget.get("replacement_reserve",[]))==40,len(budget.get("replacement_reserve",[])))

icons=load("gmod_spawnicon_coverage.json")
if icons:
    ck("gmod_icon_coverage_total",icons.get("gmod_props")==120,icons)
    ck("gmod_fallback_previews_120",icons.get("fallback_geometry_previews_available")==120,icons.get("fallback_geometry_previews_available"))
    ck("native_spawnicon_result_recorded",icons.get("native_spawnicons_found") is not None,icons.get("native_spawnicons_found"),severity="info")

prov=load("prop_payload_provenance.json")
if prov:
    ck("provenance_form_bindings_290",prov.get("form_binding_count")==290,prov.get("form_binding_count"))
    ck("provenance_thumbnails_290",prov.get("thumbnail_ok_count")==290,prov.get("thumbnail_ok_count"))
    ck("provenance_gmod_materials",prov.get("gmod_unique_material_files",0)>0,prov.get("gmod_unique_material_files"))

for rel in ("context/PROP_SUPPORT_NEXT_20.md","context/PROP_PHASE3_STATUS.md","context/THUG2_PROP_TOP20_REVIEW.md","context/PROP_RUNTIME_TEST_BATCHES.md"):
    p=ROOT/rel
    ck(rel.replace("/","_")+"_exists",p.exists(),str(p))

errors=[x for x in checks if x["severity"]=="error" and not x["pass"]]
result={
 "purpose":"Static/preflight validation for prop-focused support phase 3. It is not gameplay validation.",
 "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"pass" if not errors else "fail",
 "error_count":len(errors),
 "check_count":len(checks),
 "checks":checks,
 "playtest_required":True,
 "runtime_modified_by_validator":False,
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"status":result["status"],"checks":result["check_count"],"errors":errors},indent=2))