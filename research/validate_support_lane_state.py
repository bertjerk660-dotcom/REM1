from pathlib import Path
import json, hashlib, datetime

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
GAME=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas")
DATA=GAME/"Data"
OUT=ROOT/"build/validation/support_lane_state.json"
OUT.parent.mkdir(parents=True,exist_ok=True)

EXPECTED={
    "live_v85_dll":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
    "astra_v88_dll":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
    "active_esp":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7",
    "gmod_icon_large":"9D22854C96241AFC6C3FC596E15356D38DCFA75EB073E61F943B8FC094F3161E",
    "gmod_icon_small":"9CAC7740C145C1CAE6F6823EAB03F6ADEAAB9D06A14ABA647E0AC4619EBCD25B",
    "thug2_icon_large":"5820CA60BA0EFC811F5D623F1D53BA12AADE4194A5252FC8E3A7A42FEA4B9633",
    "thug2_icon_small":"4DA787896197E76DF3C2E04BC17F929064EEB8FF65833A39B3B20362F6B62F40",
}
FILES={
    "live_v85_dll":DATA/"NVSE/Plugins/FNVGModTHUG2.dll",
    "astra_v88_dll":ROOT/"build/hud88/bin/FNVGModTHUG2.dll",
    "active_esp":DATA/"REM_GModTHUG2.esp",
    "gmod_icon_large":DATA/"textures/interface/icons/pipboyimages/weapons/rem_gmod_origin.dds",
    "gmod_icon_small":DATA/"textures/interface/icons/pipboyimages_small/weapons_small/glow_rem_gmod_origin.dds",
    "thug2_icon_large":DATA/"textures/interface/icons/pipboyimages/weapons/rem_thug2_origin.dds",
    "thug2_icon_small":DATA/"textures/interface/icons/pipboyimages_small/weapons_small/glow_rem_thug2_origin.dds",
}
SIDECARS=[
    DATA/"REM_CombineArmor_Test.esp",
    DATA/"REM_GModProps_Catalog.esp",
    DATA/"REM_WeaponPresentation_Fixes.esp",
]
PLUGINS=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

checks=[]
def ck(name,ok,details=None,severity="error"):
    checks.append({"name":name,"pass":bool(ok),"severity":severity,"details":details})

for key,p in FILES.items():
    exists=p.exists()
    ck(key+"_exists",exists,str(p))
    if exists:
        actual=sha(p)
        ck(key+"_hash",actual==EXPECTED[key],{"actual":actual,"expected":EXPECTED[key]})

plugin_lines=[]
if PLUGINS.exists():
    plugin_lines=[x.strip().lstrip("*").lower() for x in PLUGINS.read_text(errors="ignore").splitlines() if x.strip()]
for p in SIDECARS:
    ck(p.stem+"_exists",p.exists(),str(p))
    enabled=p.name.lower() in plugin_lines
    ck(p.stem+"_disabled",not enabled,{"enabled":enabled,"sha256":sha(p) if p.exists() else None})

def load(rel):
    p=ROOT/rel
    if not p.exists():
        ck("manifest_"+rel.replace("/","_")+"_exists",False,str(p))
        return None
    ck("manifest_"+rel.replace("/","_")+"_exists",True,{"path":str(p),"sha256":sha(p)})
    try:return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        ck("manifest_"+rel.replace("/","_")+"_json",False,repr(e))
        return None

combine=load("build/combine_armor/validation.json")
if combine: ck("combine_static_validation",combine.get("status")=="static_validation_pass",combine.get("status"))

prop_side=load("build/prepared/gmod_prop_catalog_sidecar/validation.json")
if prop_side: ck("gmod_prop_sidecar_validation",prop_side.get("status")=="pass",prop_side.get("status"))

thumbs=load("build/prepared/prop_menu_thumbnails/manifest.json")
if thumbs:
    ck("prop_thumbnails_290",thumbs.get("candidate_count")==290 and thumbs.get("generated")==290 and thumbs.get("failed")==0,
       {"candidate_count":thumbs.get("candidate_count"),"generated":thumbs.get("generated"),"failed":thumbs.get("failed")})

