# Local-only two-cell FO3 landscape geometry proof. Original game data is never checked in.
import pathlib, struct, zlib, hashlib, json, math
base=pathlib.Path(r'D:\REM_Dream_validation_20261011')
p=pathlib.Path(r'D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout3.esm')
data=p.read_bytes();n=len(data);o=0;stack=[];xy={};terrain={}
target={(6,7),(7,7)}
def subrecords(raw):
    off=0; extra=0
    while off+6<=len(raw):
        tag=raw[off:off+4];ln=struct.unpack_from('<H',raw,off+4)[0];off+=6
        if tag==b'XXXX':
            if off+4>len(raw):break
            extra=struct.unpack_from('<I',raw,off)[0];off+=4;continue
        if extra:ln=extra;extra=0
        if off+ln>len(raw):break
        yield tag,raw[off:off+ln]
        off+=ln
def load(raw,flags):
    if flags & 0x40000:
        sz=struct.unpack_from('<I',raw)[0]
        raw=zlib.decompress(raw[4:])
        assert len(raw)==sz
    return raw
def decode(v):
    assert len(v)>=1096
    h=struct.unpack_from('<f',v)[0]
    diff=struct.unpack_from('<1089b',v,4); rows=[]
    for y in range(33):
        row=[];xv=h
        for x in range(33):
            xv+=diff[y*33+x];row.append(xv*8.0)
            if x==0:h=xv
        rows.append(row)
    return rows
while o+24<=n and len(terrain)<2:
    while stack and o>=stack[-1][0]:stack.pop()
    kind=data[o:o+4];sz=struct.unpack_from('<I',data,o+4)[0]
    if kind==b'GRUP':
        assert sz>=24 and o+sz<=n
        stack.append((o+sz,struct.unpack_from('<i',data,o+12)[0],int.from_bytes(data[o+8:o+12],'little')))
        o+=24;continue
    assert o+24+sz<=n
    if kind in (b'LAND',b'CELL'):
        f=struct.unpack_from('<I',data,o+8)[0];fid=struct.unpack_from('<I',data,o+12)[0]
        world=next((v for _,gt,v in stack if gt==1),None)
        if world==0x3C:
            raw=load(data[o+24:o+24+sz],f)
            if kind==b'CELL':
                for tag,v in subrecords(raw):
                    if tag==b'XCLC' and len(v)>=8:xy[fid]=struct.unpack_from('<ii',v)
            else:
                cell=next((v for _,gt,v in reversed(stack) if gt in (6,8,9)),None)
                if cell in xy and xy[cell] in target:
                    v=next((v for t,v in subrecords(raw) if t==b'VHGT'),None)
                    if v is not None:
                        terrain[xy[cell]]={'h':decode(v),'land_id':f'{fid:08X}','cell':f'{cell:08X}'}
    o+=24+sz
assert len(terrain)==2, f'Found {list(terrain)}'
h0=terrain[(6,7)]['h'];h1=terrain[(7,7)]['h']
seam=[h0[y][32]-h1[y][0] for y in range(33)]
# Store the two cells as a single non-redistributed GLB.
# Unit scale here is a *provisional import assumption*, not engine-validated.
scale=64.0
verts=[];normals=[];uv=[];idx=[];cells=[(6,7),(7,7)]
for (cx,cy) in cells:
  heights=terrain[(cx,cy)]['h']
  start=len(verts)
  for yy in range(33):
    for xx in range(33):
      verts.append(((cx*4096+128*xx)/scale,heights[yy][xx]/scale,-(cy*4096+128*yy)/scale))
      uv.append((xx/32.0,yy/32.0))
  for yy in range(32):
    for xx in range(32):
      a=start+yy*33+xx;b=a+1;c=a+33;dd=c+1
      idx.extend((a,b,c,b,dd,c))
normals=[[0.0,0.0,0.0] for _ in verts]
for i in range(0,len(idx),3):
  a,b,c=(verts[idx[i]],verts[idx[i+1]],verts[idx[i+2]])
  ab=[b[j]-a[j] for j in range(3)]
  ac=[c[j]-a[j] for j in range(3)]
  face=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
  for nidx in idx[i:i+3]:
    for j in range(3):normals[nidx][j]+=face[j]
normals=[tuple(x/max(1e-8,math.sqrt(sum(v*v for v in n))) for x in n) for n in normals]
buf=bytearray();views=[]
def add(vals,fmt):
    start=len(buf)
    buf.extend(struct.pack('<'+fmt*len(vals),*vals))
    while len(buf)%4:buf.append(0)
    views.append({'buffer':0,'byteOffset':start,'byteLength':len(buf)-start})
    return len(views)-1
pv=add([x for point in verts for x in point],'f')
nv=add([x for point in normals for x in point],'f')
uvv=add([x for point in uv for x in point],'f')
iv=add(idx,'I')
lo=[min(v[j] for v in verts) for j in range(3)];hi=[max(v[j] for v in verts) for j in range(3)]
gltf={'asset':{'version':'2.0','generator':'REM Dream isolated LAND audit'},'buffers':[{'byteLength':len(buf)}],'bufferViews':[dict(v,target=(34963 if i==iv else 34962)) for i,v in enumerate(views)],
'accessors':[{'bufferView':pv,'componentType':5126,'count':len(verts),'type':'VEC3','min':lo,'max':hi},{'bufferView':nv,'componentType':5126,'count':len(normals),'type':'VEC3'},{'bufferView':uvv,'componentType':5126,'count':len(uv),'type':'VEC2'},{'bufferView':iv,'componentType':5125,'count':len(idx),'type':'SCALAR'}],
'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3,'mode':4}]}],
'nodes':[{'mesh':0,'name':'FO3_Esm_LAND_6_7_and_7_7'}],'scenes':[{'nodes':[0]}],'scene':0}
jsonb=json.dumps(gltf,separators=(',',':')).encode('utf-8')
jsonb+=b' ' * ((-len(jsonb))%4)
glb=struct.pack('<III',0x46546C67,2,12+8+len(jsonb)+8+len(buf))+struct.pack('<I4s',len(jsonb),b'JSON')+jsonb+struct.pack('<I4s',len(buf),b'BIN\x00')+buf
file=base/'fo3_original_two_cells_6_7_7_7.glb'
file.write_bytes(glb)
report={'source_esmbinary_sha256':'D9FB0A33AF495DDB43992B96EA74F2741B123FEFDB1FCDCEA28096F7649B0D06','worldspace':'0000003C','cells':[{**{k:v for k,v in terrain[t].items() if k!='h'},'xy':t} for t in cells],
'seam_delta_min':min(seam),'seam_delta_max':max(seam),'seam_delta_abs_max':max(map(abs,seam)),
'height_conversion':'offset float+signed differences, factor 8 original engine units; scale /64 units-per-metre PROVISIONAL',
'triangles':len(idx)//3,'vertices':len(verts),'glb_path':str(file),'glb_sha256':hashlib.sha256(glb).hexdigest(),'glb_bytes':len(glb)}
(base/'fo3_two_cell_mesh_probe.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
