#!/usr/bin/env python3
"""Validate local source/staging identities for prepared Opus visual packages.

Workflow/provenance tool only. It does not build, convert, deploy or launch Fallout.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

DEFAULT_MANIFEST = "build/prepared/opus_visual_source_validation_20261007.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="FNV_GMOD_THUG2 workspace root")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST)
    ap.add_argument("--package", action="append", dest="packages",
                    help="Package ID to validate (repeatable); default validates all")
    ap.add_argument("--report", help="Optional JSON report output path")
    args = ap.parse_args()

    root = Path(args.root)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    selected = set(args.packages or data["packages"].keys())
    report = {
        "schema": "rem.opus_visual_source_validation_result.v1",
        "root": str(root),
        "manifest": str(manifest_path),
        "packages": {},
        "pass": True,
        "file_count": 0,
        "error_count": 0,
    }

    for package_id, package in data["packages"].items():
        if package_id not in selected:
            continue
        pkg = {"status": package["status"], "pass": True, "files": []}
        for spec in package["files"]:
            path = root / Path(spec["path"])
            item = {"path": spec["path"], "expected_sha256": spec["sha256"]}
            report["file_count"] += 1
            if not path.is_file():
                item.update({"exists": False, "pass": False, "error": "missing"})
                pkg["pass"] = False
                report["pass"] = False
                report["error_count"] += 1
            else:
                actual = sha256(path)
                ok = actual == spec["sha256"].upper()
                item.update({
                    "exists": True,
                    "bytes": path.stat().st_size,
                    "actual_sha256": actual,
                    "pass": ok,
                })
                if not ok:
                    item["error"] = "sha256_mismatch"
                    pkg["pass"] = False
                    report["pass"] = False
                    report["error_count"] += 1
            pkg["files"].append(item)
        report["packages"][package_id] = pkg

    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = root / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    for package_id, pkg in report["packages"].items():
        print(f"{package_id}: {'PASS' if pkg['pass'] else 'FAIL'} ({len(pkg['files'])} files)")
        for item in pkg["files"]:
            if not item["pass"]:
                print(f"  {item['path']}: {item.get('error')}")
    print(f"TOTAL: {'PASS' if report['pass'] else 'FAIL'}; files={report['file_count']}; errors={report['error_count']}")
    return 0 if report["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
