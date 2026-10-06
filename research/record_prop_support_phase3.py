from pathlib import Path
import json,hashlib,datetime,re
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
VALID=json.loads((ROOT/"build/validation/prop_support_phase3.json").read_text())
SUP=json.loads((ROOT/"build/validation/support_lane_state.json").read_text())
SUM=json.loads((ROOT/"build/prepared/prop_support_phase3/summary.json").read_text())
REL=json.loads((ROOT/"build/prepared/release_install_manifest/summary.json").read_text())
THUG=json.loads((ROOT/"build/prepared/prop_support_phase3/thug2_promotion_queue.json").read_text())
BUDGET=json.loads((ROOT/"build/prepared/prop_support_phase3/menu_budget.json").read_text())

plan=ROOT/"context/PROP_SUPPORT_NEXT_20.md"
s=plan.read_text(encoding="utf-8")
s=s.replace("19. **Build prop release/provenance metadata — IN PROGRESS.** Current prop payloads/manifests are indexed; phase-3 outputs still need to be folded into the release/support validator.",
            f"19. **Build prop release/provenance metadata — COMPLETE.** Phase-3 outputs are folded into the release manifest and unified support validator; release support-manifest count is {REL['support_manifests']}.")
s=s.replace("20. **Validate, record and push this prop phase to GitHub — IN PROGRESS.** Add phase-3 validation, build manifest and update CURRENT_STATE/OPEN_WORK on prep/prop-content-phase3.",
            f"20. **Validate, record and push this prop phase to GitHub — READY TO PUSH.** Prop validator passes {VALID['check_count']} checks with zero errors and unified support validator passes {len(SUP['checks'])}; docs/build manifest are recorded locally. Final gate is GitHub branch verification.")
plan.write_text(s,encoding="utf-8")

state=ROOT/"context/CURRENT_STATE.md"
cs=state.read_text(encoding="utf-8")
cs=re.sub(r"Unified support validator now passes \d+ static/preflight checks","Unified support validator now passes %d static/preflight checks"%len(SUP["checks"]),cs)
cs=re.sub(r"Unified support validator passes \d+ checks","Unified support validator passes %d checks"%len(SUP["checks"]),cs)
marker="## Prop support phase 3 — 2026-10-06"
block=f"""
{marker}
- New non-Astra/non-Opus prop-focused workflow is tracked in context/PROP_SUPPORT_NEXT_20.md.
- Runtime/Astra code was not modified. Installed v85, main ESP and isolated v88 hashes remain protected.
- Ready player-facing prop catalog remains 290: 170 native FNV + 120 converted GMod/Source.
- A unified static quality/utility ledger now covers all 290 ready props; all retain form binding, collision evidence and generated support thumbnails.
- 56 representative props are prepared in 5 human runtime test batches; runtime results are still pending.
- GMod dependency audit covers all 120 curated props, 85 unique material files and source-authored mobility evidence.
- Native mounted GMod SpawnIcon lookup found 0 matching prebuilt icons for this curated set; 120/120 generated geometry previews remain fallback/audit assets only.
- THUG2 prop work is ranked, not falsely promoted: all 85 spatial geometry candidates are scored and a top-20 visual leaf review packet is prepared.
- Menu growth policy targets 310 first while staying inside 300-320. Up to 20 validated THUG2 props can be added before replacement pressure; 40 lower-priority current entries are ranked as a later replacement reserve only.
- Dedicated prop validator passes {VALID['check_count']} checks with zero errors. Unified support validator passes {len(SUP['checks'])} checks with zero errors.
- Release/install metadata now indexes {REL['support_manifests']} support manifests and still reports no missing core files.
- No phase-3 prop has been called gameplay-verified; sidecars remain disabled and human collision/scale/contact testing is required.
"""
if marker in cs:
    cs=cs.split(marker)[0].rstrip()+"\n\n"+block.strip()+"\n"
else:
    cs=cs.rstrip()+"\n\n"+block.strip()+"\n"
state.write_text(cs,encoding="utf-8")

