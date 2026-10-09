"""Source Engine weapon (w_ world + c_ view) -> Fallout: New Vegas weapon NIFs (O01).

Job-file driven, hash-verified, staging-only, byte-reproducible.

Rules (evidence in README / O01 notes):
  * World model: mesh taken into the GMod right-hand bone frame (bone-merge attach
    point), axes mapped hand(x fwd, -z up, y side) -> FNV weapon (X fwd, Y up, Z side).
  * Grip: translated so the bottom of its handle sits where the vanilla 10mm grip
    bottom sits (translation only; barrel stays on +X). Same offset for both models.
  * View model: registered onto the world model by similarity ICP (all vertices),
    then given the identical world transform, so 1st/3rd person share size and grip.
  * Root BSFadeNode + Prn=Weapon (P-F004). ProjectileNode at the GMod muzzle.
  * World model gets dynamic Havok collision from the original physics SMD.
  * Materials from VMTs: env mask scaled by $envmaptint, $selfillum alpha -> glow map,
    UnlitGeneric -> full glow. Shader/material fields copied from vanilla templates.

Usage: python convert_source_weapon.py <job.json> --root <ws> --fnv-data <Data> --stage <dir>
"""
import argparse, io, json, math, os, subprocess, sys, time
from pathlib import Path

if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from convert_source_static import (parse_smd, parse_vmt, sha256, bounds, sub, dot, cross, norm,
                                   split_convex_pieces, convex_planes, load_ref, first, copy_fields,
                                   NIF_V, NIF_UV, NIF_UV2, HAVOK_SCALE)
from smd_skeleton import parse_skeleton, world_transforms, to_local, mv
from icp_fit import icp
from similarity_fit import apply as sim_apply
from dds_write import write_dds
from vtf_decode import decode as vtf_decode

TOOL_VERSION = "source_to_fnv/convert_source_weapon 1.1.0"
PP_FIELDS = ["shader_type", "shader_flags", "shader_flags_2", "environment_map_scale", "texture_clamp_mode"]
MAT_FIELDS = ["specular_color", "emissive_color", "glossiness", "alpha", "emit_multi"]


def parse_vmt_full(path):
    """VMT key/values accepting quoted and unquoted values ("$selfillum" 1)."""
    import re
    t = Path(path).read_text(encoding="utf-8", errors="ignore")
    t = "\n".join(l.split("//")[0] for l in t.splitlines())
    shader = (re.match(r'\s*"?(\w+)"?', t) or [None, ""])[1]
    kv = {}
    for k, q, u in re.findall(r'"?\$(\w+)"?[ \t]+(?:"([^"]*)"|([^\s"{}]+))', t):
        kv[k.lower()] = q if q else u
    return {"shader": shader, **kv}


def vtf_rgba(vtf, work=None, vtfcmd=None):
    """Decode with the in-repo decoder. VTFCmd's TGA export drops DXT5 alpha (F017)."""
    return vtf_decode(vtf)


def hand_space(smd, bone):
    n, b = parse_skeleton(smd)
    W = world_transforms(n, b)
    H = W[bone]
    R = H[0]
    rt = lambda v: mv([[R[j][i] for j in range(3)] for i in range(3)], v)  # rotate into bone frame
    tris = [(m, [(to_local(H, v[0]), rt(v[1]), v[2]) for v in vs]) for m, vs in parse_smd(smd)]
    return tris, W


def hand_to_fnv(v, S):
    x, y, z = v
    return (x * S, -z * S, y * S)


def grip_bottom_centroid(pts, depth=3.0):
    ymin = min(p[1] for p in pts)
    sel = [p for p in pts if p[1] <= ymin + depth]
    return tuple(sum(p[i] for p in sel) / len(sel) for i in range(3)), len(sel)


def vanilla_grip_bottom(ref, shape_name, depth=3.0):
    for blk in ref.blocks:
        if type(blk).__name__ in ("NiTriStrips", "NiTriShape") and blk.name == shape_name.encode():
            return grip_bottom_centroid([(v.x, v.y, v.z) for v in blk.data.vertices], depth)
    raise SystemExit(f"vanilla grip shape {shape_name} not found")


