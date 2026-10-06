from pathlib import Path
import json,hashlib,datetime
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
LOCALAPP=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV")
BASE=ROOT/"build/prepared/prop_support_phase4"
OUT=ROOT/"build/validation/prop_support_phase4.json"
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
def ck(name,ok,details=None,severity="error"):checks.append({"name":name,"pass":bool(ok),"severity":severity,"details":details})

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
 except Exception as e:ck(name.replace("/","_")+"_json",False,repr(e));return None

summary=load("summary.json")
if summary:
 ck("current_ready_290",summary.get("current_ready_props")==290,summary.get("current_ready_props"))
 ck("planned_first_wave_310",summary.get("planned_first_wave")==310,summary.get("planned_first_wave"))
 ck("gmod_reserve_80",summary.get("gmod_reserve_selected")==80,summary.get("gmod_reserve_selected"))
 ck("diversified_wave_20",summary.get("thug2_diversified_selected")==20,summary.get("thug2_diversified_selected"))
 ck("no_runtime_modification",summary.get("runtime_or_astra_code_modified") is False,summary.get("runtime_or_astra_code_modified"))

wave=load("thug2_diversified_first_wave.json")
if wave:
 expected={
  "Skate - Rails Handrails":6,"Skate - Quarterpipes Halfpipes Ramps":5,
  "Skate - Ledges Hubbas Curbs":4,"Street - Benches Tables Chairs":2,
  "Street - Fences Barriers Poles Pipes":2,"Skate - Stairs Platforms Misc":1
 }
 ck("wave_target_20",wave.get("selected")==20,wave.get("selected"))
 ck("wave_category_quota",wave.get("category_counts")==expected,wave.get("category_counts"))
 ids={(r.get("level"),r.get("identifier")) for r in wave.get("records",[])}
 ck("wave_unique_20",len(ids)==20,len(ids))

leaf=load("thug2_diversified_leaf_review.json")
if leaf:
 rec=leaf.get("records",[])
 ck("leaf_review_20",len(rec)==20,len(rec))
 ck("leaf_preview_all_exist",all((ROOT/r["preview"]).exists() for r in rec),
    [r["preview"] for r in rec if not (ROOT/r["preview"]).exists()])
 ck("leaf_no_complex",leaf.get("status_counts",{}).get("complex_review")==0,leaf.get("status_counts"))
 ck("leaf_not_promoted",all(r.get("promotion_state")=="not_promoted_visual_confirmation_required" for r in rec),None)

reserve=load("gmod_reserve_pool.json")
if reserve:
 rec=reserve.get("records",[])
 ck("reserve_count_80",len(rec)==80,len(rec))
 ck("reserve_unique",len({r["source_model"].lower() for r in rec})==80,None)
 ck("reserve_nifs_exist",all(Path(r["output_nif"]).exists() for r in rec),
    [r["output_nif"] for r in rec if not Path(r["output_nif"]).exists()])
 missing=[]
 for r in rec:
  for m in r.get("materials",[]):
   for k in ("base","normal"):
    p=m.get(k)
    if p and not Path(p).exists():missing.append(p)
 ck("reserve_materials_exist",not missing,missing)
 ck("reserve_not_promoted",all(r.get("state")=="reserve_only_not_in_default_catalog" for r in rec),None)

tax=load("menu_taxonomy_v2.json")
if tax:
 ck("taxonomy_current_290",len(tax.get("current_entries",[]))==290,len(tax.get("current_entries",[])))
 ck("taxonomy_future_20",len(tax.get("planned_thug2_first_wave",[]))==20,len(tax.get("planned_thug2_first_wave",[])))
 ck("taxonomy_target_range",tax.get("target_range")==[300,320],tax.get("target_range"))

plan=load("promotion_plan.json")
if plan:
 fr=plan.get("thug2_form_reservations",[])
 ck("form_reservations_20",len(fr)==20,len(fr))
 ck("form_reservation_ids_unique",len({x["proposed_local_id"] for x in fr})==20,None)
 ck("form_reservation_edids_unique",len({x["proposed_edid"].lower() for x in fr})==20,None)
 ck("no_form_created",all(x.get("state")=="reserved_only_no_esp_record_created" for x in fr),None)

ledger=load("thug2_promotion_validation_ledger.json")
if ledger:
 rec=ledger.get("records",[])
 ck("promotion_ledger_20",len(rec)==20,len(rec))
 ck("promotion_all_blocked",all(r.get("overall")=="blocked_pending_visual_review" for r in rec),None)
 ck("promotion_checks_pending",all(all(v=="pending" for v in r.get("checks",{}).values()) for r in rec),None)

packet=load("review_packet.json")
if packet:
 p=ROOT/packet["contact_sheet"]
 ck("contact_sheet_exists",p.exists(),str(p))
 if p.exists():ck("contact_sheet_hash",sha(p)==packet.get("contact_sheet_sha256"),{"actual":sha(p),"expected":packet.get("contact_sheet_sha256")})

errors=[x for x in checks if x["severity"]=="error" and not x["pass"]]
result={
 "purpose":"Static/preflight validation for prop-focused support phase 4. This is not gameplay or visual identity validation.",
 "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"pass" if not errors else "fail","error_count":len(errors),"check_count":len(checks),
 "checks":checks,"playtest_required":True,"visual_leaf_review_required":True,"runtime_modified_by_validator":False
}
OUT.write_text(json.dumps(result,indent=2))
print(json.dumps({"status":result["status"],"checks":result["check_count"],"errors":errors},indent=2))