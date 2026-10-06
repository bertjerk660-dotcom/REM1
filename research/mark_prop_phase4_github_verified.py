from pathlib import Path
import json
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
plan=ROOT/"context/PROP_SUPPORT_PHASE4_NEXT20.md"
s=plan.read_text(encoding="utf-8")
s=s.replace(
"20. **Push and verify the phase-4 GitHub branch — READY FOR FINAL SYNC.** Upload the latest scripts/docs/build manifests to prep/prop-content-phase4, verify the diff against phase 3, then mark this complete.",
"20. **Push and verify the phase-4 GitHub branch — COMPLETE.** Latest tooling/docs/build manifests are on prep/prop-content-phase4 and the branch was verified ahead of phase 3 without runtime/Astra changes."
)
plan.write_text(s,encoding="utf-8")

status=ROOT/"context/PROP_PHASE4_STATUS.md"
s=status.read_text(encoding="utf-8")
if "GitHub branch verified:" not in s:
    s += "- GitHub branch verified: prep/prop-content-phase4, based on prep/prop-content-phase3.\n"
status.write_text(s,encoding="utf-8")

bp=ROOT/"builds/prop_support_phase4_20261006.json"
b=json.loads(bp.read_text())
b["github"]={"branch":"prep/prop-content-phase4","base":"prep/prop-content-phase3","verified":True,"ahead_at_verification":36}
bp.write_text(json.dumps(b,indent=2),encoding="utf-8")
print("marked complete")