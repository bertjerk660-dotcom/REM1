from pathlib import Path
import json, hashlib, datetime

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"build/handoffs/gpt6_opus/feed_bundle"
OUT.mkdir(parents=True,exist_ok=True)
PLUGIN=ROOT/"third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin"
MAIN=PLUGIN/"main.cpp"
PRE=ROOT/"build/prepared/pre_opus_20261006"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def meta(p):
    p=Path(p)
    rel=str(p.relative_to(ROOT)).replace("\\","/") if p.exists() and ROOT in p.parents else str(p)
    return {"path":rel,"exists":p.exists(),"bytes":p.stat().st_size if p.exists() and p.is_file() else None,"sha256":sha(p) if p.exists() and p.is_file() else None}

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8-sig"))

runtime=load("build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json")
pre_summary=load("build/prepared/pre_opus_20261006/summary.json")
tool_assets=load("build/prepared/gmod_tool_physgun_asset_handoff/manifest.json")
board=load("build/prepared/thug2_skateboard_asset_handoff/manifest.json")
phys_gap=load("build/prepared/pre_opus_20261006/physgun_provenance_gap.json")

queue={
 "schema":"rem.opus_visual_execution_queue.v2",
 "generated":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "ownership":{
   "chatgpt":"workflow/orchestration, manifests, evidence, validation planning",
   "opus":"visual/model/material/rigging/conversion/animation implementation and related visual integration code",
   "astra":"native/deep runtime mechanics, physics, camera hooks, crash-sensitive state integration",
   "ida":"IDA Pro 6.8 only"
 },
 "protected_baseline":{
   "runtime_dll_sha256":"BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41",
   "main_esp_sha256":"0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7",
   "active_source_sha256":sha(MAIN),
   "rule":"Do not overwrite the deployed baseline during Opus visual work."
 },
 "tasks":[
  {"id":"O01","title":"Golden Source bench end-to-end proof","priority":1,"inputs":["build/handoffs/gpt6_opus/GOLDEN_BENCH_IMPLEMENTATION_HANDOFF.md","build/prepared/pre_opus_20261006/bench_source_packet.json"],"outputs":["isolated bench NIF/materials/collision","disabled test sidecar","implementation manifest"],"gates":["visible","source-faithful materials","credible scale/orientation","collision","spawnable","save/load","no crash"],"stop_on_failure":True},
  {"id":"O02","title":"Tool Gun first/third/world visual implementation","priority":2,"depends":["O01"],"inputs":["build/prepared/pre_opus_20261006/c_toolgun_source_packet.json","build/prepared/pre_opus_20261006/w_toolgun_source_packet.json","build/prepared/gmod_hl_weapon_models/manifest.json","build/handoffs/gpt6_opus/WEAPON_VISIBILITY_ACCEPTANCE_MATRIX.md"],"outputs":["isolated Tool Gun visual candidate","attachment/scale manifest"],"gates":["first-person visible","third-person visible","world/drop visible","hands/attachment credible","no missing materials","no crash"]},
  {"id":"O03","title":"Physics Gun presentation provenance + visual candidate","priority":3,"depends":["O01"],"inputs":["build/prepared/pre_opus_20261006/c_superphyscannon_source_packet.json","build/prepared/pre_opus_20261006/w_physics_source_packet.json","build/prepared/pre_opus_20261006/physgun_provenance_gap.json","build/prepared/gmod_tool_physgun_asset_handoff/manifest.json"],"outputs":["provenance verdict","isolated visual candidate only if source constraint is satisfied"],"gates":["no fabricated v_Physics substitute","world model identity proven","materials resolve","candidate isolated","no mechanics changes"]},
  {"id":"O04","title":"THUG2 skateboard visual identity and attachment pipeline","priority":4,"depends":["O01"],"inputs":["build/prepared/thug2_skateboard_asset_handoff/manifest.json","build/prepared/thug2_skateboard_asset_handoff/scale_attachment_analysis.json","build/prepared/pre_opus_20261006/thug2_evidence_index.json"],"outputs":["one canonical board visual identity","held attachment candidate","riding/feet attachment candidate","animation-ready rig/attachment manifest"],"gates":["same mesh/material identity held/riding/world","no geometry recreation","scale/axes documented","attachment parents documented","source animation names preserved"]},
  {"id":"O05","title":"THUG2 animation asset/retarget preparation","priority":5,"depends":["O04"],"inputs":["third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/thug2_anim_data.inc","build/prepared/pre_opus_20261006/thug2_evidence_index.json"],"outputs":["retarget map","animation asset candidates","visual/animation implementation manifest"],"gates":["original timing preserved","bone mapping explicit","no stale bone-pointer assumptions","no runtime camera/physics rewrite"]},
  {"id":"O06","title":"THUG2 environment prop visual conversion wave","priority":6,"depends":["O01"],"inputs":["build/handoffs/gpt6_opus/thug2_props/conversion_queue.json","build/prepared/pre_opus_20261006/thug2_prop_evidence_index.json"],"outputs":["independently split/converted visual candidates","per-prop provenance/scale/material manifests"],"gates":["original geometry only","visual identity reviewed","materials/UVs preserved","scale documented","collision candidate documented"],"note":"Do not import THUG2 maps or force semantic/gap identifiers into props."}
 ],
 "reserved_for_astra":["real GMod Q-menu compatibility runtime","Tool Gun lifecycle/tool execution mechanics","Physics Gun target/hold/rotate/freeze/drop/launch mechanics","THUG2 movement/physics/camera/runtime state machine","crash-sensitive NVSE/native hooks","final runtime promotion"]
}
(OUT/"OPUS_VISUAL_QUEUE.json").write_text(json.dumps(queue,indent=2),encoding="utf-8")

