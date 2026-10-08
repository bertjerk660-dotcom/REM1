# Opus handoff — start here (prep set 2026-10-09)

This folder is the cover note and checklist for handing the project to Claude Opus. It is documentation only. No runtime files were changed to produce it.

## Read in this order
1. `01_BASELINE_FREEZE.md` — what is currently deployed, with hashes and load order.
2. `02_THUG2_EVIDENCE_INVENTORY.md` — what THUG2 evidence exists locally and what the GitHub snapshot is missing.
3. `03_FAILURE_EVIDENCE_MAP.md` — each known failure and the evidence to read first.
4. `04_FIRST_TASK_ACCEPTANCE.md` — acceptance criteria per package.
5. `05_REGRESSION_MATRIX.md` — behaviour that must not regress.
6. `06_PHYSGUN_PROVENANCE_GAP.md` — the unresolved Physics Gun model.
Machine-readable hash lists: `thug2_file_hashes.txt`, `thug2_folder_fingerprints.txt`, `v_physics_search.txt`.

## What Opus should start with: O00, not the skate fixes

The governing documents are `context/HANDOFFS/OPUS_LAUNCH_SEQUENCE_2026-10-07.md` and `context/OPUS_READINESS_BOARD.md`. They set the order:

- **O00 — Golden Source bench conversion proof.** READY. This is the first package. It converts one static prop (`models/props_c17/bench01a.mdl`, Half-Life 2) through the Source-to-Fallout mesh, material and collision pipeline in an isolated sidecar. It is a pipeline proof, not a player-facing feature. No weapon conversion starts until it passes its in-game gate.
- **O01 — Toolgun presentation.** Ready only after O00 passes.
- **O02–O04 — Q-menu, Toolgun behaviour, Physgun.** Waiting on Codex evidence closure.
- **O05–O07b — THUG2 movement, camera, animation/attachment, HUD, audio.** Waiting on Codex evidence C04 to C08.

**Clarification on O00:** it is a Golden Source bench, a single Half-Life 2 bench prop. It is not a skate package and not a weapon. It is the test that the asset pipeline works end to end before weapons use it. The readiness board says Opus must not receive anything that treats static conversion success as runtime proof.

## The skate issue, and why it is not tomorrow's first task

The readiness board says the THUG2 packages (O05 to O07b) are WAITING FOR CODEX. Their evidence has not been completed. If you hand Opus the skate fixes first, it would be working against that gate. The failures themselves are real and documented: the Fallout HUD stays on, the board doesn't reach the feet, the animations don't play, and G grinds anywhere (F008, F010, F011). The acceptance criteria for a skate-fix candidate are in `04_FIRST_TASK_ACCEPTANCE.md`, section "Packages O05 to O07".

If you want Opus to work on skate tomorrow anyway, that is the project owner's decision to make, not a documentation one. I'd suggest O00 first, then the skate fixes once the Codex gates are closed.

## Corrections to earlier statements

- The four THUG2 `ASTRA_*` handoffs are present locally. Their absence applied only to the uploaded `REM1-main.zip`.
- The GitHub snapshot is behind the local workspace (see `02`). Commit the context and manifests before handing off, so Opus reads one source.
- The crash attribution to retargeting (F003) is **not proven**. The deployed DLL does not match the v85 manifest, so the 2026-10-09 test cannot be attributed to v85.

## Before anything is handed over

1. Commit `context/` updates, `build/prepared/opus_prep_2026-10-09/` and the handoff docs to one prep branch. Choose the branch name (two are in use).
2. Confirm the DLL was built from `main.cpp` `4517D804...`, or accept the baseline as "unproven build".
3. Re-hash `skateheldx.nif`.
4. Decide: disable sidecars 3 and 4 for the Opus test (recommended).
5. Confirm the O00 scope with Opus and the project owner.

## Open questions for the project owner

- Is O00 the agreed first package, or should the skate fixes go first?
- Which prep branch is canonical?
- Does a fallback for `v_physics` need approval? See `06`.
- Is there a second GMod install or content mount to search?

## Ownership, as stated in the current documents

- Claude Opus: all implementation, visual, model, animation and UI integration.
- Codex: investigation, reverse engineering with IDA Pro 6.8, and runtime validation.
- Normal GPT: coordination, evidence intake, manifests and packets.
Older references to "GPT6_OPUS" and "ASTRA" ownership are historical and not authority.
