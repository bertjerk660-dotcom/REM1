"""Write a minimal, isolated Fallout: New Vegas test plugin holding STAT records.

Deterministic (no timestamps), depends only on FalloutNV.esm. Also provides a
parser used by the validator to prove the plugin contains only intended records.

Usage:
  python build_static_sidecar.py --out <file.esp> --edid REM_GoldenBench01a \
      --model rem\\golden_bench\\bench01a.nif --obnd -67 -21 0 67 21 70
  python build_static_sidecar.py --inspect <file.esp>
"""
import argparse, json, struct

FORM_VERSION = 15  # Fallout: New Vegas
HEDR_VERSION = 1.34


def sub(tag, data):
    return tag.encode() + struct.pack("<H", len(data)) + data


def zstr(s):
    return s.encode("cp1252") + b"\0"


def record(tag, formid, payload, flags=0):
    return struct.pack("<4sIIIIHH", tag.encode(), len(payload), flags, formid, 0, FORM_VERSION, 0) + payload


def group(label, payload):
    # group version 0, matching the project's working REM_GModTHUG2.esp
    return struct.pack("<4sI4siHHHH", b"GRUP", 24 + len(payload), label.encode(), 0, 0, 0, 0, 0) + payload


def build(stats, author="REM O00 pipeline", desc="Isolated O00 test sidecar. Not for release."):
    recs = b""
    next_id = 0x800
    ids = []
    for s in stats:
        fid = 0x01000000 | next_id
        next_id += 1
        payload = (sub("EDID", zstr(s["edid"])) + sub("OBND", struct.pack("<6h", *s["obnd"]))
                   + sub("MODL", zstr(s["model"])))
        recs += record("STAT", fid, payload)
        ids.append(fid)
    grp = group("STAT", recs)
    hedr = struct.pack("<fiI", HEDR_VERSION, len(stats) + 1, next_id)
    tes4 = (sub("HEDR", hedr) + sub("CNAM", zstr(author)) + sub("SNAM", zstr(desc))
            + sub("MAST", zstr("FalloutNV.esm")) + sub("DATA", b"\0" * 8))
    return record("TES4", 0, tes4) + grp, ids


def parse_subs(buf):
    out, i = [], 0
    while i < len(buf):
        tag, n = struct.unpack_from("<4sH", buf, i)
        out.append((tag.decode(), buf[i + 6:i + 6 + n]))
        i += 6 + n
    return out


def inspect(path):
    b = open(path, "rb").read()
    res = {"records": [], "groups": []}
    i = 0
    while i < len(b):
        tag = b[i:i + 4].decode()
        if tag == "GRUP":
            size, label = struct.unpack_from("<I4s", b, i + 4)
            res["groups"].append(label.decode())
            i += 24  # descend into the group's records
            continue
        _t, size, flags, fid = struct.unpack_from("<4sIII", b, i)
        subs = parse_subs(b[i + 24:i + 24 + size])
        r = {"type": tag, "formid": f"{fid:08X}", "flags": flags}
        for st, data in subs:
            if st in ("EDID", "MODL", "MAST", "CNAM"):
                r.setdefault(st, []).append(data.rstrip(b"\0").decode("cp1252"))
            elif st == "OBND":
                r["OBND"] = list(struct.unpack("<6h", data))
            elif st == "HEDR":
                v, n, nxt = struct.unpack("<fiI", data)
                r["HEDR"] = {"version": round(v, 2), "num_records": n, "next_object_id": f"{nxt:X}"}
        res["records"].append(r)
        i += 24 + size
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--edid")
    ap.add_argument("--model")
    ap.add_argument("--obnd", nargs=6, type=int)
    ap.add_argument("--inspect")
    a = ap.parse_args()
    if a.inspect:
        print(json.dumps(inspect(a.inspect), indent=2))
        return
    data, ids = build([{"edid": a.edid, "model": a.model, "obnd": a.obnd}])
    open(a.out, "wb").write(data)
    print("wrote", a.out, "formids", [f"{x:08X}" for x in ids])


if __name__ == "__main__":
    main()