lines=MAIN.read_text(encoding="utf-8",errors="ignore").splitlines()
symbol_lines={}
for area in runtime.get("areas",[]):
    for item in area.get("symbols",[]):
        if ":" in item:
            name,ln=item.rsplit(":",1)
            try:symbol_lines[name]=int(ln)
            except:pass
wanted=["ApplyGModWeaponAnimationProfile","GetEquippedGModRuntimeWeapon","EnsureGModWeaponForms","EnterSkateMode","ExitSkateMode","SpawnConvertedProp","UpdatePendingSpawn","OpenBuildMenu","UpdateSkateMode","PollControls"]
code_md=["# Opus code context — visual integration boundaries","","Generated from current project-authored runtime source. This is visual/model/animation integration context, not authorization to take over Astra-owned deep runtime mechanics.",f"Source: {runtime['active_source']['path']}",f"SHA256: {sha(MAIN)}",""]
for name in wanted:
    ln=symbol_lines.get(name)
    if not ln: continue
    radius=34 if name not in ("UpdateSkateMode","PollControls") else 24
    a=max(1,ln-radius); b=min(len(lines),ln+radius)
    code_md += [f"## {name}",f"Recorded anchor line {ln}; excerpt {a}-{b}.","~~~cpp"]
    code_md += [f"{i:05d}: {lines[i-1]}" for i in range(a,b+1)]
    code_md += ["~~~",""]
for inc in ["gmod_weapon_defs.inc","gmod_tool_defs.inc"]:
    p=PLUGIN/inc
    code_md += [f"## {inc}",f"SHA256: {sha(p)}","~~~cpp",p.read_text(encoding="utf-8",errors="ignore").rstrip(),"~~~",""]
anim=(PLUGIN/"thug2_anim_data.inc").read_text(encoding="utf-8",errors="ignore").splitlines()
ranges=[(1,min(35,len(anim)))]
for i,x in enumerate(anim,1):
    if "static const THUG2AnimClip kTHUG2AnimClips[]" in x:
        ranges.append((i,min(len(anim),i+40))); break
code_md += ["## thug2_anim_data.inc structural excerpt",f"Full file SHA256: {sha(PLUGIN/'thug2_anim_data.inc')}"]
for a,b in ranges:
    code_md += [f"Excerpt {a}-{b}:","~~~cpp"]+[f"{i:05d}: {anim[i-1]}" for i in range(a,b+1)]+["~~~"]
code_md += ["","Astra owns live retarget/cache/runtime integration. Opus should return visual/rig/animation assets plus explicit bone/attachment mappings for Astra to consume."]
(OUT/"CODE_CONTEXT.md").write_text("\n".join(code_md)+"\n",encoding="utf-8")

