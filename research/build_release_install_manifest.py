from pathlib import Path
import hashlib,json,collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
GAME=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas")
DATA=GAME/"Data"
OUT=ROOT/"build/prepared/release_install_manifest"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def file_row(p,role,state,source,redistribution="project-build/test only"):
    return {"path":str(p),"exists":p.exists(),"bytes":p.stat().st_size if p.exists() else None,
            "sha256":sha(p) if p.exists() else None,"role":role,"state":state,
            "source":source,"redistribution_note":redistribution}

core=[
 file_row(DATA/"NVSE/Plugins/FNVGModTHUG2.dll","NVSE runtime bridge","current_test_baseline_v85","project build"),
 file_row(DATA/"REM_GModTHUG2.esp","main content plugin","current_active_test_esp","project build"),
 file_row(ROOT/"build/hud88/bin/FNVGModTHUG2.dll","Astra v88 candidate","protected_not_installed","project build"),
 file_row(DATA/"REM_GModProps_Catalog.esp","curated GMod prop base forms","disabled_test_sidecar","project build"),
 file_row(DATA/"REM_CombineArmor_Test.esp","Combine armor test form","disabled_test_sidecar","project build"),
 file_row(DATA/"REM_WeaponPresentation_Fixes.esp","RPG presentation override","disabled_test_sidecar","project build"),
]
icons=[
 DATA/"textures/interface/icons/pipboyimages/weapons/rem_gmod_origin.dds",
 DATA/"textures/interface/icons/pipboyimages_small/weapons_small/glow_rem_gmod_origin.dds",
 DATA/"textures/interface/icons/pipboyimages/weapons/rem_thug2_origin.dds",
 DATA/"textures/interface/icons/pipboyimages_small/weapons_small/glow_rem_thug2_origin.dds",
]
icon_rows=[file_row(p,"Pip-Boy source-origin icon","installed_support_asset","derived from user's installed source-game logo asset") for p in icons]
board_paths=[DATA/"meshes/rem/thug2"/x for x in ["skateboard.nif","skateboard_visual.nif","skateheldx.nif","skateworld.nif"]]
board_rows=[file_row(p,"THUG2 skateboard geometry/container","installed_support_asset","derived from user's installed THUG2 board asset") for p in board_paths]
combine_rows=[
 file_row(DATA/"meshes/rem/gmod/armor/CombineSoldierFullBody.nif","Combine wearable mesh","installed_test_asset","derived from user's installed GMod/Source Combine asset"),
 file_row(DATA/"meshes/rem/gmod/Combine_Soldier.nif","Combine world mesh","installed_test_asset","derived from user's installed GMod/Source Combine asset"),
]

gmod=json.loads((ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json").read_text())
prop_files={}
for r in gmod["records"]:
    p=Path(r["output_nif"])
    if p.exists():prop_files[str(p).lower()]=file_row(p,"curated GMod/Source prop NIF","installed_support_asset","derived from user's installed GMod/mounted Source model")
    for m in r.get("materials",[]):
        for k in ("base","normal"):
            q=m.get(k)
            if q:
                qp=Path(q)
                if qp.exists():prop_files[str(qp).lower()]=file_row(qp,"curated Source prop texture","installed_support_asset","derived from user's installed mounted Source material")
prop_rows=list(prop_files.values())

catalog=json.loads((ROOT/"build/prepared/final_prop_catalog_handoff/manifest.json").read_text())
fnv_refs=[r for r in catalog["ready_records"] if r["source"]=="Fallout New Vegas"]
gmod_refs=[r for r in catalog["ready_records"] if r["source"].startswith("Garry")]

staged_manifests=[
 "build/prepared/final_prop_catalog_handoff/manifest.json",
 "build/prepared/final_prop_catalog_thumbnails/manifest.json",
 "build/prepared/qmenu_content_adapter/manifest.json",
 "build/prepared/gmod_qmenu_source_inventory/manifest.json",
 "build/prepared/gmod_weapon_runtime_candidates/manifest.json",
 "build/prepared/gmod_weapon_runtime_candidates/resolved_sound_events/manifest.json",
 "build/prepared/gmod_tool_physgun_asset_handoff/manifest.json",
 "build/prepared/thug2_skateboard_asset_handoff/manifest.json",
 "build/prepared/thug2_ui_asset_handoff/manifest.json",
 "build/prepared/input_control_matrix/manifest.json",
 "build/prepared/thug2_prop_catalog/target_classification.json",
 "build/prepared/regression_test_packs/manifest.json",
 "build/prepared/historical_artifact_registry/manifest.json",
 "build/prepared/prop_support_phase3/summary.json",
 "build/validation/prop_support_phase3.json",
 "build/prepared/prop_support_phase4/summary.json",
 "build/validation/prop_support_phase4.json",
]
manifest_rows=[]
for rel in staged_manifests:
    p=ROOT/rel
    manifest_rows.append(file_row(p,"reproducibility/support manifest","project_source_metadata","project generated metadata","safe to commit"))

result={
 "purpose":"Eventual install/package manifest. It records current test baseline plus staged assets; it is not a claim that the mashup is release-ready.",
 "core_runtime":core,"origin_icons":icon_rows,"skateboard_assets":board_rows,"combine_test_assets":combine_rows,
 "curated_gmod_prop_payload_files":prop_rows,
 "curated_catalog":{"ready_count":catalog["ready_count"],"fnv_native_refs":len(fnv_refs),"gmod_custom_refs":len(gmod_refs),
                    "note":"FNV native models/forms are host-game dependencies and are not duplicated into a release payload."},
 "support_manifests":manifest_rows,
 "not_release_ready":[
   "Astra v88 is not installed or gameplay-validated.",
   "THUG2 complete skate runtime/camera/animation/physics is pending.",
   "Real GMod Q-menu/Tool Gun/Physgun runtime compatibility is pending.",
   "Disabled prop/armor/presentation sidecars require isolated gameplay validation before promotion.",
   "Weapon first-person animation integration and remaining visual QA are pending."
 ],
 "packaging_policy":[
   "Do not commit or redistribute proprietary source-game archives/executables.",
   "Package only transformed/project runtime files as legally appropriate; keep source provenance and hashes.",
   "Native FNV assets referenced from base/DLC masters remain host dependencies rather than copied payload."
 ]
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
summary={
 "core_files":len(core),"origin_icons":len(icon_rows),"board_files":len(board_rows),
 "combine_test_files":len(combine_rows),"gmod_prop_payload_files":len(prop_rows),
 "fnv_native_catalog_refs":len(fnv_refs),"gmod_custom_catalog_refs":len(gmod_refs),
 "support_manifests":len(manifest_rows),"missing_core":[x["path"] for x in core if not x["exists"]]
}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))