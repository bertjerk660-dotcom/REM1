"""Software preview of a converted NIF (per-shape textures, z-buffered, orthographic).

Lets a reviewer check UV orientation, texture mapping, axis and scale without
the game. Renders three views. Each shape uses its own slot-0 texture resolved
under --texroot (the staging Data dir); glow maps are added on top.

Usage: python render_preview.py <file.nif> <out.png> [--texroot <dir>] [--views front,side,top]
       (legacy form: render_preview.py <file.nif> <diffuse.dds> <out.png>)
"""
import argparse, sys, time
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat
from PIL import Image, ImageDraw

VIEWS = {
    "front": ("front (looking +Y)", lambda v: (v[0], v[2], -v[1])),
    "side": ("side (looking -X)", lambda v: (v[1], v[2], v[0])),
    "top": ("top (looking -Z)", lambda v: (v[0], v[1], v[2])),
    "wside": ("weapon side (looking -Z: X fwd, Y up)", lambda v: (v[0], v[1], v[2])),
    "wtop": ("weapon top (looking -Y: X fwd, Z side)", lambda v: (v[0], -v[2], v[1])),
    "wrear": ("weapon rear (looking +X)", lambda v: (-v[2], v[1], -v[0])),
}


def load(nif, texroot, fallback):
    d = NifFormat.Data()
    with open(nif, "rb") as f:
        d.read(f)
    cache, tris = {}, []

    def tex(rel):
        if not rel:
            return None
        if rel not in cache:
            p = Path(texroot) / rel.replace("\\", "/") if texroot else None
            cache[rel] = Image.open(p).convert("RGB") if p and p.exists() else None
        return cache[rel]
    for b in d.blocks:
        if type(b).__name__ != "NiTriShape" or not b.data:
            continue
        pp = next((p for p in b.properties if type(p).__name__ == "BSShaderPPLightingProperty"), None)
        slots = [t.decode("cp1252") for t in pp.texture_set.textures] if pp and pp.texture_set else []
        diff = tex(slots[0]) if slots else None
        glow = tex(slots[2]) if len(slots) > 2 else None
        diff = diff or fallback
        D = b.data
        V = [(v.x, v.y, v.z) for v in D.vertices]
        N = [(n.x, n.y, n.z) for n in D.normals]
        T = [(t.u, t.v) for t in D.uv_sets[0]]
        for t in D.triangles:
            i = (t.v_1, t.v_2, t.v_3)
            tris.append(([V[k] for k in i], [N[k] for k in i], [T[k] for k in i], diff, glow))
    return tris


def render(tris, proj, size, light):
    W, H = size
    pts = [proj(v) for t in tris for v in t[0]]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    s = 0.9 * min(W / (max(xs) - min(xs) + 1e-9), H / (max(ys) - min(ys) + 1e-9))
    ox = (W - s * (max(xs) - min(xs))) / 2 - s * min(xs)
    oy = (H - s * (max(ys) - min(ys))) / 2 - s * min(ys)
    img = Image.new("RGB", size, (40, 44, 52)); px = img.load()
    zb = [[-1e9] * W for _ in range(H)]
    for V, N, T, tex, glow in tris:
        tp = tex.load(); tw, th = tex.size
        gp = glow.load() if glow else None
        S = [(ox + s * p[0], H - (oy + s * p[1]), p[2]) for p in (proj(v) for v in V)]
        x0, x1 = max(0, int(min(q[0] for q in S))), min(W - 1, int(max(q[0] for q in S)) + 1)
        y0, y1 = max(0, int(min(q[1] for q in S))), min(H - 1, int(max(q[1] for q in S)) + 1)
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = S
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-9:
            continue
        nl = [max(0.25, sum(a * b for a, b in zip(n, light))) for n in N]
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                w0 = ((by - cy) * (x - cx) + (cx - bx) * (y - cy)) / den
                w1 = ((cy - ay) * (x - cx) + (ax - cx) * (y - cy)) / den
                w2 = 1 - w0 - w1
                if w0 < 0 or w1 < 0 or w2 < 0:
                    continue
                z = w0 * az + w1 * bz + w2 * cz
                if z <= zb[y][x]:
                    continue
                zb[y][x] = z
                u = w0 * T[0][0] + w1 * T[1][0] + w2 * T[2][0]
                v = w0 * T[0][1] + w1 * T[1][1] + w2 * T[2][1]
                tx, ty = int(u % 1 * tw) % tw, int(v % 1 * th) % th
                r, g, b = tp[tx, ty][:3]
                k = w0 * nl[0] + w1 * nl[1] + w2 * nl[2]
                r, g, b = r * k, g * k, b * k
                if gp:
                    gw, gh = glow.size
                    gr, gg, gb = gp[int(u % 1 * gw) % gw, int(v % 1 * gh) % gh][:3]
                    r, g, b = min(255, r + gr), min(255, g + gg), min(255, b + gb)
                px[x, y] = (int(r), int(g), int(b))
    return img


def main():
    if len(sys.argv) == 4 and not sys.argv[1].startswith("-") and sys.argv[2].lower().endswith(".dds"):
        nif, dds, out = sys.argv[1:4]
        texroot, views, fallback = None, ["front", "side", "top"], Image.open(dds).convert("RGB")
    else:
        ap = argparse.ArgumentParser()
        ap.add_argument("nif"); ap.add_argument("out")
        ap.add_argument("--texroot"); ap.add_argument("--views", default="front,side,top")
        a = ap.parse_args()
        nif, out, texroot, views = a.nif, a.out, a.texroot, a.views.split(",")
        fallback = Image.new("RGB", (4, 4), (180, 180, 180))
    tris = load(nif, texroot, fallback)
    L = (0.3, 0.6, 0.74)
    panels = []
    for k in views:
        label, pr = VIEWS[k]
        im = render(tris, pr, (620, 320), L)
        ImageDraw.Draw(im).text((8, 6), label, fill=(230, 230, 230))
        panels.append(im)
    sheet = Image.new("RGB", (620, 320 * len(panels)), (20, 20, 24))
    for i, p in enumerate(panels):
        sheet.paste(p, (0, 320 * i))
    sheet.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
