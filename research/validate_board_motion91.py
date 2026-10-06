from pathlib import Path
import json,struct,math,bisect
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
OUT=ROOT/"build/board_animation91"
def acc(j,b,i):
 a=j["accessors"][i];v=j["bufferViews"][a["bufferView"]];assert a["componentType"]==5126
 n={"SCALAR":1,"VEC3":3,"VEC4":4}[a["type"]];start=v.get("byteOffset",0)+a.get("byteOffset",0)
 return [list(struct.unpack_from("<"+"f"*n,b,start+k*v.get("byteStride",4*n))) for k in range(a["count"])]
def sample(ts,vs,t,rot,interp):
 if t<=ts[0]:return vs[0]
 if t>=ts[-1]:return vs[-1]
 k=bisect.bisect_right(ts,t)-1;u=(t-ts[k])/(ts[k+1]-ts[k]);a=vs[k];b=vs[k+1]
 if interp=="STEP":return a
 assert interp=="LINEAR"
 if not rot:return [x*(1-u)+y*u for x,y in zip(a,b)]
 a=norm(a);b=norm(b);d=sum(x*y for x,y in zip(a,b))
 if d<0:b=[-x for x in b];d=-d
 if d>0.9995:
  return norm([x*(1-u)+y*u for x,y in zip(a,b)])
 angle=math.acos(max(-1,min(1,d)))
 return [(math.sin((1-u)*angle)*x+math.sin(u*angle)*y)/math.sin(angle) for x,y in zip(a,b)]
def matrix(t,q,s):
 x,y,z,w=norm(q)
 r=[[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]
 return [[r[i][k]*s[k] for k in range(3)]+[t[i]] for i in range(3)]+[[0,0,0,1]]
def norm(q):
 n=math.sqrt(sum(x*x for x in q));assert n>1e-12;return [x/n for x in q]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
rows=[]
for p in sorted(OUT.glob("*.glb")):
 raw=p.read_bytes();n=struct.unpack_from("<I",raw,12)[0];j=json.loads(raw[20:20+n]);b=raw[28+n:]
 nodes=j["nodes"];parents={c:i for i,x in enumerate(nodes) for c in x.get("children",[])}
 board=next(i for i,x in enumerate(nodes) if x.get("name","").lower()=="bone_board_root")
 tracks={};duration=0
 for c in j["animations"][0]["channels"]:
  sam=j["animations"][0]["samplers"][c["sampler"]];ts=[x[0] for x in acc(j,b,sam["input"])];vs=acc(j,b,sam["output"])
  tracks[(c["target"]["node"],c["target"]["path"])]=(ts,vs,sam.get("interpolation","LINEAR"));duration=max(duration,ts[-1])
 samples=[]
 for t in [duration*k/16 for k in range(17)]:
  def world(i,seen=None):
   seen=set() if seen is None else seen;assert i not in seen;seen.add(i)
   nd=nodes[i];parts={}
   for key,default in [("translation",[0,0,0]),("rotation",[0,0,0,1]),("scale",[1,1,1])]:
    v=nd.get(key,default)
    if (i,key) in tracks:
     ts,vs,interp=tracks[(i,key)];v=sample(ts,vs,t,key=="rotation",interp)
    parts[key]=v
   local=[[nd["matrix"][i+4*k] for k in range(4)] for i in range(4)] if "matrix" in nd else matrix(parts["translation"],parts["rotation"],parts["scale"])
   return mul(world(parents[i],seen),local) if i in parents else local
  m=world(board);assert all(math.isfinite(v) for row in m for v in row);samples.append(m)
 delta=max(math.sqrt(sum((x[i][k]-samples[0][i][k])**2 for i in range(4) for k in range(4))) for x in samples)
 if p.stem in ["ollie","land","manual","kickflip"]:assert delta>1e-5,p.stem+" did not move"
 rows.append({"clip":p.name,"duration":duration,"samples":17,"finite_world_transforms":True,"max_matrix_delta":delta,"status":"pass"})
report={"checks":rows,"interpretation":"Offline GLTF transform evaluation only; no engine/visual parity claim"}
(OUT/"motion_validation.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
