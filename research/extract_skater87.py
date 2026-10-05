from pathlib import Path
import json,hashlib,subprocess,struct,math,concurrent.futures
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SRC=Path(r"C:\IDA68WORK\thug2_datap_unpack\DATAP\anims")
SKE=Path(r"C:\IDA68WORK\THUG2\skeletons_pre_unpack\skeletons\skeletons\THPS6_Human.ske.ps2")
TOOL=ROOT/"third_party/tools/neversoft-multitool-main/src/NeversoftMultitool/bin/Release/net10.0/NeversoftMultitool.exe"
OUT=ROOT/"build/skater87"
OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(p):
 b=p.read_bytes()
 magic,ver,total=struct.unpack_from("<4sII",b)
 assert magic==b"glTF" and ver==2 and total==len(b)
 n,t=struct.unpack_from("<II",b,12); assert t==0x4e4f534a
 j=json.loads(b[20:20+n])
 assert j.get("animations") and j.get("nodes")
 channels=j["animations"][0]["channels"]
 return {"nodes":len(j["nodes"]),"channels":len(channels),"board_nodes":[x["name"] for x in j["nodes"] if "board" in x.get("name","").lower() or "trucks" in x.get("name","").lower()]}
def convert(p):
 d=OUT/"glb"/p.parent.name; d.mkdir(parents=True,exist_ok=True)
 target=d/p.name.replace(".ska.ps2",".glb")
 rec={"source":str(p.relative_to(SRC)),"source_sha256":sha(p)}
 try:
  if not target.exists():
   r=subprocess.run([str(TOOL),"ska",str(p),"--ske",str(SKE),"--format","glb","-o",str(d)],capture_output=True,text=True,timeout=60)
   if r.returncode: raise RuntimeError(r.stdout[-900:]+r.stderr[-500:])
  rec.update(validate(target)); rec.update(status="structural_pass",output=str(target.relative_to(OUT)),output_sha256=sha(target))
 except Exception as e:rec.update(status="failed",error=str(e))
 return rec
files=sorted(p for d in SRC.glob("thps6_skater*") if d.is_dir() for p in d.glob("*.ska.ps2"))
print("SOURCE CLIPS",len(files),flush=True)
records=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for rec in pool.map(convert,files):
  records.append(rec)
  if len(records)%50==0:print("EXPORTED",len(records),"FAILED",sum(r["status"]=="failed" for r in records),flush=True)
report={"id":"skater87-extraction","skeleton_sha256":sha(SKE),"tool_sha256":sha(TOOL),"source_count":len(files),"converted":sum(r["status"]=="structural_pass" for r in records),"failed":sum(r["status"]=="failed" for r in records),"validation":"GLB container/channels only; motion, binding and visual fidelity NOT verified","runtime_integration":False,"clips":records}
(OUT/"manifest.json").write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!="clips"}),flush=True)