coverage=load("build/prepared/prop_menu_content_handoff/form_coverage_audit.json")
if coverage:
    ck("prop_form_coverage_expected_counts",
       coverage.get("candidate_count")==290 and coverage.get("with_existing_form")==153 and coverage.get("missing_form")==137,
       {k:coverage.get(k) for k in ("candidate_count","with_existing_form","missing_form","by_source")})

weapon=load("build/prepared/gmod_weapon_runtime_candidates/summary.json")
if weapon:
    ck("weapon_model_staging",not weapon.get("missing_models"),weapon.get("missing_models"))
    ck("weapon_texture_staging",weapon.get("missing_textures_count")==0,weapon.get("missing_textures_count"))
    ck("weapon_view_world_candidates",weapon.get("view_candidates")==48 and weapon.get("world_candidates")==48,
       {"view":weapon.get("view_candidates"),"world":weapon.get("world_candidates")})
    ck("weapon_unresolved_sound_events_recorded",weapon.get("unresolved_sound_refs_count",0)>=0,
       weapon.get("unresolved_sound_refs_count"),severity="info")

board=load("build/prepared/thug2_skateboard_asset_handoff/manifest.json")
if board:
    ck("thug2_board_source_glb",len(board.get("source_board_glb",[]))>=1,len(board.get("source_board_glb",[])))
    ck("thug2_board_animation_assets",board.get("motoskateboard_animation_count")==20,board.get("motoskateboard_animation_count"))
    held=next((x for x in board.get("live_nifs",[]) if x.get("name")=="skateheldx.nif"),None)
    ck("held_board_container",bool(held and held.get("stats",{}).get("root_type")=="BSFadeNode" and
                                    {"name":"Prn","value":"Weapon"} in held.get("stats",{}).get("extras",[])),
       held)

ui=load("build/prepared/thug2_ui_asset_handoff/summary.json")
if ui:
    ck("thug2_ui_assets_complete",not ui.get("missing") and ui.get("asset_count")==49,
       {"asset_count":ui.get("asset_count"),"missing":ui.get("missing")})
    ck("thug2_ui_preview_conversions",ui.get("image_conversions")==22 and ui.get("image_conversions_success")==22,
       {"total":ui.get("image_conversions"),"success":ui.get("image_conversions_success")})

handoff=load("build/prepared/prop_menu_content_handoff/manifest.json")
if handoff:
    ck("compact_ready_prop_count",handoff.get("ready_candidate_count")==290,
       {"ready":handoff.get("ready_candidate_count"),"sources":handoff.get("ready_by_source")})

thugprops=load("build/prepared/thug2_prop_catalog/embedded_prop_handoff/manifest.json")
if thugprops:
    ck("thug2_prop_handoff_106",thugprops.get("target_count")==106,thugprops.get("target_count"))
    ck("thug2_prop_qb_context",
       all(x.get("with_qb_context")==x.get("targets") for x in thugprops.get("levels",[])),
       thugprops.get("levels"))

wp=load("build/prepared/weapon_inventory_presentation_audit.json")
if wp:
    ck("weapon_inventory_audit_present",wp.get("gmod_weapon_count")==49,
       {"count":wp.get("gmod_weapon_count"),"clean":wp.get("gmod_clean_count"),"issues":wp.get("issue_counts")})
    ck("skateboard_inventory_presentation",not wp.get("skateboard",{}).get("issues"),
       wp.get("skateboard",{}).get("issues"))


finalcat=load("build/prepared/final_prop_catalog_handoff/summary.json")
if finalcat:
    ck("final_prop_catalog_290",
       finalcat.get("ready_count")==290 and finalcat.get("all_ready_have_form_binding") is True,
       {"ready":finalcat.get("ready_count"),"by_source":finalcat.get("ready_by_source"),
        "form_binding":finalcat.get("all_ready_have_form_binding")})
    tc=finalcat.get("thumbnail_coverage",{})
    ck("final_prop_thumbnails_attached_290",
       tc.get("ready")==290 and tc.get("attached")==290 and not tc.get("missing"),
       tc)

finalthumb=load("build/prepared/final_prop_catalog_thumbnails/manifest.json")
if finalthumb:
    ck("final_prop_thumbnail_generation",
       finalthumb.get("candidate_count")==290 and finalthumb.get("generated")==290 and finalthumb.get("failed")==0,
       {k:finalthumb.get(k) for k in ("candidate_count","generated","failed")})