def add_geometry(root, name, tris, tex, matprop, pp):
    vmap, verts, idx = {}, [], []
    for vs in tris:
        f = []
        for p, n, uv in vs:
            k = (tuple(round(c, 5) for c in p), tuple(round(c, 5) for c in n), tuple(round(c, 6) for c in uv))
            if k not in vmap:
                vmap[k] = len(verts); verts.append(k)
            f.append(vmap[k])
        idx.append(f)
    sh = NifFormat.NiTriShape(); sh.name = name.encode(); sh.flags = 14
    sh.rotation.set_identity(); sh.scale = 1.0
    d = NifFormat.NiTriShapeData()
    d.num_vertices = len(verts); d.has_vertices = True; d.vertices.update_size()
    d.has_normals = True; d.normals.update_size(); d.num_uv_sets = 1; d.uv_sets.update_size()
    for i, (p, n, uv) in enumerate(verts):
        d.vertices[i].x, d.vertices[i].y, d.vertices[i].z = p
        d.normals[i].x, d.normals[i].y, d.normals[i].z = n
        d.uv_sets[0][i].u, d.uv_sets[0][i].v = uv
    d.has_vertex_colors = False; d.consistency_flags = 0x4000
    lo, hi = bounds([v[0] for v in verts]); c = tuple((lo[i] + hi[i]) / 2 for i in range(3))
    d.center.x, d.center.y, d.center.z = c
    d.radius = max(math.dist(v[0], c) for v in verts)
    d.num_triangles = len(idx); d.num_triangle_points = 3 * len(idx); d.has_triangles = True
    d.triangles.update_size()
    for i, (a, b, cc) in enumerate(idx):
        d.triangles[i].v_1, d.triangles[i].v_2, d.triangles[i].v_3 = a, b, cc
    sh.data = d
    m = NifFormat.NiMaterialProperty(); copy_fields(m, matprop[0], MAT_FIELDS)
    if matprop[1] is not None:  # explicit emissive override
        m.emissive_color.r, m.emissive_color.g, m.emissive_color.b = matprop[1][:3]; m.emit_multi = matprop[1][3]
    p = NifFormat.BSShaderPPLightingProperty(); copy_fields(p, pp, PP_FIELDS)
    ts = NifFormat.BSShaderTextureSet(); ts.num_textures = 6; ts.textures.update_size()
    for i, t in enumerate(tex):
        ts.textures[i] = t.encode()
    p.texture_set = ts
    sh.add_property(m); sh.add_property(p)
    sh.update_tangent_space()
    root.add_child(sh)
    return len(verts), len(idx)


