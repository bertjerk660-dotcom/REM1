"""Deterministic uncompressed DDS writer (A8R8G8B8 with a full mip chain).

Fallout: New Vegas reads uncompressed 32-bit DDS. Writing it ourselves keeps the
pipeline free of external encoders and makes output byte-reproducible.
"""
import struct
from PIL import Image

DDSD_CAPS, DDSD_HEIGHT, DDSD_WIDTH, DDSD_PITCH = 0x1, 0x2, 0x4, 0x8
DDSD_PIXELFORMAT, DDSD_MIPMAPCOUNT = 0x1000, 0x20000
DDPF_ALPHAPIXELS, DDPF_RGB = 0x1, 0x40
DDSCAPS_COMPLEX, DDSCAPS_TEXTURE, DDSCAPS_MIPMAP = 0x8, 0x1000, 0x400000


def mip_chain(img):
    img = img.convert("RGBA")
    chain = [img]
    w, h = img.size
    while w > 1 or h > 1:
        w, h = max(1, w // 2), max(1, h // 2)
        chain.append(chain[-1].resize((w, h), Image.BOX))
    return chain


def write_dds(img, path):
    chain = mip_chain(img)
    w, h = chain[0].size
    flags = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PITCH | DDSD_PIXELFORMAT | DDSD_MIPMAPCOUNT
    pf = struct.pack("<II4sIIIII", 32, DDPF_RGB | DDPF_ALPHAPIXELS, b"\0\0\0\0", 32,
                     0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    hdr = struct.pack("<4sIIIIIII", b"DDS ", 124, flags, h, w, w * 4, 0, len(chain))
    hdr += b"\0" * 44 + pf
    hdr += struct.pack("<IIIII", DDSCAPS_COMPLEX | DDSCAPS_TEXTURE | DDSCAPS_MIPMAP, 0, 0, 0, 0)
    assert len(hdr) == 128
    body = bytearray()
    for m in chain:
        r, g, b, a = m.split()
        body += Image.merge("RGBA", (b, g, r, a)).tobytes()  # BGRA byte order
    with open(path, "wb") as f:
        f.write(hdr)
        f.write(body)
    return {"width": w, "height": h, "mips": len(chain), "format": "A8R8G8B8"}
