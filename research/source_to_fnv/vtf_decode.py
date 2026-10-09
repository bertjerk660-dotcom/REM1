"""Pure-Python VTF (v7.x) top-mip decoder for DXT1 / DXT5 / BGRA8888 / BGR888.

Why: VTFCmd's TGA export drops the DXT5 alpha channel (writes 255), which loses
Source $selfillum / phong / transparency masks. This decoder keeps it.
Verified against VTFCmd RGB output (see validate_o01_static / F017).
"""
import struct
from PIL import Image

FMT_BGR888, FMT_BGRA8888, FMT_DXT1, FMT_DXT5, FMT_RGBA8888 = 3, 12, 13, 15, 0
BPP = {FMT_DXT1: 0.5, FMT_DXT5: 1.0, FMT_BGRA8888: 4, FMT_BGR888: 3, FMT_RGBA8888: 4}


def _c565(c):
    r, g, b = (c >> 11) & 31, (c >> 5) & 63, c & 31
    return (r << 3 | r >> 2, g << 2 | g >> 4, b << 3 | b >> 2)


def _color_block(blk, dxt1):
    c0, c1, bits = struct.unpack("<HHI", blk)
    p0, p1 = _c565(c0), _c565(c1)
    if c0 > c1 or not dxt1:
        p2 = tuple((2 * a + b) // 3 for a, b in zip(p0, p1))
        p3 = tuple((a + 2 * b) // 3 for a, b in zip(p0, p1))
        pal = [p0 + (255,), p1 + (255,), p2 + (255,), p3 + (255,)]
    else:
        p2 = tuple((a + b) // 2 for a, b in zip(p0, p1))
        pal = [p0 + (255,), p1 + (255,), p2 + (255,), (0, 0, 0, 0)]
    return [pal[(bits >> (2 * i)) & 3] for i in range(16)]


def _alpha_block(blk):
    a0, a1 = blk[0], blk[1]
    bits = int.from_bytes(blk[2:8], "little")
    if a0 > a1:
        pal = [a0, a1] + [((6 - i) * a0 + (i + 1) * a1) // 7 for i in range(6)]
    else:
        pal = [a0, a1] + [((4 - i) * a0 + (i + 1) * a1) // 5 for i in range(4)] + [0, 255]
    return [pal[(bits >> (3 * i)) & 7] for i in range(16)]


def decode(path):
    b = open(path, "rb").read()
    if b[:4] != b"VTF\0":
        raise ValueError("not a VTF")
    w, h = struct.unpack_from("<HH", b, 16)
    fmt = struct.unpack_from("<i", b, 52)[0]
    if fmt not in BPP:
        raise ValueError(f"unsupported VTF format {fmt}")
    size = int(max(4, w) * max(4, h) * BPP[fmt]) if fmt in (FMT_DXT1, FMT_DXT5) else w * h * BPP[fmt]
    top = b[-size:]  # largest mip is stored last
    if fmt in (FMT_BGRA8888, FMT_BGR888, FMT_RGBA8888):
        mode = {FMT_BGRA8888: "BGRA", FMT_BGR888: "BGR", FMT_RGBA8888: "RGBA"}[fmt]
        return Image.frombytes("RGBA" if len(mode) == 4 else "RGB", (w, h), top, "raw", mode).convert("RGBA")
    px = bytearray(w * h * 4)
    bw, bh = max(1, w // 4), max(1, h // 4)
    step = 8 if fmt == FMT_DXT1 else 16
    for by in range(bh):
        for bx in range(bw):
            o = (by * bw + bx) * step
            if fmt == FMT_DXT1:
                cols = _color_block(top[o:o + 8], True)
            else:
                al = _alpha_block(top[o:o + 8])
                cols = [c[:3] + (a,) for c, a in zip(_color_block(top[o + 8:o + 16], False), al)]
            for i, c in enumerate(cols):
                x, y = bx * 4 + (i & 3), by * 4 + (i >> 2)
                if x < w and y < h:
                    k = (y * w + x) * 4
                    px[k:k + 4] = bytes(c)
    return Image.frombytes("RGBA", (w, h), bytes(px))
