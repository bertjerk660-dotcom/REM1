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

TOOL_VERSION = "source_to_fnv/convert_source_weapon 1.2.0"
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


def nif_points(ref):
    """All geometry vertices of a NIF in root space (node chains applied)."""
    out = []

    def walk(n, R, t, s):
        if n is None:
            return
        r = n.rotation
        Rn = [[r.m_11, r.m_12, r.m_13], [r.m_21, r.m_22, r.m_23], [r.m_31, r.m_32, r.m_33]]
        tn = (n.translation.x, n.translation.y, n.translation.z)
        wt = tuple(t[i] + s * sum(tn[j] * R[j][i] for j in range(3)) for i in range(3))
        wR = [[sum(Rn[i][k] * R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        ws = s * n.scale
        if type(n).__name__ in ("NiTriStrips", "NiTriShape") and n.data and n.data.num_vertices:
            for v in n.data.vertices:
                out.append(tuple(wt[i] + ws * (v.x * wR[0][i] + v.y * wR[1][i] + v.z * wR[2][i]) for i in range(3)))
        for c in getattr(n, "children", []) or []:
            walk(c, wR, wt, ws)
    walk(ref.roots[0], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], (0.0, 0.0, 0.0), 1.0)
    return out


def shaft_centre(pts, band=2.0, min_pts=8):
    """Centre of a melee shaft cross-section at hand height (|y| < band). The band widens
    until it holds enough vertices (sparse cylinders have rings far apart)."""
    while True:
        sel = [p for p in pts if abs(p[1]) < band]
        if len(sel) >= min_pts or band > 64:
            break
        band *= 2
    if not sel:
        raise SystemExit("no shaft vertices near hand height")
    return tuple(sum(p[i] for p in sel) / len(sel) for i in range(3)), {"n": len(sel), "band": band}


def qc_attachment(qc_path, name):
    import re
    t = Path(qc_path).read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'\$attachment\s+"%s"\s+"([^"]+)"\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)' % re.escape(name), t)
    return (m.group(1), (float(m.group(2)), float(m.group(3)), float(m.group(4)))) if m else None


def pca_axes(pts):
    """Principal axes (columns, largest variance first) via Jacobi on the 3x3 covariance."""
    n = len(pts); c = [sum(p[i] for p in pts) / n for i in range(3)]
    A = [[sum((p[i] - c[i]) * (p[j] - c[j]) for p in pts) / n for j in range(3)] for i in range(3)]
    V = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(50):
        p, q = max(((0, 1), (0, 2), (1, 2)), key=lambda ij: abs(A[ij[0]][ij[1]]))
        if abs(A[p][q]) < 1e-12:
            break
        th = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
        cs, sn = math.cos(th), math.sin(th)
        for k in range(3):
            akp, akq = A[k][p], A[k][q]
            A[k][p], A[k][q] = cs * akp - sn * akq, sn * akp + cs * akq
        for k in range(3):
            apk, aqk = A[p][k], A[q][k]
            A[p][k], A[q][k] = cs * apk - sn * aqk, sn * apk + cs * aqk
        for k in range(3):
            vkp, vkq = V[k][p], V[k][q]
            V[k][p], V[k][q] = cs * vkp - sn * vkq, sn * vkp + cs * vkq
    order = sorted(range(3), key=lambda i: -A[i][i])
    return [[V[r][i] for i in order] for r in range(3)], c, [A[i][i] for i in order]


def pca_inits(src, dst):
    """Candidate similarity starts aligning principal axes (4 proper sign choices)."""
    Es, cs, vs = pca_axes(src); Ed, cd, vd = pca_axes(dst)
    s0 = math.sqrt(vd[0] / vs[0])
    inits = []
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        D = [[Ed[r][0] * sx, Ed[r][1] * sy, 0] for r in range(3)]
        cr = [D[1][0] * D[2][1] - D[2][0] * D[1][1], D[2][0] * D[0][1] - D[0][0] * D[2][1], D[0][0] * D[1][1] - D[1][0] * D[0][1]]
        for r in range(3):
            D[r][2] = cr[r]
        S = [[Es[r][0], Es[r][1], 0] for r in range(3)]
        cs2 = [S[1][0] * S[2][1] - S[2][0] * S[1][1], S[2][0] * S[0][1] - S[0][0] * S[2][1], S[0][0] * S[1][1] - S[1][0] * S[0][1]]
        for r in range(3):
            S[r][2] = cs2[r]
        R = [[sum(D[i][k] * S[j][k] for k in range(3)) for j in range(3)] for i in range(3)]  # D * S^T
        rc = sim_apply(s0, R, (0, 0, 0), cs)
        inits.append((s0, R, tuple(cd[i] - rc[i] for i in range(3))))
    return inits


def add_geometry(root, name, tris, tex, matprop, pp, extras=None):
    extras = extras or {}
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
    if extras.get("glossiness") is not None:  # Source $phongexponent (only with a bumpmap)
        m.glossiness = float(extras["glossiness"])
    sh.add_property(m); sh.add_property(p)
    if extras.get("alpha_flags") is not None:  # e.g. Source $additive -> ONE/ONE blending
        al = NifFormat.NiAlphaProperty(); al.flags = extras["alpha_flags"]; al.threshold = 0
        sh.add_property(al)
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
        tx, matprop, pp = tex_for[mat][:3]
        extras = tex_for[mat][3] if len(tex_for[mat]) > 3 else None
        stats[mat] = add_geometry(root, f"{variant['nif_name']}:{mat}", [vs for m, vs in tris_fnv if m == mat], tx, matprop, pp, extras)
    if muzzle is not None:  # melee weapons have no muzzle
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

    # grip registration to the vanilla donor (translation only)
    gr = job["grip_reference"]
    ref_grip = load_ref(a.fnv_data, *gr["nif"])
    mode = gr.get("mode", "bottom")
    handle_mat = job["world"].get("handle_material")
    w_pts = [p for m, vs in w_fnv0 if handle_mat in (None, m) for p, _, _ in vs]
    if mode == "bottom":
        # Optional x-windows keep the search on the grip: FNV weapon origins sit at the hand, so
        # the donor grip lies near x=0; the Source grip lies just ahead of the R_Hand origin.
        # Without them a magazine hanging lower than the grip can be picked (O08c finding).
        win = gr.get("window")
        dwin = (lambda p: win["donor_x"][0] <= p[0] <= win["donor_x"][1]) if win else (lambda p: True)
        swin = (lambda p: win["source_x"][0] <= p[0] <= win["source_x"][1]) if win else (lambda p: True)
        if gr.get("shape", "*") == "*":
            g10, n10 = grip_bottom_centroid([p for p in nif_points(ref_grip) if dwin(p)])
        else:
            g10, n10 = vanilla_grip_bottom(ref_grip, gr["shape"])
        gtg, ntg = grip_bottom_centroid([p for p in w_pts if swin(p)])
        off = tuple(g10[i] - gtg[i] for i in range(3))
    elif mode == "shaft":  # melee: centre the shaft on the donor shaft at hand height; keep grip position along shaft
        g10, n10 = shaft_centre(nif_points(ref_grip))
        gtg, ntg = shaft_centre(w_pts)
        off = (g10[0] - gtg[0], 0.0, g10[2] - gtg[2])
    else:
        raise SystemExit(f"unknown grip mode {mode}")
    rep["grip"] = {"mode": mode, "vanilla_10mm_grip_bottom" if mode == "bottom" else "donor_reference": g10,
                   "toolgun_grip_bottom_before" if mode == "bottom" else "source_reference_before": gtg,
                   "offset_fnv": off, "samples": [n10, ntg]}
    shift = lambda p: (p[0] + off[0], p[1] + off[1], p[2] + off[2])
    w_fnv = [(m, [(shift(p), n, (uv[0], 1.0 - uv[1])) for p, n, uv in vs]) for m, vs in w_fnv0]
    hb = job["world"]["hand_bone"]
    if job["world"].get("muzzle_bone"):
        mz = to_local(W[hb], W[job["world"]["muzzle_bone"]][1])
        muzzle = shift(hand_to_fnv(mz, S))
    elif job["world"].get("muzzle_attachment"):
        att = qc_attachment(P(job["world"]["muzzle_attachment"]["qc"]), job["world"]["muzzle_attachment"]["name"])
        bR, bt = W[att[0]]
        world_pt = tuple(bt[i] + mv(bR, att[1])[i] for i in range(3))
        muzzle = shift(hand_to_fnv(to_local(W[hb], world_pt), S))
        rep["muzzle_attachment"] = {"bone": att[0], "offset": att[1]}
    else:
        muzzle = None

    # view model: same hand frame (c_ rigs that hold the gun in R_Hand) or registered onto the world model
    vmode = job["view"].get("mode", "icp_to_world")
    c_tris, _ = hand_space(P("c_ref_smd"), job["view"]["bone"])
    if vmode == "same_hand_frame":
        rep["view_registration"] = {"mode": vmode, "bone": job["view"]["bone"]}
        c_fnv = [(m, [(shift(hand_to_fnv(p, S)), hand_to_fnv(n, 1.0), (uv[0], 1.0 - uv[1])) for p, n, uv in vs])
                 for m, vs in c_tris]
    else:
        cu = sorted({tuple(round(x, 4) for x in p) for _, vs in c_tris for p, _, _ in vs})
        wu = sorted({tuple(round(x, 4) for x in p) for _, vs in w_tris for p, _, _ in vs})
        if "init_rotation_to_world" in job["view"]:
            R0 = job["view"]["init_rotation_to_world"]; s0 = job["view"]["init_scale"]
            cc = tuple(sum(p[i] for p in cu) / len(cu) for i in range(3)); wc = tuple(sum(p[i] for p in wu) / len(wu) for i in range(3))
            rc = sim_apply(s0, R0, (0, 0, 0), cc)
            inits = [(s0, R0, tuple(wc[i] - rc[i] for i in range(3)))]
        else:
            # identity start (c_ rigs already in the R_Hand frame) plus principal-axis starts
            inits = [(1.0, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], (0.0, 0.0, 0.0))] + pca_inits(cu, wu)
        sfix = job["view"].get("fixed_scale")
        lo_s, hi_s = job["view"].get("scale_range", [0.0, 1e9])
        if sfix is not None:
            inits = [(sfix, R_, t_) for _s, R_, t_ in inits]
        best = None
        for init in inits:
            res = icp(cu, wu, init, s_fixed=sfix, cell=job["view"].get("icp_cell", 0.5))
            if not (lo_s <= res[0] <= hi_s):  # reject degenerate fits (e.g. shrinking onto one part)
                continue
            if best is None or res[3]["median"] < best[3]["median"]:
                best = res
        if best is None:
            raise SystemExit("no view-model registration within the allowed scale range")
        s, R, t, st = best
        rep["view_registration"] = {"mode": vmode, "scale": s, "R": R, "t": t, "starts_tried": len(inits), **st}
        need = job["view"].get("min_within_0.01", 0.99)
        max_med = job["view"].get("max_median")
        if (max_med is None and st["within_0.01"] < need) or (max_med is not None and st["median"] > max_med):
            raise SystemExit(f"view model does not register onto world model ({st})")
        rot = lambda n: tuple(sum(R[i][k] * n[k] for k in range(3)) for i in range(3))
        c_fnv = [(m, [(shift(hand_to_fnv(sim_apply(s, R, t, p), S)), hand_to_fnv(rot(n), 1.0), (uv[0], 1.0 - uv[1]))
                      for p, n, uv in vs]) for m, vs in c_tris]

    # textures and shader assignment
    work = stage / "_work"; vtfcmd = root / job["vtfcmd"]
    trel = Path(job["output"]["texture_dir"]); wp = lambda r: str(r).replace("/", "\\")
    flat = Image.new("RGBA", (64, 64), (128, 128, 255, 0))
    nrel = trel / job.get("flat_normal", "toolgun_flat_n.dds"); (stage / nrel).parent.mkdir(parents=True, exist_ok=True)
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
        extras = {}
        bump = None
        if "bump" in spec:
            # Source tangent-space normal map; its alpha is the phong mask (FNV reads normal alpha as
            # the specular mask) unless $normalmapalphaenvmapmask redirects it to the env mask.
            bump = vtf_rgba(P(spec["bump"]), work, vtfcmd)
            r_, g_, b_, a_ = bump.split()
            phong = vmt.get("phong") == "1"
            spec_a = a_ if phong and vmt.get("normalmapalphaenvmapmask") != "1" else \
                (a_ if phong else Image.new("L", bump.size, 0))
            npath = trel / f"{mat}_n.dds"
            write_dds(Image.merge("RGBA", (r_, g_, b_, spec_a)), stage / npath)
            slots[1] = wp(npath)
            rec["normal"] = {"path": npath.as_posix(), "spec_from_alpha": phong}
            if phong and vmt.get("phongexponent"):
                extras["glossiness"] = float(vmt["phongexponent"])
        tint = [float(x) for x in vmt.get("envmaptint", "[1 1 1]").strip("[]").split()]
        k = sum(tint) / 3.0
        if "envmapmask" in spec:
            mimg = vtf_rgba(P(spec["envmapmask"]), work, vtfcmd).convert("L").point(lambda v: int(round(v * k)))
            mpath = trel / f"{mat}_m.dds"; write_dds(mimg.convert("RGBA"), stage / mpath)
            slots[4], slots[5] = job["cubemap"], wp(mpath)
            rec["envmask"] = {"path": mpath.as_posix(), "tint_scale": k}
        elif bump is not None and vmt.get("normalmapalphaenvmapmask") == "1" and vmt.get("envmap"):
            mimg = bump.split()[3].point(lambda v: int(round(v * k)))
            mpath = trel / f"{mat}_m.dds"; write_dds(mimg.convert("RGBA"), stage / mpath)
            slots[4], slots[5] = job["cubemap"], wp(mpath)
            rec["envmask"] = {"path": mpath.as_posix(), "tint_scale": k, "from": "normal alpha"}
        if vmt.get("additive") == "1":
            extras["alpha_flags"] = 1  # blend on, src ONE, dst ONE
            rec["additive"] = True
        if slots[2] and slots[4]:
            pp, mp = pp_glow, (mat_metal, (1.0, 1.0, 1.0, 1.0))
        elif slots[2]:
            pp, mp = pp_flat, (mat_metal, (1.0, 1.0, 1.0, 1.0))
        elif slots[4]:
            pp, mp = pp_metal, (mat_metal, None)
        else:
            pp, mp = pp_flat, (mat_metal, None)  # no env, no glow: PP lighting without env mapping
        tex_for[mat] = (slots, mp, pp, extras) if extras else (slots, mp, pp)
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
    (stage / job.get("report_name", "o01_conversion_report.json")).write_text(json.dumps(rep, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: rep[k] for k in ("grip", "muzzle_fnv", "collision")}, indent=1, default=str))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "shapes"} for k, v in rep["outputs"].items() if k in ("world", "view")}, indent=1))
    print("view registration:", {k: v for k, v in rep["view_registration"].items() if k in ("mode", "scale", "median", "within_0.01", "p95")})


if __name__ == "__main__":
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit(subprocess.run([sys.executable, *sys.argv], env=dict(os.environ, PYTHONHASHSEED="0")).returncode)
    main()
