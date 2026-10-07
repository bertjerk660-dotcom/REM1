#!/usr/bin/env python3
"""Validate Claude Opus implementation candidate manifests.

Workflow validator only. It never builds, deploys, launches or modifies the game.

Modes:
- preflight: validates package identity, evidence/provenance references, acceptance,
  preservation, runtime-test ownership and rollback intent before implementation.
- freeze: validates exact implementation/candidate identity and hashed outputs before
  the candidate may be handed to Codex for runtime validation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9A-Fa-f]{64}$")
SHA_RE = re.compile(r"^[0-9A-Fa-f]{7,64}$")

def nonempty(v):
    return isinstance(v, str) and bool(v.strip())

def add(errors, condition, message):
    if not condition:
        errors.append(message)

def validate_repo_refs(root: Path | None, paths, errors, field):
    if root is None:
        return
    for p in paths:
        if not isinstance(p, str) or not p.strip():
            errors.append(f"{field}: invalid empty/non-string reference")
            continue
        if not (root / Path(p)).exists():
            errors.append(f"{field}: referenced path does not exist under root: {p}")

def validate_output_hashes(outputs, errors):
    count = 0
    for group, entries in outputs.items():
        if not isinstance(entries, list):
            errors.append(f"outputs.{group}: must be a list")
            continue
        for i, entry in enumerate(entries):
            count += 1
            if not isinstance(entry, dict):
                errors.append(
                    f"outputs.{group}[{i}]: freeze entries must be objects with path and sha256"
                )
                continue
            path = entry.get("path")
            sha = entry.get("sha256")
            add(errors, nonempty(path), f"outputs.{group}[{i}].path missing")
            add(errors, isinstance(sha, str) and bool(SHA256_RE.match(sha)),
                f"outputs.{group}[{i}].sha256 must be 64 hex chars")
    return count

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--mode", choices=("preflight", "freeze"), default="preflight")
    ap.add_argument("--root", help="Optional project root used to verify repo-relative references")
    ap.add_argument("--report", help="Optional JSON validation report")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = Path(args.root) if args.root else None
    errors = []

    add(errors, data.get("schema") == "rem.opus_implementation_candidate.v1",
        "schema must be rem.opus_implementation_candidate.v1")
    add(errors, nonempty(data.get("package_id")), "package_id missing")
    add(errors, nonempty(data.get("package_name")), "package_name missing")
    add(errors, nonempty(data.get("goal")), "goal missing")
    add(errors, data.get("owner") == "Claude Opus", "owner must be Claude Opus")

    src = data.get("source_identity", {})
    add(errors, nonempty(src.get("main_source_path")), "source_identity.main_source_path missing")
    add(errors, isinstance(src.get("main_source_sha256"), str)
        and bool(SHA256_RE.match(src.get("main_source_sha256", ""))),
        "source_identity.main_source_sha256 must be 64 hex chars")
    prov = src.get("required_provenance_files", [])
    add(errors, isinstance(prov, list) and len(prov) > 0,
        "source_identity.required_provenance_files must be non-empty")
    if isinstance(prov, list):
        validate_repo_refs(root, prov, errors, "source_identity.required_provenance_files")

    inputs = data.get("inputs", {})
    for key in ("asset_packets", "failure_knowledge", "acceptance_rows",
                "preserved_working_behavior"):
        val = inputs.get(key)
        add(errors, isinstance(val, list) and len(val) > 0,
            f"inputs.{key} must be non-empty")
    if isinstance(inputs.get("asset_packets"), list):
        validate_repo_refs(root, inputs["asset_packets"], errors, "inputs.asset_packets")

    validation = data.get("validation", {})
    add(errors, validation.get("runtime_owner") == "Codex",
        "validation.runtime_owner must be Codex")
    add(errors, nonempty(validation.get("runtime_test_pack")),
        "validation.runtime_test_pack missing")
    if nonempty(validation.get("runtime_test_pack")):
        validate_repo_refs(root, [validation["runtime_test_pack"]], errors,
                           "validation.runtime_test_pack")

    promotion = data.get("promotion", {})
    add(errors, promotion.get("canonical_state_updated") is False,
        "promotion.canonical_state_updated must remain false before runtime validation")
    add(errors, nonempty(promotion.get("reason")), "promotion.reason missing")

    runtime = data.get("runtime_identity", {})
    add(errors, nonempty(runtime.get("required_mode_state")),
        "runtime_identity.required_mode_state missing")

    rollback = data.get("rollback", {})
    add(errors, isinstance(rollback.get("backup_paths"), list), "rollback.backup_paths must be list")
    add(errors, isinstance(rollback.get("previous_hashes"), dict),
        "rollback.previous_hashes must be object")

    if args.mode == "freeze":
        for key in ("parent_branch", "implementation_branch"):
            add(errors, nonempty(data.get(key)), f"{key} missing")
        for key in ("parent_commit", "implementation_commit"):
            v = data.get(key, "")
            add(errors, isinstance(v, str) and bool(SHA_RE.match(v)),
                f"{key} must be a git SHA")

        changes = data.get("changes")
        add(errors, isinstance(changes, list) and len(changes) > 0,
            "changes must be non-empty at freeze")

        outputs = data.get("outputs", {})
        add(errors, isinstance(outputs, dict), "outputs must be object")
        output_count = validate_output_hashes(outputs if isinstance(outputs, dict) else {}, errors)
        add(errors, output_count > 0, "at least one hashed output artifact is required at freeze")

        for key in ("plugins_txt", "loadorder_txt"):
            val = runtime.get(key)
            add(errors, isinstance(val, list) and len(val) > 0,
                f"runtime_identity.{key} must be non-empty at freeze")
        add(errors, nonempty(runtime.get("test_save")), "runtime_identity.test_save missing at freeze")
        add(errors, nonempty(runtime.get("test_location")),
            "runtime_identity.test_location missing at freeze")

        for key in ("build", "static", "asset_reference_resolution"):
            val = validation.get(key)
            add(errors, nonempty(val) and val.lower() not in {"pending", "not_run", "unknown"},
                f"validation.{key} must be resolved before freeze")
        add(errors, validation.get("runtime_status") in {"not_run", "pending"},
            "validation.runtime_status must be not_run/pending before Codex execution")

        has_rollback = (
            bool(rollback.get("backup_paths"))
            or nonempty(rollback.get("revert_commit"))
            or bool(rollback.get("previous_hashes"))
        )
        add(errors, has_rollback, "rollback plan must contain backup_paths, previous_hashes or revert_commit")

    report = {
        "schema": "rem.opus_candidate_manifest_validation.v1",
        "manifest": str(manifest_path),
        "mode": args.mode,
        "pass": not errors,
        "error_count": len(errors),
        "errors": errors,
    }

    if args.report:
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"{args.mode.upper()}: {'PASS' if not errors else 'FAIL'}; errors={len(errors)}")
    for e in errors:
        print(f"- {e}")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
