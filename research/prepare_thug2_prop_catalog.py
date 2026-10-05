from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
import subprocess


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def glb_stats(path: Path):
    try:
        with path.open("rb") as f:
            magic, _version, _total = struct.unpack("<4sII", f.read(12))
            if magic != b"glTF":
                return {"parse_error": "not glTF"}
            length, _chunk_type = struct.unpack("<II", f.read(8))
            doc = json.loads(f.read(length).decode("utf-8").rstrip("\x00 "))

        triangles = 0
        for mesh in doc.get("meshes", []):
            for primitive in mesh.get("primitives", []):
                accessor_index = primitive.get("indices")
                if accessor_index is not None:
                    triangles += int(doc["accessors"][accessor_index].get("count", 0)) // 3
        return {
            "nodes": len(doc.get("nodes", [])),
            "meshes": len(doc.get("meshes", [])),
            "materials": len(doc.get("materials", [])),
            "images": len(doc.get("images", [])),
            "triangles": triangles,
        }
    except Exception as exc:
        return {"parse_error": repr(exc)}


def convert_mesh(tool: Path, source: Path, texture_source: Path | None, output: Path):
    output.mkdir(parents=True, exist_ok=True)
    command = [str(tool), "mesh", str(source), "-o", str(output), "--format", "glb"]
    if texture_source and texture_source.exists():
        command += ["--tex", str(texture_source)]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=120,
    )
    glbs = list(output.glob("*.glb"))
    return result.returncode, result.stdout, glbs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path.cwd())
    ap.add_argument("--thug2-root", type=Path, required=True,
                    help="Extracted THUG2 DATAP root")
    ap.add_argument("--multitool", type=Path, required=True,
                    help="NeversoftMultitool executable")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    root = args.project_root.resolve()
    source_root = args.thug2_root.resolve()
    tool = args.multitool.resolve()
    out = (args.output or root / "build/prepared/thug2_prop_catalog").resolve()

    standalone_sources = out / "standalone_sources"
    standalone_glb = out / "standalone_glb"
    level_sources = out / "level_sources"
    level_glb = out / "level_glb"
    for directory in (standalone_sources, standalone_glb, level_sources, level_glb):
        directory.mkdir(parents=True, exist_ok=True)

    standalone = []
    model_files = sorted(source_root.rglob("*.mdl.ps2"))
    for index, model in enumerate(model_files, 1):
        rel = model.relative_to(source_root)
        package = standalone_sources / rel.parent
        package.mkdir(parents=True, exist_ok=True)

        companions = []
        for item in model.parent.iterdir():
            if item.is_file() and (
                item.suffix.lower() in {".ps2", ".chk", ".pre", ".txt", ".ini"}
                or item == model
            ):
                target = package / item.name
                if not target.exists() or target.stat().st_size != item.stat().st_size:
                    shutil.copy2(item, target)
                companions.append(
                    {"name": item.name, "size": item.stat().st_size, "sha256": sha256(item)}
                )

        texture = model.with_name(model.name.replace(".mdl.ps2", ".tex.ps2"))
        conversion_dir = standalone_glb / rel.parent / model.name.replace(".mdl.ps2", "")
        try:
            code, log, glbs = convert_mesh(
                tool,
                model,
                texture if texture.exists() else model.parent,
                conversion_dir,
            )
            conversion = {
                "returncode": code,
                "log_tail": "\n".join(log.splitlines()[-12:]),
                "outputs": [
                    {
                        "path": g.relative_to(root).as_posix()
                        if g.is_relative_to(root)
                        else str(g),
                        "size": g.stat().st_size,
                        "sha256": sha256(g),
                        "stats": glb_stats(g),
                    }
                    for g in glbs
                ],
            }
        except Exception as exc:
            conversion = {"returncode": -999, "error": repr(exc), "outputs": []}

        standalone.append(
            {
                "relative": rel.as_posix(),
                "size": model.stat().st_size,
                "sha256": sha256(model),
                "source_companions": companions,
                "conversion": conversion,
            }
        )
        if index % 20 == 0:
            print(f"standalone {index}/{len(model_files)}", flush=True)

    levels = []
    level_root = source_root / "levels"
    geom_files = sorted(
        p for p in level_root.rglob("*.geom.ps2")
        if not p.name.lower().endswith("_net.geom.ps2")
    )
    for index, geom in enumerate(geom_files, 1):
        rel = geom.relative_to(level_root)
        stem = geom.name[:-len(".geom.ps2")]
        texture = geom.with_name(stem + ".tex.ps2")
        collision = geom.with_name(stem + ".col.ps2")

        package = level_sources / rel.parent
        package.mkdir(parents=True, exist_ok=True)
        sources = []
        for item in (geom, texture, collision):
            if item.exists():
                shutil.copy2(item, package / item.name)
                sources.append(
                    {
                        "kind": item.name.split(".")[-2],
                        "relative": item.relative_to(source_root).as_posix(),
                        "size": item.stat().st_size,
                        "sha256": sha256(item),
                    }
                )

        conversion_dir = level_glb / rel.parent
        try:
            code, log, glbs = convert_mesh(tool, geom, texture, conversion_dir)
            conversion = {
                "returncode": code,
                "log_tail": "\n".join(log.splitlines()[-12:]),
                "outputs": [
                    {
                        "path": g.relative_to(root).as_posix()
                        if g.is_relative_to(root)
                        else str(g),
                        "size": g.stat().st_size,
                        "sha256": sha256(g),
                        "stats": glb_stats(g),
                    }
                    for g in glbs
                ],
            }
        except Exception as exc:
            conversion = {"returncode": -999, "error": repr(exc), "outputs": []}

        levels.append(
            {"level_bundle": rel.as_posix(), "sources": sources, "conversion": conversion}
        )
        print(f"level {index}/{len(geom_files)} {rel}", flush=True)

    manifest = {
        "purpose": "THUG2 model and level-geometry staging for later prop extraction.",
        "standalone_model_count": len(standalone),
        "standalone_converted": sum(
            1 for x in standalone
            if x["conversion"]["returncode"] == 0 and x["conversion"]["outputs"]
        ),
        "primary_level_geom_count": len(levels),
        "level_geom_converted": sum(
            1 for x in levels
            if x["conversion"]["returncode"] == 0 and x["conversion"]["outputs"]
        ),
        "standalone_models": standalone,
        "level_bundles": levels,
        "notes": [
            "Standalone MDL assets are direct prop candidates.",
            "Level GEOM exports contain many generic leaf meshes; embedded benches, rails and other furniture require later QB/scene correlation and splitting.",
            "Network duplicate _net GEOM bundles are intentionally not converted.",
            "No claim is made that every level leaf is safe as an independent spawnable prop.",
        ],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({
        "standalone_model_count": manifest["standalone_model_count"],
        "standalone_converted": manifest["standalone_converted"],
        "primary_level_geom_count": manifest["primary_level_geom_count"],
        "level_geom_converted": manifest["level_geom_converted"],
    }, indent=2))


if __name__ == "__main__":
    main()
