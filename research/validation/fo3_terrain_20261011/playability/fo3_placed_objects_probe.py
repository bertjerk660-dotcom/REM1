# Inventory placed objects in two original Fallout 3 outdoor Wasteland cells.
# Metadata only; no game assets or extracted meshes are saved to GitHub.
import mmap, pathlib, struct, zlib, json, collections, hashlib
path=pathlib.Path(r"D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm")
outfile=pathlib.Path(r"D:\REM_Dream_validation_20261011\fo3_placed_objects_two_cells.json")
target={0x000017A1:(6,7),0x000017A0:(7,7)}
objects=[];groups=collections.Counter();types=collections.Counter();issues=[]
with open(path,'rb') as f:
    data=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    limit=len(data);p=0;stack=[]
    while p+24<=limit:
        while stack and p>=stack[-1][0]:stack.pop()
        typ=data[p:p+4];sz=struct.unpack_from('<I',data,p+4)[0]
        if typ==b'GRUP':
            if sz<24 or p+sz>limit:issues.append(('bad_group',p,sz));break
            kind=struct.unpack_from('<i',data,p+12)[0]
            label=struct.unpack_from('<I',data,p+8)[0]
            stack.append((p+sz,kind,label))
            groups[kind]+=1;p+=24;continue
        if sz>limit-p-24:issues.append(('bad_record',p,sz));break
        cell=next((label for _,kind,label in reversed(stack) if kind==6),None)
        if cell in target and typ in (b'REFR',b'ACHR',b'ACRE',b'LAND',b'PMIS'):
            types[typ.decode()]+=1
            if typ!=b'LAND':
                flags=struct.unpack_from('<I',data,p+8)[0]
                fid=struct.unpack_from('<I',data,p+12)[0]
                raw=data[p+24:p+24+sz]
                if flags&0x40000:
                    try:raw=zlib.decompress(raw[4:])
                    except Exception as e:issues.append(('bad_zlib',p,str(e)));p+=24+sz;continue
                q=0;base=None;placement=None;scale=1.0;extra_size=0
                while q+6<=len(raw):
                    tag=raw[q:q+4];n=struct.unpack_from('<H',raw,q+4)[0];q+=6
                    if tag==b'XXXX' and n==4 and q+4<=len(raw):
                        extra_size=struct.unpack_from('<I',raw,q)[0];q+=4;continue
                    if extra_size:n=extra_size;extra_size=0
                    if q+n>len(raw):break
                    sub=raw[q:q+n];q+=n
                    if tag==b'NAME' and n>=4:base=struct.unpack_from('<I',sub)[0]
                    if tag==b'DATA' and n>=24:placement=struct.unpack_from('<6f',sub)
                    if tag==b'XSCL' and n>=4:scale=struct.unpack_from('<f',sub)[0]
                if base is not None and placement is not None:
                    x,y,z,rx,ry,rz=placement
                    objects.append(dict(kind=typ.decode(),cell=f'{cell:08X}',xy=target[cell],id=f'{fid:08X}',base=f'{base:08X}',position=[x,y,z],rotation=[rx,ry,rz],scale=scale,
                        in_cell=(target[cell][0]*4096<=x< (target[cell][0]+1)*4096 and target[cell][1]*4096<=y<(target[cell][1]+1)*4096)))
        p+=24+sz
    data.close()
counts=collections.Counter(o['kind'] for o in objects);basecounts=collections.Counter(o['base'] for o in objects)
obj_in=[o for o in objects if o['in_cell']]
result=dict(source_esm_sha256='D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06',cells={f'{k:08X}':v for k,v in target.items()},counts=dict(counts),raw_record_counts=dict(types),object_count=len(objects),placed_within_cell=len(obj_in),top_base_ids=basecounts.most_common(25),examples=obj_in[:70],all_placed=obj_in,scan_issues=issues[:10])
outfile.write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ('all_placed','examples')},indent=2)[:9000])
print('EXAMPLES',json.dumps(result['examples'][:12],indent=2)[:4500])