openp=ROOT/"context/OPEN_WORK.md"
ow=openp.read_text(encoding="utf-8")
ow=re.sub(r"current pass count is \d+","current pass count is %d"%len(SUP["checks"]),ow)
marker2="## Prop support phase 3 remaining gates"
block2=f"""
{marker2}
- Execute the 5 prepared representative prop runtime batches and write results into build/prepared/prop_support_phase3/runtime_validation_ledger.json.
- Keep REM_GModProps_Catalog.esp disabled outside its isolated prop test.
- Visually verify the top-20 THUG2 candidate leaves before any split/conversion; none are standalone props yet.
- Promote THUG2 props only after independent geometry, scale, collision, texture and spawn-safety validation.
- Keep the player-facing prop browser within 300-320. First target is 310; after that, replace lower-priority/redundant entries rather than allowing unbounded growth.
- Do not interpret generated geometry previews as native GMod SpawnIcons; the real Q-menu runtime remains Astra-owned.
"""
if marker2 in ow:
    ow=ow.split(marker2)[0].rstrip()+"\n\n"+block2.strip()+"\n"
else:
    ow=ow.rstrip()+"\n\n"+block2.strip()+"\n"
openp.write_text(ow,encoding="utf-8")

rel_doc=ROOT/"context/RELEASE_MANIFEST.md"
rd=rel_doc.read_text(encoding="utf-8")
rd=re.sub(r"Current result: \d+ checks / zero errors",f"Current result: {len(SUP['checks'])} checks / zero errors",rd)
rd=re.sub(r"Reproducibility/support manifests are indexed separately(?:; current count: \d+)?\.",f"Reproducibility/support manifests are indexed separately; current count: {REL['support_manifests']}.",rd)
rel_doc.write_text(rd,encoding="utf-8")

bp=ROOT/"builds/prop_support_phase3_20261006.json"
build={
 "build":"prop_support_phase3_20261006",
 "branch":"prep/prop-content-phase3",
 "parent_support":"prep/support-workflow",
 "goal":"Advance the merged game's prop/content side without modifying Astra/Opus runtime work.",
 "changes":[
   "new prop-focused 20-step support workflow",
   "290-prop static quality/utility and redundancy ledgers",
   "GMod 120-prop scale/mobility/material dependency audit",
   "FNV form/content dependency hints",
   "56-prop / 5-batch human runtime test plan and 290-prop pending validation ledger",
   "85 THUG2 spatial candidates ranked plus top-20 visual leaf review packet",
   "300-320 menu budget with first target 310 and 40-entry replacement reserve",
   "native GMod SpawnIcon lookup result recorded; support fallbacks retained",
   "phase-3 prop validator integrated into unified support validation and release metadata"
 ],
 "validation":{
   "prop_phase3":{"status":VALID["status"],"checks":VALID["check_count"],"errors":VALID["error_count"]},
   "unified_support":{"status":SUP["status"],"checks":len(SUP["checks"]),"errors":SUP["error_count"]}
 },
 "playtest":"not_run",
 "runtime_changes":False,
 "protected_hashes":{
   "installed_v85":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
   "astra_v88":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
   "main_esp":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7"
 },
 "prop_summary":SUM,
 "thug2_top20":[{"level":x["level"],"identifier":x["identifier"],"category":x["category"],"score":x["promotion_review_score"]} for x in THUG["top20"]],
 "menu_budget":{"current":BUDGET["current_ready"],"range":BUDGET["target_range"],"first_wave_target":BUDGET["first_wave_target"],"replacement_reserve":len(BUDGET["replacement_reserve"])},
 "known_gates":[
   "Human prop runtime batches not run.",
   "THUG2 top-20 requires visual leaf confirmation before splitting/conversion.",
   "Real GMod Q-menu runtime remains Astra-owned.",
   "No current ready prop has been removed or promoted based only on static scoring."
 ]
}
bp.write_text(json.dumps(build,indent=2),encoding="utf-8")
print(json.dumps({"build":str(bp),"prop_checks":VALID["check_count"],"support_checks":len(SUP["checks"]),"support_manifests":REL["support_manifests"]},indent=2))