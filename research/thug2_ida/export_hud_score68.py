# IDAPython 6.8 / Python 2.7. Run on an isolated copy of the existing database.
import idaapi, idautils, idc, json, os, hashlib
idaapi.autoWait()
out = os.environ["THUG2_AUDIT_OUTPUT"]
terms = ("hud", "special", "combo", "score", "trick", "balance", "menu", "screen", "font", "skater")
records = []
for item in idautils.Strings():
    try:
        value = str(item)
    except Exception:
        continue
    if len(value) > 240 or not any(t in value.lower() for t in terms):
        continue
    refs = []
    for xr in idautils.XrefsTo(item.ea, 0):
        start = idc.GetFunctionAttr(xr.frm, idc.FUNCATTR_START)
        # Data references can be registration-name tables. Record neighbors,
        # never assume a neighboring word is a function without further proof.
        neighbors = []
        if start == idc.BADADDR:
            for off in (-8, -4, 0, 4, 8):
                ptr = idc.Dword(xr.frm + off)
                seg = idaapi.getseg(ptr)
                neighbors.append({"offset": off, "value": hex(ptr),
                    "segment": idc.SegName(ptr) if seg else None,
                    "function": idc.GetFunctionName(ptr) if seg else None})
        refs.append({"ea": hex(xr.frm), "type": xr.type,
            "function_start": None if start == idc.BADADDR else hex(start),
            "neighbors": neighbors})
    records.append({"text": value, "ea": hex(item.ea), "references": refs})
input_path = idc.GetInputFilePath()
report = {"ida_version": idaapi.get_kernel_version(), "processor": idaapi.get_inf_structure().procName,
    "input_path": input_path, "input_sha256": hashlib.sha256(open(input_path,"rb").read()).hexdigest(),
    "status": "discovery_only_not_verified_runtime_equivalence", "strings": records}
with open(out, "w") as f:
    json.dump(report, f, indent=2, sort_keys=True)
idc.Exit(0)