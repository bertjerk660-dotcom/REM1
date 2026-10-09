"""Source Engine static prop -> Fallout: New Vegas NIF converter (O00 pipeline).

Reproducible, job-file driven. Reads original decompiled SMD/QC and VTF/VMT
inputs, verifies their hashes, and writes ONLY into a staging directory.

Conversion rules (see research/source_to_fnv/README.md for justification):
  * Scale: 1 Source unit (1 inch) -> 1.7778 FNV units (FNV unit = 1.428 cm).
  * Axes: Source +X forward -> FNV +Y forward (90 deg about +Z); Z stays up.
  * Origin: moved to the visual base (min Z = 0) so placement does not sink.
  * UV: SMD V is bottom-up; NIF V is top-down -> v' = 1 - v.
  * Collision: each Source convex solid becomes one bhkConvexVerticesShape
    (no single-hull fallback). Havok units = NIF units / 7.
  * Havok material: from $surfaceprop via an explicit table; unknown -> error.
  * Rigid body / shader flags are copied from vanilla reference NIFs.

Usage:
  python convert_source_static.py <job.json> --root <workspace> --fnv-data <FNV Data dir> --stage <staging dir>
"""
import argparse, hashlib, io, json, math, re, subprocess, sys, time
from pathlib import Path

if not hasattr(time, "clock"):  # pyffi 2.2.3 predates Python 3.8
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from bsa_read import BSA
from dds_write import write_dds

TOOL_VERSION = "source_to_fnv/convert_source_static 1.0.0"
NIF_V, NIF_UV, NIF_UV2 = 0x14020007, 11, 34
HAVOK_SCALE = 7.0

# Source surfaceprop -> Fallout3HavokMaterial. Deliberately explicit: no default.
SURFACEPROP_TO_FO_HAVOK = {
    "wood": "MAT_WOOD", "wood_furniture": "MAT_WOOD", "wood_crate": "MAT_WOOD",
    "wood_plank": "MAT_WOOD", "wood_panel": "MAT_WOOD", "wood_box": "MAT_WOOD",
    "wood_solid": "MAT_HEAVY_WOOD", "wood_lowdensity": "MAT_WOOD",
    "metal": "MAT_METAL", "metal_box": "MAT_METAL", "metalpanel": "MAT_SHEET_METAL",
    "metalvent": "MAT_HOLLOW_METAL", "metal_barrel": "MAT_HOLLOW_METAL",
    "solidmetal": "MAT_HEAVY_METAL", "chainlink": "MAT_CHAIN", "chain": "MAT_CHAIN",
    "concrete": "MAT_STONE", "concrete_block": "MAT_STONE", "rock": "MAT_STONE",
    "brick": "MAT_STONE", "glass": "MAT_GLASS", "dirt": "MAT_DIRT", "sand": "MAT_SAND",
    "grass": "MAT_GRASS", "cloth": "MAT_CLOTH", "carpet": "MAT_CLOTH", "flesh": "MAT_ORGANIC",
}


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()


# ---------------------------------------------------------------- source parsing
def parse_smd(path):
    lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip().lower() == "triangles") + 1
    tris = []
    while i < len(lines) and lines[i].strip().lower() != "end":
        mat = lines[i].strip()
        vs = []
        for j in range(1, 4):
            t = lines[i + j].split()
            vs.append(((float(t[1]), float(t[2]), float(t[3])),
                       (float(t[4]), float(t[5]), float(t[6])),
                       (float(t[7]), float(t[8]))))
        tris.append((mat, vs))
        i += 4
    return tris


