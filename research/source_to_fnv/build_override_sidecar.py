"""Build an isolated FNV override plugin that changes only presentation fields of
existing records (model path, object bounds), copying every other subrecord
byte-for-byte from the source plugin. Deterministic.

Spec JSON:
{
  "source_plugin": "<path>", "masters": ["FalloutNV.esm", "REM_GModTHUG2.esp"],
  "author": "...", "description": "...",
  "overrides": [ {"formid": "01000803", "type": "WEAP", "MODL": "rem\\...\\w.nif",
                  "OBND": [x1,y1,z1,x2,y2,z2], "drop": ["MODT"]} ]
}
Usage: python build_override_sidecar.py <spec.json> --out <file.esp>
"""
import argparse, json, struct, zlib
from esp_read import subrecords, walk

GROUP_ORDER = ["STAT", "WEAP"]  # order of top groups written (subset used)


def sub(tag, data):
    return tag.encode() + struct.pack("<H", len(data)) + data


def zstr(s):
    return s.encode("cp1252") + b"\0"


def raw_records(path):
    b = open(path, "rb").read()
    tes4_size = struct.unpack_from("<I", b, 4)[0]
    out = {}

    def scan(start, end):
        i = start
        while i < end:
            tag = b[i:i + 4].decode("cp1252", "replace")
            if tag == "GRUP":
                size = struct.unpack_from("<I", b, i + 4)[0]
                scan(i + 24, i + size)
                i += size
                continue
            size, flags, fid = struct.unpack_from("<III", b, i + 4)
            out[(tag, fid)] = (b[i:i + 24], b[i + 24:i + 24 + size])
            i += 24 + size
    scan(24 + tes4_size, len(b))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.loads(open(a.spec, encoding="utf-8-sig").read())
    recs = raw_records(spec["source_plugin"])
    by_group = {}
    for o in spec["overrides"]:
        fid = int(o["formid"], 16)
        hdr, data = recs[(o["type"], fid)]
        flags = struct.unpack_from("<I", hdr, 8)[0]
        if flags & 0x40000:
            raise SystemExit("compressed source record not supported")
        out = b""
        for tag, val in subrecords(data):
            if tag in o.get("drop", []):
                continue
            if tag == "MODL" and "MODL" in o:
                val = zstr(o["MODL"])
            if tag == "OBND" and "OBND" in o:
                val = struct.pack("<6h", *o["OBND"])
            out += sub(tag, val)
        nh = hdr[:4] + struct.pack("<I", len(out)) + hdr[8:]
        by_group.setdefault(o["type"], []).append(nh + out)
    body = b""
    nrec = 0
    for g in GROUP_ORDER:
        if g in by_group:
            payload = b"".join(by_group[g])
            body += struct.pack("<4sI4siHHHH", b"GRUP", 24 + len(payload), g.encode(), 0, 0, 0, 0, 0) + payload
            nrec += 1 + len(by_group[g])
    tes4 = sub("HEDR", struct.pack("<fiI", 1.34, nrec, 0x800))
    tes4 += sub("CNAM", zstr(spec.get("author", "REM pipeline")))
    tes4 += sub("SNAM", zstr(spec.get("description", "")))
    for m in spec["masters"]:
        tes4 += sub("MAST", zstr(m)) + sub("DATA", b"\0" * 8)
    head = struct.pack("<4sIIIIHH", b"TES4", len(tes4), 0, 0, 0, 15, 0)
    open(a.out, "wb").write(head + tes4 + body)
    print("wrote", a.out, "records", nrec)


if __name__ == "__main__":
    main()
