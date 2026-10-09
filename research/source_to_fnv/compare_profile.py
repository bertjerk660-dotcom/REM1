"""Side-profile overlay of a Source weapon (in its R_Hand frame, mapped to FNV
weapon axes) against a vanilla FNV donor NIF. Used to choose grip registration.

Usage: python compare_profile.py <ref.smd> <hand bone> <bsa internal donor nif> <out.png> [--shape NAME]
"""
import argparse, io, sys, time
from pathlib import Path
if not hasattr(time, "clock"):
    time.clock = time.perf_counter
sys.path.insert(0, str(Path(__file__).parent))
from smd_skeleton import parse_skeleton, world_transforms, to_local
from convert_source_static import parse_smd
from bsa_read import BSA
from pyffi.formats.nif import NifFormat
from PIL import Image, ImageDraw

DATA = r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data"
S = 1.7777778


def donor_tris(internal):
    d = NifFormat.Data()
    d.read(io.BytesIO(BSA(Path(DATA) / "Fallout - Meshes.bsa").read(internal)))
    out = []
    for b in d.blocks:
        if type(b).__name__ in ("NiTriStrips", "NiTriShape") and b.data and b.data.num_vertices:
            # include node translation of direct parents (good enough for statics; weapons are flat)
            V = b.data.vertices
            for t in b.data.get_triangles():
                out.append([(V[i].x + b.translation.x, V[i].y + b.translation.y, V[i].z + b.translation.z) for i in t])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("smd"); ap.add_argument("bone"); ap.add_argument("donor"); ap.add_argument("out")
    a = ap.parse_args()
    n, b = parse_skeleton(a.smd)
    W = world_transforms(n, b)
    H = W[a.bone]
    tg = []
    for m, vs in parse_smd(a.smd):
        tri = []
        for v in vs:
            x, y, z = to_local(H, v[0])
            tri.append((x * S, -z * S, y * S))
        tg.append(tri)
    dn = donor_tris(a.donor)
    pts = [p for t in tg + dn for p in t]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    Wd, Hd = 900, 520
    sc = 0.85 * min(Wd / (max(xs) - min(xs)), Hd / (max(ys) - min(ys)))
    ox = (Wd - sc * (max(xs) - min(xs))) / 2 - sc * min(xs)
    oy = (Hd - sc * (max(ys) - min(ys))) / 2 - sc * min(ys)
    P = lambda p: (ox + sc * p[0], Hd - (oy + sc * p[1]))
    img = Image.new("RGB", (Wd, Hd), (24, 26, 32)); dr = ImageDraw.Draw(img)
    for t in tg:
        dr.polygon([P(p) for p in t], fill=(150, 160, 175))
    for t in dn:
        dr.polygon([P(p) for p in t], outline=(230, 70, 70))
    o = P((0, 0, 0)); dr.ellipse([o[0] - 5, o[1] - 5, o[0] + 5, o[1] + 5], outline=(255, 255, 0), width=2)
    dr.text((10, 8), f"FNV axes X fwd/right, Y up. grey=Source {Path(a.smd).stem} (origin=R_Hand)  red=donor {Path(a.donor).stem}  yellow=origin", fill=(230, 230, 230))
    img.save(a.out)
    gx = [p[0] for t in tg for p in t]; gy = [p[1] for t in tg for p in t]
    dx = [p[0] for t in dn for p in t]; dy = [p[1] for t in dn for p in t]
    print(f"source x[{min(gx):.1f},{max(gx):.1f}] y[{min(gy):.1f},{max(gy):.1f}] | donor x[{min(dx):.1f},{max(dx):.1f}] y[{min(dy):.1f},{max(dy):.1f}]")


if __name__ == "__main__":
    main()
