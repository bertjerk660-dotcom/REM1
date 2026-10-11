# Original Fallout 3 ESM base record classes and model paths for placed two-cell objects.
import mmap,struct,zlib,collections,json,pathlib
dir=pathlib.Path(r"D:\REM_Dream_validation_20261011")
j=json.loads((dir/'fo3_placed_objects_two_cells.json').read_text())
wanted={int(o['base'],16) for o in j['all_placed']}
data_file=r"D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm"
seen={}
with open(data_file,'rb') as f:
    b=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    p=0;end=len(b)
    while p+24<=end and len(seen)<len(wanted):
        tag=b[p:p+4];size=struct.unpack_from('<I',b,p+4)[0]
        if tag==b'GRUP':
            assert size>=24 and p+size<=end
            p+=24;continue
        if size>end-p-24:break
        fid=struct.unpack_from('<I',b,p+12)[0]
        if fid in wanted:
            flags=struct.unpack_from('<I',b,p+8)[0];chunk=b[p+24:p+24+size]
            if flags&0x40000:chunk=zlib.decompress(chunk[4:])
            x=0;edid=None;model=None;full=None;bounds=None;ext=0
            while x+6<=len(chunk):
                sub=chunk[x:x+4];n=struct.unpack_from('<H',chunk,x+4)[0];x+=6
                if sub==b'XXXX' and n==4 and x+4<=len(chunk):ext=struct.unpack_from('<I',chunk,x)[0];x+=4;continue
                if ext:n=ext;ext=0
                if x+n>len(chunk):break
                val=chunk[x:x+n];x+=n
                if sub==b'EDID':edid=val.split(b'\0')[0].decode('utf8',errors='replace')
                if sub==b'FULL':full=val.split(b'\0')[0].decode('utf8',errors='replace')
                if sub==b'MODL':model=val.split(b'\0')[0].decode('utf8',errors='replace')
                if sub==b'OBND' and n>=12:bounds=struct.unpack_from('<6h',val)
            seen[fid]={'type':tag.decode('latin1'),'edid':edid,'full':full,'model':model,'obnd':bounds}
        p+=24+size
    b.close()
cnt=collections.Counter(seen.get(int(o['base'],16),{}).get('type','MISSING') for o in j['all_placed'])
result=dict(base_count=len(wanted),resolved=len(seen),counts=dict(cnt),base_records={f'{k:08X}':v for k,v in seen.items()})
(dir/'fo3_two_cell_base_models.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2)[:13500])
