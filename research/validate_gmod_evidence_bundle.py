#!/usr/bin/env python3
"""Validate authored GMOD evidence metadata, not runtime parity or payload licences."""
import argparse
import hashlib
import json
import re
from pathlib import Path

CLASSES = {
    "Lua", "native code", "engine-provided interface", "asset", "model",
    "texture/material", "font", "sound", "configuration",
    "Source-engine dependency", "compatibility/adaptation requirement",
}
ROOTS = {
    "qmenu", "prop_browser", "prop_icons", "toolgun", "tool_selection",
    "duplicator", "remover", "camera", "physgun", "physgun_beam",
    "physgun_highlighting", "notifications", "hud", "input",
}
PAYLOAD_EXTENSIONS = {
    ".dll", ".exe", ".vpk", ".gma", ".lua", ".mdl", ".vvd", ".vtx",
    ".phy", ".vmt", ".vtf", ".ttf", ".otf", ".wav", ".mp3", ".ogg",
    ".nif", ".kf", ".esp", ".esm", ".idb", ".i64", ".smd", ".qc",
}
HASH = re.compile(r"^[0-9a-fA-F]{64}$")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_dir = root / "manifests/gmod_2026-10-07"
    doc_dir = root / "context/GMOD_2026-10-07"
    errors, checks, inputs = [], [], []

    def check(condition, label):
        checks.append({"check": label, "pass": bool(condition)})
        if not condition:
            errors.append(label)

    def walk(value, label):
        if isinstance(value, dict):
            for key, child in value.items():
                if "sha256" in key.lower() and child is not None:
                    if isinstance(child, str):
                        check(bool(HASH.fullmatch(child)), label + ": valid " + key)
                walk(child, label + "." + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, label + "[" + str(index) + "]")

    loaded = {}
    for path in sorted(manifest_dir.glob("*.json")):
        if args.output and path.resolve() == args.output.resolve():
            continue
        if path.name == "bundle_validation.json":
            continue
        raw = path.read_bytes()
        rel = path.relative_to(root).as_posix()
        inputs.append({"path": rel, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeError, ValueError) as exc:
            check(False, rel + ": strict UTF-8 JSON: " + str(exc))
            continue
        check(True, rel + ": strict UTF-8 JSON (no BOM or appended tool output)")
        loaded[path.name] = value
        walk(value, rel)

    graph = loaded.get("dependency_graph.json", {})
    check(bool(graph), "dependency graph exists")
    nodes = graph.get("nodes", [])
    ids = [node.get("id") for node in nodes]
    check(len(ids) == len(set(ids)), "graph node IDs unique")
    check(ROOTS <= set(graph.get("root_systems", [])), "all fourteen required subsystem roots represented")
    for node in nodes:
        check(node.get("type") in CLASSES, "graph class: " + str(node.get("id")))
        for evidence in node.get("evidence", []):
            check((root / evidence).is_file(), "graph evidence file exists: " + evidence)
    for edge in graph.get("edges", []):
        check(edge.get("from") in ids and edge.get("to") in ids,
              "graph edge resolves: " + str(edge.get("from")) + " -> " + str(edge.get("to")))

    for path in sorted(doc_dir.glob("*.md")):
        raw = path.read_bytes()
        inputs.append({"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        check(bool(raw.strip()), "authored report nonempty: " + path.name)

    published = [p for base in (doc_dir, manifest_dir) for p in base.rglob("*") if p.is_file()]
    for path in published:
        check(path.suffix.lower() not in PAYLOAD_EXTENSIONS,
              "no proprietary payload extension in evidence bundle: " + path.relative_to(root).as_posix())

    provenance = loaded.get("asset_provenance.json")
    check(provenance is not None, "asset provenance manifest exists")
    if provenance is not None:
        if isinstance(provenance, list):
            entries = provenance
        else:
            entries = provenance.get("entries", provenance.get("files", provenance.get("components", [])))
        check(bool(entries), "asset provenance records exist")
        for number, entry in enumerate(entries):
            label = "asset record " + str(number)
            check(entry.get("commit_safe", entry.get("may_commit", entry.get("safe_to_commit"))) is False,
                  label + ": original payload explicitly excluded from Git")
            check(bool(entry.get("source_path", entry.get("original_path", entry.get("source_absolute_path")))),
                  label + ": original source path recorded")
            check(bool(entry.get("status")), label + ": status recorded")
            check(bool(entry.get("type")) and bool(entry.get("subsystem")),
                  label + ": component type and owning subsystem recorded")
            check(bool(entry.get("reason")) and isinstance(entry.get("dependencies"), list),
                  label + ": reason and dependency list recorded")
            internal = entry.get("internal_path", "")
            check(bool(internal) and ".." not in internal.split("/") and not internal.startswith("/"),
                  label + ": safe original internal path")
            if entry.get("sha256"):
                check(bool(entry.get("destination_path")), label + ": verified original has staging destination")
                check(entry.get("destination_sha256") == entry.get("sha256") and entry.get("sha256_match") is True,
                      label + ": recorded source/destination SHA-256 match")
                if entry.get("source_kind") == "vpk":
                    check(entry.get("crc32_validated") is True and bool(entry.get("archive_path")),
                          label + ": VPK CRC and source archive recorded")
            else:
                check("absent" in entry.get("status", "") or "error" in entry.get("status", ""),
                      label + ": missing original explicitly unresolved")

    required_reports = {
        "README.md", "REPOSITORY_RECONCILIATION.md", "ARCHITECTURE_REPORT.md",
        "QMENU_ARCHITECTURE.md", "TOOLGUN_ARCHITECTURE.md", "PHYSGUN_ARCHITECTURE.md",
        "OTHER_OVERLAY_SYSTEMS.md", "INTEGRATION_BOUNDARY.md", "COMPATIBILITY_MATRIX.md",
        "EXISTING_IMPLEMENTATION_AUDIT.md", "IDA68_NATIVE_REPORT.md", "STAGING_SUMMARY.md",
    }
    for name in sorted(required_reports):
        check((doc_dir / name).is_file(), "required deliverable exists: " + name)
    for name in ("native_boundary_client.json", "native_boundary_server.json"):
        native = loaded.get(name, {})
        check(native.get("ida_version") == "6.8", name + ": actual IDA 6.8 execution")
        check(bool(native.get("functions")) and bool(native.get("module_sha256")),
              name + ": module identity and function records present")
    snapshot = loaded.get("runtime_snapshot.json", {})
    check(snapshot.get("end_of_pass_comparison", {}).get("all_four_files_match_baseline") is True,
          "source and deployed runtime hashes unchanged at end of GMOD pass")

    result = {
        "schema": "rem.gmod_evidence_bundle_validation.v1",
        "scope": "strict metadata, graph links, report existence, hashes and payload exclusion; not runtime/playtest validation",
        "pass": not errors,
        "check_count": len(checks),
        "error_count": len(errors),
        "errors": errors,
        "graph_nodes": len(nodes),
        "graph_edges": len(graph.get("edges", [])),
        "required_roots": len(ROOTS),
        "input_files": inputs,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "input_files"}, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
