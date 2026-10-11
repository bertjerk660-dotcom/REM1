# Authored non-invasive Fallout 3 ESM LAND inventory/probe.
# Source game data stays local; do not commit derived heightmaps.
import struct, zlib, json, hashlib, pathlib, math, sys
p=pathlib.Path(r"D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm")
out=pathlib.Path(r"D:\REM_Dream_validation_20261011\fo3_terrain_inventory.json")
data=p.read_bytes(); n=len(data)
u32=lambda at:struct.unpack_from("<I",data,at)[0]
stack=[]; offset=0; records=0; groups=0; land=0; good=0; compressed=0; errors=[]
cells={}; samples=[]; candidate=[]
def parse_sub(raw):
  pos=0; extra=None
  while pos+6<=len(raw):
    tag=raw[pos:pos+4]; size=struct.unpack_from("<H",raw,pos+4)[0];pos+=6
    if tag==b"XXXX":
      if size!=4 or pos+4>len(raw):break
      extra=struct.unpack_from("<I",raw,pos)[0]; pos+=4;continue
    if extra is not None: size=extra;extra=None
    if pos+size>len(raw):break
    yield tag, raw[pos:pos+size]
    pos+=size
while offset+24<=n:
  while stack and offset>=stack[-1][0]:stack.pop()
  sig=data[offset:offset+4];sz=u32(offset+4)
  if sig==b"GRUP":
    if sz<24 or offset+sz>n:
      errors.append(f"invalid group at {offset} size {sz}");break
    label=data[offset+8:offset+12];kind=struct.unpack_from("<i",data,offset+12)[0]
    stack.append((offset+sz,kind,label));groups+=1
    offset+=24
    continue
  if sz>n-offset-24:
    errors.append(f"invalid record {sig!r} at {offset} size {sz}");break
  flags=u32(offset+8);fid=u32(offset+12);records+=1
  if sig in (b"LAND",b"CELL"):
    raw=data[offset+24:offset+24+sz]
    if flags&0x40000:
      try:
        expected=struct.unpack_from("<I",raw)[0]
        raw=zlib.decompress(raw[4:])
        if len(raw)!=expected:errors.append(f"unexpected decompressed size at {offset}")
        compressed+=1
      except Exception as ex:
        errors.append(f"decompression {sig.decode()} at {offset}: {ex}");offset+=sz+24;continue
    if sig==b"CELL":
      for k,v in parse_sub(raw):
        if k==b"XCLC" and len(v)>=8:cells[fid]=struct.unpack_from("<ii",v)
    else:
      land+=1;vg=None
      for k,v in parse_sub(raw):
        if k==b"VHGT":vg=v;break
      if vg is not None and len(vg)>=1096:
        vals=struct.unpack_from("<f",vg)[0];deltas=struct.unpack_from("<1089b",vg,4)
        # Raw absolute-delta integration. Vertical scaling requires original-game confirmation.
        rows=[];previous_row_start=vals
        for y in range(33):
          value=previous_row_start;row=[]
          for x in range(33):
            value+=deltas[y*33+x]
            row.append(value*8.0)
            if x==0:previous_row_start=value
          rows.append(row)
        flat=[h for row in rows for h in row]
        kinds=[(k,l.hex()) for _,k,l in stack]
        w=next((int.from_bytes(l,'little') for _,k,l in stack if k==1),None)
        cg=next((int.from_bytes(l,'little') for _,k,l in reversed(stack) if k in (6,8,9)),None)
        entry=dict(land_formid=f"{fid:08X}",cell_group=f"{cg:08X}" if cg is not None else None,world_group=f"{w:08X}" if w is not None else None,offset=offset,compressed=bool(flags&0x40000),range=[min(flat),max(flat)],average=sum(flat)/len(flat),grid="33x33")
        good+=1
        if len(samples)<12:samples.append(entry)
        if w==0x3C and len(candidate)<40:
          entry['height_digest']=hashlib.sha256(struct.pack('<1089f',*flat)).hexdigest()
          entry['heights']=rows
          candidate.append(entry)
  offset+=24+sz
  if records>12000000: errors.append("record limit");break
summary=dict(file=str(p),file_sha256=hashlib.sha256(data).hexdigest(),size=n,records=records,groups=groups,land_records=land,valid_vhgt=good,compressed_records=compressed,cells_with_xclc=len(cells),parse_issues=errors[:10],samples=samples,selected=[])
for ent in candidate[:3]:
  cellid=int(ent['cell_group'],16) if ent['cell_group'] else None
  ent['cell_xy']=cells.get(cellid)
  summary['selected'].append({k:v for k,v in ent.items() if k!='heights'})
out.write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k!='samples'},indent=2)[:10000])
