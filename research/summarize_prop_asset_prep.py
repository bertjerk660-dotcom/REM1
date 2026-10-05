from pathlib import Path
import argparse
import json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", type=Path, default=Path.cwd())
    args = ap.parse_args()

    root = args.project_root.resolve()
    prep = root / "build/prepared"
    out = root / "build/manifests"
    out.mkdir(parents=True, exist_ok=True)

    gmod = json.loads((prep / "gmod_hl_weapon_models/manifest.json").read_text(encoding="utf-8"))
    fnv = json.loads((prep / "fnv_prop_catalog/manifest.json").read_text(encoding="utf-8"))
    thug = json.loads((prep / "thug2_prop_catalog/manifest.json").read_text(encoding="utf-8"))
    qb = json.loads((prep / "thug2_prop_catalog/qb_prop_keyword_index.json").read_text(encoding="utf-8"))

    summaries = {
        "gmod_hl_actual_weapon_models_summary.json": {
            "purpose": "Actual Source/GMod/Half-Life weapon model package preparation for later Astra integration.",
            "staging_root": "build/prepared/gmod_hl_weapon_models",
            "unique_referenced_models": gmod["unique_referenced_models"],
            "staged_models": gmod["staged_models"],
            "unstaged_models": gmod["unstaged_models"],
            "unstaged": [
                {
                    "model": x["model"],
                    "roles": x["roles"],
                    "weapon_classes": x["weapon_classes"],
                }
                for x in gmod["records"]
                if not x["staged"]
            ],
            "integration_performed": False,
        },
        "fnv_prop_catalog_summary.json": {
            "purpose": "Native FNV environmental/world NIF preparation for later GMod-style spawn-menu registration.",
            "staging_root": "build/prepared/fnv_prop_catalog",
            "archives_scanned": [x["name"] for x in fnv["archives_scanned"]],
            "unique_nif_paths": fnv["unique_nif_paths"],
            "staged_prop_candidates": fnv["staged_prop_candidates"],
            "staged_bytes": fnv["staged_bytes"],
            "category_counts": fnv["category_counts"],
            "tag_counts": fnv["tag_counts"],
            "integration_performed": False,
        },
        "thug2_prop_catalog_summary.json": {
            "purpose": "THUG2 standalone and level-embedded geometry preparation for later GMod-style spawn-menu extraction.",
            "staging_root": "build/prepared/thug2_prop_catalog",
            "standalone_model_count": thug["standalone_model_count"],
            "standalone_converted": thug["standalone_converted"],
            "standalone_failures": [
                {
                    "relative": x["relative"],
                    "returncode": x["conversion"]["returncode"],
                    "error": x["conversion"].get("error"),
                }
                for x in thug["standalone_models"]
                if x["conversion"]["returncode"] != 0 or not x["conversion"]["outputs"]
            ],
            "primary_level_geom_count": thug["primary_level_geom_count"],
            "level_geom_converted": thug["level_geom_converted"],
            "level_qb_decompiled": qb["decompiled_q_files"],
            "keyword_match_lines": qb["match_lines"],
            "keyword_identifiers": qb["unique_keyword_identifiers"],
            "integration_performed": False,
        },
    }

    for name, report in summaries.items():
        (out / name).write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()
