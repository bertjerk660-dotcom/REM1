import json, os
root = r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2"
p = os.path.join(root, "build", "prepared", "thug2_prop_catalog", "target_classification.json")
j = json.load(open(p, encoding="utf-8"))
rows = [x for x in j["records"] if x.get("confidence") == "not_ready"]
semantic = [x for x in rows if x["classification"] == "semantic_or_gap_identifier"]
named = [x for x in rows if x["classification"] == "unresolved_named_target"]
out = {
  "source": "build/prepared/thug2_prop_catalog/target_classification.json",
  "original_not_ready_count": len(rows),
  "semantic_non_prop_count": len(semantic),
  "named_without_geometry_binding_count": len(named),
  "extractable_geometry_from_unresolved": 0,
  "resolution": "Remove all 21 from the extractable-prop queue unless later original-game evidence binds an entry to a LevelGeometry component. The existing 85 spatial_geometry_candidate records remain the embedded geometry extraction pool.",
  "semantic_non_props": semantic,
  "named_without_geometry_binding": named
}
op = os.path.join(root, "build", "prepared", "prop_support_phase4", "thug2_21_resolution.json")
json.dump(out, open(op, "w", encoding="utf-8"), indent=2)
print(json.dumps({k:out[k] for k in ("original_not_ready_count","semantic_non_prop_count","named_without_geometry_binding_count","extractable_geometry_from_unresolved")}, indent=2))

[executed on device: DESKTOP-6PTSS3D (ac6e0673-c817-443f-a58e-9e6494209436)]