from __future__ import annotations
from pathlib import Path
import json, struct, zlib, hashlib, re

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
HANDOFF=ROOT/"build/prepared/prop_menu_content_handoff"
META=json.loads((HANDOFF/"runtime_mesh_metadata.json").read_text(encoding="utf-8"))
OUT=HANDOFF/"form_coverage_audit.json"

TARGET_SIGS={b"STAT",b"MSTT",b"ACTI",b"CONT",b"FURN",b"DOOR",b"TREE",b"LIGH",b"AMMO"}
COMPRESSED=0x00040000

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def norm(s:str)->str:
    s=s.replace("/","\\").lstrip("\\").lower()
    if s.startswith("meshes\\"):s=s[7:]
    return s

def parse_subrecords(data:bytes):
    out=[]
    i=0
    ext=None
    n=len(data)
    while i+6<=n:
        sig=data[i:i+4]; sz=struct.unpack_from("<H",data,i+4)[0]; i+=6
        if sig==b"XXXX":
            if sz!=4 or i+4>n:break
            ext=struct.unpack_from("<I",data,i)[0]; i+=4
            continue
        size=ext if ext is not None else sz
        ext=None
        if i+size>n:break
        out.append((sig,data[i:i+size]))
        i+=size
    return out

def dec_string(b:bytes)->str:
    return b.split(b"\x00",1)[0].decode("cp1252","ignore")

def walk_plugin(path:Path):
    raw=path.read_bytes()
    rows=[]
    counts={}
    errors=[]
    def walk(start,end,depth=0):
        pos=start
        while pos+8<=end:
            sig=raw[pos:pos+4]
            if sig==b"GRUP":
                if pos+24>end:
                    errors.append(f"truncated group header @{pos}"); return
                size=struct.unpack_from("<I",raw,pos+4)[0]
                if size<24 or pos+size>end:
                    errors.append(f"bad group size {size} @{pos}"); return
                walk(pos+24,pos+size,depth+1)
                pos+=size
                continue
            if pos+24>end:
                return
            size,flags,formid=struct.unpack_from("<III",raw,pos+4)
            rec_end=pos+24+size
            if rec_end>end or size>200_000_000:
                errors.append(f"bad record {sig!r} size {size} @{pos}"); return
            counts[sig.decode("latin1","ignore")]=counts.get(sig.decode("latin1","ignore"),0)+1
            if sig in TARGET_SIGS:
                payload=raw[pos+24:rec_end]
                if flags & COMPRESSED:
                    if len(payload)>=4:
                        expected=struct.unpack_from("<I",payload,0)[0]
                        try:
                            payload=zlib.decompress(payload[4:])
                            if len(payload)!=expected:
                                errors.append(f"{sig.decode()} {formid:08X} decompressed {len(payload)} != {expected}")
                        except Exception as e:
                            errors.append(f"{sig.decode()} {formid:08X} decompress error {e}")
                            payload=b""
                subs=parse_subrecords(payload)
                vals={}
                modls=[]
                for ss,bb in subs:
                    if ss in (b"EDID",b"FULL"):
                        vals.setdefault(ss.decode(),dec_string(bb))
                    if ss==b"MODL":
                        p=dec_string(bb)
                        if p:modls.append(p)
                for mp in modls:
                    key=norm(mp)
                    if key in META:
                        rows.append({
                            "model":key,
                            "plugin":path.name,
                            "signature":sig.decode(),
                            "formid":f"{formid:08X}",
                            "edid":vals.get("EDID",""),
                            "full":vals.get("FULL",""),
                            "raw_model":mp,
                        })
            pos=rec_end
    # TES4 is a record; start at 0 and let generic walker parse it.
    walk(0,len(raw))
    return rows,counts,errors

# Scan all official FNV masters and the project's active ESP; sidecar test ESP is
# intentionally excluded from canonical form coverage.
plugin_paths=[]
for name in [
    "FalloutNV.esm","DeadMoney.esm","HonestHearts.esm","OldWorldBlues.esm",
    "LonesomeRoad.esm","GunRunnersArsenal.esm","ClassicPack.esm",
    "MercenaryPack.esm","TribalPack.esm","CaravanPack.esm","REM_GModTHUG2.esp"
]:
    p=DATA/name
    if p.exists():plugin_paths.append(p)

matches=[]
plugin_info=[]
for p in plugin_paths:
    rows,counts,errors=walk_plugin(p)
    matches.extend(rows)
    plugin_info.append({"name":p.name,"sha256":sha(p),"bytes":p.stat().st_size,
                        "record_counts":counts,"errors":errors,"matches":len(rows)})
    print(p.name,"matches",len(rows),"errors",len(errors),flush=True)

by_model={}
for r in matches:by_model.setdefault(r["model"],[]).append(r)

records=[]
for model,meta in META.items():
    found=by_model.get(model,[])
    records.append({**meta,"normalized_model":model,"existing_forms":found,
                    "has_existing_form":bool(found)})

by_source={}
for r in records:
    s=r["source"]
    d=by_source.setdefault(s,{"total":0,"with_existing_form":0,"missing_form":0})
    d["total"]+=1
    if r["has_existing_form"]:d["with_existing_form"]+=1
    else:d["missing_form"]+=1

result={
    "purpose":"Binary plugin audit of base-form coverage for the 290 ready prop candidates. Avoids creating duplicate records.",
    "plugins_scanned":plugin_info,
    "candidate_count":len(records),
    "with_existing_form":sum(r["has_existing_form"] for r in records),
    "missing_form":sum(not r["has_existing_form"] for r in records),
    "by_source":by_source,
    "records":records,
    "status":"pass",
    "notes":[
        "Native FNV candidates with existing vanilla records should be referenced by FormID rather than duplicated.",
        "Converted GMod/Source NIFs without existing records are candidates for a disabled sidecar STAT/MSTT catalog.",
        "This audit is read-only and does not modify plugins."
    ]
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("candidate_count","with_existing_form","missing_form","by_source")},indent=2))