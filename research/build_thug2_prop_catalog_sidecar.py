from pathlib import Path
import json,struct,hashlib,shutil,sys

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
BASE=ROOT/"build/prepared/prop_support_phase4"
LEDGER=BASE/"thug2_promotion_validation_ledger.json"
OUTDIR=ROOT/"build/prepared/thug2_prop_catalog_sidecar"
OUTDIR.mkdir(parents=True,exist_ok=True)

def srec(sig,payload):
    if len(payload)<=0xFFFF:return sig+struct.pack("<H",len(payload))+payload
    return b"XXXX"+struct.pack("<H",4)+struct.pack("<I",len(payload))+sig+b"\x00\x00"+payload
def zstr(s):return s.encode("cp1252","replace")+b"\x00"
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

ledger=json.loads(LEDGER.read_text(encoding="utf-8"))
ready=[r for r in ledger["records"] if r.get("overall")=="ready_for_sidecar"]
blocked=[r for r in ledger["records"] if r.get("overall")!="ready_for_sidecar"]

# Safe default: refuse to create an ESP until at least one candidate was explicitly
# promoted by completing every validation gate and assigning a real NIF path.
if not ready:
    report={
      "status":"blocked_no_validated_candidates",
      "ready":0,"blocked":len(blocked),
      "message":"No THUG2 prop has passed visual identity, split/conversion, material, collision, scale and runtime gates. Sidecar not created.",
      "required_ready_fields":["runtime_mesh_path","object_bounds","proposed_local_id","proposed_edid","display_name"],
    }
    (OUTDIR/"build_report.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    raise SystemExit(0)

records=[];form_map=[]
for r in ready:
    missing=[k for k in ("runtime_mesh_path","object_bounds","proposed_local_id","proposed_edid","display_name") if not r.get(k)]
    if missing:raise SystemExit(f"ready candidate {r.get('identifier')} missing {missing}")
    nif=DATA/"meshes"/Path(r["runtime_mesh_path"])
    if not nif.exists():raise SystemExit(f"NIF missing: {nif}")
    local=int(str(r["proposed_local_id"]),16)
    fid=0x01000000|local
    bounds=[int(x) for x in r["object_bounds"]]
    if len(bounds)!=6:raise SystemExit("object_bounds must have 6 int16 values")
    body=b"".join([
      srec(b"EDID",zstr(r["proposed_edid"])),
      srec(b"OBND",struct.pack("<6h",*bounds)),
      srec(b"FULL",zstr(r["display_name"])),
      srec(b"MODL",zstr(r["runtime_mesh_path"])),
      srec(b"DATA",b"\x00"),
    ])
    rec=b"MSTT"+struct.pack("<IIIIHH",len(body),0,fid,0,15,0)+body
    records.append(rec)
    form_map.append({"formid_file":f"{fid:08X}","local_id":f"{local:06X}","edid":r["proposed_edid"],"model":r["runtime_mesh_path"],"nif_sha256":sha(nif)})

tes4_body=b"".join([
  srec(b"HEDR",struct.pack("<fII",1.34,len(records)+1,(max(int(x["local_id"],16) for x in form_map)+1) if form_map else 0x800)),
  srec(b"CNAM",zstr("REM support pipeline")),
  srec(b"SNAM",zstr("Validated THUG2 standalone prop catalog sidecar.")),
  srec(b"MAST",zstr("FalloutNV.esm")),srec(b"DATA",b"\x00"*8),
])
tes4=b"TES4"+struct.pack("<IIIIHH",len(tes4_body),0,0,0,15,0)+tes4_body
grp_payload=b"".join(records)
grp=b"GRUP"+struct.pack("<I",24+len(grp_payload))+b"MSTT"+struct.pack("<IHHI",0,0,0,0)+grp_payload
out=OUTDIR/"REM_THUG2Props_Catalog.esp"
out.write_bytes(tes4+grp)
report={"status":"built_local_disabled_candidate","records":len(records),"plugin":str(out),"sha256":sha(out),"form_map":form_map,"install_performed":False}
(OUTDIR/"build_report.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))