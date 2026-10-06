from pathlib import Path
import json,struct,zlib,hashlib,collections

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
STATIC=json.loads((ROOT/"build/prepared/fnv_prop_catalog_curated/static_audit.json").read_text())
OUT=ROOT/"build/prepared/fnv_prop_catalog_curated/form_coverage_static_clean.json"

targets={r["path"].replace("/","\\").lower().removeprefix("meshes\\"):r
         for r in STATIC["records"] if r["static_candidate_ok"]}
SIGS={b"STAT",b"MSTT",b"ACTI",b"CONT",b"FURN",b"DOOR",b"TREE",b"LIGH",b"AMMO"}
COMP=0x40000

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def norm(s):
    s=s.replace("/","\\").lstrip("\\").lower()
    return s[7:] if s.startswith("meshes\\") else s

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

def scan(path):
    raw=path.read_bytes();rows=[];errors=[]
    def walk(a,b):
        pos=a
        while pos+8<=b:
            sig=raw[pos:pos+4]
            if sig==b"GRUP":
                if pos+24>b:return
                size=struct.unpack_from("<I",raw,pos+4)[0]
                if size<24 or pos+size>b:return
                walk(pos+24,pos+size);pos+=size;continue
            if pos+24>b:return
            size,flags,fid=struct.unpack_from("<III",raw,pos+4);end=pos+24+size
            if end>b or size>200_000_000:return
            if sig in SIGS:
                payload=raw[pos+24:end]
                if flags&COMP:
                    try:payload=zlib.decompress(payload[4:])
                    except Exception as e:errors.append(f"{sig!r} {fid:08X}: {e}");payload=b""
                vals={}
                for s,v in subs(payload):
                    if s in (b"EDID",b"FULL",b"MODL"):vals.setdefault(s.decode(),[]).append(v)
                for mv in vals.get("MODL",[]):
                    mp=norm(ds(mv))
                    if mp in targets:
                        rows.append({"model":mp,"plugin":path.name,"signature":sig.decode(),
                                     "formid":f"{fid:08X}","edid":ds(vals.get("EDID",[b""])[0]),
                                     "full":ds(vals.get("FULL",[b""])[0])})
            pos=end
    walk(0,len(raw));return rows,errors

plugins=[p for p in [DATA/"FalloutNV.esm",DATA/"REM_GModTHUG2.esp"] if p.exists()]
matches=[];plugin_info=[]
for p in plugins:
    rows,errors=scan(p);matches+=rows
    plugin_info.append({"name":p.name,"sha256":sha(p),"matches":len(rows),"errors":errors})
by=collections.defaultdict(list)
for r in matches:by[r["model"]].append(r)
records=[]
for mp,r in targets.items():
    records.append({
        "path":r["path"],"spawn_category":r["spawn_category"],
        "dimensions":r.get("dimensions"),"triangles":r.get("triangles"),
        "existing_forms":by.get(mp,[]),"has_existing_form":bool(by.get(mp))
    })
cats={}
for r in records:
    c=cats.setdefault(r["spawn_category"],{"total":0,"with_form":0,"missing_form":0})
    c["total"]+=1
    c["with_form"]+=int(r["has_existing_form"])
    c["missing_form"]+=int(not r["has_existing_form"])
result={
    "purpose":"Existing base-form coverage for all 278 static-clean FNV prop candidates, used to avoid creating unnecessary custom forms.",
    "static_clean_count":len(records),
    "with_existing_form":sum(r["has_existing_form"] for r in records),
    "missing_form":sum(not r["has_existing_form"] for r in records),
    "category_summary":cats,
    "plugins_scanned":plugin_info,
    "records":records
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("static_clean_count","with_existing_form","missing_form","category_summary")},indent=2))