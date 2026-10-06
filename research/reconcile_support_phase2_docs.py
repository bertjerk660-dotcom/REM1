from pathlib import Path
import json
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
VALID=json.loads((ROOT/"build/validation/support_lane_state.json").read_text())
REL=json.loads((ROOT/"build/prepared/release_install_manifest/summary.json").read_text())
TARGET=json.loads((ROOT/"build/prepared/thug2_prop_catalog/target_classification.json").read_text())
TOOL=json.loads((ROOT/"build/prepared/gmod_tool_physgun_asset_handoff/manifest.json").read_text())
CTRL=json.loads((ROOT/"build/prepared/input_control_matrix/manifest.json").read_text())
HIST=json.loads((ROOT/"build/prepared/historical_artifact_registry/manifest.json").read_text())
REG=json.loads((ROOT/"build/prepared/regression_test_packs/manifest.json").read_text())
nchecks=len(VALID.get("checks",[]))

def replace_count(path):
    s=path.read_text(encoding="utf-8")
    s=s.replace("passes 94 static/preflight checks","passes %d static/preflight checks"%nchecks)
    s=s.replace("current pass count is 94","current pass count is %d"%nchecks)
    s=s.replace("passes 94 checks","passes %d checks"%nchecks)
    path.write_text(s,encoding="utf-8")

for rel in ["context/CURRENT_STATE.md","context/OPEN_WORK.md","context/SUPPORT_20_POINT_TRACKER.md"]:
    replace_count(ROOT/rel)

doc=ROOT/"context/RELEASE_MANIFEST.md"
lines=[
"# Release / Install Manifest","",
"Generated from the current support pipeline. This is a staging/install manifest, not a claim that the mashup is release-ready.","",
"## Current package index",
f"- Core runtime/test files: {REL['core_files']}; missing core files: {len(REL['missing_core'])}.",
f"- Pip-Boy origin icons: {REL['origin_icons']}.",
f"- THUG2 skateboard NIFs: {REL['board_files']}.",
f"- Combine Soldier test NIFs: {REL['combine_test_files']}.",
f"- Curated transformed GMod prop payload files: {REL['gmod_prop_payload_files']}.",
f"- Native FNV catalog references: {REL['fnv_native_catalog_refs']}.",
f"- Custom GMod catalog references: {REL['gmod_custom_catalog_refs']}.",
f"- Reproducibility/support manifests indexed: {REL['support_manifests']}.",
"- Installed runtime remains v85; Astra v88 remains protected and not installed.",
"- All support sidecars are disabled in the baseline load order.","",
"## Promotion gates",
f"- Run the unified support validator with zero errors; current result: {VALID['status']} ({nchecks} checks).",
"- Run baseline boot/load/save/reload.",
"- Run representative inventory/drop/pickup/container/trade tests.",
"- Run representative curated-prop scale/texture/collision tests.",
"- Run the isolated Combine armor player/NPC/drop/save-load pack before any Enclave/Remnants replacement.",
"- Run Astra-owned THUG2 skate and real GMod Q-menu/Tool Gun/Physgun runtime packs before release.","",
"Machine-readable details: build/prepared/release_install_manifest/manifest.json and summary.json."
]
doc.write_text("\n".join(lines)+"\n",encoding="utf-8")

bp=ROOT/"builds/support_phase2_20261006.json"
b=json.loads(bp.read_text(encoding="utf-8"))
b["validation"]={"status":VALID["status"],"checks":nchecks,"error_count":VALID["error_count"]}
b["canonical_support"]={
  "input_control_matrix_entries":len(CTRL.get("matrix",[])),
  "input_source_files":len(CTRL.get("source_files",[])),
  "tool_physgun_assets":{"requested":TOOL.get("requested"),"resolved":TOOL.get("resolved"),"missing":TOOL.get("missing")},
  "thug2_prop_classification":TARGET.get("classification_counts"),
  "historical_artifact_count":HIST.get("artifact_count"),
  "regression_pack_count":REG.get("pack_count"),
  "gmod_prop_payload_files":REL.get("gmod_prop_payload_files"),
}
bp.write_text(json.dumps(b,indent=2),encoding="utf-8")

fp=ROOT/"context/FAILURE_KNOWLEDGE.md"
s=fp.read_text(encoding="utf-8")
entry="""
## FS002 - Parallel support generators can leave stale duplicate manifests
Observed 2026-10-06 while reconciling the support lane. Parallel work produced smaller duplicate artifacts beside richer canonical outputs: a 28/27 Tool Gun/Physgun inventory beside the canonical 36/33 handoff, a 7-pack regression file beside the canonical 8-pack set, and a 41-item version inventory beside the canonical 63-item historical registry. A stale local 20-point tracker also lagged the GitHub support branch.
Durable rule: before updating support docs or validators, compare local and GitHub support state and prefer the explicitly canonical artifacts named by context/SUPPORT_20_POINT_TRACKER.md. Do not overwrite a richer/newer manifest with a smaller duplicate merely because the duplicate was generated later in the current chat. Preserve superseded evidence, but drive status/validation from the canonical manifest.
"""
if "## FS002 - Parallel support generators" not in s:
    s=s.rstrip()+"\n\n"+entry.strip()+"\n"
    fp.write_text(s,encoding="utf-8")

sp=ROOT/"builds/support_phase2_reconciliation_20261006.json"
rec={
 "purpose":"Reconcile concurrent support outputs and restore the intended disabled-sidecar baseline without changing v85/v88 runtime binaries.",
 "validator":{"status":VALID["status"],"checks":nchecks,"errors":VALID["error_count"]},
 "canonical_counts":{
   "props_ready":290,
   "thug2_targets":106,
   "thug2_target_classes":TARGET.get("classification_counts"),
   "control_matrix_entries":len(CTRL.get("matrix",[])),
   "tool_physgun_requested":TOOL.get("requested"),
   "tool_physgun_resolved":TOOL.get("resolved"),
   "historical_artifacts":HIST.get("artifact_count"),
   "regression_packs":REG.get("pack_count"),
   "gmod_prop_payload_files":REL.get("gmod_prop_payload_files"),
 },
 "baseline_restored":{
   "plugins_txt":"REM_GModTHUG2.esp only",
   "combine_test_sidecar_disabled":True,
   "runtime_dll_unchanged":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
   "astra_v88_unchanged":"6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439",
   "main_esp_unchanged":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7"
 },
 "playtest":"not_run"
}
sp.write_text(json.dumps(rec,indent=2),encoding="utf-8")
print(json.dumps({"validator_checks":nchecks,"release_payload_files":REL["gmod_prop_payload_files"],"regression_packs":REG["pack_count"],"historical_artifacts":HIST["artifact_count"]},indent=2))