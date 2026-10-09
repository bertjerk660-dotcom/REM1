"""Generic static acceptance validator for converted Source weapons (O01/O08 family).

Expectations come from the job (materials, grip mode, view registration limits),
the VMTs (glow / env / normal map / additive) and the sidecar spec (records,
DLL-identity rule). Same 12 checks as validate_o01_static.

Usage: python validate_weapon_static.py --job <job.json> --spec <spec.json> --root <ws> --fnv-data <Data>
          --stage <stage> --repro-stage <stage2> --protected <json> --report <out>
"""
import argparse, hashlib, json, math, subprocess, sys, time, warnings
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
warnings.filterwarnings("ignore")
from pyffi.formats.nif import NifFormat
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from bsa_read import BSA
from esp_read import subrecords
from build_override_sidecar import raw_records
from convert_source_weapon import parse_vmt_full

H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()


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
    st, data_dir, root = Path(a.stage), Path(a.fnv_data), Path(a.root)
    ESP = spec["esp_name"]
    report_name = job.get("report_name", "o01_conversion_report.json")
    conv = json.loads((st / report_name).read_text(encoding="utf-8"))
    res = {}
    chk = lambda n, k, ok, d: res.__setitem__(f"{n:02d}_{k}", {"pass": bool(ok), "detail": d})
    models = {k: st / job[k]["output"] for k in ("world", "view")}
    P = lambda k: root / job["inputs"][k]["path"]

    # 1 parse
    D = {}
    try:
        D = {k: nif(p) for k, p in models.items()}
        chk(1, "nifs_parse", all(d.version == 0x14020007 and d.user_version == 11 for d in D.values()), {k: len(d.blocks) for k, d in D.items()})
    except Exception as e:
        chk(1, "nifs_parse", False, str(e))

    # 2 container
    has_muzzle = conv.get("muzzle_fnv") is not None
    det, ok2 = {}, True
    for k, d in D.items():
        r = d.roots[0]
        prn = [e.string_data.decode() for e in r.extra_data_list if type(e).__name__ == "NiStringExtraData" and e.name == b"Prn"]
        proj = [c for c in r.children if c and c.name == b"ProjectileNode"]
        col = r.collision_object is not None
        det[k] = {"root": type(r).__name__, "prn": prn, "projectile_node": len(proj), "collision": col}
        ok2 &= type(r).__name__ == "BSFadeNode" and prn == ["Weapon"] and len(proj) == (1 if has_muzzle else 0) and col == (k == "world")
    chk(2, "weapon_container", ok2, det)

    # 3 textures resolve
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

    # 4 material mapping derived from the VMTs
    mm, ok4 = {}, True
    for d in D.values():
        for s in (b for b in d.blocks if type(b).__name__ == "NiTriShape"):
            mat = s.name.decode().split(":")[-1]
            spec_m = job["materials"][mat]
            vmt = parse_vmt_full(P(spec_m["vmt"]))
            pp = next(p for p in s.properties if type(p).__name__ == "BSShaderPPLightingProperty")
            tx = [t.decode() for t in pp.texture_set.textures]
            want_glow = vmt.get("selfillum") == "1" or vmt["shader"].lower() == "unlitgeneric"
            want_env = "envmapmask" in spec_m or ("bump" in spec_m and vmt.get("normalmapalphaenvmapmask") == "1" and bool(vmt.get("envmap")))
            want_norm = "bump" in spec_m
            want_add = vmt.get("additive") == "1"
            alpha = [p for p in s.properties if type(p).__name__ == "NiAlphaProperty"]
            good = (bool(tx[2]) == want_glow and bool(tx[4] and tx[5]) == want_env
                    and (tx[1].endswith(f"{mat}_n.dds") if want_norm else tx[1].endswith("_flat_n.dds"))
                    and (len(alpha) == 1) == want_add)
            mm[mat] = {"flags": hex(int(pp.shader_flags)), "glow": tx[2], "env": tx[4], "mask": tx[5], "normal": tx[1],
                       "additive": bool(alpha), "expected": {"glow": want_glow, "env": want_env, "normal": want_norm, "additive": want_add}, "ok": good}
            ok4 &= good
    chk(4, "material_mapping", ok4, mm)

    # 5 strings
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
        strings += [(ESP, v.split(b"\0")[0].decode("cp1252", "replace")) for tag, v in subrecords(body) if tag in ("EDID", "FULL", "MODL", "ICON", "MICO")]
    bad = [f"{fn}: {s}" for fn, s in strings if any(p in s.lower() for p in pats)]
    chk(5, "no_absolute_paths", not bad, {"strings_checked": len(strings), "bad": bad})

    # 6 grip registration and sanity
    g = conv["grip"]; off = g["offset_fnv"]
    if g["mode"] == "bottom":
        after = [g["toolgun_grip_bottom_before"][i] + off[i] for i in range(3)]
        gerr = math.dist(after, g["vanilla_10mm_grip_bottom"])
    else:
        before = g["source_reference_before"]; ref = g["donor_reference"]
        gerr = math.hypot(before[0] + off[0] - ref[0], before[2] + off[2] - ref[2])
    w = conv["outputs"]["world"]["bounds"]; dims = [w[1][i] - w[0][i] for i in range(3)]
    mz = conv.get("muzzle_fnv")
    mz_ok = mz is None or (w[0][0] - 2 <= mz[0] <= w[1][0] + 2 and w[0][1] - 2 <= mz[1] <= w[1][1] + 2)
    ok6 = gerr < 1e-6 and max(dims) < 80 and min(dims) > 0.5 and mz_ok
    chk(6, "grip_registration", ok6, {"mode": g["mode"], "grip_error": gerr, "offset": off, "dims_xyz": dims, "muzzle": mz, "muzzle_within_bounds": mz_ok})

    # 7 first-person vs world agreement
    v = conv["outputs"]["view"]["bounds"]
    derr = max(abs(v[k][i] - w[k][i]) for k in range(2) for i in range(3))
    reg = conv["view_registration"]
    lim = job["view"].get("max_bounds_diff", 3.5)
    med_ok = reg.get("median") is None or reg["median"] <= job["view"].get("max_median", 0.5)
    chk(7, "view_world_registration", derr <= lim and med_ok,
        {"bounds_max_diff": derr, "limit": lim, "scale": reg.get("scale"), "median": reg.get("median"), "p95": reg.get("p95")})

    # 8 provenance
    prov = {k: H(root / s["path"]) == s["sha256"].upper() for k, s in job["inputs"].items()}
    chk(8, "source_provenance", all(prov.values()), {"all": len(prov), "pinned": job.get("pinned_inputs", []), "mismatch": [k for k, ok in prov.items() if not ok]})

    # 9 sidecar overrides only
    side = raw_records(st / ESP); orig = raw_records(spec["source_plugin"])
    keys = sorted(f"{t}:{f:08X}" for t, f in side)
    want = sorted(f"{o['type']}:{int(o['formid'], 16):08X}" for o in spec["overrides"])
    diffs = {}
    for o in spec["overrides"]:
        key = (o["type"], int(o["formid"], 16))
        a_s = [(t, x) for t, x in subrecords(orig[key][1]) if t not in o.get("drop", [])]
        b_s = subrecords(side[key][1])
        diffs[o["formid"]] = {"changed": [t for (t, x), (u, y) in zip(a_s, b_s) if t != u or x != y],
                              "same_count": len(a_s) == len(b_s), "header_flags_same": orig[key][0][8:12] == side[key][0][8:12]}
    dll = data_dir / "NVSE" / "Plugins" / "FNVGModTHUG2.dll"
    dll_fix = dll.exists() and b"identified by owning plugin" in dll.read_bytes()
    weap_over = any(o["type"] == "WEAP" for o in spec["overrides"])
    weap_ok = (not weap_over) or (not spec.get("weap_dll_identified", True)) or (spec.get("requires_dll_identity_fix") and dll_fix)
    ok9 = keys == want and weap_ok and all(set(x["changed"]) <= {"MODL", "OBND"} and x["same_count"] and x["header_flags_same"] for x in diffs.values())
    chk(9, "sidecar_overrides_only", ok9, {"records": keys, "per_record": diffs, "weap_dll_identified": spec.get("weap_dll_identified"),
                                           "deployed_dll_has_identity_fix": dll_fix})

    # 10 protected
    prot = json.loads(Path(a.protected).read_text(encoding="utf-8-sig"))
    now = {k: H(x["path"]) for k, x in prot.items()}
    chk(10, "protected_unchanged", all(now[k] == prot[k]["sha256"] for k in prot), now)

    # 11 no unrelated outputs
    expected = {job["world"]["output"], job["view"]["output"], ESP, report_name} | \
               {x["path"] for k, x in conv["outputs"].items() if k.startswith("tex:") or k == "flat_normal"}
    actual = {p.relative_to(st).as_posix() for p in st.rglob("*") if p.is_file() and "_work" not in p.parts}
    chk(11, "no_unrelated_outputs", actual == expected, {"unexpected": sorted(actual - expected), "missing": sorted(expected - actual)})

    # 12 reproducible
    rs = Path(a.repro_stage)
    subprocess.run([sys.executable, str(HERE / "convert_source_weapon.py"), a.job, "--root", a.root, "--fnv-data", a.fnv_data,
                    "--stage", str(rs)], check=True, capture_output=True)
    subprocess.run([sys.executable, str(HERE / "build_override_sidecar.py"), a.spec, "--out", str(rs / ESP)], check=True, capture_output=True)
    cmp = {r: H(st / r) == H(rs / r) for r in sorted(expected - {report_name})}
    chk(12, "reproducible", all(cmp.values()), cmp)

    out = {"validator": "validate_weapon_static 1.0.0", "all_pass": all(x["pass"] for x in res.values()), "checks": res,
           "hashes": {r: H(st / r) for r in sorted(expected)}}
    Path(a.report).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    for k, x in res.items():
        print(("PASS " if x["pass"] else "FAIL ") + k)
    print("ALL PASS" if out["all_pass"] else "FAILURES PRESENT")
    sys.exit(0 if out["all_pass"] else 1)


if __name__ == "__main__":
    main()
