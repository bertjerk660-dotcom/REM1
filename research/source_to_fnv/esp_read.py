"""Read-only FNV plugin reader: walks all groups (nested, compressed records) and
dumps chosen record types with key subrecords. Never writes plugins.

Usage: python esp_read.py <plugin.esp> --types WEAP STAT --match tool
"""
import argparse, json, struct, zlib


def subrecords(buf):
    out, i, big = [], 0, None
    while i < len(buf):
        tag, n = struct.unpack_from("<4sH", buf, i)
        tag = tag.decode("cp1252", "replace")
        if tag == "XXXX":
            big = struct.unpack_from("<I", buf, i + 6)[0]
            i += 6 + n
            continue
        if big is not None:
            n, big = big, None
        out.append((tag, buf[i + 6:i + 6 + n]))
        i += 6 + n
    return out


def walk(b, start, end, types, out):
    i = start
    while i < end:
        tag = b[i:i + 4].decode("cp1252", "replace")
        if tag == "GRUP":
            size = struct.unpack_from("<I", b, i + 4)[0]
            walk(b, i + 24, i + size, types, out)
            i += size
            continue
        size, flags, fid = struct.unpack_from("<III", b, i + 4)
        data = b[i + 24:i + 24 + size]
        if tag in types:
            if flags & 0x40000:
                data = zlib.decompress(data[4:])
            out.append((tag, fid, flags, subrecords(data)))
        i += 24 + size


def zs(d):
    return d.split(b"\0")[0].decode("cp1252", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plugin")
    ap.add_argument("--types", nargs="+", default=["WEAP"])
    ap.add_argument("--match", default="")
    a = ap.parse_args()
    b = open(a.plugin, "rb").read()
    tes4_size = struct.unpack_from("<I", b, 4)[0]
    tes4 = subrecords(b[24:24 + tes4_size])
    masters = [zs(d) for t, d in tes4 if t == "MAST"]
    recs = []
    walk(b, 24 + tes4_size, len(b), set(a.types), recs)
    res = {"masters": masters, "records": []}
    for tag, fid, flags, subs in recs:
        d = {"type": tag, "formid": f"{fid:08X}", "flags": hex(flags)}
        for t, v in subs:
            if t in ("EDID", "FULL", "MODL", "MOD2", "MOD3", "MOD4", "ICON", "MICO"):
                d.setdefault(t, []).append(zs(v))
            elif t in ("WNAM", "ETYP", "BIPL", "INAM", "REPL", "NAM0", "YNAM", "ZNAM", "SNAM", "XNAM"):
                d.setdefault(t, []).append(f"{struct.unpack_from('<I', v)[0]:08X}" if len(v) >= 4 else v.hex())
            elif t in ("DNAM",):
                d["DNAM_len"] = len(v)
                if tag == "WEAP" and len(v) >= 4:
                    d["DNAM_animtype"] = struct.unpack_from("<I", v, 0)[0]
            elif t == "DATA" and tag == "WEAP":
                d["DATA"] = v.hex()
            elif t == "OBND":
                d["OBND"] = list(struct.unpack("<6h", v))
        d["subrecord_order"] = [t for t, _ in subs]
        if not a.match or a.match.lower() in json.dumps(d).lower():
            res["records"].append(d)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
