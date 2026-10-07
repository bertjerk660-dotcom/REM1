#!/usr/bin/env python3
"""Validate structural presence of Codex C01-C08 readiness outputs.

This validator checks only that required files exist, Markdown reports are non-empty,
and JSON outputs parse. It does NOT decide whether evidence is semantically complete.
Normal-GPT review against each original stop condition is still mandatory.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

DEFAULT_CONTRACT = "build/prepared/codex_c01_c08_output_contract_20261007.json"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--contract", default=DEFAULT_CONTRACT)
    ap.add_argument("--package", action="append", dest="packages")
    ap.add_argument("--report")
    args = ap.parse_args()

    root = Path(args.root)
    contract_path = Path(args.contract)
    if not contract_path.is_absolute():
        contract_path = root / contract_path
    data = json.loads(contract_path.read_text(encoding="utf-8"))
    selected = set(args.packages or data["packages"].keys())

    result = {
        "schema": "rem.codex_readiness_output_validation.v1",
        "structural_pass": True,
        "semantic_review_required": True,
        "packages": {},
        "missing_count": 0,
        "invalid_json_count": 0,
    }

    for pid, spec in data["packages"].items():
        if pid not in selected:
            continue
        pkg = {"points": spec["points"], "structural_pass": True, "files": []}
        for rel in spec["required"]:
            p = root / rel
            item = {"path": rel, "exists": p.is_file()}
            if not p.is_file():
                item["pass"] = False
                item["error"] = "missing"
                result["missing_count"] += 1
                pkg["structural_pass"] = False
                result["structural_pass"] = False
            elif p.suffix.lower() == ".json":
                try:
                    json.loads(p.read_text(encoding="utf-8"))
                    item["pass"] = True
                except Exception as exc:
                    item["pass"] = False
                    item["error"] = f"invalid_json:{exc}"
                    result["invalid_json_count"] += 1
                    pkg["structural_pass"] = False
                    result["structural_pass"] = False
            else:
                size = p.stat().st_size
                item["bytes"] = size
                item["pass"] = size > 0
                if size <= 0:
                    item["error"] = "empty_report"
                    pkg["structural_pass"] = False
                    result["structural_pass"] = False
            pkg["files"].append(item)
        result["packages"][pid] = pkg

    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = root / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for pid, pkg in result["packages"].items():
        print(f"{pid}: {'STRUCTURAL PASS' if pkg['structural_pass'] else 'INCOMPLETE'}")
        for item in pkg["files"]:
            if not item["pass"]:
                print(f"  {item['path']}: {item.get('error')}")
    print(
        f"TOTAL: {'STRUCTURAL PASS' if result['structural_pass'] else 'INCOMPLETE'}; "
        f"missing={result['missing_count']}; invalid_json={result['invalid_json_count']}; "
        "semantic_review_required=true"
    )
    return 0 if result["structural_pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
