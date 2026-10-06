from pathlib import Path
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")

rp=ROOT/"research/build_release_install_manifest.py"
s=rp.read_text(encoding="utf-8")
anchor=' "build/validation/prop_support_phase3.json",\n'
addition=' "build/prepared/prop_support_phase4/summary.json",\n "build/validation/prop_support_phase4.json",\n'
if addition.strip() not in s:
    if anchor not in s:raise SystemExit("release anchor missing")
    s=s.replace(anchor,anchor+addition)
rp.write_text(s,encoding="utf-8")

vp=ROOT/"research/validate_support_lane_state.py"
v=vp.read_text(encoding="utf-8")
anchor2='errors=[x for x in checks if x["severity"]=="error" and not x["pass"]]\n'
block=r'''
prop_phase4_path=ROOT/"build/validation/prop_support_phase4.json"
if prop_phase4_path.exists():
    prop_phase4=json.loads(prop_phase4_path.read_text(encoding="utf-8"))
    ck("prop_support_phase4_validator",
       prop_phase4.get("status")=="pass" and prop_phase4.get("error_count")==0 and prop_phase4.get("check_count")==50,
       {"status":prop_phase4.get("status"),"checks":prop_phase4.get("check_count"),"errors":prop_phase4.get("error_count")})
else:
    ck("prop_support_phase4_validator",False,str(prop_phase4_path))

'''
if "prop_phase4_path=ROOT/" not in v:
    if anchor2 not in v:raise SystemExit("validator anchor missing")
    v=v.replace(anchor2,block+anchor2)
vp.write_text(v,encoding="utf-8")
print("phase4 integrated")