"""Extract original THUG2 PS2 UI/script/font sources; no conversion or emulation claimed."""
from pathlib import Path
import argparse, hashlib, json, re, struct
p=argparse.ArgumentParser()
p.add_argument("source",type=Path)
p.add_argument("output",type=Path)
a=p.parse_args()
hed_path=a.source/"DATAP.HED"
wad_path=a.source/"DATAP.WAD"
hed=hed_path.read_bytes()
wad_size=wad_path.stat().st_size
entries=[]
seen=set()
with wad_path.open("rb") as wad:
    for m in re.finditer(rb"\\[ -~]{3,220}\x00",hed):
        path=m.group()[:-1].decode("ascii")
        low=path.lower()
        if not (any(t in low for t in ("hud","menu","font","special","score","combo","balance","screen")) or low.endswith((".qb",".qb.ps2"))):
            continue
        if m.start()<8 or (m.start()-8)%4:
            continue
        offset,size=struct.unpack_from("<II",hed,m.start()-8)
        if size<=0 or offset+size>wad_size:
            raise ValueError("Invalid HED range: "+path)
        parts=path.strip("\\").split("\\")
        if any(v in ("",".","..") or ":" in v for v in parts):
            raise ValueError("Unsafe archive path")
        rel=Path(*parts)
        if str(rel).lower() in seen:
            raise ValueError("Duplicate entry "+path)
        seen.add(str(rel).lower())
        wad.seek(offset)
        data=wad.read(size)
        if len(data)!=size:
            raise ValueError("Short read")
        dst=a.output/rel
        dst.parent.mkdir(parents=True,exist_ok=True)
        if dst.exists() and dst.read_bytes()!=data:
            raise ValueError("Refusing to overwrite differing file: "+str(dst))
        dst.write_bytes(data)
        entries.append({"source_path":path,"offset":offset,"size":size,
            "sha256":hashlib.sha256(data).hexdigest(),"relative_output":rel.as_posix()})
report={"format":"THUG2_PS2_DATAP_HED_WAD","hed_sha256":hashlib.sha256(hed).hexdigest(),
    "wad_size":wad_size,"status":"original_bytes_extracted_not_runtime_integrated","entries":entries}
a.output.mkdir(parents=True,exist_ok=True)
(a.output/"manifest.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"entries":len(entries),"bytes":sum(v["size"] for v in entries),
    "ui_examples":[v["source_path"] for v in entries if any(t in v["source_path"].lower() for t in ("hud","font","score","special"))][:45]}))