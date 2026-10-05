from pathlib import Path
import argparse
import json
import re


TERMS = [
    "bench", "rail", "railing", "fence", "chair", "table", "barrier", "sign",
    "lamp", "light", "trash", "bin", "box", "crate", "cone", "hydrant", "door",
    "window", "pipe", "pole", "plant", "tree", "rock", "ramp", "stairs", "stair",
    "ledge", "wall", "kiosk", "phone", "mail", "vending", "cabinet", "shelf",
    "sofa", "couch", "seat", "desk", "terminal", "locker", "bed", "counter",
    "barrel", "cart",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("decompiled_q_root", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    base = args.decompiled_q_root.resolve()
    output = args.output or base.parent / "qb_prop_keyword_index.json"

    matches = []
    identifiers = {}

    q_files = sorted(base.rglob("*.q"))
    for source in q_files:
        lines = source.read_text(encoding="utf-8", errors="ignore").splitlines()
        for number, line in enumerate(lines, 1):
            low = line.lower()
            hit = [term for term in TERMS if term in low]
            if not hit:
                continue

            names = re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", line)
            names = [name for name in names if any(term in name.lower() for term in hit)]
            for name in names:
                row = identifiers.setdefault(
                    name, {"count": 0, "terms": set(), "files": set()}
                )
                row["count"] += 1
                row["terms"].update(hit)
                row["files"].add(source.relative_to(base).as_posix())

            matches.append(
                {
                    "file": source.relative_to(base).as_posix(),
                    "line": number,
                    "terms": hit,
                    "text": line.strip()[:600],
                    "identifiers": names,
                }
            )

    name_rows = [
        {
            "identifier": name,
            "count": row["count"],
            "terms": sorted(row["terms"]),
            "files": sorted(row["files"]),
        }
        for name, row in identifiers.items()
    ]
    name_rows.sort(key=lambda x: (-x["count"], x["identifier"].lower()))

    report = {
        "decompiled_q_files": len(q_files),
        "match_lines": len(matches),
        "unique_keyword_identifiers": len(name_rows),
        "warning": "Broad lexical discovery only. Substring matches can contain false positives; use QB/scene context before treating an identifier as a prop.",
        "identifiers": name_rows,
        "matches": matches,
    }
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({
        "decompiled_q_files": report["decompiled_q_files"],
        "match_lines": report["match_lines"],
        "unique_keyword_identifiers": report["unique_keyword_identifiers"],
    }, indent=2))


if __name__ == "__main__":
    main()