def parse_qc(path):
    t = Path(path).read_text(encoding="utf-8", errors="ignore")
    g = lambda pat: (re.search(pat, t, re.I) or [None, None])[1]
    return {
        "staticprop": bool(re.search(r"^\s*\$staticprop", t, re.I | re.M)),
        "surfaceprop": (g(r'\$surfaceprop\s+"([^"]+)"') or "").lower(),
        "bbox": [float(x) for x in (g(r"\$bbox\s+([-\d.\s]+)") or "").split()[:6]],
        "concave": bool(re.search(r"\$concave", t, re.I)),
        "maxconvexpieces": int(g(r"\$maxconvexpieces\s+(\d+)") or 0),
        "mass": float(g(r"\$mass\s+([\d.]+)") or 0),
    }


def parse_vmt(path):
    t = Path(path).read_text(encoding="utf-8", errors="ignore")
    t = "\n".join(l.split("//")[0] for l in t.splitlines())  # drop comments
    kv = dict((k.lower(), v) for k, v in re.findall(r'"?\$(\w+)"?\s+"([^"]*)"', t))
    shader = (re.match(r'\s*"?(\w+)"?', t) or [None, ""])[1]
    return {"shader": shader, **kv}


# ---------------------------------------------------------------- geometry
def smd_to_model(v):
    """Crowbar decompiled static-prop SMD frame -> compiled Source model frame.

    studiomdl rotates $staticprop geometry 90 deg about +Z when compiling, so the
    decompiled SMD is in the pre-rotation frame. Verified per asset against the
    hull stored in the .mdl header (see check_model_frame)."""
    x, y, z = v
    return (-y, x, z)


def model_to_fnv(v):
    """Source model frame (x fwd, y left, z up) -> FNV (x right, y fwd, z up)."""
    x, y, z = v
    return (-y, x, z)


def make_xform(scale, z_shift):
    def p(v):
        x, y, z = model_to_fnv(smd_to_model(v))
        return (x * scale, y * scale, z * scale + z_shift)

    def n(v):
        return model_to_fnv(smd_to_model(v))
    return p, n


def mdl_hull(mdl_path):
    import struct
    b = Path(mdl_path).read_bytes()
    return list(struct.unpack_from("<3f", b, 0x68)), list(struct.unpack_from("<3f", b, 0x74))


def check_model_frame(phy_tris, hull, tol=0.6):
    """Physics SMD mapped into the model frame must match the compiled hull
    (studiomdl pads the hull by a small, even margin)."""
    lo, hi = bounds([smd_to_model(v[0]) for _m, vs in phy_tris for v in vs])
    err = max(max(abs(lo[i] - hull[0][i]), abs(hi[i] - hull[1][i])) for i in range(3))
    return err, lo, hi


def bounds(pts):
    return [min(q[i] for q in pts) for i in range(3)], [max(q[i] for q in pts) for i in range(3)]


def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    l = math.sqrt(dot(a, a))
    return (a[0] / l, a[1] / l, a[2] / l) if l > 1e-12 else None


def split_convex_pieces(tris):
    """Group physics triangles into connected solids (one per Source convex piece)."""
    key = lambda v: (round(v[0], 3), round(v[1], 3), round(v[2], 3))
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for _m, vs in tris:
        ks = [key(v[0]) for v in vs]
        for k in ks[1:]:
            parent[find(k)] = find(ks[0])
    groups = {}
    for _m, vs in tris:
        groups.setdefault(find(key(vs[0][0])), []).append([v[0] for v in vs])
    return [groups[k] for k in sorted(groups, key=lambda k: k)]


def convex_planes(piece_tris, eps):
    verts = sorted({tuple(round(c, 5) for c in v) for t in piece_tris for v in t})
    cen = tuple(sum(v[i] for v in verts) / len(verts) for i in range(3))
    planes = []
    for a, b, c in piece_tris:
        nrm = norm(cross(sub(b, a), sub(c, a)))
        if nrm is None:
            continue
        d = dot(nrm, a)
        if dot(nrm, cen) - d > 0:  # make outward
            nrm, d = (-nrm[0], -nrm[1], -nrm[2]), -d
        if not any(dot(nrm, q[0]) > 0.9999 and abs(d - q[1]) < eps for q in planes):
            planes.append((nrm, d))
    worst = max(dot(n_, v) - d_ for n_, d_ in planes for v in verts)
    return verts, planes, worst


