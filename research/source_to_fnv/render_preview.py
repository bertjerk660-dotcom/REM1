"""Software preview of a converted static NIF (textured, z-buffered, orthographic).

Lets a reviewer check UV orientation, texture mapping, axis and scale without
the game. Renders front (looking +Y), side (looking -X) and top views.

Usage: python render_preview.py <file.nif> <diffuse.dds> <out.png>
"""
import sys, time
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat
from PIL import Image, ImageDraw


def load(nif):
    d = NifFormat.Data()
    with open(nif, "rb") as f:
        d.read(f)
    tris = []
    for b in d.blocks:
        if type(b).__name__ == "NiTriShapeData":
            V = [(v.x, v.y, v.z) for v in b.vertices]
            N = [(n.x, n.y, n.z) for n in b.normals]
            T = [(t.u, t.v) for t in b.uv_sets[0]]
            for t in b.triangles:
                i = (t.v_1, t.v_2, t.v_3)
                tris.append(([V[k] for k in i], [N[k] for k in i], [T[k] for k in i]))
    return tris, d


def render(tris, tex, proj, size, light):
    W, H = size
    pts = [proj(v) for t in tris for v in t[0]]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    s = 0.9 * min(W / (max(xs) - min(xs)), H / (max(ys) - min(ys)))
    ox, oy = (W - s * (max(xs) - min(xs))) / 2 - s * min(xs), (H - s * (max(ys) - min(ys))) / 2 - s * min(ys)
    img = Image.new("RGB", size, (40, 44, 52))
    px = img.load()
    zb = [[-1e9] * W for _ in range(H)]
    tw, th = tex.size
    tp = tex.load()
    for V, N, T in tris:
        P = [proj(v) for v in V]
        S = [(ox + s * p[0], H - (oy + s * p[1]), p[2]) for p in P]
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
                r, g, b = tp[int(u % 1 * tw) % tw, int(v % 1 * th) % th][:3]
                k = w0 * nl[0] + w1 * nl[1] + w2 * nl[2]
                px[x, y] = (int(r * k), int(g * k), int(b * k))
    return img


def main():
    nif, dds, out = sys.argv[1:4]
    tris, _ = load(nif)
    tex = Image.open(dds).convert("RGB")
    L = (0.3, -0.6, 0.74)
    views = [
        ("front (looking +Y)", lambda v: (v[0], v[2], -v[1])),
        ("side (looking -X)", lambda v: (v[1], v[2], v[0])),
        ("top (looking -Z)", lambda v: (v[0], v[1], v[2])),
    ]
    panels = []
    for label, pr in views:
        im = render(tris, tex, pr, (520, 300), L)
        ImageDraw.Draw(im).text((8, 6), label, fill=(230, 230, 230))
        panels.append(im)
    sheet = Image.new("RGB", (520, 300 * len(panels) + 300), (20, 20, 24))
    for i, p in enumerate(panels):
        sheet.paste(p, (0, 300 * i))
    t = tex.resize((260, 260))
    sheet.paste(t, (10, 300 * len(panels) + 20))
    ImageDraw.Draw(sheet).text((280, 300 * len(panels) + 20), "diffuse texture (DDS as written)", fill=(230, 230, 230))
    sheet.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
