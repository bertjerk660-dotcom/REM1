from pathlib import Path
import json,struct,math,hashlib,collections
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
def values(j,blob,index):
    a=j["accessors"][index];v=j["bufferViews"][a["bufferView"]]
    assert a["componentType"]==5126 and "sparse" not in a
    size={"SCALAR":1,"VEC3":3,"VEC4":4}[a["type"]]
    stride=v.get("byteStride",size*4);start=v.get("byteOffset",0)+a.get("byteOffset",0)
    assert start+(a["count"]-1)*stride+size*4<=len(blob)
    return [struct.unpack_from("<"+"f"*size,blob,start+i*stride) for i in range(a["count"])]
rows=[]
for p in sorted((ROOT/"build/skater87/glb").rglob("*.glb")):
    row={"clip":str(p.relative_to(ROOT/"build/skater87/glb"))}
    try:
        data=p.read_bytes();n=struct.unpack_from("<I",data,12)[0];j=json.loads(data[20:20+n])
        offset=20+n;blen,btype=struct.unpack_from("<II",data,offset);assert btype==0x004e4942
        blob=data[offset+8:offset+8+blen]
        nodes=j["nodes"];board=[i for i,x in enumerate(nodes) if x.get("name","").lower()=="bone_board_root"];assert len(board)==1
        b=board[0];parents={c:i for i,x in enumerate(nodes) for c in x.get("children",[])}
        row["board_node"]=b;row["parent"]=nodes[parents[b]].get("name") if b in parents else None
        tracks=[]
        for anim in j.get("animations",[]):
            for c in anim["channels"]:
                if c["target"]["node"]!=b:continue
                sampler=anim["samplers"][c["sampler"]];times=[x[0] for x in values(j,blob,sampler["input"])];out=values(j,blob,sampler["output"])
                assert times and all(math.isfinite(t) for t in times) and all(x<y for x,y in zip(times,times[1:]))
                assert all(math.isfinite(x) for v in out for x in v)
                interpolation=sampler.get("interpolation","LINEAR")
                assert len(out)==len(times)*(3 if interpolation=="CUBICSPLINE" else 1)
                track={"path":c["target"]["path"],"keys":len(times),"start":times[0],"end":times[-1],"interpolation":interpolation}
                if track["path"]=="rotation":
                    norms=[sum(x*x for x in q)**0.5 for q in out]
                    track["quaternion_norm_range"]=[min(norms),max(norms)]
                    assert min(norms)>0.00001
                tracks.append(track)
        row["tracks"]=tracks;row["status"]="tracked" if tracks else "static_bind_pose"
        row["source_sha256"]=hashlib.sha256(data).hexdigest()
    except Exception as e:row["status"]="failed";row["error"]=str(e) or type(e).__name__
    rows.append(row)
report={"scope":"board root tracks only; no visual or source/runtime parity claim","counts":dict(collections.Counter(x["status"] for x in rows)),"parents":dict(collections.Counter(x.get("parent","unknown") for x in rows)),"clips":rows}
out=ROOT/"build/lifecycle89/board_track_audit.json";out.write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!="clips"}))
print(json.dumps([x for x in rows if x["status"]=="failed"][:5]))
