from pathlib import Path
import json,struct,zlib,hashlib,re

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
ESP=DATA/"REM_GModTHUG2.esp"
GMOD=json.loads((ROOT/"research/gmod_weapon_manifest.json").read_text())
RUNTIME=json.loads((ROOT/"build/prepared/gmod_weapon_runtime_candidates/manifest.json").read_text())
OUT=ROOT/"build/prepared/weapon_inventory_presentation_audit.json"

COMP=0x40000
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def subs(data):
    out=[];i=0;ext=None
    while i+6<=len(data):
        s=data[i:i+4];n=struct.unpack_from("<H",data,i+4)[0];i+=6
        if s==b"XXXX":
            if i+4>len(data):break
            ext=struct.unpack_from("<I",data,i)[0];i+=4;continue
        n=ext if ext is not None else n;ext=None
        if i+n>len(data):break
        out.append((s,data[i:i+n]));i+=n
    return out
def ds(b):return b.split(b"\0",1)[0].decode("cp1252","ignore")
def norm(s):
    return s.replace("/","\\").lstrip("\\").lower()
def model_rel(abs_path):
    if not abs_path:return None
    p=Path(abs_path)
    try:return norm(str(p.relative_to(DATA/"meshes")))
    except:return norm(str(p))

raw=ESP.read_bytes()
records={}
def walk(a,b):
    pos=a
    while pos+8<=b:
        sig=raw[pos:pos+4]
        if sig==b"GRUP":
            sz=struct.unpack_from("<I",raw,pos+4)[0];walk(pos+24,pos+sz);pos+=sz;continue
        if pos+24>b:return
        sz,flags,fid=struct.unpack_from("<III",raw,pos+4);end=pos+24+sz
        if end>b:return
        if sig in (b"WEAP",b"STAT"):
            data=raw[pos+24:end]
            if flags&COMP:
                try:data=zlib.decompress(data[4:])
                except:data=b""
            vv={}
            for s,v in subs(data):vv.setdefault(s.decode("latin1"),[]).append(v)
            r={"sig":sig.decode(),"fid":fid,"formid":f"{fid:08X}","flags":flags}
            for k in ("EDID","FULL","MODL","ICON","MICO"):
                if k in vv:r[k]=ds(vv[k][0])
            if "WNAM" in vv and len(vv["WNAM"][0])>=4:r["WNAM"]=struct.unpack_from("<I",vv["WNAM"][0],0)[0]
            records[fid]=r
        pos=end
walk(0,len(raw))

runtime_by_class={w["class"]:w for w in RUNTIME["weapons"]}
manifest_by_class={w["class"]:w for w in GMOD["weapons"] if not w.get("abstract_base")}

rows=[]
for cls,w in sorted(manifest_by_class.items()):
    edid="REMGW_"+cls
    weap=next((r for r in records.values() if r.get("sig")=="WEAP" and r.get("EDID")==edid),None)
    rr=runtime_by_class.get(cls,{})
    expected_world=model_rel((rr.get("world") or {}).get("converted_nif"))
    expected_view=model_rel((rr.get("view") or {}).get("converted_nif"))
    row={"class":cls,"expected_edid":edid,"expected_world_model":expected_world,"expected_view_model":expected_view,
         "source_world_model":w.get("world_model"),"source_view_model":w.get("view_model")}
    issues=[]
    if not weap:
        issues.append("missing_WEAP_record")
        row["issues"]=issues;rows.append(row);continue
    row.update({"formid":weap["formid"],"full":weap.get("FULL"),"flags":f"{weap['flags']:08X}",
                "world_model":weap.get("MODL"),"icon":weap.get("ICON"),"mico":weap.get("MICO"),
                "wnam":f"{weap['WNAM']:08X}" if weap.get("WNAM") is not None else None})
    if not weap.get("FULL"):issues.append("missing_display_name")
    if weap["flags"]!=0:issues.append("nonzero_record_flags_review")
    gicon="interface\\icons\\pipboyimages\\weapons\\rem_gmod_origin.dds"
    gsmall="interface\\icons\\pipboyimages_small\\weapons_small\\glow_rem_gmod_origin.dds"
    if norm(weap.get("ICON",""))!=gicon:issues.append("missing_or_wrong_large_origin_icon")
    if norm(weap.get("MICO",""))!=gsmall:issues.append("missing_or_wrong_small_origin_icon")
    world=norm(weap.get("MODL",""))
    if expected_world and world!=expected_world:issues.append("world_model_differs_from_prepared_source_candidate")
    if world:
        if not (DATA/"meshes"/Path(world)).exists():issues.append("world_model_file_missing")
    else:issues.append("world_model_path_missing")
    wnam=weap.get("WNAM")
    stat=records.get(wnam) if wnam is not None else None
    row["view_stat"]=stat
    view=norm(stat.get("MODL","")) if stat else ""
    row["view_model"]=view
    if not stat or stat.get("sig")!="STAT":issues.append("WNAM_missing_or_not_STAT")
    if expected_view and view!=expected_view:issues.append("view_model_differs_from_prepared_source_candidate")
    if view and not (DATA/"meshes"/Path(view)).exists():issues.append("view_model_file_missing")
    row["issues"]=issues
    rows.append(row)

# THUG2 skateboard
board=next((r for r in records.values() if r.get("sig")=="WEAP" and r.get("EDID")=="REMTHUG2Skateboard"),None)
board_issues=[]
if not board:board_issues.append("missing_WEAP_record")
else:
    if norm(board.get("ICON",""))!="interface\\icons\\pipboyimages\\weapons\\rem_thug2_origin.dds":board_issues.append("wrong_large_icon")
    if norm(board.get("MICO",""))!="interface\\icons\\pipboyimages_small\\weapons_small\\glow_rem_thug2_origin.dds":board_issues.append("wrong_small_icon")
    if not board.get("FULL"):board_issues.append("missing_display_name")
    if board.get("MODL") and not (DATA/"meshes"/Path(norm(board["MODL"]))).exists():board_issues.append("held_model_missing")
    stat=records.get(board.get("WNAM")) if board.get("WNAM") is not None else None
    if not stat:board_issues.append("board_WNAM_missing")
    elif stat.get("MODL") and not (DATA/"meshes"/Path(norm(stat["MODL"]))).exists():board_issues.append("board_world_model_missing")

issue_counts={}
for r in rows:
    for x in r["issues"]:issue_counts[x]=issue_counts.get(x,0)+1
result={
    "purpose":"Read-only audit of Pip-Boy naming/icons/model references/drop-friendly generic record flags for staged GMod/THUG2 weapon records.",
    "esp_sha256":sha(ESP),
    "gmod_weapon_count":len(rows),
    "gmod_clean_count":sum(not r["issues"] for r in rows),
    "issue_counts":issue_counts,
    "weapons":rows,
    "skateboard":{"record":board,"issues":board_issues},
    "notes":[
        "A zero generic record flags field is consistent with ordinary droppable inventory records, but gameplay drop/pickup still requires runtime playtest.",
        "World/view model comparisons use the actual prepared Source model conversion map; mismatches are evidence for later presentation cleanup, not automatic runtime fixes.",
        "This audit does not alter REM_GModTHUG2.esp or Astra candidates."
    ]
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("gmod_weapon_count","gmod_clean_count","issue_counts")},indent=2))
print("SKATEBOARD",board_issues)
print("ISSUES")
for r in rows:
    if r["issues"]:print(r["class"],r["issues"],"world",r.get("world_model"),"expected",r.get("expected_world_model"),"view",r.get("view_model"),"expectedv",r.get("expected_view_model"))