from pathlib import Path
import json,hashlib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
B=ROOT/"build/prepared/prop_support_phase4"
files={
 "leaf_review":"thug2_diversified_leaf_review.json",
 "reserve":"gmod_reserve_pool.json",
 "taxonomy":"menu_taxonomy_v2.json",
 "wave":"thug2_diversified_first_wave.json",
 "promotion":"promotion_plan.json",
 "ledger":"thug2_promotion_validation_ledger.json",
}
data={k:json.loads((B/v).read_text()) for k,v in files.items()}
summary={
 "purpose":"Prop-focused support phase 4: diversify THUG2 first-wave review and build a compact replacement/reserve path without changing runtime code.",
 "current_ready_props":data["taxonomy"]["current_ready_count"],
 "planned_first_wave":data["taxonomy"]["planned_first_wave_count"],
 "gmod_reserve_selected":data["reserve"]["selected_reserve"],
 "gmod_reserve_eligible":data["reserve"]["eligible_after_filters"],
 "thug2_diversified_selected":data["wave"]["selected"],
 "thug2_diversified_categories":data["wave"]["category_counts"],
 "leaf_review_status_counts":data["leaf_review"]["status_counts"],
 "form_reservations":len(data["promotion"]["thug2_form_reservations"]),
 "promotion_ledger_entries":len(data["ledger"]["records"]),
 "runtime_playtest":"not_run",
 "runtime_or_astra_code_modified":False,
}
(B/"summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))