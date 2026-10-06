import json, hashlib
from pathlib import Path
root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
out=root/"build/prepared/agent_handoff_2026-10-06"
out.mkdir(parents=True,exist_ok=True)
cls=json.loads((root/"build/prepared/thug2_prop_catalog/target_classification.json").read_text(encoding="utf-8-sig"))
ready=[x for x in cls["records"] if x.get("confidence")!="not_ready"]
assert len(ready)==85
for i,x in enumerate(ready,1):
    x["handoff_rank"]=i
    x["source_level_glb"]=f"build/prepared/thug2_prop_catalog/level_glb/{x['level']}/{x['level']}.glb"
    x["conversion_gate"]="isolate original component -> preserve original material -> convert to NIF -> collision/scale validation -> sidecar spawn test"
    x["do_not"]="Do not recreate or infer missing geometry."
prop={"schema":"rem.thug2.prop_conversion_inputs.v1","count":len(ready),"records":ready}
(out/"thug2_85_conversion_inputs.json").write_text(json.dumps(prop,indent=2),encoding="utf-8")
assets=json.loads((root/"build/prepared/gmod_tool_physgun_asset_handoff/manifest.json").read_text(encoding="utf-8-sig"))
phys=[a for a in assets["assets"] if any(k in a["path"].lower() for k in ("phys","weapon_physgun"))]
pkg={"schema":"rem.gmod.physgun.implementation_package.v1","status":"implementation_ready_evidence_assets_not_runtime_complete","native_evidence":"context/HANDOFFS/PHYSGUN_IDA68_EVIDENCE_CLOSURE.md","asset_manifest":"build/prepared/gmod_tool_physgun_asset_handoff/manifest.json","physgun_assets":phys,"known_asset_gap":["models/weapons/v_physics.mdl","models/weapons/v_physics.vvd","models/weapons/v_physics.dx90.vtx"],"state_machine":["IDLE_TRACE","ACQUIRE","HOLD","ROTATE","DISTANCE_ADJUST","FREEZE","DROP","PUNT","CLEANUP"],"required_state":["grabbed entity/reference","target-local hit offset","hold distance","target orientation","actor/ragdoll state","beam endpoint","hold-controller state"],"integration_gates":["ordinary movable prop pickup","beam endpoint attachment","stable hold while moving","wheel distance adjustment","rotation","freeze/reacquire","drop","punt","invalid/static rejection","NPC/ragdoll","weapon-switch cleanup","cell/save/load cleanup","original sounds/effects transitions"],"rule":"Use IDA Pro 6.8 evidence and original GMod assets/scripts; do not substitute invented behavior."}
(out/"physgun_implementation_package.json").write_text(json.dumps(pkg,indent=2),encoding="utf-8")
manifest={"schema":"rem.agent_handoff.v1","target_agents":["GPT-6","Opus 5.5"],"physgun_package":"physgun_implementation_package.json","thug2_prop_package":"thug2_85_conversion_inputs.json","thug2_count":85,"proprietary_assets_committed":False,"runtime_success_claimed":False}
for fn in ["physgun_implementation_package.json","thug2_85_conversion_inputs.json"]:
    b=(out/fn).read_bytes();manifest.setdefault("sha256",{})[fn]=hashlib.sha256(b).hexdigest().upper()
(out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]