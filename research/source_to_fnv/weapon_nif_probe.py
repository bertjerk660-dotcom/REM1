"""Summarise weapon NIF conventions: root, extra data (Prn etc.), node tree with
local transforms, geometry bounds in root space, textures. Read-only.

Usage: python weapon_nif_probe.py <file.nif | bsa:Archive.bsa:internal\\path.nif> ...
"""
import io, sys, time
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat
sys.path.insert(0, str(Path(__file__).parent))
from bsa_read import BSA

DATA = r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data"


def load(spec):
    d = NifFormat.Data()
    if spec.startswith("bsa:"):
        _, arc, internal = spec.split(":", 2)
        d.read(io.BytesIO(BSA(Path(DATA) / arc).read(internal)))
    else:
        with open(spec, "rb") as f:
            d.read(f)
    return d


def mat(n):
    r = n.rotation
    return [[r.m_11, r.m_12, r.m_13], [r.m_21, r.m_22, r.m_23], [r.m_31, r.m_32, r.m_33]]


def xf(parent, node):
    # returns world (root-space) transform as (R, t, s)
    R, t, s = parent
    r = mat(node)
    nt = (node.translation.x, node.translation.y, node.translation.z)
    # Gamebryo: child_world = parent_R * (s_parent * child_t) + parent_t; rotations row-major applied as v*R
    wt = tuple(t[i] + s * sum(nt[j] * R[j][i] for j in range(3)) for i in range(3))
    wR = [[sum(r[i][k] * R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return (wR, wt, s * node.scale)


def apply(T, v):
    R, t, s = T
    return tuple(t[i] + s * sum(v[j] * R[j][i] for j in range(3)) for i in range(3))


def walk(n, T, d, out, seen):
    if n is None or id(n) in seen:
        return
    seen.add(id(n))
    tn = type(n).__name__
    name = n.name.decode("cp1252", "replace") if hasattr(n, "name") and n.name else ""
    line = "  " * d + f"{tn} '{name}'"
    if hasattr(n, "translation"):
        T = xf(T, n) if d > 0 else (mat(n), (n.translation.x, n.translation.y, n.translation.z), n.scale)
        line += f" t=({n.translation.x:.2f},{n.translation.y:.2f},{n.translation.z:.2f}) s={n.scale:.3f}"
    out.append(line)
    for e in getattr(n, "extra_data_list", []) or []:
        v = getattr(e, "string_data", None)
        v = v.decode("cp1252", "replace") if isinstance(v, bytes) else getattr(e, "integer_data", "")
        out.append("  " * (d + 1) + f"[extra] {type(e).__name__} '{e.name.decode('cp1252','replace') if e.name else ''}' = {v}")
    if tn in ("NiTriShape", "NiTriStrips") and n.data and n.data.num_vertices:
        pts = [apply(T, (v.x, v.y, v.z)) for v in n.data.vertices]
        lo = [min(p[i] for p in pts) for i in range(3)]
        hi = [max(p[i] for p in pts) for i in range(3)]
        out.append("  " * (d + 1) + f"bounds_root lo=({lo[0]:.1f},{lo[1]:.1f},{lo[2]:.1f}) hi=({hi[0]:.1f},{hi[1]:.1f},{hi[2]:.1f}) verts={n.data.num_vertices} skin={n.skin_instance is not None}")
        for p in n.properties:
            if type(p).__name__ == "BSShaderPPLightingProperty" and p.texture_set:
                tx = [t.decode("cp1252", "replace") for t in p.texture_set.textures]
                out.append("  " * (d + 1) + f"tex={tx[:2]} env={tx[4] if len(tx)>4 else ''} m={tx[5] if len(tx)>5 else ''} flags={hex(int(p.shader_flags))}")
            if type(p).__name__ in ("NiAlphaProperty",):
                out.append("  " * (d + 1) + f"alpha flags={p.flags} thr={p.threshold}")
    for c in getattr(n, "children", []) or []:
        walk(c, T, d + 1, out, seen)


for spec in sys.argv[1:]:
    d = load(spec)
    print("=" * 10, spec, f"(blocks {len(d.blocks)})")
    out = []
    for r in d.roots:
        walk(r, None, 0, out, set())
    print("\n".join(out[:80]))
