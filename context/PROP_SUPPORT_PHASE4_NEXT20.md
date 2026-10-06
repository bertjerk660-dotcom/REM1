# Prop-focused next 20 — phase 4

Purpose: continue useful prop/environment work without touching Astra/Opus-owned THUG2 runtime, animation, camera, real GMod Q-menu runtime or native Tool Gun/Physgun mechanics.

Status legend: COMPLETE = reproducible support work finished; IN PROGRESS = useful evidence exists but more support work remains; HUMAN GATE = requires in-game/visual confirmation; ASTRA GATE = reserved high-risk runtime/model integration.

1. Reconcile the prop source of truth from GitHub and local manifests — COMPLETE. Phase 3 remains 290 ready props + 106 THUG2 targets; phase 4 branches from prep/prop-content-phase3.
2. Protect the active runtime before prop work — COMPLETE. v85, the main ESP and isolated v88 hashes were rechecked; no runtime/Astra code was modified.
3. Replace the rail-heavy THUG2 top-20 with a diversified first-wave review set — COMPLETE. New quota: 6 rails, 5 ramps, 4 ledges, 2 benches/tables, 2 fences/pipes and 1 stairs/platform target.
4. Render actual candidate-leaf previews for the diversified THUG2 wave — COMPLETE. 20 review previews generated from converted level GLB leaf geometry.
5. Score THUG2 leaf isolation/complexity — COMPLETE. 13 high-priority and 7 medium-priority candidates; none are auto-promoted.
6. Build a practical GMod reserve library — COMPLETE. 80 extra converted/collision-bearing props selected from 797 eligible non-default candidates, balanced 10 per category.
7. Unify the cross-game prop taxonomy for the real Q-menu adapter — COMPLETE. Current 290 entries and the planned THUG2 first wave map into source-neutral skate/physics/environment/street buckets.
8. Reserve THUG2 prop form metadata without creating live records — COMPLETE. 20 future REM_THUG2Props_Catalog.esp IDs/EDIDs are reserved only; no ESP records were written.
9. Build per-candidate THUG2 material provenance — PENDING. Record material slots/texture references from each selected GLB leaf before extraction.
10. Assign collision strategy per THUG2 candidate — PENDING. Rails/ramps/ledges normally remain static skate obstacles; movable treatment requires explicit evidence and separate testing.
11. Create standalone extraction packages for the visually confirmed THUG2 leaves — HUMAN GATE. Do not split geometry until the preview is confirmed to match the named source object.
12. Convert confirmed THUG2 standalone props to FNV NIF — ASTRA/MODEL GATE. Keep original source geometry/material identity and validate scale/collision independently.
13. Build a category deficit/excess report for the 310-entry target — IN PROGRESS. Taxonomy counts exist; convert them into explicit swap/add targets before promotion.
14. Map each failed/default prop to a reserve replacement — PENDING. Use the 80-item GMod reserve instead of returning to the full 7,507/13,003-model archives.
15. Generate final thumbnails for promoted THUG2 props — PENDING. Only after a standalone NIF exists; support previews are not native GMod SpawnIcons.
16. Expand runtime prop test batches with reserve fallbacks — PENDING. Add one reserve candidate behind every representative default item that fails scale/material/collision tests.
17. Prepare the THUG2 sidecar schema/build script — IN PROGRESS. Form IDs/EDIDs are reserved; actual sidecar generation waits for validated NIFs.
18. Run phase-4 static/preflight validation — COMPLETE. 46 checks pass with zero errors; this is not gameplay validation.
19. Record phase-4 manifests/docs and integrate with release/support metadata — IN PROGRESS. Local phase-4 summary, review packet, reserve pool and promotion ledgers exist; GitHub artifact index/update is next.
20. Push and verify the prop phase-4 branch — IN PROGRESS. Upload tooling/docs/manifests to prep/prop-content-phase4, verify branch diff, and leave Astra/runtime branches untouched.

Current prop numbers:
- Ready player-facing catalog: 290.
- Planned first-wave catalog if all 20 THUG2 candidates eventually pass: 310.
- GMod reserve: 80 selected from 797 eligible filtered candidates.
- THUG2 diversified review set: 20 ({'Skate - Rails Handrails': 6, 'Skate - Quarterpipes Halfpipes Ramps': 5, 'Skate - Ledges Hubbas Curbs': 4, 'Street - Benches Tables Chairs': 2, 'Street - Fences Barriers Poles Pipes': 2, 'Skate - Stairs Platforms Misc': 1}).
- THUG2 leaf review: {'high_review_priority': 13, 'medium_review_priority': 7, 'complex_review': 0}.
- Runtime playtest: NOT RUN for phase 4.

Immediate safe work after this checkpoint:
- Material provenance for the 20 THUG2 leaves.
- Collision-strategy ledger for the 20 THUG2 leaves.
- 310-entry category deficit/excess plan.
- Default-to-reserve fallback mapping.
- Phase-4 GitHub artifact index and branch verification.