from __future__ import annotations
import time
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pathlib import Path
import json, struct, hashlib, math, re, shutil
from pyffi.formats.nif import NifFormat

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
HANDOFF=ROOT/"build/prepared/prop_menu_content_handoff"
COVERAGE=json.loads((HANDOFF/"form_coverage_audit.json").read_text(encoding="utf-8"))
GMOD=json.loads((ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json").read_text(encoding="utf-8"))
OUTDIR=ROOT/"build/prepared/gmod_prop_catalog_sidecar"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"REM_GModProps_Catalog.esp"
LIVE=DATA/"REM_GModProps_Catalog.esp"
MAP=OUTDIR/"form_map.json"
REPORT=OUTDIR/"build_report.json"

# Only custom GMod/Source candidates missing a form. Native FNV missing forms are
# deliberately not created here; they remain review-only to avoid making arbitrary
# records for kit pieces.
missing_gmod={
    r["normalized_model"]:r for r in COVERAGE["records"]
    if r["source"].startswith("Garry") and not r["has_existing_form"]
}

gmod_by_runtime={}
for r in GMOD["records"]:
    p=r["output_nif_relative"].replace("/","\\").lower()
    if p.startswith("meshes\\"):p=p[7:]
    gmod_by_runtime[p]=r

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def srec(sig:bytes,payload:bytes)->bytes:
    assert len(sig)==4
    if len(payload)<=0xFFFF:
        return sig+struct.pack("<H",len(payload))+payload
    return b"XXXX"+struct.pack("<H",4)+struct.pack("<I",len(payload))+sig+b"\x00\x00"+payload

def zstr(s:str)->bytes:
    return s.encode("cp1252","replace")+b"\x00"

def get_bounds(nif:Path):
    d=NifFormat.Data()
    with nif.open("rb") as f:d.read(f)
    root=d.roots[0] if d.roots else None
    pts=[]
    for b in d.get_global_iterator():
        dat=getattr(b,"data",None)
        if dat is None or not hasattr(dat,"vertices") or not getattr(dat,"has_vertices",False):
            continue
        try:m=b.get_transform(relative_to=root) if root is not None else None
        except Exception:m=None
        for v in dat.vertices:
            x,y,z=float(v.x),float(v.y),float(v.z)
            if m is not None:
                x,y,z=(x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
                       x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
                       x*m.m_13+y*m.m_23+z*m.m_33+m.m_43)
            pts.append((x,y,z))
    if not pts:return (-16,-16,-16,16,16,16)
    mn=[math.floor(min(p[k] for p in pts)) for k in range(3)]
    mx=[math.ceil(max(p[k] for p in pts)) for k in range(3)]
    # OBND uses signed int16.
    vals=[max(-32768,min(32767,int(x))) for x in (*mn,*mx)]
    return tuple(vals)

def nice_name(source_model:str)->str:
    stem=Path(source_model.replace("\\","/")).stem
    # Preserve recognizable source names but make them readable.
    stem=re.sub(r"^(prop_|props_)", "", stem, flags=re.I)
    stem=stem.replace("_"," ").replace("-"," ")
    stem=re.sub(r"\s+"," ",stem).strip()
    return "GMod "+stem if stem else "GMod Prop"

def safe_edid(source_model:str,index:int)->str:
    stem=Path(source_model.replace("\\","/")).stem
    stem=re.sub(r"[^A-Za-z0-9]+","_",stem).strip("_")
    stem=stem[:42] or f"Prop{index:03d}"
    return f"REMGP_{index:03d}_{stem}"

records=[]
form_map=[]
first_form=0x01000800
for idx,key in enumerate(sorted(missing_gmod),1):
    src=gmod_by_runtime.get(key)
    if not src:
        raise RuntimeError(f"curated source metadata missing for {key}")
    nif_rel=src["output_nif_relative"].replace("/","\\")
    if nif_rel.lower().startswith("meshes\\"):nif_rel=nif_rel[7:]
    nif=DATA/"meshes"/Path(nif_rel)
    if not nif.exists():raise FileNotFoundError(nif)
    bounds=get_bounds(nif)
    edid=safe_edid(src["source_model"],idx)
    full=nice_name(src["source_model"])
    formid=first_form+(idx-1)
    body=b"".join([
        srec(b"EDID",zstr(edid)),
        srec(b"OBND",struct.pack("<6h",*bounds)),
        srec(b"FULL",zstr(full)),
        srec(b"MODL",zstr(nif_rel)),
        srec(b"DATA",b"\x00"),
    ])
    hdr=b"MSTT"+struct.pack("<IIIIHH",len(body),0,formid,0,15,0)
    records.append(hdr+body)
    form_map.append({
        "formid_file":f"{formid:08X}",
        "local_id":f"{formid&0x00FFFFFF:06X}",
        "edid":edid,"full":full,
        "source_model":src["source_model"],
        "nif":nif_rel,
        "nif_sha256":sha(nif),
        "object_bounds":bounds,
        "category":src["category"],
        "mass":src.get("mass"),
    })

# TES4 header: version 1.34, record count includes TES4 + 120 MSTT records.
tes4_body=b"".join([
    srec(b"HEDR",struct.pack("<fII",1.34,len(records)+1,(first_form+len(records))&0x00FFFFFF)),
    srec(b"CNAM",zstr("REM support pipeline")),
    srec(b"SNAM",zstr("Disabled sidecar catalog for curated GMod props; no runtime/menu code.")),
    srec(b"MAST",zstr("FalloutNV.esm")),
    srec(b"DATA",b"\x00"*8),
])
tes4=b"TES4"+struct.pack("<IIIIHH",len(tes4_body),0,0,0,15,0)+tes4_body
grp_payload=b"".join(records)
# GRUP size includes the 24-byte group header.
grp=b"GRUP"+struct.pack("<I",24+len(grp_payload))+b"MSTT"+struct.pack("<IHHI",0,0,0,0)+grp_payload
blob=tes4+grp
OUT.write_bytes(blob)
# Install the disabled sidecar file. It is not added to plugins.txt.
shutil.copy2(OUT,LIVE)

plugins=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")
enabled=False
if plugins.exists():
    enabled=any(line.strip().lstrip("*").lower()==LIVE.name.lower() for line in plugins.read_text(errors="ignore").splitlines())

MAP.write_text(json.dumps({"records":form_map},indent=2),encoding="utf-8")
report={
    "purpose":"Disabled sidecar MSTT catalog for the 120 curated GMod/Source props that have no existing FNV/REM base form.",
    "record_count":len(records),
    "plugin":str(LIVE),
    "plugin_sha256":sha(LIVE),
    "plugin_bytes":LIVE.stat().st_size,
    "enabled":enabled,
    "native_fnv_missing_forms_excluded":sum(1 for r in COVERAGE["records"] if r["source"]=="Fallout New Vegas" and not r["has_existing_form"]),
    "first_formid_file":form_map[0]["formid_file"] if form_map else None,
    "last_formid_file":form_map[-1]["formid_file"] if form_map else None,
    "records":form_map,
    "runtime_integration_performed":False,
}
REPORT.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({k:report[k] for k in ("record_count","plugin","plugin_sha256","plugin_bytes","enabled","native_fnv_missing_forms_excluded","first_formid_file","last_formid_file")},indent=2))