fnvforms=load("build/prepared/fnv_prop_catalog_curated/ready_existing_forms.json")
if fnvforms:
    ck("fnv_ready_existing_forms_170",
       fnvforms.get("count")==170 and not fnvforms.get("shortfalls"),
       {"count":fnvforms.get("count"),"shortfalls":fnvforms.get("shortfalls")})
    ck("fnv_ready_all_form_bound",
       all(bool(r.get("form_plugin") and r.get("formid_file")) for r in fnvforms.get("records",[])),
       None)

presfix=load("build/prepared/weapon_presentation_fix_sidecar/validation.json")
if presfix:
    ck("weapon_presentation_sidecar_validation",presfix.get("status")=="pass",presfix.get("status"))

ui_full=load("build/prepared/thug2_ui_asset_handoff/manifest.json")
if ui_full:
    ck("thug2_ui_asset_manifest_no_missing",not ui_full.get("missing"),ui_full.get("missing"))
    ck("thug2_ui_image_previews_22",
       ui_full.get("image_conversions_success")==22,
       ui_full.get("image_conversions_success"))


thumbq=load("build/prepared/final_prop_catalog_thumbnails/quality_audit.json")
if thumbq:
    ck("prop_thumbnail_quality_290_clean",
       thumbq.get("count")==290 and thumbq.get("clean")==290 and thumbq.get("flagged")==0,
       {k:thumbq.get(k) for k in ("count","clean","flagged","flag_counts")})

qadapter=load("build/prepared/qmenu_content_adapter/manifest.json")
if qadapter:
    ck("qmenu_content_adapter_290",
       qadapter.get("entry_count")==290,
       {"entry_count":qadapter.get("entry_count"),"categories":len(qadapter.get("categories",[]))})

sounds=load("build/prepared/gmod_weapon_runtime_candidates/weapon_sound_handoff.json")
if sounds:
    ck("weapon_sound_handoff_resolved",
       sounds.get("weapon_count")==49 and sounds.get("unresolved_count")==0,
       {"weapon_count":sounds.get("weapon_count"),"unresolved":sounds.get("unresolved")})

sounddefs=load("build/prepared/gmod_weapon_runtime_candidates/resolved_sound_events/summary.json")
if sounddefs:
    ck("source_named_sound_definitions_resolved",
       sounddefs.get("input_events")==15 and sounddefs.get("resolved_definitions")==15 and not sounddefs.get("unresolved_after"),
       sounddefs)

toolphys=load("build/prepared/gmod_tool_physgun_assets/manifest.json")
if toolphys:
    missing=toolphys.get("missing_assets",[])
    ck("tool_physgun_assets_expected_coverage",
       toolphys.get("asset_count")==28 and toolphys.get("asset_resolved_count")==27 and missing==["models/weapons/v_physics.mdl"],
       {"resolved":toolphys.get("asset_resolved_count"),"missing":missing})
    ck("tool_physgun_sound_events",
       all(bool(x.get("definitions")) for x in toolphys.get("sound_events",[])),
       [{"event":x.get("event"),"defs":len(x.get("definitions",[]))} for x in toolphys.get("sound_events",[])])

ctrl=load("build/prepared/thug2_controller_map/manifest.json")
if ctrl:
    ck("thug2_controller_source_map",
       len(ctrl.get("decompiled_source_files",[]))>=8 and bool(ctrl.get("trigger_usage")),
       {"files":len(ctrl.get("decompiled_source_files",[])),"usage_files":len(ctrl.get("trigger_usage",{}))})

spatial=load("build/prepared/thug2_prop_catalog/spatial_prop_candidates/mapping.json")
if spatial:
    ck("thug2_spatial_target_mapping_inventory",
       spatial.get("targets")==106 and spatial.get("mapped",0)>0,
       {"targets":spatial.get("targets"),"mapped":spatial.get("mapped"),"no_position":spatial.get("no_position")})

components=load("build/prepared/thug2_prop_catalog/component_evidence.json")
if components:
    ck("thug2_component_evidence_inventory",
       components.get("target_count")==106 and components.get("with_component_evidence",0)>0,
       {k:components.get(k) for k in ("target_count","with_component_evidence","with_position_evidence")})