# ---------------------------------------------------------------- textures
def vtf_to_image(vtf, work, vtfcmd):
    work.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(vtfcmd), "-file", str(vtf), "-output", str(work), "-exportformat", "tga", "-silent"],
                   capture_output=True, text=True, timeout=60)
    tga = work / (Path(vtf).stem + ".tga")
    if not tga.exists():
        raise RuntimeError(f"VTFCmd failed to decode {vtf}")
    return Image.open(tga).convert("RGB")


# ---------------------------------------------------------------- NIF assembly
def load_ref(fnv_data, bsa_name, internal):
    d = NifFormat.Data()
    d.read(io.BytesIO(BSA(Path(fnv_data) / bsa_name).read(internal)))
    return d


def first(data, tname, pred=lambda b: True):
    return next(b for b in data.blocks if type(b).__name__ == tname and pred(b))


def copy_fields(dst, src, names):
    """Copy named fields from a vanilla reference block (recursing into structs)."""
    for n in names:
        s, d = getattr(src, n), getattr(dst, n)
        if hasattr(s, "_get_attribute_list"):
            copy_fields(d, s, [a.name for a in s._get_attribute_list()])
        elif isinstance(s, list):  # fixed-size pyffi arrays
            for i, x in enumerate(s):
                d[i] = x
        else:
            setattr(dst, n, s)


# Fields copied from vanilla NIFs (everything else is derived from the source asset).
PP_FIELDS = ["shader_type", "shader_flags", "shader_flags_2", "environment_map_scale", "texture_clamp_mode"]
MAT_FIELDS = ["specular_color", "emissive_color", "glossiness", "alpha", "emit_multi"]
BODY_FIELDS = ["havok_col_filter", "unknown_int_1", "unknown_int_2", "unknown_3_ints", "collision_response",
               "unknown_byte", "process_contact_callback_delay", "unknown_2_shorts", "havok_col_filter_copy",
               "unknown_6_shorts", "mass", "linear_damping", "angular_damping", "friction", "restitution",
               "max_linear_velocity", "max_angular_velocity", "penetration_depth", "motion_system",
               "deactivator_type", "solver_deactivation", "quality_type", "unknown_int_6", "unknown_int_7",
               "unknown_int_8", "unknown_int_9"]