packet_names=["bench_source_packet.json","c_toolgun_source_packet.json","w_toolgun_source_packet.json","c_superphyscannon_source_packet.json","w_physics_source_packet.json","c_crowbar_source_packet.json","w_crowbar_source_packet.json","c_pistol_source_packet.json","w_pistol_source_packet.json","c_smg1_source_packet.json","w_smg1_source_packet.json"]
packets=[]
for name in packet_names:
    p=PRE/name
    if not p.exists(): continue
    j=json.loads(p.read_text(encoding="utf-8-sig"))
    packets.append({
      "id":j.get("id"),"model":j.get("model"),"packet":meta(p),"source_package":j.get("source_package"),
      "required_model_components":[{k:x.get(k) for k in ("relative","resolved","bytes","sha256","local_source","required")} for x in j.get("model_components",[]) if x.get("required")],
      "materials":[{k:x.get(k) for k in ("relative","resolved","bytes","sha256","local_source")} for x in j.get("materials",[])],
      "qc":[x.get("file") for x in j.get("qc",[]) if x.get("file")],
      "geometry":[x.get("file") for x in j.get("geometry",[]) if x.get("file")],
      "missing_dependencies":j.get("missing_dependencies",[])
    })
asset_index={
 "schema":"rem.opus_asset_reference_index.v1",
 "generated":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "policy":"GitHub-safe metadata only. Proprietary game binaries/assets remain on the authorized local machine and are referenced by path/hash.",
 "pre_opus_summary":pre_summary,
 "source_packets":packets,
 "tool_physgun_asset_handoff":{"requested":tool_assets.get("requested"),"resolved":tool_assets.get("resolved"),"missing":tool_assets.get("missing"),"manifest":meta(ROOT/"build/prepared/gmod_tool_physgun_asset_handoff/manifest.json")},
 "skateboard":{"manifest":meta(ROOT/"build/prepared/thug2_skateboard_asset_handoff/manifest.json"),"scale_analysis":meta(ROOT/"build/prepared/thug2_skateboard_asset_handoff/scale_attachment_analysis.json"),"animation_count":board.get("motoskateboard_animation_count"),"live_nifs":board.get("live_nifs",[])},
 "thug2":{"evidence_index":meta(ROOT/"build/prepared/pre_opus_20261006/thug2_evidence_index.json"),"prop_evidence_index":meta(ROOT/"build/prepared/pre_opus_20261006/thug2_prop_evidence_index.json"),"checked_assets":pre_summary.get("thug2_checked_assets"),"hash_failures":pre_summary.get("thug2_hash_failures")},
 "converter_inventory":meta(ROOT/"build/prepared/pre_opus_20261006/converter_inventory.json"),
 "physgun_provenance_gap":phys_gap
}
(OUT/"ASSET_REFERENCE_INDEX.json").write_text(json.dumps(asset_index,indent=2),encoding="utf-8")

prompt="""# Opus visual implementation start prompt

Continue the Fallout New Vegas + Garry's Mod + THUG2 merge from canonical repository bertjerk660-dotcom/REM1 and the authorized Windows workspace.

Read in order:
1. AGENTS.md
2. context/BOOTSTRAP.md
3. context/GOAL.md
4. context/CURRENT_STATE.md
5. context/ARCHITECTURE.md
6. context/DECISIONS.md
7. context/FAILURE_KNOWLEDGE.md
8. context/HANDOFFS/START_HERE_GPT6_OPUS.md
9. build/handoffs/gpt6_opus/EXECUTION_SEQUENCE.md
10. build/handoffs/gpt6_opus/feed_bundle/OPUS_VISUAL_QUEUE.json
11. build/handoffs/gpt6_opus/feed_bundle/ASSET_REFERENCE_INDEX.json
12. build/handoffs/gpt6_opus/feed_bundle/CODE_CONTEXT.md

Before changing anything, run research/validate_gpt6_opus_handoff.ps1 and research/validate_opus_feed_bundle.ps1. Stop on source/hash drift.

Ownership:
- Opus: visual/model/material/rigging/conversion/animation implementation plus visual integration code.
- GPT-6 Astra: native/deep runtime mechanics, Physics Gun manipulation mechanics, real Q-menu compatibility runtime, THUG2 movement/physics/camera state machine, crash-sensitive NVSE hooks and final runtime promotion.
- Normal ChatGPT: orchestration, evidence, manifests and validation planning.
- IDA Pro 6.8 only when reverse engineering is required.

Start with O01 only: authentic HL2 models/props_c17/bench01a.mdl golden-prop proof. Do not batch-convert further assets until O01 passes static and human runtime gates. Keep deployed v85 DLL/ESP protected and use isolated candidates/sidecars.

Do not fabricate or recreate missing original assets. The models/weapons/v_Physics.{mdl,vvd,dx90.vtx} provenance gap stays explicit unless resolved from authentic installed source evidence.

After each Opus task return: exact changed files, source/output hashes, implementation manifest, static validation result, exact candidate identity, human runtime evidence when run, blockers, and rollback instructions. Compilation alone is not completion.
"""
(OUT/"OPUS_START_PROMPT.md").write_text(prompt,encoding="utf-8")

