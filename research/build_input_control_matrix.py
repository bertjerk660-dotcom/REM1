from pathlib import Path
import json, hashlib

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=ROOT/"build/prepared/thug2_controller_map/decompiled"
OUT=ROOT/"build/prepared/input_control_matrix"
OUT.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

sources=[]
for p in sorted(SRC.rglob("*.q")):
    sources.append({"path":str(p.relative_to(ROOT)).replace("\\","/"),"sha256":sha(p),"bytes":p.stat().st_size})

matrix=[
 {"mode":"THUG2 skate","action":"Ollie / jump family","ps2_input":"X / Cross","xbox_equivalent":"A","evidence":"groundtricks.q uses PressAndRelease Up+X and JumpSlot; Xbox menu remap maps A to the PS2 choose/Cross role.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Flip trick family","ps2_input":"Square + direction/sequence","xbox_equivalent":"X + direction/sequence","evidence":"airtricks.q special-air slots use direction pairs + Square; Xbox remap maps X to pad_square.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Grab trick family","ps2_input":"Circle + direction/sequence","xbox_equivalent":"B + direction/sequence","evidence":"airtricks.q special-air slots use direction pairs + Circle; Xbox remap maps B to pad_circle.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Grind / lip / many manual-special families","ps2_input":"Triangle + direction/sequence","xbox_equivalent":"Y + direction/sequence","evidence":"grindlist.q, liptricks.q and manualtricks.q repeatedly use Triangle; Xbox remap exposes Y as triangle-style menu event.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Manual","ps2_input":"Up then Down","xbox_equivalent":"Up then Down","evidence":"manualtricks.q maps Up,Down to Trick_Manual.","confidence":"direct source"},
 {"mode":"THUG2 skate","action":"Nose Manual","ps2_input":"Down then Up","xbox_equivalent":"Down then Up","evidence":"manualtricks.q maps Down,Up to Trick_NoseManual.","confidence":"direct source"},
 {"mode":"THUG2 skate","action":"Nollie modifier","ps2_input":"L2","xbox_equivalent":"Left trigger full","evidence":"groundtricks.q uses L2 for ToggleNollieRegular; Xbox button-remap maps full left trigger to pad_l2.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Switch / stance modifier","ps2_input":"R2","xbox_equivalent":"Right trigger full","evidence":"groundtricks.q uses R2 for ToggleSwitchRegular; Xbox button-remap maps full right trigger to pad_r2.","confidence":"source-supported mapping"},
 {"mode":"THUG2 skate","action":"Revert slots","ps2_input":"R2 / L2","xbox_equivalent":"Full right / full left trigger","evidence":"groundtricks.q Reverts array binds ExtraSlot1/2 to R2/L2.","confidence":"direct source + remap"},
 {"mode":"THUG2 skate","action":"Switch skating <-> walking control trigger","ps2_input":"L1 + R1","xbox_equivalent":"Black","evidence":"switch_control.q directly declares PressTwoAnyOrder L1,R1 and xbox_trigger = Press black.","confidence":"direct source"},
 {"mode":"THUG2 menu","action":"Choose/confirm","ps2_input":"X / Cross","xbox_equivalent":"A","evidence":"menubuttonremap.q maps PS2 X and Xbox A to pad_choose.","confidence":"direct source"},
 {"mode":"THUG2 menu","action":"Back","ps2_input":"Triangle","xbox_equivalent":"B / Back depending context","evidence":"menubuttonremap.q maps PS2 triangle to pad_back and Xbox B plus Back to pad_back.","confidence":"direct source"},
 {"mode":"THUG2 menu","action":"Square-style option","ps2_input":"Square","xbox_equivalent":"X","evidence":"menubuttonremap.q maps both to pad_square.","confidence":"direct source"},
 {"mode":"THUG2 menu","action":"Circle-style option","ps2_input":"Circle","xbox_equivalent":"B","evidence":"menubuttonremap.q maps both to pad_circle.","confidence":"direct source"},
 {"mode":"GMod Q menu","action":"Open/hold Q menu","keyboard_mouse":"Q","evidence":"Project requirement: real GMod Q/spawn menu workflow; runtime port remains Astra-owned.","confidence":"product requirement"},
 {"mode":"GMod Tool Gun","action":"Primary tool action","keyboard_mouse":"Left mouse","evidence":"Real gmod_tool/shared.lua delegates PrimaryAttack to tool:LeftClick(trace).","confidence":"direct installed GMod source"},
 {"mode":"GMod Tool Gun","action":"Secondary tool action","keyboard_mouse":"Right mouse","evidence":"Real gmod_tool/shared.lua delegates SecondaryAttack to tool:RightClick(trace).","confidence":"direct installed GMod source"},
 {"mode":"GMod Tool Gun","action":"Tool reload action","keyboard_mouse":"Reload binding","evidence":"Real gmod_tool/shared.lua delegates Reload to tool:Reload(trace).","confidence":"direct installed GMod source"},
 {"mode":"GMod Tool Gun","action":"Select tool","keyboard_mouse":"Real Q-menu tool panel","evidence":"Real Tool Gun reads gmod_toolmode; project forbids Fallout prompt selectors.","confidence":"direct installed GMod source + product requirement"},
 {"mode":"GMod Physics Gun","action":"Pick up / hold target","keyboard_mouse":"Right mouse","evidence":"Project owner explicitly requires RMB pickup/hold for the integrated Physgun.","confidence":"product requirement override"},
 {"mode":"GMod Physics Gun","action":"Launch held target","keyboard_mouse":"Left mouse","evidence":"Project owner explicitly requires LMB launch for the integrated Physgun.","confidence":"product requirement override"},
 {"mode":"Fallout baseline","action":"Normal host controls","keyboard_mouse":"Use current Fallout binding","xbox_equivalent":"Use current Fallout binding","evidence":"Product rule: normal Fallout gameplay remains active outside imported modes.","confidence":"product requirement"}
]

result={
 "purpose":"Authoritative support-lane control/input evidence matrix. It documents source bindings and product overrides without implementing runtime input code.",
 "source_files":sources,
 "matrix":matrix,
 "notes":[
   "THUG2 source uses PS2-style symbolic button names in gameplay QB; Xbox equivalents are only asserted where the original remap/source directly supports them.",
   "Do not replace user-customizable Fallout baseline bindings with hard-coded assumptions.",
   "Astra owns the actual input-mode switching, controller polling and runtime state integration."
 ]
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")

md=["# Input Control Matrix","","Generated from decompiled local THUG2 QB evidence, installed GMod Lua and project requirements.","",
"| Mode | Action | PS2/source | Xbox | Keyboard/mouse | Confidence |","|---|---|---|---|---|---|"]
for r in matrix:
    md.append("| {} | {} | {} | {} | {} | {} |".format(
        r.get("mode","").replace("|","/"),r.get("action","").replace("|","/"),
        r.get("ps2_input","—").replace("|","/"),r.get("xbox_equivalent","—").replace("|","/"),
        r.get("keyboard_mouse","—").replace("|","/"),r.get("confidence","").replace("|","/")))
md += ["","Runtime implementation remains Astra-owned; this document is input evidence and a handoff contract, not proof of an integrated controller layer."]
(OUT/"CONTROL_MATRIX.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps({"matrix_entries":len(matrix),"source_files":len(sources)},indent=2))