sidecars=load("build/prepared/support_sidecars/manifest.json")
if sidecars:
    ck("support_sidecars_all_disabled",
       sidecars.get("all_disabled") is True and len(sidecars.get("sidecars",[]))==3,
       [{"name":x.get("name"),"enabled":x.get("enabled")} for x in sidecars.get("sidecars",[])])

modelaudit=load("build/prepared/gmod_weapon_runtime_candidates/model_presentation_audit.json")
if modelaudit:
    unexpected=[]
    allowed={
      ("gmod_camera","view","missing_candidate"),
      ("weapon_fists","view","no_geometry"),
      ("weapon_fists","view","no_shapes"),
      ("weapon_fists","world","missing_candidate"),
    }
    for r in modelaudit.get("records",[]):
        for role in ("view","world"):
            for f in r.get(role,{}).get("flags",[]):
                if (r.get("class"),role,f) not in allowed:
                    unexpected.append({"class":r.get("class"),"role":role,"flag":f})
    ck("weapon_model_presentation_no_unexpected_flags",
       modelaudit.get("weapon_count")==49 and not unexpected,
       {"unexpected":unexpected,"flag_counts":modelaudit.get("flag_counts")})

boardscale=load("build/prepared/thug2_skateboard_asset_handoff/scale_attachment_analysis.json")
if boardscale:
    ck("skateboard_scale_attachment_evidence",
       len(boardscale.get("comparisons",[]))==4,
       {"source_glb_dimensions":boardscale.get("source_glb_dimensions"),"comparisons":len(boardscale.get("comparisons",[]))})


release=load("build/prepared/release_install_manifest.json")
if release:
    ck("release_manifest_no_required_gaps",
       not release.get("summary",{}).get("missing_required"),
       release.get("summary"))

reg=load("build/prepared/regression_packs.json")
if reg:
    ids={x.get("id") for x in reg.get("packs",[])}
    expected={"baseline_fnv","inventory_gmod","skateboard_item","prop_sample","combine_armor","qmenu_future","release_smoke"}
    ck("regression_pack_coverage",
       expected.issubset(ids),
       sorted(ids))

qa_matrix=load("build/prepared/weapon_inventory_qa_matrix.json")
if qa_matrix:
    ck("weapon_inventory_qa_matrix",
       qa_matrix.get("gmod_weapons")==49 and not qa_matrix.get("skateboard",{}).get("static_issues"),
       {"gmod_weapons":qa_matrix.get("gmod_weapons"),"static_clean":qa_matrix.get("static_clean_gmod"),
        "skateboard_issues":qa_matrix.get("skateboard",{}).get("static_issues")})

versioned=load("build/prepared/versioned_artifact_inventory.json")
if versioned:
    ck("versioned_artifact_inventory",
       versioned.get("artifact_count",0)>0 and versioned.get("classification_counts",{}).get("known_bad",0)>0,
       {"artifact_count":versioned.get("artifact_count"),"classification_counts":versioned.get("classification_counts")})

tracker_path=ROOT/"context/SUPPORT_20_POINT_TRACKER.md"
ck("support_20_point_tracker_exists",tracker_path.exists(),str(tracker_path))
handoff_dir=ROOT/"context/HANDOFFS"
handoffs=list(handoff_dir.glob("ASTRA_*.md")) if handoff_dir.exists() else []
ck("astra_handoff_packets_8",len(handoffs)==8,[x.name for x in handoffs])


canonical_release=load("build/prepared/release_install_manifest/summary.json")
if canonical_release:
    ck("canonical_release_manifest_payload",
       canonical_release.get("gmod_prop_payload_files")==205 and
       canonical_release.get("fnv_native_catalog_refs")==170 and
       canonical_release.get("gmod_custom_catalog_refs")==120 and
       not canonical_release.get("missing_core"),
       canonical_release)

control_matrix=load("build/prepared/input_control_matrix/manifest.json")
if control_matrix:
    ck("canonical_input_control_matrix",
       len(control_matrix.get("matrix",[]))==22 and
       len(control_matrix.get("source_files",[]))==17,
       {"matrix_entries":len(control_matrix.get("matrix",[])),
        "source_files":len(control_matrix.get("source_files",[]))})

