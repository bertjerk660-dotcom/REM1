from pathlib import Path
import json, subprocess, shutil, hashlib

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
VPK=Path(r"C:\Program Files (x86)\Steam\steamapps\common\GarrysMod\bin\vpk.exe")
IDX=ROOT/"build/prepared/gmod_weapon_runtime_candidates/sound_vpk_index.txt"
GMOD_MAN=ROOT/"build/prepared/gmod_prop_menu_curated/manifest.json"
OUT=ROOT/"build/prepared/prop_menu_thumbnails/native_gmod_spawnicons"
TMP=OUT/"_extract"
OUT.mkdir(parents=True,exist_ok=True)
TMP.mkdir(parents=True,exist_ok=True)

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest().upper()

# path -> dir VPK
mapping={}
archive=None
for line in IDX.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
    s=line.strip()
    if not s:continue
    if s.startswith("### "):
        archive=Path(s[4:].strip())
        continue
    if archive is not None:
        mapping.setdefault(s.replace("\\","/").lower(),archive)

m=json.loads(GMOD_MAN.read_text())
rows=[]
for i,r in enumerate(m["records"],1):
    src=r["source_model"].replace("\\","/").lower()
    if src.endswith(".mdl"):src=src[:-4]
    candidates=[
        f"materials/spawnicons/{src}.png",
        f"materials/spawnicons/{src}.vtf",
    ]
    found=None
    for c in candidates:
        a=mapping.get(c.lower())
        if a:
            found=(c,a);break
    row={"source_model":r["source_model"],"category":r["category"],"spawnicon_found":bool(found)}
    if found:
        rel,archive=found
        # Extract into temp tree, then copy to stable flat/name-preserving tree.
        work=TMP/f"{i:03d}"
        if work.exists():shutil.rmtree(work)
        work.mkdir(parents=True)
        cp=subprocess.run([str(VPK),"x",str(archive),rel],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
        extracted=work/Path(rel)
        if extracted.exists():
            dest=OUT/Path(rel)
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(extracted,dest)
            row.update({
                "archive":str(archive),
                "archive_path":rel,
                "local_path":str(dest),
                "sha256":sha(dest),
                "bytes":dest.stat().st_size,
                "extract_returncode":cp.returncode,
            })
        else:
            row.update({"archive":str(archive),"archive_path":rel,"extract_returncode":cp.returncode,"extract_log":cp.stdout[-1000:]})
    rows.append(row)

if TMP.exists():shutil.rmtree(TMP)
result={
    "purpose":"Extract native Source/GMod spawnicon assets where the mounted content already provides them. Missing entries retain the locally-rendered geometry preview as a support fallback; final Q-menu runtime remains Astra-owned.",
    "gmod_props":len(rows),
    "native_spawnicons_found":sum(bool(x["spawnicon_found"] and x.get("local_path")) for x in rows),
    "native_spawnicons_missing":sum(not bool(x.get("local_path")) for x in rows),
    "records":rows
}
(OUT/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("gmod_props","native_spawnicons_found","native_spawnicons_missing")},indent=2))
