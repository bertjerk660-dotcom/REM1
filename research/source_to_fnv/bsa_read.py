"""Minimal read-only reader for Fallout 3 / New Vegas BSA archives (version 104).

Used to pull vanilla reference files (e.g. a stock static NIF) for comparison.
Never writes into the game install.

Usage:
  python bsa_read.py <archive.bsa> --list <substring>
  python bsa_read.py <archive.bsa> --extract <internal\\path.nif> --out <file>
"""
import argparse, struct, zlib
from pathlib import Path


class BSA:
    def __init__(self, path):
        self.path = Path(path)
        self.entries = {}
        with open(self.path, "rb") as f:
            hdr = f.read(36)
            magic, ver, off, aflags, nfold, nfile, lfold, lfile, fflags = struct.unpack("<4sIIIIIIIH", hdr[:34])
            if magic != b"BSA\x00" or ver != 104:
                raise ValueError(f"unsupported BSA {magic} v{ver}")
            self.compressed_default = bool(aflags & 0x4)
            self.embed_names = bool(aflags & 0x100)
            f.seek(off)
            folders = [struct.unpack("<QII", f.read(16)) for _ in range(nfold)]
            recs = []
            for _h, count, _o in folders:
                n = f.read(1)[0]
                dname = f.read(n).rstrip(b"\x00").decode("cp1252")
                for _ in range(count):
                    _fh, size, foff = struct.unpack("<QII", f.read(16))
                    recs.append((dname, size, foff))
            names = f.read(lfile).split(b"\x00")
            for (dname, size, foff), nm in zip(recs, names):
                key = (dname + "\\" + nm.decode("cp1252")).lower()
                self.entries[key] = (size, foff)

    def read(self, internal):
        size, off = self.entries[internal.lower().replace("/", "\\")]
        comp = self.compressed_default ^ bool(size & 0x40000000)
        size &= 0x3FFFFFFF
        with open(self.path, "rb") as f:
            f.seek(off)
            data = f.read(size)
        if self.embed_names:
            n = data[0]
            data = data[1 + n:]
        if comp:
            data = zlib.decompress(data[4:])
        return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bsa")
    ap.add_argument("--list")
    ap.add_argument("--extract")
    ap.add_argument("--out")
    a = ap.parse_args()
    b = BSA(a.bsa)
    if a.list is not None:
        for k in sorted(b.entries):
            if a.list.lower() in k:
                print(k)
    if a.extract:
        Path(a.out).write_bytes(b.read(a.extract))
        print("wrote", a.out)


if __name__ == "__main__":
    main()
