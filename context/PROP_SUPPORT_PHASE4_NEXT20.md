# Prop-focused next 20 — phase 4

Purpose: continue useful prop/environment work without touching Astra/Opus-owned THUG2 runtime, animation, camera, real GMod Q-menu runtime or native Tool Gun/Physgun mechanics.

Status legend: COMPLETE = reproducible support work finished; COMPLETE PREP = support side is finished but a human/Astra gate remains; HUMAN GATE = requires visual/in-game confirmation; ASTRA GATE = reserved model/runtime integration.

1. **Reconcile prop source truth — COMPLETE.** Phase 4 is based on the verified phase-3 set: 290 ready props (170 FNV + 120 GMod/Source), plus the 106 THUG2 target archive.
2. **Protect runtime/Astra state — COMPLETE.** Installed v85, main ESP and isolated v88 hashes remain unchanged; no runtime code was modified.
3. **Diversify the THUG2 first-wave review set — COMPLETE.** 20 candidates: 6 rails, 5 ramps, 4 ledges, 2 benches/tables, 2 fences/pipes and 1 stairs/platform target.
4. **Render actual THUG2 candidate-leaf previews — COMPLETE.** All 20 diversified candidates have converted-level GLB geometry previews and leaf metrics.
5. **Score THUG2 leaf isolation/complexity — COMPLETE.** 13 high-priority + 7 medium-priority, 0 complex; none are auto-promoted.
6. **Build a compact GMod reserve pool — COMPLETE.** 80 reserve props selected from 797 eligible converted/collision-bearing candidates, balanced across 8 useful categories.
7. **Unify the cross-game prop taxonomy — COMPLETE.** Current 290 + hidden future THUG2 entries map to source-neutral skate/physics/environment/street buckets for the future real GMod Q-menu adapter.
8. **Reserve future THUG2 form metadata safely — COMPLETE PREP.** 20 future local IDs/EDIDs are reserved; no live ESP records were created.
9. **Build THUG2 material provenance — COMPLETE.** Material/image references are recorded for all 20/20 diversified leaf candidates.
10. **Assign collision strategy per THUG2 candidate — COMPLETE PREP.** 16 are planned as static skate obstacles and 4 as static environment props; Physgun mobility is not inferred from level geometry.
11. **Split visually confirmed THUG2 objects from level geometry — HUMAN GATE.** Preview identity must be confirmed first; no split is considered validated yet.
12. **Convert confirmed THUG2 standalone objects to FNV NIF — ASTRA/MODEL GATE.** Preserve original geometry/material identity and independently validate scale/collision.
13. **Build the 310-entry category balance plan — COMPLETE.** Deficits are [('Skate / Ramps & Stairs', 3), ('Skate / Ledges & Barriers', 1), ('Environment / Utility', 2)]; excesses are [('Skate / Benches & Tables', 5)].
14. **Map every default prop to reserve replacements — COMPLETE.** All 290 ready props have 3 ranked GMod reserve fallbacks.
15. **Generate final thumbnails for promoted THUG2 standalone props — PENDING BY DESIGN.** This begins only after a validated standalone NIF exists; current leaf previews are review evidence only.
16. **Expand runtime test batches with reserve fallbacks — COMPLETE PREP.** 56 representative test props in 5 batches now carry two reserve fallbacks each.
17. **Prepare the THUG2 prop sidecar builder — COMPLETE PREP / SAFELY BLOCKED.** Builder status is blocked_no_validated_candidates with 0 ready / 20 blocked; it refuses to create an ESP until promotion gates pass.
18. **Run prop phase-4 validation — COMPLETE.** 66 checks pass with zero errors. This is static/preflight evidence, not gameplay validation.
19. **Integrate prop phase 4 into release/support metadata — COMPLETE.** Release index now tracks 17 support manifests; unified support validator passes 112 checks with zero errors.
20. **Push and verify the phase-4 GitHub branch — READY FOR FINAL SYNC.** Upload the latest scripts/docs/build manifests to prep/prop-content-phase4, verify the diff against phase 3, then mark this complete.

## Current prop numbers
- Ready player-facing catalog: 290.
- Planned first-wave total if all 20 THUG2 candidates eventually pass: 310.
- GMod reserve: 80 selected from 797 eligible filtered candidates.
- THUG2 diversified wave: 20 ({'Skate - Rails Handrails': 6, 'Skate - Quarterpipes Halfpipes Ramps': 5, 'Skate - Ledges Hubbas Curbs': 4, 'Street - Benches Tables Chairs': 2, 'Street - Fences Barriers Poles Pipes': 2, 'Skate - Stairs Platforms Misc': 1}).
- Leaf-review status: {'high_review_priority': 13, 'medium_review_priority': 7, 'complex_review': 0}.
- Prop phase-4 validator: 66 / zero errors.
- Unified support validator: 112 / zero errors.
- Runtime playtest: NOT RUN for phase 4.

## Remaining gates that cannot be honestly marked complete here
- Human visual confirmation that each chosen GLB leaf is the intended THUG2 object.
- Standalone object splitting and source-faithful model conversion for confirmed THUG2 candidates.
- In-game prop scale/material/collision/contact/cleanup testing.
- Real GMod Q-menu runtime and native Tool Gun/Physgun behavior remain Astra-owned.