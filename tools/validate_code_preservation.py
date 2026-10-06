#!/usr/bin/env python3
"""Fail-closed preservation handoff validator. No proprietary payload is stored here."""
from pathlib import Path
import ast, hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
REQ=[
"context/CODE_PRESERVATION_SEMANTICS.md","context/IDA68_PRESERVATION_HANDOFF.md",
"context/THUG2_CODE_PRESERVATION.md","context/GMOD_INTERFACE_PRESERVATION.md",
"context/RUNTIME_OWNERSHIP_CONTRACT.md","context/THUG2_INTEGRATION_PROVENANCE.json"]
PROV=ROOT/"context/THUG2_INTEGRATION_PROVENANCE.json"
bad=[]; ok=[]
for rel in REQ:
 p=ROOT/rel
 (ok if p.exists() else bad).append(("exists",rel))
if PROV.exists():
 d=json.loads(PROV.read_text(encoding="utf-8"))
 if d["thug2_executable"]["sha256"]!="91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1": bad.append(("hash","THUG2 executable provenance"))
 if d["fnv_skeleton"]["sha256"]!="C6667DD94FD10392F851F748438B7C69C0D2CB407448BECAE6431D5ED1994C4C": bad.append(("hash","FNV skeleton provenance"))
 dirty={"Bip01 PelvisE","Bip01 Neck/","Bip01 L Hand+","Bip01 R Hand-"}
 vals=set(d["validated_bone_map"]["mapping"].values())
 if dirty & vals: bad.append(("bone-map","legacy malformed target present"))
 if d["validated_bone_map"]["missing_targets"]: bad.append(("bone-map","target absent from verified skeleton"))
 if d["ida68"]["required_version"]!="6.8": bad.append(("ida","wrong required IDA version"))
# Repository must not archive known proprietary payload extensions.
for p in ROOT.rglob("*"):
 if p.is_file() and p.suffix.lower() in {".iso",".elf",".idb",".id0",".id1",".id2",".nam",".til"}:
  bad.append(("proprietary-or-local-analysis-payload",str(p.relative_to(ROOT))))
report={"passed":not bad,"checks_ok":ok,"failures":bad}
print(json.dumps(report,indent=2))
sys.exit(0 if not bad else 1)
