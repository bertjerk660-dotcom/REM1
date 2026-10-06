from pathlib import Path
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")

# Add prop phase-3 metadata to the release/install manifest generator.
rp=ROOT/"research/build_release_install_manifest.py"
s=rp.read_text(encoding="utf-8")
anchor=' "build/prepared/historical_artifact_registry/manifest.json",\n'
addition=' "build/prepared/prop_support_phase3/summary.json",\n "build/validation/prop_support_phase3.json",\n'
if addition.strip() not in s:
    if anchor not in s: raise SystemExit("release manifest anchor missing")
    s=s.replace(anchor,anchor+addition)
rp.write_text(s,encoding="utf-8")

# Fold the dedicated prop validator into the unified support validator.
vp=ROOT/"research/validate_support_lane_state.py"
v=vp.read_text(encoding="utf-8")
anchor2='errors=[x for x in checks if x["severity"]=="error" and not x["pass"]]\n'
block=r'''
prop_phase3_path=ROOT/"build/validation/prop_support_phase3.json"
if prop_phase3_path.exists():
    prop_phase3=json.loads(prop_phase3_path.read_text(encoding="utf-8"))
    ck("prop_support_phase3_validator",
       prop_phase3.get("status")=="pass" and prop_phase3.get("error_count")==0 and prop_phase3.get("check_count")==52,
       {"status":prop_phase3.get("status"),"checks":prop_phase3.get("check_count"),"errors":prop_phase3.get("error_count")})
else:
    ck("prop_support_phase3_validator",False,str(prop_phase3_path))

'''
if "prop_phase3_path=ROOT/" not in v:
    if anchor2 not in v: raise SystemExit("support validator anchor missing")
    v=v.replace(anchor2,block+anchor2)
vp.write_text(v,encoding="utf-8")
print("integrated")