from pathlib import Path
import struct,zlib,hashlib,shutil,json

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
SRC=DATA/"REM_GModTHUG2.esp"
OUTDIR=ROOT/"build/prepared/weapon_presentation_fix_sidecar"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"REM_WeaponPresentation_Fixes.esp"
LIVE=DATA/OUT.name
RPG_FID=0x01000810

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

def subrecords(data):
    out=[];i=0;ext=None
    while i+6<=len(data):
        s=data[i:i+4];n=struct.unpack_from("<H",data,i+4)[0];i+=6
        if s==b"XXXX":
            ext=struct.unpack_from("<I",data,i)[0];i+=4;continue
        n=ext if ext is not None else n;ext=None
        if i+n>len(data):break
        out.append([s,data[i:i+n]]);i+=n
    return out

def srec(sig,payload):
    if len(payload)<=0xFFFF:return sig+struct.pack("<H",len(payload))+payload
    return b"XXXX"+struct.pack("<H",4)+struct.pack("<I",len(payload))+sig+b"\0\0"+payload
def zstr(s):return s.encode("cp1252")+b"\0"

raw=SRC.read_bytes()
found=None
def walk(a,b):
    global found
    pos=a
    while pos+8<=b and found is None:
        sig=raw[pos:pos+4]
        if sig==b"GRUP":
            sz=struct.unpack_from("<I",raw,pos+4)[0];walk(pos+24,pos+sz);pos+=sz;continue
        if pos+24>b:return
        sz,flags,fid=struct.unpack_from("<III",raw,pos+4);end=pos+24+sz
        if end>b:return
        if sig==b"WEAP" and fid==RPG_FID:
            data=raw[pos+24:end]
            if flags&0x40000:data=zlib.decompress(data[4:])
            found=(flags,subrecords(data))
            return
        pos=end
walk(0,len(raw))
if not found:raise RuntimeError("RPG record not found")
flags,subs=found

replacements={
    b"MODL":zstr(r"rem\gmod\weapons\w_rocket_launcher.nif"),
    b"ICON":zstr(r"Interface\Icons\PipboyImages\Weapons\rem_gmod_origin.dds"),
    b"MICO":zstr(r"Interface\Icons\PipboyImages_small\Weapons_small\glow_rem_gmod_origin.dds"),
}
seen=set()
new=[]
for s,v in subs:
    if s in replacements:
        new.append((s,replacements[s]));seen.add(s)
    else:new.append((s,v))
# Insert absent presentation fields before ETYP/WNAM/DATA region.
insert_at=next((i for i,(s,_v) in enumerate(new) if s in (b"ETYP",b"WNAM",b"DATA")),len(new))
for s in (b"MODL",b"ICON",b"MICO"):
    if s not in seen:
        new.insert(insert_at,(s,replacements[s]));insert_at+=1
payload=b"".join(srec(s,v) for s,v in new)
rec=b"WEAP"+struct.pack("<IIIIHH",len(payload),flags & ~0x40000,RPG_FID,0,15,0)+payload

tes4_body=b"".join([
    srec(b"HEDR",struct.pack("<fII",1.34,2,0x800)),
    srec(b"CNAM",zstr("REM support pipeline")),
    srec(b"SNAM",zstr("Disabled override: RPG model/icon presentation only.")),
    srec(b"MAST",zstr("FalloutNV.esm")),srec(b"DATA",b"\0"*8),
    srec(b"MAST",zstr("REM_GModTHUG2.esp")),srec(b"DATA",b"\0"*8),
])
tes4=b"TES4"+struct.pack("<IIIIHH",len(tes4_body),0,0,0,15,0)+tes4_body
grp=b"GRUP"+struct.pack("<I",24+len(rec))+b"WEAP"+struct.pack("<IHHI",0,0,0,0)+rec
OUT.write_bytes(tes4+grp)
shutil.copy2(OUT,LIVE)
plugins=Path(r"C:\Users\BRAD\AppData\Local\FalloutNV\plugins.txt")
enabled=plugins.exists() and any(x.strip().lstrip("*").lower()==LIVE.name.lower() for x in plugins.read_text(errors="ignore").splitlines())
report={
 "purpose":"Disabled sidecar override for the one clear inventory-presentation defect found by support audit: GMod RPG missing world model and GMod origin icons.",
 "plugin":str(LIVE),"sha256":sha(LIVE),"bytes":LIVE.stat().st_size,"enabled":enabled,
 "override_formid_file":"01000810","edid":"REMGW_weapon_rpg",
 "changes":{"MODL":r"rem\gmod\weapons\w_rocket_launcher.nif","ICON":r"Interface\Icons\PipboyImages\Weapons\rem_gmod_origin.dds","MICO":r"Interface\Icons\PipboyImages_small\Weapons_small\glow_rem_gmod_origin.dds"},
 "source_esp_sha256":sha(SRC),"runtime_integration_performed":False
}
(OUTDIR/"build_report.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))