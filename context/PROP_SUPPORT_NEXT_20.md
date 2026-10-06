# Prop-focused non-Astra / non-Opus next 20

Purpose: keep progressing the mashup through safe, reproducible prop/content work without modifying Astra v88, THUG2 runtime code, the real Q-menu runtime or native Tool Gun/Physgun mechanics.

Status legend: COMPLETE = support/static preparation finished; IN PROGRESS = useful prep exists but human or model-review work remains; PENDING = not started or intentionally waits for earlier gates.

1. **Reconcile prop source truth — COMPLETE.** Canonical working set is 290 ready props (170 FNV + 120 GMod/Source) plus 106 THUG2 targets, of which 85 are spatial geometry candidates.
2. **Build a unified per-prop quality ledger — COMPLETE.** Form binding, dimensions, thumbnail coverage, collision/material evidence, utility and runtime-pending state are recorded for all 290.
3. **Detect likely duplicate/variant clutter — COMPLETE.** Variant groups are flagged for review only; nothing is auto-removed.
4. **Score props for skate usefulness — COMPLETE.** Rails/ramps/ledges/stairs receive highest utility, then benches/beams/barriers/physics clutter.
5. **Set the compact-menu growth budget — COMPLETE.** Keep the player-facing browser at 300–320; first target is 310 by promoting up to 20 validated THUG2 props.
6. **Audit GMod prop collision/mobility evidence — COMPLETE STATIC.** All 120 curated GMod props retain conversion collision evidence; source mass is recorded for mobility review.
7. **Audit GMod prop scale outliers — COMPLETE STATIC.** Category-specific size limits are rechecked; flagged entries require human in-game scale confirmation rather than automatic rescaling.
8. **Audit GMod material dependencies — COMPLETE STATIC.** Unique referenced material payloads are hashed and missing paths are recorded.
9. **Audit FNV form/content dependencies — COMPLETE STATIC.** Each native prop keeps plugin/FormID/EDID plus a path-based content hint for later load-order testing.
10. **Check category balance and weak spots — COMPLETE.** Current ready counts and source/category distribution are machine-recorded for future swaps.
11. **Build representative human prop test batches — COMPLETE PREP.** 56 representative props are split into 5 batches covering all source/category groups plus size extremes.
12. **Preserve stable spawn identity for testing — COMPLETE PREP.** Every test row carries plugin, file FormID and EDID; final console load-order prefix must be resolved at test time.
13. **Keep support sidecars isolated — COMPLETE PREP.** Prop catalog sidecar stays disabled outside its dedicated test pack.
14. **Create the 290-prop runtime validation ledger — COMPLETE PREP.** Spawn/scale/material/collision/contact/cleanup fields all begin pending human validation.
15. **Rank THUG2 geometry candidates for extraction review — COMPLETE.** All 85 spatial candidates are ranked by category usefulness, confidence, leaf count and spatial distance.
16. **Prepare the first THUG2 prop visual-review packet — COMPLETE PREP.** Top 20 candidates are listed with source level, position, candidate leaf IDs, bounds and triangle evidence. Actual splitting/conversion remains model work.
17. **Build a replacement reserve for later THUG2 promotion — COMPLETE PREP.** 40 lower-utility/redundancy candidates are ranked; no existing prop is removed yet.
18. **Audit native GMod SpawnIcon coverage — COMPLETE.** Native mounted spawnicons found for the curated set: 0/120; all 120 GMod entries retain generated geometry-preview fallback.
19. **Build prop release/provenance metadata — COMPLETE.** Phase-3 outputs are folded into the release manifest and unified support validator; release support-manifest count is 15.
20. **Validate, record and push this prop phase to GitHub — READY TO PUSH.** Prop validator passes 52 checks with zero errors and unified support validator passes 111; docs/build manifest are recorded locally. Final gate is GitHub branch verification.

## Immediate human gates
- Run the five representative prop batches with preflight/postflight capture.
- Do not call scale/collision/playability verified until observed in Fallout.
- Do not enable REM_GModProps_Catalog.esp except for its isolated test.
- THUG2 top-20 entries are review targets only, not yet standalone spawnable props.

## Machine-readable outputs
- build/prepared/prop_support_phase3/catalog_quality_ledger.json
- build/prepared/prop_support_phase3/redundancy_audit.json
- build/prepared/prop_support_phase3/category_balance.json
- build/prepared/prop_support_phase3/gmod_prop_dependency_audit.json
- build/prepared/prop_support_phase3/fnv_prop_dependency_hints.json
- build/prepared/prop_support_phase3/runtime_test_batches.json
- build/prepared/prop_support_phase3/runtime_validation_ledger.json
- build/prepared/prop_support_phase3/thug2_promotion_queue.json
- build/prepared/prop_support_phase3/menu_budget.json
- build/prepared/prop_support_phase3/gmod_spawnicon_coverage.json
- build/prepared/prop_support_phase3/prop_payload_provenance.json