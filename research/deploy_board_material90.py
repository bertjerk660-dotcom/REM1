from pathlib import Path
import hashlib,json,shutil,subprocess,datetime
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
OUT=ROOT/"build/attachment90";PKG=OUT/"package/Data"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proc=subprocess.run(["powershell.exe","-NoProfile","-Command","@(Get-Process FalloutNV -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True)
assert proc.stdout.strip()=="0","Close Fallout before replacing loaded board assets"
report=json.loads((OUT/"board_material_repair.json").read_text())
backup=ROOT/"backups/board_material90";assert not backup.exists(),"Already deployed or backup exists"
dll=DATA/"NVSE/Plugins/FNVGModTHUG2.dll";before=sha(dll)
for n in report["nifs"]:
 assert sha(DATA/"meshes/rem/thug2"/n["name"])==n["before_sha256"],"Concurrent NIF edit"
 assert sha(PKG/"meshes/rem/thug2"/n["name"])==n["after_sha256"]
for t in report["textures"]:
 assert not (DATA/t["path"]).exists(),"Destination texture already exists"
 assert sha(PKG/t["path"])==t["sha256"]
backup.mkdir(parents=True)
for n in report["nifs"]:shutil.copy2(DATA/"meshes/rem/thug2"/n["name"],backup/n["name"])
try:
 for t in report["textures"]:
  dst=DATA/t["path"];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/t["path"],dst)
 for n in report["nifs"]:
  dst=DATA/"meshes/rem/thug2"/n["name"];shutil.copy2(PKG/"meshes/rem/thug2"/n["name"],dst);assert sha(dst)==n["after_sha256"]
 assert sha(dll)==before
except Exception:
 for n in report["nifs"]:shutil.copy2(backup/n["name"],DATA/"meshes/rem/thug2"/n["name"])
 raise
report.update(deployed=True,deployed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),backup=str(backup),live_dll_sha256=sha(dll),runtime_visibility="not_tested")
(OUT/"board_material_deployment.json").write_text(json.dumps(report,indent=2))
print(json.dumps({"deployed":True,"nifs":3,"textures":4,"live_dll_unchanged":True,"backup":str(backup)}))
