import struct,zlib,hashlib,wave,re
from pathlib import Path
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
esp=DATA/"REM_Goodsprings_CombineDeathclawEncounter.esp"
dll=DATA/"NVSE/Plugins/REMGoodspringsResponse.dll"
wav=DATA/"Sound/fx/rem/goodsprings/captain_claw_thanks.wav"
src=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\third_party\NVSE-6.4.9\fnv_goodsprings_response_plugin\main.cpp")

def subs(d):
    out=[];i=0;ext=None
    while i+6<=len(d):
        s=d[i:i+4];n=struct.unpack_from("<H",d,i+4)[0];i+=6
        if s==b"XXXX": ext=struct.unpack_from("<I",d,i)[0];i+=4;continue
        if ext is not None:n,ext=ext,None
        if i+n>len(d):raise RuntimeError(("bad sub",i,s,n,len(d)))
        out.append((s,d[i:i+n]));i+=n
    return out
def z(v):return v.split(b"\0",1)[0].decode("cp1252","ignore")
b=esp.read_bytes(); records=[]
def walk(st,en,stack):
    pos=st
    while pos<en:
        sig=b[pos:pos+4]
        if sig==b"GRUP":
            sz=struct.unpack_from("<I",b,pos+4)[0]
            if sz<24 or pos+sz>en:raise RuntimeError(("bad group",pos,sz,en))
            lab=b[pos+8:pos+12];typ=struct.unpack_from("<i",b,pos+12)[0]
            walk(pos+24,pos+sz,stack+[(lab,typ)]);pos+=sz;continue
        sz,fl,fid=struct.unpack_from("<III",b,pos+4);re=pos+24+sz
        if re>en:raise RuntimeError(("bad record",pos,sz,en))
        d=b[pos+24:re]
        if fl&0x40000:d=zlib.decompress(d[4:])
        records.append((sig,fid,fl,subs(d),stack))
        pos=re
tes4sz=struct.unpack_from("<I",b,4)[0]; tes4=subs(b[24:24+tes4sz]); walk(24+tes4sz,len(b),[])
byid={fid:(sig,fl,ss,stack) for sig,fid,fl,ss,stack in records}
# Guard
sig,fl,ss,stack=byid[0x02000800]
guard_full=next(z(v) for s,v in ss if s==b"FULL")
acbs=next(v for s,v in ss if s==b"ACBS")
gdata=next(v for s,v in ss if s==b"DATA")
aidt=next(v for s,v in ss if s==b"AIDT")
cnto=[struct.unpack("<Ii",v[:8]) for s,v in ss if s==b"CNTO"]
# Response base
rsig,rfl,rss,rstack=byid[0x02000801]
response_full=next(z(v) for s,v in rss if s==b"FULL")
raidt=next(v for s,v in rss if s==b"AIDT")
# Captain
csig,cfl,css,cstack=byid[0x02000802]
captain_full=next(z(v) for s,v in css if s==b"FULL")
cpkids=[struct.unpack("<I",v)[0] for s,v in css if s==b"PKID"]
caidt=next(v for s,v in css if s==b"AIDT")
# reward global
gsig,gfl,gss,gstack=byid[0x0200080F]
gedid=next(z(v) for s,v in gss if s==b"EDID"); gval=struct.unpack("<f",next(v for s,v in gss if s==b"FLTV"))[0]
# refs
resp_refs=[fid for fid in byid if 0x02000804<=fid<=0x0200080D]
cap_ref=byid[0x0200080E]
# PE machine
db=dll.read_bytes(); peoff=struct.unpack_from("<I",db,0x3C)[0]; machine=struct.unpack_from("<H",db,peoff+4)[0]
# wav
with wave.open(str(wav),"rb") as w:
    wavinfo=(w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes(),w.getnframes()/w.getframerate())
source=src.read_text(errors="ignore").lower()
print("ESP_SHA",hashlib.sha256(b).hexdigest().upper())
print("DLL_SHA",hashlib.sha256(db).hexdigest().upper())
print("WAV_SHA",hashlib.sha256(wav.read_bytes()).hexdigest().upper())
print("DLL_MACHINE",hex(machine),"x86_ok",machine==0x14c)
print("WAV",wavinfo)
print("GUARD",guard_full,"health",struct.unpack_from("<i",gdata,0)[0],"speed",struct.unpack_from("<H",acbs,14)[0],"aggression",aidt[0],"confidence",aidt[1],"inventory",[(f"{f:08X}",c) for f,c in cnto])
print("RESPONSE",response_full,"aggression",raidt[0],"confidence",raidt[1],"factions",sum(1 for s,v in rss if s==b"SNAM"),"packages",sum(1 for s,v in rss if s==b"PKID"),"refs",len(resp_refs))
print("CAPTAIN",captain_full,"aggression",caidt[0],"confidence",caidt[1],"packages",[f"{x:08X}" for x in cpkids],"disabled",bool(cap_ref[1]&0x800))
print("GLOBAL",gedid,gval)
print("NO_TELEPORT",("moveto" not in source and "move to" not in source),"has_enable",'"enable"' in source,"has_evp",'"evp"' in source)
print("ONE_PROMPT",source.count("messagebox")==1)
print("REWARD_EGG","000e6627" in source)
