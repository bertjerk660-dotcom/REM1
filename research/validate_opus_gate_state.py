#!/usr/bin/env python3
"""Check that Opus package unlock states do not outrun reviewed Codex evidence.

This is a workflow consistency validator. It never changes readiness state and never
treats file presence as semantic evidence completion.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

COMPLETE = "COMPLETE"

DEPENDENCIES = {
    "O02": ["C01"],
    "O03": ["C01", "C02"],
    "O04": ["C03"],
    "O05": ["C04", "C08"],
    "O05b": ["C05"],
    "O06": ["C06"],
    "O07": ["C07"],
    "O07b": [],
}

READY_STATES = {
    "READY_FOR_OPUS",
    "READY",
    "READY_WITH_PREFLIGHT",
}

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate-matrix", required=True)
    ap.add_argument("--semantic-status", required=True)
    ap.add_argument("--report")
    args = ap.parse_args()

    matrix = load(args.gate_matrix)
    semantic = load(args.semantic_status)
    gates = semantic.get("gates", {})
    packages = matrix.get("packages", {})
    errors = []
    notes = []

    for package_id, reqs in DEPENDENCIES.items():
        pkg = packages.get(package_id)
        if pkg is None:
            errors.append(f"{package_id}: missing from gate matrix")
            continue
        status = str(pkg.get("status", ""))
        complete = [g for g in reqs if gates.get(g, {}).get("status") == COMPLETE]
        missing = [g for g in reqs if g not in complete]

        if status in READY_STATES and missing:
            errors.append(
                f"{package_id}: status={status} but reviewed gates not COMPLETE: {', '.join(missing)}"
            )
        elif not missing and reqs and status not in READY_STATES:
            notes.append(
                f"{package_id}: all structural semantic dependencies COMPLETE; normal GPT should review/finalize packet before changing package state"
            )

    # Special rules that are not purely C01-C08.
    o00 = packages.get("O00", {})
    if o00.get("status") != "READY_FOR_OPUS":
        errors.append("O00: expected READY_FOR_OPUS in current preparation baseline")

    for pid in ("O01", "O08a", "O08b", "O08c"):
        pkg = packages.get(pid, {})
        if pkg.get("status") not in {"READY_AFTER_O00_PASS", "READY_FOR_OPUS"}:
            errors.append(f"{pid}: unexpected visual package state {pkg.get('status')!r}")

    earned = 0
    points = {"C01":3,"C02":3,"C03":3,"C04":3,"C05":2,"C06":2,"C07":2,"C08":1}
    for gate, value in points.items():
        st = gates.get(gate, {})
        declared = st.get("points_earned", 0)
        expected = value if st.get("status") == COMPLETE else 0
        if declared != expected:
            errors.append(
                f"{gate}: points_earned={declared}, expected={expected} for status={st.get('status')}"
            )
        earned += expected

    declared_total = semantic.get("total_points_earned_from_c01_c08")
    if declared_total != earned:
        errors.append(
            f"semantic total points={declared_total}, expected={earned} from reviewed COMPLETE gates"
        )

    baseline = 81
    report = {
        "schema":"rem.opus_gate_state_validation.v1",
        "pass": not errors,
        "baseline_preparation_readiness": baseline,
        "semantic_gate_points_earned": earned,
        "computed_preparation_readiness": baseline + earned,
        "errors": errors,
        "notes": notes,
    }

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"GATE STATE: {'PASS' if not errors else 'FAIL'}; readiness={baseline + earned}/100; errors={len(errors)}")
    for e in errors:
        print(f"- ERROR: {e}")
    for n in notes:
        print(f"- NOTE: {n}")
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