def build_nif(job, vis_tris, pieces, qc, tex_paths, ref_static, ref_env, out_path):
    e = NifFormat.Fallout3HavokMaterial
    hav_mat = dict(zip(e._enumkeys, e._enumvalues))[SURFACEPROP_TO_FO_HAVOK[qc["surfaceprop"]]]

    root = NifFormat.BSFadeNode()
    root.name = job["nif_name"].encode()
    root.flags = 14
    root.rotation.set_identity()
    root.scale = 1.0
    bsx = NifFormat.BSXFlags()
    bsx.name = b"BSX"
    bsx.integer_data = 2  # Havok only, as on vanilla static benches
    root.add_extra_data(bsx)

    # one NiTriShape per Source material group
    mats = []
    for m, _ in vis_tris:
        if m not in mats:
            mats.append(m)
    for gi, mat in enumerate(mats):
        vmap, verts, tris = {}, [], []
        for m, vs in vis_tris:
            if m != mat:
                continue
            idx = []
            for v in vs:
                k = (tuple(round(c, 5) for c in v[0]), tuple(round(c, 5) for c in v[1]), tuple(round(c, 6) for c in v[2]))
                if k not in vmap:
                    vmap[k] = len(verts)
                    verts.append(k)
                idx.append(vmap[k])
            tris.append(idx)
        shape = NifFormat.NiTriShape()
        shape.name = f"{job['nif_name']}:{gi}".encode()
        shape.flags = 14
        shape.rotation.set_identity()
        shape.scale = 1.0
        dat = NifFormat.NiTriShapeData()
        dat.num_vertices = len(verts)
        dat.has_vertices = True
        dat.vertices.update_size()
        dat.has_normals = True
        dat.normals.update_size()
        dat.num_uv_sets = 1
        dat.uv_sets.update_size()
        for i, (p, n, uv) in enumerate(verts):
            dat.vertices[i].x, dat.vertices[i].y, dat.vertices[i].z = p
            dat.normals[i].x, dat.normals[i].y, dat.normals[i].z = n
            dat.uv_sets[0][i].u, dat.uv_sets[0][i].v = uv
        dat.has_vertex_colors = False
        dat.consistency_flags = 0x4000  # CT_STATIC
        lo, hi = bounds([v[0] for v in verts])
        c = tuple((lo[i] + hi[i]) / 2 for i in range(3))
        dat.center.x, dat.center.y, dat.center.z = c
        dat.radius = max(math.sqrt(dot(sub(v[0], c), sub(v[0], c))) for v in verts)
        dat.num_triangles = len(tris)
        dat.num_triangle_points = 3 * len(tris)
        dat.has_triangles = True
        dat.triangles.update_size()
        for i, (a, b, cc) in enumerate(tris):
            dat.triangles[i].v_1, dat.triangles[i].v_2, dat.triangles[i].v_3 = a, b, cc
        shape.data = dat

        matprop = NifFormat.NiMaterialProperty()
        copy_fields(matprop, first(ref_static, "NiMaterialProperty"), MAT_FIELDS)
        pp = NifFormat.BSShaderPPLightingProperty()
        copy_fields(pp, first(ref_env, "BSShaderPPLightingProperty", lambda b: int(b.shader_flags) == 0x82000081),
                    PP_FIELDS)
        ts = NifFormat.BSShaderTextureSet()
        ts.num_textures = 6
        ts.textures.update_size()
        for i, t in enumerate(tex_paths[mat]):
            ts.textures[i] = t.encode()
        pp.texture_set = ts
        shape.add_property(matprop)
        shape.add_property(pp)
        shape.update_tangent_space()
        root.add_child(shape)

    # collision: one convex shape per Source solid
    lst = NifFormat.bhkListShape()
    lst.material.material = hav_mat
    lst.num_sub_shapes = len(pieces)
    lst.sub_shapes.update_size()
    for i, (pverts, planes) in enumerate(pieces):
        cvs = NifFormat.bhkConvexVerticesShape()
        cvs.material.material = hav_mat
        cvs.radius = 0.1
        cvs.num_vertices = len(pverts)
        cvs.vertices.update_size()
        for j, v in enumerate(pverts):
            cvs.vertices[j].x, cvs.vertices[j].y, cvs.vertices[j].z = (c / HAVOK_SCALE for c in v)
            cvs.vertices[j].w = 0.0
        cvs.num_normals = len(planes)
        cvs.normals.update_size()
        for j, (n, d) in enumerate(planes):
            cvs.normals[j].x, cvs.normals[j].y, cvs.normals[j].z = n
            cvs.normals[j].w = -d / HAVOK_SCALE
        lst.sub_shapes[i] = cvs
    body = NifFormat.bhkRigidBodyT()
    copy_fields(body, first(ref_static, "bhkRigidBodyT"), BODY_FIELDS)
    body.rotation.w = 1.0  # identity; translation/velocities/inertia/center stay zero (fixed static)
    body.shape = lst
    coll = NifFormat.bhkCollisionObject()
    coll.flags = 1
    coll.target = root
    coll.body = body
    root.collision_object = coll

    data = NifFormat.Data(version=NIF_V, user_version=NIF_UV, user_version_2=NIF_UV2)
    data.roots = [root]
    data.header.endian_type = 1  # little endian, as in every vanilla FNV NIF
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        data.write(f)
    # read-back gate: the file must parse and keep its block layout
    chk = NifFormat.Data()
    with open(out_path, "rb") as f:
        chk.read(f)
    if chk.version != NIF_V or chk.user_version != NIF_UV or chk.user_version_2 != NIF_UV2:
        raise SystemExit("NIF read-back version mismatch")
    if [type(b).__name__ for b in chk.blocks] != [type(b).__name__ for b in data.blocks]:
        raise SystemExit("NIF read-back block layout mismatch")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("--root", required=True, help="workspace root holding the source inputs")
    ap.add_argument("--fnv-data", required=True, help="Fallout NV Data dir (read-only, vanilla references)")
    ap.add_argument("--stage", required=True, help="staging Data-like output dir")
    a = ap.parse_args()
    job = json.loads(Path(a.job).read_text(encoding="utf-8"))
    root, stage = Path(a.root), Path(a.stage)
    report = {"tool": TOOL_VERSION, "job": job["job"], "inputs": {}, "outputs": {}, "checks": {}}

    # 1. verify source identity
    inp = {}
    for k, spec in job["inputs"].items():
        p = root / spec["path"]
        h = sha256(p)
        ok = h == spec["sha256"].upper()
        report["inputs"][k] = {"path": spec["path"], "sha256": h, "match": ok}
        if not ok:
            raise SystemExit(f"HASH MISMATCH {k}: {h}")
        inp[k] = p

    qc = parse_qc(inp["qc"])
    vmt = parse_vmt(inp["vmt"])
    if qc["surfaceprop"] not in SURFACEPROP_TO_FO_HAVOK:
        raise SystemExit(f"no Havok mapping for surfaceprop '{qc['surfaceprop']}' (refusing silent fallback)")
    report["source"] = {"qc": qc, "vmt": vmt}

    vis_src = parse_smd(inp["reference_smd"])
    phy_src = parse_smd(inp["physics_smd"])
    s_lo, s_hi = bounds([v[0] for _m, vs in vis_src for v in vs])
    p_lo, p_hi = bounds([v[0] for _m, vs in phy_src for v in vs])
    report["source"]["visual_bounds"] = [s_lo, s_hi]
    report["source"]["physics_bounds"] = [p_lo, p_hi]
    report["source"]["visual_triangles"] = len(vis_src)
    report["source"]["physics_triangles"] = len(phy_src)

    # 2. frame check against the compiled model, then transform
    hull = mdl_hull(inp["mdl"])
    ferr, mlo, mhi = check_model_frame(phy_src, hull)
    report["source"]["mdl_hull"] = hull
    report["source"]["physics_bounds_model_frame"] = [mlo, mhi]
    report["checks"]["model_frame_max_error"] = ferr
    if ferr > 0.6:
        raise SystemExit(f"SMD->model frame does not match .mdl hull (err {ferr:.3f}); refusing to guess orientation")
    S = job["scale"]
    P, N = make_xform(S, -s_lo[2] * S)
    vis = [(m, [(P(v[0]), N(v[1]), (v[2][0], 1.0 - v[2][1])) for v in vs]) for m, vs in vis_src]
    phy = [(m, [(P(v[0]), N(v[1]), v[2]) for v in vs]) for m, vs in phy_src]
    f_lo, f_hi = bounds([v[0] for _m, vs in vis for v in vs])
    report["fnv"] = {"visual_bounds": [f_lo, f_hi], "scale": S, "z_shift": -s_lo[2] * S}

    # seat height: z of largest up-facing area in the lower 60% of the model
    area_by_z = {}
    for _m, vs in vis:
        a_, b_, c_ = (v[0] for v in vs)
        cr = cross(sub(b_, a_), sub(c_, a_))
        ar = math.sqrt(dot(cr, cr)) / 2
        nz = norm(cr)
        if nz and nz[2] > 0.9 and a_[2] < f_lo[2] + 0.6 * (f_hi[2] - f_lo[2]):
            z = round((a_[2] + b_[2] + c_[2]) / 3, 0)
            area_by_z[z] = area_by_z.get(z, 0) + ar
    report["fnv"]["seat_height_estimate"] = max(area_by_z, key=area_by_z.get) if area_by_z else None

    # 3. collision pieces
    pieces = []
    for pt in split_convex_pieces(phy):
        pv, planes, worst = convex_planes(pt, eps=0.01 * S)
        pieces.append((pv, planes, worst))
    report["collision"] = {
        "pieces": len(pieces), "qc_maxconvexpieces": qc["maxconvexpieces"],
        "max_convexity_violation_fnv_units": max(w for _a, _b, w in pieces),
        "havok_material": SURFACEPROP_TO_FO_HAVOK[qc["surfaceprop"]],
        "per_piece": [{"verts": len(a), "planes": len(b)} for a, b, _w in pieces],
    }
    if qc["maxconvexpieces"] and len(pieces) > qc["maxconvexpieces"]:
        raise SystemExit("more physics pieces than QC allows")
    if report["collision"]["max_convexity_violation_fnv_units"] > 0.05 * S:
        raise SystemExit("a physics piece is not convex")

    # 4. textures
    work = stage / "_work"
    tex_rel = Path(job["output"]["texture_dir"])
    base_img = vtf_to_image(inp["basetexture"], work, root / job["vtfcmd"])
    mask_img = vtf_to_image(inp["envmapmask"], work, root / job["vtfcmd"])
    outs = {}
    stem = job["nif_name"]
    outs["diffuse"] = (tex_rel / f"{stem}.dds", base_img.convert("RGBA"))
    outs["envmask"] = (tex_rel / f"{stem}_m.dds", mask_img.convert("L").convert("RGBA"))
    flat = Image.new("RGBA", (64, 64), (128, 128, 255, 0))  # Source has no bumpmap/phong
    outs["normal"] = (tex_rel / f"{stem}_n.dds", flat)
    for k, (rel, img) in outs.items():
        p = stage / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        info = write_dds(img, p)
        report["outputs"][k] = {"path": rel.as_posix(), "sha256": sha256(p), **info}
    winpath = lambda r: str(r).replace("/", "\\")
    tex_paths = {m: [winpath(outs["diffuse"][0]), winpath(outs["normal"][0]), "", "",
                     job["cubemap"], winpath(outs["envmask"][0])]
                 for m in {m for m, _ in vis}}

    # 5. NIF
    ref_static = load_ref(a.fnv_data, *job["reference_static"])
    ref_env = load_ref(a.fnv_data, *job["reference_envmasked"])
    nif_rel = Path(job["output"]["mesh"])
    nif_path = stage / nif_rel
    build_nif(job, vis, [(p, pl) for p, pl, _w in pieces], qc, tex_paths, ref_static, ref_env, nif_path)
    report["outputs"]["nif"] = {"path": nif_rel.as_posix(), "sha256": sha256(nif_path), "bytes": nif_path.stat().st_size}
    report["obnd"] = [math.floor(f_lo[0]), math.floor(f_lo[1]), math.floor(f_lo[2]),
                      math.ceil(f_hi[0]), math.ceil(f_hi[1]), math.ceil(f_hi[2])]
    (stage / "o00_conversion_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("fnv", "collision", "obnd")}, indent=2))
    print("NIF", report["outputs"]["nif"])


if __name__ == "__main__":
    # pyffi builds the NIF header string table from a set, so its order follows
    # Python's per-process string hash seed. Pin the seed for byte-identical output.
    import os
    if os.environ.get("PYTHONHASHSEED") != "0":
        env = dict(os.environ, PYTHONHASHSEED="0")
        sys.exit(subprocess.run([sys.executable, *sys.argv], env=env).returncode)
    main()
