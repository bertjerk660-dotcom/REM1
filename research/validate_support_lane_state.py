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