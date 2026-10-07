#!/usr/bin/env python3
"""Validate Codex C01-C08 readiness-output structure.

Modes:
- baseline: preparation-time inventory. Missing future Codex deliverables are PENDING,
  not failures. Existing files are still checked for emptiness/JSON validity.
- delivery: run after Codex claims a package delivery. Missing/empty/invalid required
  files are structural failures.

Neither mode decides semantic completeness. Normal-GPT review against the original
stop condition remains mandatory before any readiness points are awarded.
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
    ap.add_argument("--mode", choices=("baseline", "delivery"), default="baseline")
    ap.add_argument("--report")
    args = ap.parse_args()

    root = Path(args.root)
    contract_path = Path(args.contract)
    if not contract_path.is_absolute():
        contract_path = root / contract_path
    data = json.loads(contract_path.read_text(encoding="utf-8"))
    selected = set(args.packages or data["packages"].keys())

    result = {
        "schema": "rem.codex_readiness_output_validation.v2",
        "mode": args.mode,
        "contract_consistent": True,
        "delivery_structural_pass": True if args.mode == "delivery" else None,
        "semantic_review_required": True,
        "packages": {},
        "pending_count": 0,
        "missing_count": 0,
        "empty_count": 0,
        "invalid_json_count": 0,
    }

    for pid, spec in data["packages"].items():
        if pid not in selected:
            continue

        pkg = {
            "points": spec["points"],
            "status": "STRUCTURAL_PASS" if args.mode == "delivery" else "PENDING",
            "delivery_structural_pass": True if args.mode == "delivery" else None,
            "files": [],
        }
        present_count = 0

        for rel in spec["required"]:
            p = root / rel
            item = {"path": rel, "exists": p.is_file()}

            if not p.is_file():
                if args.mode == "baseline":
                    item["status"] = "PENDING_EXPECTED_OUTPUT"
                    item["pass"] = None
                    result["pending_count"] += 1
                else:
                    item["status"] = "MISSING"
                    item["pass"] = False
                    item["error"] = "missing_after_delivery_claim"
                    result["missing_count"] += 1
                    pkg["delivery_structural_pass"] = False
                    result["delivery_structural_pass"] = False
                pkg["files"].append(item)
                continue

            present_count += 1
            if p.suffix.lower() == ".json":
                try:
                    json.loads(p.read_text(encoding="utf-8"))
                    item["status"] = "PRESENT_VALID_JSON"
                    item["pass"] = True
                except Exception as exc:
                    item["status"] = "INVALID_JSON"
                    item["pass"] = False
                    item["error"] = f"invalid_json:{exc}"
                    result["invalid_json_count"] += 1
                    result["contract_consistent"] = False
                    if args.mode == "delivery":
                        pkg["delivery_structural_pass"] = False
                        result["delivery_structural_pass"] = False
            else:
                size = p.stat().st_size
                item["bytes"] = size
                if size > 0:
                    item["status"] = "PRESENT_NONEMPTY"
                    item["pass"] = True
                else:
                    item["status"] = "EMPTY_REPORT"
                    item["pass"] = False
                    item["error"] = "empty_report"
                    result["empty_count"] += 1
                    result["contract_consistent"] = False
                    if args.mode == "delivery":
                        pkg["delivery_structural_pass"] = False
                        result["delivery_structural_pass"] = False
            pkg["files"].append(item)

        if args.mode == "baseline":
            if present_count == 0:
                pkg["status"] = "PENDING_NOT_DELIVERED"
            elif present_count < len(spec["required"]):
                pkg["status"] = "PARTIAL_DELIVERY"
            else:
                pkg["status"] = "PRESENT_AWAITING_SEMANTIC_REVIEW"
        elif not pkg["delivery_structural_pass"]:
            pkg["status"] = "STRUCTURAL_FAIL"

        result["packages"][pid] = pkg

    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = root / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    for pid, pkg in result["packages"].items():
        print(f"{pid}: {pkg['status']}")
        for item in pkg["files"]:
            if item.get("pass") is False:
                print(f"  {item['path']}: {item.get('error')}")

    if args.mode == "baseline":
        print(
            f"TOTAL BASELINE: {'CONSISTENT' if result['contract_consistent'] else 'INVALID'}; "
            f"pending={result['pending_count']}; invalid_json={result['invalid_json_count']}; "
            "semantic_review_required=true"
        )
        return 0 if result["contract_consistent"] else 1

    print(
        f"TOTAL DELIVERY: {'STRUCTURAL PASS' if result['delivery_structural_pass'] else 'STRUCTURAL FAIL'}; "
        f"missing={result['missing_count']}; empty={result['empty_count']}; "
        f"invalid_json={result['invalid_json_count']}; semantic_review_required=true"
    )
    return 0 if result["delivery_structural_pass"] and result["contract_consistent"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