canonical_toolphys=load("build/prepared/gmod_tool_physgun_asset_handoff/manifest.json")
if canonical_toolphys:
    expected_missing={
      "models/weapons/v_physics.mdl",
      "models/weapons/v_physics.vvd",
      "models/weapons/v_physics.dx90.vtx",
    }
    ck("canonical_tool_physgun_asset_handoff",
       canonical_toolphys.get("requested")==36 and
       canonical_toolphys.get("resolved")==33 and
       set(canonical_toolphys.get("missing",[]))==expected_missing,
       {"requested":canonical_toolphys.get("requested"),
        "resolved":canonical_toolphys.get("resolved"),
        "missing":canonical_toolphys.get("missing")})

target_classes=load("build/prepared/thug2_prop_catalog/target_classification.json")
if target_classes:
    c=target_classes.get("classification_counts",{})
    ck("canonical_thug2_prop_target_classification",
       target_classes.get("target_count")==106 and
       c.get("spatial_geometry_candidate")==85 and
       c.get("semantic_or_gap_identifier")==14 and
       c.get("unresolved_named_target")==7,
       {"target_count":target_classes.get("target_count"),
        "classification_counts":c})

historical=load("build/prepared/historical_artifact_registry/manifest.json")
if historical:
    known_bad=[r for r in historical.get("records",[]) if r.get("category")=="known_bad_do_not_run"]
    ck("canonical_historical_artifact_registry",
       historical.get("artifact_count")==63 and
       any(r.get("path")=="research/patch_v74_advdupe_physgun.py" for r in known_bad),
       {"artifact_count":historical.get("artifact_count"),
        "known_bad":[r.get("path") for r in known_bad]})

canonical_reg=load("build/prepared/regression_test_packs/manifest.json")
if canonical_reg:
    ids={x.get("id") for x in canonical_reg.get("packs",[])}
    expected_ids={
      "baseline_fallout","inventory_presentation","rpg_presentation_fix",
      "gmod_prop_catalog","combine_armor","skateboard_baseline",
      "astra_skate_activation","astra_qmenu_tool_physgun",
    }
    ck("canonical_regression_test_packs",
       canonical_reg.get("pack_count")==8 and ids==expected_ids,
       {"pack_count":canonical_reg.get("pack_count"),"ids":sorted(ids)})

if tracker_path.exists():
    tracker_text=tracker_path.read_text(encoding="utf-8",errors="ignore")
    ck("support_tracker_reconciled_canonical",
       "205 GMod prop payload files" in tracker_text and
       "85 have source QB position" in tracker_text and
       "Eight repeatable packs" in tracker_text,
       {"bytes":tracker_path.stat().st_size})


artifact_index=load("builds/support_phase2_artifacts_20261006.json")
if artifact_index:
    ck("canonical_support_artifact_index",
       artifact_index.get("artifact_count")==27 and artifact_index.get("all_present") is True,
       {"artifact_count":artifact_index.get("artifact_count"),
        "all_present":artifact_index.get("all_present")})

failure_path=ROOT/"context/FAILURE_KNOWLEDGE.md"
if failure_path.exists():
    failure_text=failure_path.read_text(encoding="utf-8",errors="ignore")
    ck("parallel_support_manifest_failure_rule_recorded",
       "FS002 - Parallel support generators can leave stale duplicate manifests" in failure_text,
       str(failure_path))


prop_phase3_path=ROOT/"build/validation/prop_support_phase3.json"
if prop_phase3_path.exists():
    prop_phase3=json.loads(prop_phase3_path.read_text(encoding="utf-8"))
    ck("prop_support_phase3_validator",
       prop_phase3.get("status")=="pass" and prop_phase3.get("error_count")==0 and prop_phase3.get("check_count")==52,
       {"status":prop_phase3.get("status"),"checks":prop_phase3.get("check_count"),"errors":prop_phase3.get("error_count")})
else:
    ck("prop_support_phase3_validator",False,str(prop_phase3_path))

errors=[x for x in checks if x["severity"]=="error" and not x["pass"]]
result={
    "purpose":"Unified support-lane static/preflight validator. It must not be interpreted as gameplay validation.",
    "timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status":"pass" if not errors else "fail",
    "error_count":len(errors),
    "checks":checks,
    "playtest_required":True,
    "astra_v88_modified_by_validator":False,
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"status":result["status"],"checks":len(checks),"errors":errors},indent=2))