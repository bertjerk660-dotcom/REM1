"""O01 static acceptance validator (Tool Gun presentation).

Usage: python validate_o01_static.py --job jobs/o01_toolgun.json --spec jobs/o01_sidecar_spec.json \
   --root <ws> --fnv-data <Data> --stage <stage> --repro-stage <stage2> --protected <json> --report <out>
"""
import argparse, hashlib, io, json, math, struct, subprocess, sys, time
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from bsa_read import BSA
from esp_read import subrecords
from build_override_sidecar import raw_records

H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
ESP = "REM_O01_ToolGun_Test.esp"


def nif(p):
    d = NifFormat.Data()
    with open(p, "rb") as f:
        d.read(f)
    return d


def main():
    ap = argparse.ArgumentParser()
    for x in ("--job", "--spec", "--root", "--fnv-data", "--stage", "--repro-stage", "--protected", "--report"):
        ap.add_argument(x, required=True)
    a = ap.parse_args()
    job = json.loads(Path(a.job).read_text(encoding="utf-8-sig"))
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8-sig"))
    st, data_dir = Path(a.stage), Path(a.fnv_data)
    conv = json.loads((st / "o01_conversion_report.json").read_text(encoding="utf-8"))
    res = {}
    chk = lambda n, k, ok, d: res.__setitem__(f"{n:02d}_{k}", {"pass": bool(ok), "detail": d})
    models = {k: st / job[k]["output"] for k in ("world", "view")}
    D = {}

    # 1 both NIFs parse with FNV version
    try:
        D = {k: nif(p) for k, p in models.items()}
        chk(1, "nifs_parse", all(d.version == 0x14020007 and d.user_version == 11 for d in D.values()),
            {k: len(d.blocks) for k, d in D.items()})
    except Exception as e:
        chk(1, "nifs_parse", False, str(e))

    # 2 weapon container: BSFadeNode root, Prn=Weapon, ProjectileNode, world collision only
    det, ok2 = {}, True
    for k, d in D.items():
        r = d.roots[0]
        prn = [e.string_data.decode() for e in r.extra_data_list if type(e).__name__ == "NiStringExtraData" and e.name == b"Prn"]
        proj = [c for c in r.children if c and c.name == b"ProjectileNode"]
        col = r.collision_object is not None
        det[k] = {"root": type(r).__name__, "prn": prn, "projectile_node": len(proj), "collision": col}
        ok2 &= type(r).__name__ == "BSFadeNode" and prn == ["Weapon"] and len(proj) == 1 and col == (k == "world")
    chk(2, "weapon_container", ok2, det)

    # 3 textures resolve (staged or vanilla BSA)
    bsas = [BSA(data_dir / n) for n in ("Fallout - Textures.bsa", "Fallout - Textures2.bsa")]
    miss, refs = [], set()
    for d in D.values():
        for ts in (b for b in d.blocks if type(b).__name__ == "BSShaderTextureSet"):
            for t in ts.textures:
                t = t.decode()
                if t:
                    refs.add(t)
                    if not ((st / t.replace("\\", "/")).exists() or any(t.lower() in b.entries for b in bsas)):
                        miss.append(t)
    chk(3, "textures_resolve", refs and not miss, {"referenced": sorted(refs), "missing": miss})

    # 4 material mapping: glow on selfillum/unlit parts, env mask on masked parts
    mm, ok4 = {}, True
    for d in D.values():
        for s in (b for b in d.blocks if type(b).__name__ == "NiTriShape"):
            mat = s.name.decode().split(":")[-1]
            pp = next(p for p in s.properties if type(p).__name__ == "BSShaderPPLightingProperty")
            tx = [t.decode() for t in pp.texture_set.textures]
            want_glow = mat in ("toolgun2", "toolgun3", "screen")
            want_env = mat in ("toolgun", "toolgun2", "toolgun3")
            good = bool(tx[2]) == want_glow and bool(tx[4] and tx[5]) == want_env
            cover = None
            if tx[2]:  # glow coverage must follow the source mask, not flood the part (F017)
                from PIL import Image
                gi = Image.open(st / tx[2].replace("\\", "/")).convert("L")
                cover = sum(1 for v in gi.getdata() if v > 8) / (gi.size[0] * gi.size[1])
                if mat in ("toolgun2", "toolgun3"):
                    good = good and cover < 0.10
            mm[mat] = {"flags": hex(int(pp.shader_flags)), "glow": tx[2], "glow_coverage": cover,
                       "env": tx[4], "mask": tx[5], "ok": good}
            ok4 &= good
    chk(4, "material_mapping", ok4, mm)

    # 5 no absolute paths in any string the game reads (NIF strings, plugin text subrecords)
    pats = (":\\", ":/", "users\\", "engineer station", "documents\\")
    strings = []
    for k, d in D.items():
        for b in d.blocks:
            for attr in ("name", "string_data", "file_name"):
                v = getattr(b, attr, None)
                if isinstance(v, bytes) and v:
                    strings.append((models[k].name, v.decode("cp1252", "replace")))
            if type(b).__name__ == "BSShaderTextureSet":
                strings += [(models[k].name, t.decode("cp1252", "replace")) for t in b.textures]
    for (t, f), (h, body) in raw_records(st / ESP).items():
        strings += [(ESP, v.split(b"\0")[0].decode("cp1252", "replace")) for tag, v in subrecords(body)
                    if tag in ("EDID", "FULL", "MODL", "ICON", "MICO")]
    bad = [f"{fn}: {s}" for fn, s in strings if any(p in s.lower() for p in pats)]
    chk(5, "no_absolute_paths", not bad, {"strings_checked": len(strings), "bad": bad})

    # 6 scale/orientation/grip vs vanilla 10mm
    w = conv["outputs"]["world"]["bounds"]; dims = [w[1][i] - w[0][i] for i in range(3)]
    g = conv["grip"]; after = [g["toolgun_grip_bottom_before"][i] + g["offset_fnv"][i] for i in range(3)]
    gerr = math.dist(after, g["vanilla_10mm_grip_bottom"])
    mz = conv["muzzle_fnv"]
    ok6 = dims[0] > dims[1] > dims[2] and 18 < dims[0] < 35 and gerr < 1e-6 and mz[0] > 20 and abs(mz[1] - 6) < 4
    chk(6, "scale_orientation_grip", ok6, {"dims_xyz": dims, "grip_error": gerr, "muzzle": mz,
                                            "note": "barrel +X, up +Y, length vs 10mm 22.0"})

    # 7 first-person and world share size and grip
    v = conv["outputs"]["view"]["bounds"]
    derr = max(abs(v[k][i] - w[k][i]) for k in range(2) for i in range(3))
    reg = conv["view_registration"]
    chk(7, "view_world_registration", derr < 0.01 and reg["within_0.01"] >= 0.99,
        {"bounds_max_diff": derr, "icp_scale": reg["scale"], "icp_median": reg["median"], "within_0.01": reg["within_0.01"]})

    # 8 provenance
    prov = {k: H(Path(a.root) / s["path"]) == s["sha256"].upper() for k, s in job["inputs"].items()}
    chk(8, "source_provenance", all(prov.values()), prov)

    # 9 sidecar: only the two overrides; every other subrecord identical to REM_GModTHUG2.esp
    side = raw_records(st / ESP); orig = raw_records(spec["source_plugin"])
    keys = sorted(f"{t}:{f:08X}" for t, f in side)
    diffs = {}
    for o in spec["overrides"]:
        key = (o["type"], int(o["formid"], 16))
        a_s = [(t, v) for t, v in subrecords(orig[key][1]) if t not in o.get("drop", [])]
        b_s = subrecords(side[key][1])
        changed = [t for (t, x), (u, y) in zip(a_s, b_s) if t != u or x != y]
        diffs[o["formid"]] = {"changed": changed, "dropped": o.get("drop", []), "same_count": len(a_s) == len(b_s),
                              "header_flags_same": orig[key][0][8:12] == side[key][0][8:12]}
    want = sorted(f"{o['type']}:{int(o['formid'], 16):08X}" for o in spec["overrides"])
    ok9 = keys == want and "WEAP:01000803" not in keys and all(
        set(d["changed"]) <= {"MODL", "OBND"} and d["same_count"] and d["header_flags_same"] for d in diffs.values())
    chk(9, "sidecar_overrides_only", ok9, {"records": keys, "expected": want, "per_record": diffs,
                                           "rule": "the Tool Gun WEAP must not be overridden (DLL identifies it by world-model path; F018)"})

    # 10 protected files unchanged
    prot = json.loads(Path(a.protected).read_text(encoding="utf-8-sig"))
    now = {k: H(x["path"]) for k, x in prot.items()}
    chk(10, "protected_unchanged", all(now[k] == prot[k]["sha256"] for k in prot), now)

    # 11 no unrelated outputs
    expected = {job["world"]["output"], job["view"]["output"], ESP, "o01_conversion_report.json"} | \
               {x["path"] for k, x in conv["outputs"].items() if k.startswith("tex:") or k == "flat_normal"}
    actual = {p.relative_to(st).as_posix() for p in st.rglob("*") if p.is_file() and "_work" not in p.parts}
    chk(11, "no_unrelated_outputs", actual == expected, {"unexpected": sorted(actual - expected), "missing": sorted(expected - actual)})

    # 12 reproducible
    rs = Path(a.repro_stage)
    subprocess.run([sys.executable, str(HERE / "convert_source_weapon.py"), a.job, "--root", a.root,
                    "--fnv-data", a.fnv_data, "--stage", str(rs)], check=True, capture_output=True)
    subprocess.run([sys.executable, str(HERE / "build_override_sidecar.py"), a.spec, "--out", str(rs / ESP)],
                   check=True, capture_output=True)
    cmp = {r: H(st / r) == H(rs / r) for r in sorted(expected - {"o01_conversion_report.json"})}
    chk(12, "reproducible", all(cmp.values()), cmp)

    out = {"validator": "validate_o01_static 1.0.0", "all_pass": all(x["pass"] for x in res.values()), "checks": res,
           "hashes": {r: H(st / r) for r in sorted(expected)}}
    Path(a.report).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    for k, x in res.items():
        print(("PASS " if x["pass"] else "FAIL ") + k)
    print("ALL PASS" if out["all_pass"] else "FAILURES PRESENT")
    sys.exit(0 if out["all_pass"] else 1)


if __name__ == "__main__":
    main()
