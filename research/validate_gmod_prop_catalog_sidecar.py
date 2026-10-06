from pathlib import Path
import json,struct,zlib,hashlib

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
ESP=DATA/"REM_GModProps_Catalog.esp"
REPORT=ROOT/"build/prepared/gmod_prop_catalog_sidecar/validation.json"
BUILD=json.loads((ROOT/"build/prepared/gmod_prop_catalog_sidecar/build_report.json").read_text())

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

raw=ESP.read_bytes()
records=[];errors=[]
def walk(a,b):
    pos=a
    while pos+8<=b:
        sig=raw[pos:pos+4]
        if sig==b"GRUP":
            if pos+24>b:errors.append("truncated GRUP");return
            size=struct.unpack_from("<I",raw,pos+4)[0]
            if size<24 or pos+size>b:errors.append(f"bad GRUP size @{pos}");return
            walk(pos+24,pos+size);pos+=size;continue
        if pos+24>b:return
        size,flags,fid=struct.unpack_from("<III",raw,pos+4)
        end=pos+24+size
        if end>b:errors.append(f"record overflow {sig} @{pos}");return
        payload=raw[pos+24:end]
        if flags&0x40000:
            try:payload=zlib.decompress(payload[4:])
            except Exception as e:errors.append(f"decompress {e}");payload=b""
        vals={}
        for s,v in subs(payload):
            vals.setdefault(s.decode("latin1"),[]).append(v)
        records.append({
            "sig":sig.decode("latin1"),"formid":f"{fid:08X}",
            "edid":ds(vals.get("EDID",[b""])[0]),
            "full":ds(vals.get("FULL",[b""])[0]),
            "model":ds(vals.get("MODL",[b""])[0]),
            "obnd":struct.unpack("<6h",vals["OBND"][0]) if vals.get("OBND") and len(vals["OBND"][0])==12 else None,
            "data":vals.get("DATA",[b""])[0].hex() if vals.get("DATA") else None,
        })
        pos=end
walk(0,len(raw))

mstt=[r for r in records if r["sig"]=="MSTT"]
tes4=[r for r in records if r["sig"]=="TES4"]
checks=[]
def ck(n,v,d=None):checks.append({"name":n,"pass":bool(v),"details":d})
ck("single_TES4",len(tes4)==1,len(tes4))
ck("MSTT_count_120",len(mstt)==120,len(mstt))
ck("unique_formids",len({r["formid"] for r in mstt})==len(mstt))
ck("unique_edids",len({r["edid"].lower() for r in mstt})==len(mstt))
ck("all_models_resolve",all((DATA/"meshes"/Path(r["model"])).exists() for r in mstt),
   [r["model"] for r in mstt if not (DATA/"meshes"/Path(r["model"])).exists()])
ck("all_obnd_valid",all(r["obnd"] is not None and all(-32768<=x<=32767 for x in r["obnd"]) for r in mstt))
ck("all_DATA_zero",all(r["data"]=="00" for r in mstt))
plugins=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")
enabled=plugins.exists() and any(line.strip().lstrip("*").lower()==ESP.name.lower() for line in plugins.read_text(errors="ignore").splitlines())
ck("sidecar_disabled",not enabled,enabled)
ck("hash_matches_build",sha(ESP)==BUILD["plugin_sha256"],sha(ESP))
ck("no_parse_errors",not errors,errors)

result={
 "purpose":"Static structural/reference validation of disabled GMod prop catalog sidecar.",
 "status":"pass" if all(x["pass"] for x in checks) else "fail",
 "plugin_sha256":sha(ESP),"plugin_bytes":ESP.stat().st_size,"enabled":enabled,
 "checks":checks,"record_count":len(mstt),"records":mstt,
 "runtime_playtest":"not_run"
}
REPORT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({"status":result["status"],"checks":checks},indent=2))