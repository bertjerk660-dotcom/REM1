from pathlib import Path
import json,re,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/prop_support_phase4"
QUEUE=json.loads((BASE/"thug2_conversion_review_queue.json").read_text())
TAX=json.loads((BASE/"menu_taxonomy_v2.json").read_text())
RES=json.loads((BASE/"gmod_reserve_pool.json").read_text())
OUT=BASE

def edid(level,ident,idx):
    s=re.sub(r"[^A-Za-z0-9]+","_",ident).strip("_")[:40]
    return f"REMTP_{idx:02d}_{level.upper()}_{s}"

forms=[]
first_local=0x800
for i,r in enumerate(QUEUE["records"],1):
    forms.append({
      "rank":r["rank"],"level":r["level"],"identifier":r["identifier"],
      "proposed_plugin":"REM_THUG2Props_Catalog.esp",
      "proposed_signature":"MSTT",
      "proposed_local_id":f"{first_local+i-1:06X}",
      "proposed_edid":edid(r["level"],r["identifier"],i),
      "proposed_full":r["identifier"].replace("_"," "),
      "state":"reserved_only_no_esp_record_created",
      "creation_gate":[
        "visual leaf identity confirmed",
        "standalone source geometry split from THUG2 level",
        "FNV NIF conversion succeeds",
        "textures/materials resolve",
        "collision model validated",
        "scale validated against reference",
        "spawn/contact cleanup runtime test passes"
      ]
    })

# Map first wave to taxonomy; they remain hidden/future until passed.
planned=[]
for r,f in zip(QUEUE["records"],forms):
    future=next((x for x in TAX["planned_thug2_first_wave"] if x["level"]==r["level"] and x["display_name"]==r["identifier"]),None)
    planned.append({
      **r,"form_reservation":f,
      "planned_bucket":future["bucket"] if future else None,
      "menu_visibility":"hidden_until_promoted"
    })

checklist={
 "visual_identity":"pending",
 "standalone_geometry":"pending",
 "source_material_provenance":"pending",
 "nif_structure":"pending",
 "texture_resolution":"pending",
 "collision":"pending",
 "scale":"pending",
 "spawn_safety":"pending",
 "contact_stability":"pending",
 "cleanup":"pending",
 "qmenu_metadata":"pending",
}

res={
 "purpose":"Promotion plan for THUG2 prop candidates plus GMod reserve fallback. It allocates metadata only; no runtime/plugin records are created.",
 "thug2_form_reservations":forms,
 "first_wave":planned,
 "gmod_reserve_count":RES["selected_reserve"],
 "gmod_reserve_by_category":RES["category_counts"],
 "promotion_check_template":checklist,
 "menu_policy":{
   "current":TAX["current_ready_count"],
   "first_wave_if_all_20_pass":TAX["planned_first_wave_count"],
   "target_range":TAX["target_range"],
   "rule":"Promote individually. Failed THUG2 candidates do not block the rest; use GMod reserve or keep current item count."
 }
}
(OUT/"promotion_plan.json").write_text(json.dumps(res,indent=2),encoding="utf-8")

ledger=[]
for x in planned:
    ledger.append({
      "level":x["level"],"identifier":x["identifier"],"category":x["category"],"planned_bucket":x["planned_bucket"],
      "proposed_edid":x["form_reservation"]["proposed_edid"],
      "review_status":x["review_status"],"isolation_score":x["isolation_score"],
      "checks":dict(checklist),"overall":"blocked_pending_visual_review"
    })
(OUT/"thug2_promotion_validation_ledger.json").write_text(json.dumps({
  "purpose":"Per-candidate promotion ledger; all fields begin pending.",
  "records":ledger
},indent=2),encoding="utf-8")
print(json.dumps({"form_reservations":len(forms),"gmod_reserve":RES["selected_reserve"],"target_if_all_pass":TAX["planned_first_wave_count"]},indent=2))