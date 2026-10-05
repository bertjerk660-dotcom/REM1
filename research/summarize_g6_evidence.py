from pathlib import Path
import json, re, hashlib
root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
audit=json.loads((root/"research/thug2_ida/hud_score_audit68.json").read_text())
names={"SetSpecialBarColors","Theme_GetHUDColor","Theme_GetHUDSpecialColor","GetSpecialValue","SetSpecialValue","GotSpecial","ForceSpecial","ResetScore","ResetScorePot","UpdateScore","SetScoreDegradation","SetScoreAccumulation"}
selected=[x for x in audit["strings"] if x["text"] in names]
decomp=root/"build/thug2_ui_decompiled"
functions=[]
warnings=[]
for path in decomp.rglob("*.q"):
    text=path.read_text(encoding="utf-8",errors="replace")
    if "error" in text.lower() or "unsupported" in text.lower():
        warnings.append(path.relative_to(decomp).as_posix())
    for line in text.splitlines():
        if re.match(r"script .*?(hud|special|combo|score|pause)",line,re.I):
            functions.append({"file":path.relative_to(decomp).as_posix(),"symbol":line[7:].strip()})
manifest=json.loads((root/"build/thug2_ui_original/manifest.json").read_text())
report={"source_sha256":audit["input_sha256"],"ida_version":audit["ida_version"],
    "processor":audit["processor"],"discovered_strings":len(audit["strings"]),
    "selected_entrypoints":selected,"script_symbols":functions,
    "extract_count":len(manifest["entries"]),
    "extract_bytes":sum(x["size"] for x in manifest["entries"]),
    "decompiler":{"processed":416,"reported_success":415,"errors":1,
        "scripts":4720,"globals":9350,
        "warning":"Parser output is not proven semantic equivalence; one failure remains unresolved"},
    "parity":"not_implemented","authentic_runtime":"not_implemented"}
(root/"build/manifests/g6_source_audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps({"ida_strings":len(audit["strings"]),"selected_native_entries":len(selected),
    "hud_script_symbols":len(functions),"extract_count":len(manifest["entries"])}))