handoff_paths=["context/HANDOFFS/START_HERE_GPT6_OPUS.md","build/handoffs/gpt6_opus/EXECUTION_SEQUENCE.md","build/handoffs/gpt6_opus/GOLDEN_BENCH_IMPLEMENTATION_HANDOFF.md","build/handoffs/gpt6_opus/WEAPON_VISIBILITY_ACCEPTANCE_MATRIX.md","build/handoffs/gpt6_opus/ACCEPTANCE_GATES.json","build/handoffs/gpt6_opus/REGRESSION_SPEC.json","build/handoffs/gpt6_opus/SIDECAR_STRATEGY.json","build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json","build/handoffs/gpt6_opus/runtime_harness/BASELINE.json","build/handoffs/gpt6_opus/runtime_harness/STAGED_TESTS.json","build/handoffs/gpt6_opus/runtime_harness/LOGGING_SPEC.json","build/handoffs/gpt6_opus/runtime_harness/CRASH_TRIAGE.json","research/validate_gpt6_opus_handoff.ps1"]
(OUT/"HANDOFF_INDEX.json").write_text(json.dumps({"files":[meta(ROOT/p) for p in handoff_paths]},indent=2),encoding="utf-8")

generated_files=["OPUS_VISUAL_QUEUE.json","CODE_CONTEXT.md","ASSET_REFERENCE_INDEX.json","OPUS_START_PROMPT.md","HANDOFF_INDEX.json"]
inputs=[MAIN,ROOT/"build/handoffs/gpt6_opus/RUNTIME_INTEGRATION_MAP.json",ROOT/"build/handoffs/gpt6_opus/EXECUTION_SEQUENCE.md",ROOT/"build/handoffs/gpt6_opus/GOLDEN_BENCH_IMPLEMENTATION_HANDOFF.md",ROOT/"build/prepared/pre_opus_20261006/summary.json",ROOT/"build/prepared/pre_opus_20261006/bench_source_packet.json",ROOT/"build/prepared/gmod_hl_weapon_models/manifest.json",ROOT/"build/prepared/thug2_skateboard_asset_handoff/manifest.json",ROOT/"build/prepared/pre_opus_20261006/thug2_evidence_index.json",ROOT/"build/prepared/pre_opus_20261006/thug2_prop_evidence_index.json"]
feed={"schema":"rem.opus_feed_bundle.v1","generated":datetime.datetime.now(datetime.timezone.utc).isoformat(),"mode":"PREPARATION_ONLY","ready_for_opus_visual_work":True,"source_hash":sha(MAIN),"generated_files":[meta(OUT/x) for x in generated_files],"primary_inputs":[meta(x) for x in inputs],"proprietary_assets_embedded":False,"first_task":"O01","deep_runtime_reserved_for_astra":True}
(OUT/"FEED_MANIFEST.json").write_text(json.dumps(feed,indent=2),encoding="utf-8")
print(json.dumps({"output":str(OUT),"generated_files":len(generated_files)+1,"source_packets":len(packets),"source_hash":feed["source_hash"],"first_task":feed["first_task"]},indent=2))