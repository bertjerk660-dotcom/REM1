import struct, hashlib
from pathlib import Path

src=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\REM_Goodsprings_CombineDeathclawEncounter.esp.pre_v2_20261007.bak")
out=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data\REM_Goodsprings_CombineDeathclawEncounter.esp")
b=bytearray(src.read_bytes())

def srec(sig,payload):
    return sig+struct.pack("<H",len(payload))+payload

# TES4 HEDR: increment record count and reserve the next local object id.
tes4_size=struct.unpack_from("<I",b,4)[0]
tes4=bytearray(b[24:24+tes4_size])
i=0
while i+6<=len(tes4):
    sig=tes4[i:i+4]; n=struct.unpack_from("<H",tes4,i+4)[0]
    if sig==b"HEDR":
        ver,count,nextid=struct.unpack_from("<fII",tes4,i+6)
        struct.pack_into("<fII",tes4,i+6,ver,count+1,0x00000810)
        break
    i+=6+n
b[24:24+tes4_size]=tes4

# Locate top-level CREA group and Captain Claw CREA local 02000802.
pos=24+tes4_size
crea_gpos=crea_gend=cap_pos=cap_end=None
while pos+24<=len(b):
    if b[pos:pos+4]!=b"GRUP":
        raise RuntimeError(f"expected top group at {pos}")
    gsz=struct.unpack_from("<I",b,pos+4)[0]
    label=bytes(b[pos+8:pos+12])
    gend=pos+gsz
    if label==b"CREA":
        crea_gpos,crea_gend=pos,gend
        rp=pos+24
        while rp+24<=gend:
            rsz=struct.unpack_from("<I",b,rp+4)[0]
            rend=rp+24+rsz
            if b[rp:rp+4]==b"CREA" and struct.unpack_from("<I",b,rp+12)[0]==0x02000802:
                cap_pos,cap_end=rp,rend
                break
            rp=rend
        break
    pos=gend
if cap_pos is None:
    raise RuntimeError("Captain CREA not found")

# Add persistent vanilla RunToPlayerForever package after AIDT.
cap_hdr=bytearray(b[cap_pos:cap_pos+24])
payload=bytes(b[cap_pos+24:cap_end])
i=0; insert_at=None
while i+6<=len(payload):
    sig=payload[i:i+4]; n=struct.unpack_from("<H",payload,i+4)[0]
    nxt=i+6+n
    if sig==b"AIDT":
        insert_at=nxt
        break
    i=nxt
if insert_at is None:
    raise RuntimeError("Captain AIDT not found")
package_sub=srec(b"PKID",struct.pack("<I",0x000CAFC6))
new_payload=payload[:insert_at]+package_sub+payload[insert_at:]
struct.pack_into("<I",cap_hdr,4,len(new_payload))
new_cap=bytes(cap_hdr)+new_payload

# Rebuild CREA group around the larger Captain record.
crea_body=bytes(b[crea_gpos+24:cap_pos])+new_cap+bytes(b[cap_end:crea_gend])
crea_hdr=bytearray(b[crea_gpos:crea_gpos+24])
struct.pack_into("<I",crea_hdr,4,24+len(crea_body))
new_crea_group=bytes(crea_hdr)+crea_body

# Create persistent one-time reward global at local 0200080F.
edid=b"REMCaptainClawRewarded\0"
glob_payload=srec(b"EDID",edid)+srec(b"FNAM",b"s")+srec(b"FLTV",struct.pack("<f",0.0))
glob_rec=struct.pack("<4sIIIIHH",b"GLOB",len(glob_payload),0,0x0200080F,0,15,0)+glob_payload

# Top-level group header copied from CREA for compatible stamp/version fields.
glob_gh=bytearray(crea_hdr)
glob_gh[0:4]=b"GRUP"
struct.pack_into("<I",glob_gh,4,24+len(glob_rec))
glob_gh[8:12]=b"GLOB"
struct.pack_into("<i",glob_gh,12,0)
glob_group=bytes(glob_gh)+glob_rec

# Splice: modified CREA group, then new GLOB group, then untouched remainder.
final=bytes(b[:crea_gpos])+new_crea_group+glob_group+bytes(b[crea_gend:])
out.write_bytes(final)
print("bytes",len(final))
print("sha",hashlib.sha256(final).hexdigest().upper())
print("captain_pkid",hex(0x000CAFC6))
print("reward_global","0200080F")
