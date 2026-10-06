from pathlib import Path
import struct,zlib,json,hashlib

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
ESP=DATA/"REM_WeaponPresentation_Fixes.esp"
BUILD=json.loads((ROOT/"build/prepared/weapon_presentation_fix_sidecar/build_report.json").read_text())
OUT=ROOT/"build/prepared/weapon_presentation_fix_sidecar/validation.json"

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

raw=ESP.read_bytes(); recs=[]; errors=[]
def walk(a,b):
    pos=a
    while pos+8<=b:
        sig=raw[pos:pos+4]
        if sig==b"GRUP":
            if pos+24>b:return
            n=struct.unpack_from("<I",raw,pos+4)[0]
            if n<24 or pos+n>b:errors.append("bad GRUP");return
            walk(pos+24,pos+n);pos+=n;continue
        if pos+24>b:return
        n,flags,fid=struct.unpack_from("<III",raw,pos+4);end=pos+24+n
        if end>b:errors.append("record overflow");return
        data=raw[pos+24:end]
        if flags&0x40000:
            try:data=zlib.decompress(data[4:])
            except Exception as e:errors.append(repr(e));data=b""
        vals={}
        for s,v in subs(data):vals.setdefault(s.decode("latin1"),[]).append(v)
        recs.append({
            "sig":sig.decode("latin1"),"formid":f"{fid:08X}",
            "edid":ds(vals.get("EDID",[b""])[0]),"full":ds(vals.get("FULL",[b""])[0]),
            "model":ds(vals.get("MODL",[b""])[0]),"icon":ds(vals.get("ICON",[b""])[0]),
            "mico":ds(vals.get("MICO",[b""])[0]),
            "masters":[ds(v) for v in vals.get("MAST",[])]
        })
        pos=end
walk(0,len(raw))
tes4=[x for x in recs if x["sig"]=="TES4"]; weap=[x for x in recs if x["sig"]=="WEAP"]
checks=[]
def ck(n,v,d=None):checks.append({"name":n,"pass":bool(v),"details":d})
ck("single_TES4",len(tes4)==1,len(tes4))
ck("masters",tes4 and tes4[0]["masters"]==["FalloutNV.esm","REM_GModTHUG2.esp"],tes4[0]["masters"] if tes4 else [])
ck("single_WEAP_override",len(weap)==1,len(weap))
r=weap[0] if weap else {}
ck("override_formid",r.get("formid")=="01000810",r.get("formid"))
ck("rpg_edid",r.get("edid")=="REMGW_weapon_rpg",r.get("edid"))
ck("rpg_model",r.get("model").lower()==r"rem\gmod\weapons\w_rocket_launcher.nif",r.get("model"))
ck("rpg_large_icon",r.get("icon").lower()==r"interface\icons\pipboyimages\weapons\rem_gmod_origin.dds",r.get("icon"))
ck("rpg_small_icon",r.get("mico").lower()==r"interface\icons\pipboyimages_small\weapons_small\glow_rem_gmod_origin.dds",r.get("mico"))
ck("model_resolves",(DATA/"meshes"/Path(r.get("model",""))).exists(),r.get("model"))
ck("icons_resolve",
   (DATA/"textures"/Path(r.get("icon","").replace("Interface\\","interface\\",1))).exists() and
   (DATA/"textures"/Path(r.get("mico","").replace("Interface\\","interface\\",1))).exists(),
   {"icon":r.get("icon"),"mico":r.get("mico")})
plugins=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")
enabled=plugins.exists() and any(x.strip().lstrip("*").lower()==ESP.name.lower() for x in plugins.read_text(errors="ignore").splitlines())
ck("sidecar_disabled",not enabled,enabled)
ck("hash_matches_build",sha(ESP)==BUILD["sha256"],sha(ESP))
ck("parse_errors_none",not errors,errors)
result={"purpose":"Static validation of disabled RPG presentation-fix sidecar.","status":"pass" if all(x["pass"] for x in checks) else "fail","checks":checks,"plugin_sha256":sha(ESP),"enabled":enabled}
OUT.write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))