from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path.cwd())
    ap.add_argument("--batch", type=Path)
    ap.add_argument("--weapon-manifest", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    root = args.project_root.resolve()
    batch = (args.batch or root / "build/gmod_batch").resolve()
    weapon_manifest = (args.weapon_manifest or root / "research/gmod_weapon_manifest.json").resolve()
    out = (args.output or root / "build/prepared/gmod_hl_weapon_models").resolve()
    packages = out / "packages"
    packages.mkdir(parents=True, exist_ok=True)

    source = json.loads(weapon_manifest.read_text(encoding="utf-8"))

    workers = {}
    for worker in batch.rglob("worker.json"):
        try:
            record = json.loads(worker.read_text(encoding="utf-8"))
        except Exception:
            continue
        model = (record.get("model") or "").replace("\\", "/").lower()
        if model:
            workers.setdefault(model, []).append((worker.parent, record))

    referenced = {}
    for weapon in source["weapons"]:
        for role, field in (("view", "view_model"), ("world", "world_model")):
            model = (weapon.get(field) or "").replace("\\", "/").strip()
            if not model:
                continue
            entry = referenced.setdefault(
                model.lower(),
                {"model": model, "roles": set(), "classes": set(), "engine_native": set()},
            )
            entry["roles"].add(role)
            entry["classes"].add(weapon["class"])
            entry["engine_native"].add(bool(weapon.get("engine_native")))

    records = []
    for key, entry in sorted(referenced.items()):
        matches = list(workers.get(key, []))
        fallback = False
        if not matches:
            basename = Path(entry["model"]).name.lower()
            for worker_model, values in workers.items():
                if Path(worker_model).name.lower() == basename:
                    matches.extend(values)
            fallback = bool(matches)

        rec = {
            "model": entry["model"],
            "roles": sorted(entry["roles"]),
            "weapon_classes": sorted(entry["classes"]),
            "engine_native_values": sorted(entry["engine_native"]),
            "fallback_basename_match": fallback,
            "worker_matches": [],
            "staged": False,
        }

        safe = re.sub(r"[^A-Za-z0-9_.-]+", "__", entry["model"].rsplit(".", 1)[0])
        for index, (srcdir, worker_json) in enumerate(matches):
            dst = packages / (safe if len(matches) == 1 else f"{safe}__{index + 1}")
            if dst.exists():
                shutil.rmtree(dst)
            dst.mkdir(parents=True)

            for name in ("src", "decompiled", "materials"):
                source_dir = srcdir / name
                if source_dir.exists():
                    shutil.copytree(source_dir, dst / name)
            shutil.copy2(srcdir / "worker.json", dst / "worker.json")

            files = []
            for item in dst.rglob("*"):
                if item.is_file():
                    files.append(
                        {
                            "relative": item.relative_to(dst).as_posix(),
                            "size": item.stat().st_size,
                            "sha256": sha256(item),
                        }
                    )

            rec["worker_matches"].append(
                {
                    "worker_model": worker_json.get("model"),
                    "staged_package": dst.relative_to(root).as_posix()
                    if dst.is_relative_to(root)
                    else str(dst),
                    "file_count": len(files),
                    "files": files,
                }
            )
            rec["staged"] = True
        records.append(rec)

    manifest = {
        "purpose": "Source/GMod/Half-Life weapon model staging only; no runtime integration.",
        "source_weapon_manifest": weapon_manifest.relative_to(root).as_posix()
        if weapon_manifest.is_relative_to(root)
        else str(weapon_manifest),
        "source_batch": batch.relative_to(root).as_posix() if batch.is_relative_to(root) else str(batch),
        "staging_root": out.relative_to(root).as_posix() if out.is_relative_to(root) else str(out),
        "unique_referenced_models": len(records),
        "staged_models": sum(1 for x in records if x["staged"]),
        "unstaged_models": sum(1 for x in records if not x["staged"]),
        "records": records,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in ("unique_referenced_models", "staged_models", "unstaged_models", "staging_root")}, indent=2))


if __name__ == "__main__":
    main()