def build(variant, tris_fnv, tex_for, refs, muzzle, collision, bsx, out):
    root = NifFormat.BSFadeNode(); root.name = variant["nif_name"].encode(); root.flags = 14
    root.rotation.set_identity(); root.scale = 1.0
    x = NifFormat.BSXFlags(); x.name = b"BSX"; x.integer_data = bsx; root.add_extra_data(x)
    prn = NifFormat.NiStringExtraData(); prn.name = b"Prn"; prn.string_data = b"Weapon"; root.add_extra_data(prn)
    stats = {}
    for mat in sorted({m for m, _ in tris_fnv}):
        tx, matprop, pp = tex_for[mat]
        stats[mat] = add_geometry(root, f"{variant['nif_name']}:{mat}", [vs for m, vs in tris_fnv if m == mat], tx, matprop, pp)
    pn = NifFormat.NiNode(); pn.name = b"ProjectileNode"; pn.flags = 14; pn.rotation.set_identity(); pn.scale = 1.0
    pn.translation.x, pn.translation.y, pn.translation.z = muzzle
    root.add_child(pn)
    if collision:
        pieces, hav_mat, ref_body, mass = collision
        lst = NifFormat.bhkListShape(); lst.material.material = hav_mat
        lst.num_sub_shapes = len(pieces); lst.sub_shapes.update_size()
        for i, (pv, planes) in enumerate(pieces):
            c = NifFormat.bhkConvexVerticesShape(); c.material.material = hav_mat; c.radius = 0.1
            c.num_vertices = len(pv); c.vertices.update_size()
            for j, v in enumerate(pv):
                c.vertices[j].x, c.vertices[j].y, c.vertices[j].z = (k / HAVOK_SCALE for k in v); c.vertices[j].w = 0.0
            c.num_normals = len(planes); c.normals.update_size()
            for j, (n, dd) in enumerate(planes):
                c.normals[j].x, c.normals[j].y, c.normals[j].z = n; c.normals[j].w = -dd / HAVOK_SCALE
            lst.sub_shapes[i] = c
        body = type(ref_body)()
        names = [a.name for a in ref_body._get_attribute_list() if a.name not in
                 ("shape", "translation", "rotation", "linear_velocity", "angular_velocity", "inertia", "center",
                  "num_constraints", "constraints")]
        copy_fields(body, ref_body, names)
        body.rotation.w = 1.0
        body.shape = lst
        try:
            body.update_mass_center_inertia(mass=mass, solid=True)
            stats["mass_inertia"] = "computed by pyffi"
        except Exception as e:  # fall back to vanilla template values
            copy_fields(body, ref_body, ["mass", "inertia", "center"])
            stats["mass_inertia"] = f"vanilla template ({type(e).__name__})"
        co = NifFormat.bhkCollisionObject(); co.flags = 1; co.target = root; co.body = body
        root.collision_object = co
    data = NifFormat.Data(version=NIF_V, user_version=NIF_UV, user_version_2=NIF_UV2)
    data.roots = [root]; data.header.endian_type = 1
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "wb") as f:
        data.write(f)
    chk = NifFormat.Data()
    with open(out, "rb") as f:
        chk.read(f)
    if [type(b).__name__ for b in chk.blocks] != [type(b).__name__ for b in data.blocks]:
        raise SystemExit("NIF read-back mismatch")
    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job"); ap.add_argument("--root", required=True)
    ap.add_argument("--fnv-data", required=True); ap.add_argument("--stage", required=True)
    a = ap.parse_args()
    job = json.loads(Path(a.job).read_text(encoding="utf-8-sig"))
    root, stage = Path(a.root), Path(a.stage)
    S = job["scale"]
    rep = {"tool": TOOL_VERSION, "job": job["job"], "inputs": {}, "outputs": {}, "checks": {}}
    for k, spec in job["inputs"].items():
        h = sha256(root / spec["path"])
        rep["inputs"][k] = {"path": spec["path"], "sha256": h, "match": h == spec["sha256"].upper()}
        if h != spec["sha256"].upper():
            raise SystemExit(f"HASH MISMATCH {k}")
    P = lambda k: root / job["inputs"][k]["path"]

    # world model in hand frame -> FNV axes
    w_tris, W = hand_space(P("w_ref_smd"), job["world"]["hand_bone"])
    w_fnv0 = [(m, [(hand_to_fnv(p, S), hand_to_fnv(n, 1.0), uv) for p, n, uv in vs]) for m, vs in w_tris]

    # grip registration to vanilla 10mm (translation only)
    ref_grip = load_ref(a.fnv_data, *job["grip_reference"]["nif"])
    g10, n10 = vanilla_grip_bottom(ref_grip, job["grip_reference"]["shape"])
    handle_pts = [p for m, vs in w_fnv0 if m == job["world"]["handle_material"] for p, _, _ in vs]
    gtg, ntg = grip_bottom_centroid(handle_pts)
    off = tuple(g10[i] - gtg[i] for i in range(3))
    rep["grip"] = {"vanilla_10mm_grip_bottom": g10, "toolgun_grip_bottom_before": gtg, "offset_fnv": off,
                   "samples": [n10, ntg]}
    shift = lambda p: (p[0] + off[0], p[1] + off[1], p[2] + off[2])
    w_fnv = [(m, [(shift(p), n, (uv[0], 1.0 - uv[1])) for p, n, uv in vs]) for m, vs in w_fnv0]
    mz = to_local(W[job["world"]["hand_bone"]], W[job["world"]["muzzle_bone"]][1])
    muzzle = shift(hand_to_fnv(mz, S))

    # view model registered onto world model
    c_tris, _ = hand_space(P("c_ref_smd"), job["view"]["bone"])
    cu = sorted({tuple(round(x, 4) for x in p) for _, vs in c_tris for p, _, _ in vs})
    wu = sorted({tuple(round(x, 4) for x in p) for _, vs in w_tris for p, _, _ in vs})
    R0 = job["view"]["init_rotation_to_world"]; s0 = job["view"]["init_scale"]
    cc = tuple(sum(p[i] for p in cu) / len(cu) for i in range(3)); wc = tuple(sum(p[i] for p in wu) / len(wu) for i in range(3))
    rc = sim_apply(s0, R0, (0, 0, 0), cc)
    s, R, t, st = icp(cu, wu, (s0, R0, tuple(wc[i] - rc[i] for i in range(3))))
    rep["view_registration"] = {"scale": s, "R": R, "t": t, **st}
    if st["within_0.01"] < 0.99:
        raise SystemExit(f"view model does not register onto world model ({st})")
    rot = lambda n: tuple(sum(R[i][k] * n[k] for k in range(3)) for i in range(3))
    c_fnv = [(m, [(shift(hand_to_fnv(sim_apply(s, R, t, p), S)), hand_to_fnv(rot(n), 1.0), (uv[0], 1.0 - uv[1]))
                  for p, n, uv in vs]) for m, vs in c_tris]

    # textures and shader assignment
    work = stage / "_work"; vtfcmd = root / job["vtfcmd"]
    trel = Path(job["output"]["texture_dir"]); wp = lambda r: str(r).replace("/", "\\")
    flat = Image.new("RGBA", (64, 64), (128, 128, 255, 0))
    nrel = trel / "toolgun_flat_n.dds"; (stage / nrel).parent.mkdir(parents=True, exist_ok=True)
    rep["outputs"]["flat_normal"] = {"path": nrel.as_posix(), **write_dds(flat, stage / nrel), "sha256": None}
    rep["outputs"]["flat_normal"]["sha256"] = sha256(stage / nrel)
    t_10mm = load_ref(a.fnv_data, *job["templates"]["metal"]); t_glow = load_ref(a.fnv_data, *job["templates"]["glow"])
    t_flat = load_ref(a.fnv_data, *job["templates"]["glow_no_env"])
    pp_metal = first(t_10mm, "BSShaderPPLightingProperty", lambda b: int(b.shader_flags) == 0x82000181)
    pp_glow = first(t_glow, "BSShaderPPLightingProperty", lambda b: int(b.shader_flags) == 0x82000081)
    pp_flat = first(t_flat, "BSShaderPPLightingProperty", lambda b: int(b.shader_flags) == 0x82000001)
    mat_metal = first(t_10mm, "NiMaterialProperty")
    tex_for = {}
    for mat, spec in job["materials"].items():
        vmt = parse_vmt_full(P(spec["vmt"]))
        base = vtf_rgba(P(spec["base"]), work, vtfcmd)
        rec = {"vmt": vmt}
        bpath = trel / f"{mat}.dds"
        write_dds(Image.merge("RGBA", (*base.split()[:3], Image.new("L", base.size, 255))), stage / bpath)
        slots = [wp(bpath), wp(nrel), "", "", "", ""]
        if vmt.get("selfillum") == "1" or vmt["shader"].lower() == "unlitgeneric":
            r, g, b, al = base.split()
            if vmt["shader"].lower() == "unlitgeneric":
                al = Image.new("L", base.size, 255)
            glow = Image.merge("RGBA", (Image.composite(r, Image.new("L", base.size, 0), al),
                                        Image.composite(g, Image.new("L", base.size, 0), al),
                                        Image.composite(b, Image.new("L", base.size, 0), al), Image.new("L", base.size, 255)))
            gpath = trel / f"{mat}_g.dds"; write_dds(glow, stage / gpath); slots[2] = wp(gpath)
            rec["glow"] = gpath.as_posix()
        if "envmapmask" in spec:
            tint = [float(x) for x in vmt.get("envmaptint", "[1 1 1]").strip("[]").split()]
            k = sum(tint) / 3.0
            mimg = vtf_rgba(P(spec["envmapmask"]), work, vtfcmd).convert("L").point(lambda v: int(round(v * k)))
            mpath = trel / f"{mat}_m.dds"; write_dds(mimg.convert("RGBA"), stage / mpath)
            slots[4], slots[5] = job["cubemap"], wp(mpath)
            rec["envmask"] = {"path": mpath.as_posix(), "tint_scale": k}
        if slots[2] and slots[4]:
            pp, mp = pp_glow, (mat_metal, (1.0, 1.0, 1.0, 1.0))
        elif slots[2]:
            pp, mp = pp_flat, (mat_metal, (1.0, 1.0, 1.0, 1.0))
        else:
            pp, mp = pp_metal, (mat_metal, None)
        tex_for[mat] = (slots, mp, pp)
        rec["slots"] = slots; rec["shader_flags"] = hex(int(pp.shader_flags))
        rep.setdefault("materials", {})[mat] = rec
    for f in sorted((stage / trel).glob("*.dds")):
        rep["outputs"][f"tex:{f.name}"] = {"path": (trel / f.name).as_posix(), "sha256": sha256(f)}

    # collision for world model from the original physics SMD
    phy_tris, _ = hand_space(P("w_phy_smd"), job["world"]["hand_bone"])
    phy = [(m, [(shift(hand_to_fnv(p, S)), n, uv) for p, n, uv in vs]) for m, vs in phy_tris]
    pieces = []
    for pt in split_convex_pieces(phy):
        pv, planes, worst = convex_planes(pt, eps=0.01 * S)
        pieces.append((pv, planes, worst))
    rep["collision"] = {"pieces": len(pieces), "max_convexity_violation": max(w for *_, w in pieces)}
    if rep["collision"]["max_convexity_violation"] > 0.05 * S:
        raise SystemExit("physics piece not convex")
    e = NifFormat.Fallout3HavokMaterial
    hav = dict(zip(e._enumkeys, e._enumvalues))[job["world"]["havok_material"]]
    ref_body = next(b for b in t_10mm.blocks if type(b).__name__ in ("bhkRigidBody", "bhkRigidBodyT"))
    coll = ([(pv, pl) for pv, pl, _ in pieces], hav, ref_body, job["world"]["mass"])

    for key, tris, col, bsx in (("world", w_fnv, coll, job["world"]["bsx"]), ("view", c_fnv, None, job["view"]["bsx"])):
        v = job[key]; out = stage / v["output"]
        st2 = build(v, tris, tex_for, None, muzzle, col, bsx, out)
        lo, hi = bounds([p for _, vs in tris for p, _, _ in vs])
        rep["outputs"][key] = {"path": v["output"], "sha256": sha256(out), "bytes": out.stat().st_size,
                               "bounds": [lo, hi], "shapes": st2}
    rep["muzzle_fnv"] = muzzle
    (stage / "o01_conversion_report.json").write_text(json.dumps(rep, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("grip", "muzzle_fnv", "collision")}, indent=1, default=str))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "shapes"} for k, v in rep["outputs"].items() if k in ("world", "view")}, indent=1))
    print("view registration:", {k: rep["view_registration"][k] for k in ("scale", "median", "within_0.01")})


if __name__ == "__main__":
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit(subprocess.run([sys.executable, *sys.argv], env=dict(os.environ, PYTHONHASHSEED="0")).returncode)
    main()
