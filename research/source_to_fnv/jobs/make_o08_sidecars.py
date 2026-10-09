"""Write O08a/b/c sidecar specs (presentation-only overrides) from the conversion reports.

Usage: python make_o08_sidecars.py --candidates <O08 candidates dir> --fnv-data <Data>
"""
import argparse, json, math
from pathlib import Path

PKG = {
    "a": ("crowbar", "REM_O08a_Crowbar_Test.esp", "01000808", "01000839", True),
    "b": ("pistol", "REM_O08b_Pistol_Test.esp", "0100080F", "01000840", True),
    "c": ("smg1", "REM_O08c_SMG1_Test.esp", "01000813", "01000844", False),
}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--candidates", required=True); ap.add_argument("--fnv-data", required=True)
    a = ap.parse_args()
    here = Path(__file__).parent
    for k, (n, esp, weap, stat, dll_identified) in PKG.items():
        rep = json.loads((Path(a.candidates) / f"o08{k}_{n}" / "stage_a" / f"o08{k}_conversion_report.json").read_text(encoding="utf-8"))
        lo, hi = rep["outputs"]["world"]["bounds"]
        ob = [math.floor(lo[0]), math.floor(lo[1]), math.floor(lo[2]), math.ceil(hi[0]), math.ceil(hi[1]), math.ceil(hi[2])]
        spec = {
            "source_plugin": str(Path(a.fnv_data) / "REM_GModTHUG2.esp"),
            "masters": ["FalloutNV.esm", "REM_GModTHUG2.esp"],
            "esp_name": esp,
            "author": f"REM O08{k} pipeline",
            "description": f"Isolated O08{k} test sidecar: {n} first-person (STAT) and world (WEAP) model overrides only. Not for release.",
            "weap_dll_identified": dll_identified,
            "requires_dll_identity_fix": dll_identified,
            "overrides": [
                {"formid": stat, "type": "STAT", "MODL": f"rem\\gmod\\weapons\\{n}\\c_{n}.nif", "OBND": ob, "drop": ["MODT", "MODS"]},
                {"formid": weap, "type": "WEAP", "MODL": f"rem\\gmod\\weapons\\{n}\\w_{n}.nif", "OBND": ob, "drop": ["MODT", "MODS"]},
            ],
        }
        out = here / f"o08{k}_sidecar_spec.json"
        out.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        print(out.name, "OBND", ob, "dll_identified", dll_identified)


if __name__ == "__main__":
    main()
