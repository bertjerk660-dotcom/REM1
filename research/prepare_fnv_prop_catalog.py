from pathlib import Path
import argparse
import hashlib
import json
import re

from bethesda_structs.archive import get_archive


EXCLUDED_ROOTS = {
    "characters", "character", "creatures", "creature", "weapons", "weapon",
    "armor", "armour", "pipboy", "interface", "effects", "effect",
    "projectiles", "projectile", "animations", "animation",
}

KEYWORDS = [
    "bench", "rail", "railing", "fence", "chair", "table", "barrier", "sign",
    "lamp", "light", "trash", "bin", "box", "crate", "cone", "hydrant", "door",
    "window", "pipe", "pole", "plant", "tree", "rock", "ramp", "stairs", "stair",
    "ledge", "wall", "kiosk", "phone", "mail", "vending", "cabinet", "shelf",
    "sofa", "couch", "seat", "desk", "terminal", "locker", "bed", "counter",
    "suitcase", "bottle", "can", "cart", "barrel", "tire", "tyre", "statue",
    "pot", "toilet",
]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def texture_refs(data: bytes):
    refs = []
    seen = set()
    for match in re.finditer(rb"(?i)textures[\\/][ -~]{1,220}?\.dds", data):
        value = match.group(0).decode("latin1", "ignore").replace("/", "\\")
        key = value.lower()
        if key not in seen:
            seen.add(key)
            refs.append(value)
    return refs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path.cwd())
    ap.add_argument("--fnv-data", type=Path, required=True,
                    help="Fallout New Vegas Data directory containing BSA archives")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    root = args.project_root.resolve()
    data_dir = args.fnv_data.resolve()
    out = (args.output or root / "build/prepared/fnv_prop_catalog").resolve()
    models = out / "models"
    models.mkdir(parents=True, exist_ok=True)

    bsa_files = []
    for path in sorted(data_dir.glob("*.bsa")):
        name = path.name.lower()
        if "meshes" in name or name == "update.bsa" or "main" in name:
            bsa_files.append(path)

    records = []
    latest = {}
    for bsa in bsa_files:
        archive = get_archive(str(bsa))
        for archive_file in archive.iter_files():
            rel = archive_file.filepath.as_posix().replace("\\", "/")
            low = rel.lower()
            if not low.endswith(".nif"):
                continue

            parts = [x for x in low.split("/") if x]
            try:
                mesh_index = parts.index("meshes")
                after = parts[mesh_index + 1:]
            except ValueError:
                after = parts
            top = after[0] if after else "(root)"
            candidate = top not in EXCLUDED_ROOTS

            record = {
                "archive": bsa.name,
                "path": rel,
                "size": len(archive_file.data),
                "sha256": sha_bytes(archive_file.data),
                "top_category": top,
                "spawn_prop_candidate": candidate,
                "name_tags": [key for key in KEYWORDS if key in low],
                "texture_refs": texture_refs(archive_file.data),
            }
            records.append(record)
            latest[low] = (record, archive_file.data)

    staged = []
    for _key, (record, payload) in latest.items():
        if not record["spawn_prop_candidate"]:
            continue

        source_parts = Path(record["path"]).parts
        rel = (
            Path(*source_parts[1:])
            if source_parts and source_parts[0].lower() == "meshes"
            else Path(record["path"])
        )
        target = models / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)

        staged_record = dict(record)
        staged_record["staged_path"] = (
            target.relative_to(root).as_posix() if target.is_relative_to(root) else str(target)
        )
        staged.append(staged_record)

    category_counts = {}
    tag_counts = {}
    for record in staged:
        category = record["top_category"]
        category_counts[category] = category_counts.get(category, 0) + 1
        for tag in record["name_tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    manifest = {
        "purpose": "FNV environmental/world NIF staging for later GMod-style spawn-menu registration.",
        "archives_scanned": [
            {"name": p.name, "size": p.stat().st_size, "sha256": sha_file(p)}
            for p in bsa_files
        ],
        "classification": {
            "excluded_roots": sorted(EXCLUDED_ROOTS),
            "keyword_tags": KEYWORDS,
        },
        "all_nif_records": len(records),
        "unique_nif_paths": len(latest),
        "staged_prop_candidates": len(staged),
        "staged_bytes": sum(x["size"] for x in staged),
        "category_counts": dict(sorted(category_counts.items(), key=lambda x: (-x[1], x[0]))),
        "tag_counts": dict(sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))),
        "records": sorted(staged, key=lambda x: x["path"].lower()),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out / "all_nifs_index.json").write_text(
        json.dumps({"archives": [p.name for p in bsa_files], "records": records}, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({
        "unique_nif_paths": manifest["unique_nif_paths"],
        "staged_prop_candidates": manifest["staged_prop_candidates"],
        "staged_bytes": manifest["staged_bytes"],
    }, indent=2))


if __name__ == "__main__":
    main()
