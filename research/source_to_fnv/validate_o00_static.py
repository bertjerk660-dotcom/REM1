"""O00 static acceptance validator (the 12 checks from the Opus session brief).

Usage:
  python validate_o00_static.py --job jobs/o00_bench01a.json --root <workspace> \
      --fnv-data <FNV Data> --stage <stage dir> --repro-stage <second stage dir> \
      --protected <protected_hashes.json> --report <out.json>

Exit code 0 only when every check passes.
"""
import argparse, hashlib, io, json, subprocess, sys, time
from pathlib import Path

if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from bsa_read import BSA
from build_static_sidecar import inspect as inspect_esp

H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()


def main():
    ap = argparse.ArgumentParser()
    for a in ("--job", "--root", "--fnv-data", "--stage", "--repro-stage", "--protected", "--report"):
        ap.add_argument(a, required=True)
    a = ap.parse_args()
    job = json.loads(Path(a.job).read_text(encoding="utf-8"))
    stage, data_dir = Path(a.stage), Path(a.fnv_data)
    conv = json.loads((stage / "o00_conversion_report.json").read_text(encoding="utf-8"))
    nif_path = stage / job["output"]["mesh"]
    esp_path = stage / "REM_GoldenBench_Test.esp"
    res = {}

    def check(n, name, ok, detail):
        res[f"{n:02d}_{name}"] = {"pass": bool(ok), "detail": detail}

    # 1 NIF exists and parses
    d = NifFormat.Data()
    try:
        with open(nif_path, "rb") as f:
            d.read(f)
        ok1 = d.version == 0x14020007 and d.user_version == 11 and d.user_version_2 == 34
        check(1, "nif_parses", ok1, {"blocks": len(d.blocks), "version": hex(d.version)})
    except Exception as e:
        check(1, "nif_parses", False, str(e))
        d = None

    blocks = d.blocks if d else []
    T = lambda n: [b for b in blocks if type(b).__name__ == n]
    root = d.roots[0] if d else None

    # 2 hierarchy
    shapes = T("NiTriShape")
    bsx = [x.integer_data for x in T("BSXFlags")]
    coll = T("bhkCollisionObject")
    ok2 = (root is not None and type(root).__name__ == "BSFadeNode" and bsx == [2] and len(shapes) >= 1
           and all(s in root.children for s in shapes) and len(coll) == 1 and coll[0].target is root
           and root.collision_object is coll[0])
    check(2, "hierarchy", ok2, {"root": type(root).__name__ if root else None, "bsx": bsx,
                                "shapes": len(shapes), "collision_targets_root": bool(coll and coll[0].target is root)})

    # 3 every referenced texture resolves (staged candidate or vanilla archive)
    tex_bsas = [BSA(data_dir / n) for n in ("Fallout - Textures.bsa", "Fallout - Textures2.bsa")]
    refs, missing = [], []
    for ts in T("BSShaderTextureSet"):
        for t in ts.textures:
            t = t.decode("cp1252")
            if not t:
                continue
            refs.append(t)
            staged = stage / t.replace("\\", "/")
            if not (staged.exists() or any(t.lower() in b.entries for b in tex_bsas)):
                missing.append(t)
    check(3, "textures_resolve", refs and not missing, {"referenced": refs, "missing": missing})

    # 4 material / shader mapping
    pp = T("BSShaderPPLightingProperty")
    flags = [hex(int(p.shader_flags)) for p in pp]
    slots = [[t.decode() for t in p.texture_set.textures] for p in pp]
    ok4 = (flags == ["0x82000081"] * len(pp) and all(s[4] == job["cubemap"] and s[5].endswith("_m.dds") for s in slots))
    check(4, "material_mapping", ok4, {"shader_flags": flags, "env_slot": [s[4] for s in slots],
                                       "envmask_slot": [s[5] for s in slots]})

    # 5 no absolute development paths in any output
    bad = []
    for p in [nif_path, esp_path]:
        raw = p.read_bytes().lower()
        for pat in (b":\\", b":/", b"users\\", b"/users/", b"engineer station", b"documents\\"):
            if pat in raw:
                bad.append(f"{p.name}:{pat!r}")
    check(5, "no_absolute_paths", not bad, bad)

    # 6 size / orientation / frame
    lo, hi = conv["fnv"]["visual_bounds"]
    dims = [hi[i] - lo[i] for i in range(3)]
    ok6 = (abs(lo[2]) < 1e-4 and dims[0] > dims[1] and conv["checks"]["model_frame_max_error"] < 0.6
           and 100 < dims[0] < 170 and 25 < conv["fnv"]["seat_height_estimate"] < 45)
    check(6, "size_orientation", ok6, {"dims_xyz": dims, "min_z": lo[2], "seat_height": conv["fnv"]["seat_height_estimate"],
                                       "frame_error": conv["checks"]["model_frame_max_error"],
                                       "note": "long axis on X, faces +Y, base at z=0"})

    # 7 collision present with justified material
    lst = T("bhkListShape")
    cvs = T("bhkConvexVerticesShape")
    mats = sorted({int(c.material.material) for c in cvs} | {int(l.material.material) for l in lst})
    body = T("bhkRigidBodyT")
    ok7 = (len(lst) == 1 and len(cvs) == conv["collision"]["pieces"] and mats == [9]
           and body and body[0].havok_col_filter.layer == 1 and body[0].motion_system == 7)
    check(7, "collision", ok7, {"pieces": len(cvs), "havok_material_ids": mats, "expected": "9 = MAT_WOOD",
                                "layer": body[0].havok_col_filter.layer if body else None,
                                "motion_system": body[0].motion_system if body else None})

    # 8 provenance: every source input matches the packet hash
    prov = {k: H(Path(a.root) / v["path"]) == v["sha256"].upper() for k, v in job["inputs"].items()}
    check(8, "source_provenance", all(prov.values()), prov)

    # 9 sidecar holds only the intended record
    esp = inspect_esp(esp_path)
    recs = [(r["type"], r.get("EDID", [None])[0]) for r in esp["records"]]
    model = [r.get("MODL", [None])[0] for r in esp["records"] if r["type"] == "STAT"]
    ok9 = (recs == [("TES4", None), ("STAT", "REM_GoldenBench01a")] and esp["groups"] == ["STAT"]
           and model == [job["output"]["mesh"].replace("meshes/", "", 1).replace("/", "\\")]
           and esp["records"][0].get("MAST") == ["FalloutNV.esm"])
    check(9, "sidecar_records", ok9, {"records": recs, "groups": esp["groups"], "model": model})

    # 10 protected runtime files unchanged
    prot = json.loads(Path(a.protected).read_text(encoding="utf-8"))
    now = {k: H(v["path"]) for k, v in prot.items()}
    check(10, "protected_unchanged", all(now[k] == prot[k]["sha256"] for k in prot),
          {k: {"expected": prot[k]["sha256"], "actual": now[k]} for k in prot})

    # 11 no unrelated outputs: stage holds only expected files
    expected = {job["output"]["mesh"], "REM_GoldenBench_Test.esp", "o00_conversion_report.json"} | \
               {v["path"] for k, v in conv["outputs"].items() if k != "nif"}
    actual = {p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file() and "_work" not in p.parts}
    check(11, "no_unrelated_outputs", actual == expected, {"unexpected": sorted(actual - expected),
                                                           "missing": sorted(expected - actual)})

    # 12 reproducibility: independent rerun gives identical bytes
    rs = Path(a.repro_stage)
    subprocess.run([sys.executable, str(HERE / "convert_source_static.py"), a.job, "--root", a.root,
                    "--fnv-data", a.fnv_data, "--stage", str(rs)], check=True, capture_output=True)
    obnd = conv["obnd"]
    subprocess.run([sys.executable, str(HERE / "build_static_sidecar.py"), "--out", str(rs / "REM_GoldenBench_Test.esp"),
                    "--edid", "REM_GoldenBench01a", "--model", model[0] if model else "", "--obnd", *map(str, obnd)],
                   check=True, capture_output=True)
    cmp = {}
    for rel in sorted(expected - {"o00_conversion_report.json"}):
        cmp[rel] = H(stage / rel) == H(rs / rel)
    check(12, "reproducible", all(cmp.values()), cmp)

    out = {"validator": "validate_o00_static 1.0.0", "all_pass": all(v["pass"] for v in res.values()), "checks": res,
           "hashes": {rel: H(stage / rel) for rel in sorted(expected)}}
    Path(a.report).write_text(json.dumps(out, indent=2), encoding="utf-8")
    for k, v in res.items():
        print(("PASS " if v["pass"] else "FAIL ") + k)
    print("ALL PASS" if out["all_pass"] else "FAILURES PRESENT")
    sys.exit(0 if out["all_pass"] else 1)


if __name__ == "__main__":
    main()
