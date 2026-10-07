# Branch Reconciliation — 2026-10-07

Baseline inspected: `main` at `3610b370d62fb0daa86b10f819b7704ab096809b`.

> **2026-10-08 supersession note:** the ahead/behind counts below are a historical 2026-10-07 snapshot. Current exact branch heads and relations to canonical `main` are pinned in `context/QUARANTINED_BRANCH_INDEX_2026-10-08.md` / `build/prepared/quarantined_branch_index_20261008.json`. Use that index for current decisions.

Rule: branch-only work is evidence/candidate state, not verified canonical runtime state. Do not wholesale-merge divergent branches into `main`; review/cherry-pick coherent documentation, manifests, or validated implementation only after ownership and runtime gates are satisfied.

## Current branch relationships to main

| Branch | Relation to main | Coordination interpretation |
|---|---:|---|
| prep/gmod-dependency-evidence-20261007 | identical | Safe empty preparation base; no unique work yet. |
| prep/astra-prompt4-workflow | +7 / -13 | Legacy GPT-6/Astra workflow documentation. Preserve only useful technical evidence; do not dispatch to GPT-6/Astra. |
| prep/code-preservation-20 | +135 / -43 | Large support/preparation lane. Contains tracker, regression packs, source/provenance tooling and many handoffs missing on main. Do not merge wholesale. |
| prep/pre-opus-thursday | +184 / -43 | Very large later candidate history including v84-v91-era THUG2/UI/animation evidence. Branch-only until reconciled and validated. |
| runtime/astra-phase1-input92 | +63 / -55 | Legacy-named runtime candidate containing v92 input work and v84-v91 history. Not canonical main runtime. Codex owns any future runtime validation after deliberate reconciliation. |
| feature/thug2-native-ui-g6 | +53 / -55 | Specialist THUG2 UI/animation candidate. Treat as implementation evidence, not validated completion. |
| diag/v85-retarget-quarantine | +4 / -55 | Diagnostic v84/v85 branch. Preserve failure evidence; not current canonical implementation. |
| prep/gmod-weapon-props | +13 / -55 | Older model/prop staging branch. Useful inventory evidence; reconcile before reuse. |
| prep/opus-feed-bundle-20261006 | +34 / -13 | Prepared Opus feed bundle. Review against current ownership split and latest main evidence before dispatch. |
| prep/prop-content-phase3 | +143 / -43 | Large support prop-content branch. Selective artifacts only. |
| prep/prop-content-phase4 | +183 / -43 | Later support prop-content branch. Selective artifacts only. |
| prep/support-workflow | +127 / -43 | Large support workflow branch. Contains durable preparation not present on main. Review selectively. |
| support/combine-armor-autogive-20261006 | +10 / -13 | Separate Combine-armor support work. Keep isolated from core merge reconciliation. |
| support/goodsprings-deathclaw-response-20261007 | +19 / -13 | Separate encounter/support feature. Keep isolated from core GMod/THUG2 integration. |

## Important conflicts discovered

1. `main/context/CURRENT_STATE.md` still describes the verified active runtime around v81/v82 plus 2026-10-06 human observations.
2. Diverged branches contain v84-v92 implementation/evidence. Those newer labels do **not** automatically supersede main because they are unmerged and not uniformly human-validated.
3. `context/HANDOFFS/GPT6_OPUS_READINESS_2026-10-06.md` on main references handoffs such as `ASTRA_GMOD_QMENU.md`, `ASTRA_TOOLGUN.md`, and `ASTRA_PHYSGUN.md`; equivalent files exist on large diverged support branches but are absent from main.
4. `context/SUPPORT_20_POINT_TRACKER.md` is absent from main but exists on `prep/code-preservation-20`, where it reports support preparation largely complete. Treat it as branch evidence until selectively reconciled.
5. Historical `GPT6_OPUS`, `ASTRA_*`, `runtime/astra-*`, and `*-g6` labels are obsolete ownership labels. Technical evidence may remain useful, but new work must be remapped via `context/AGENT_OWNERSHIP.md`: Codex investigates/tests, Opus implements.

## Reconciliation policy

- Never promote a branch-only runtime version by version number alone.
- Compare source hashes, parent build, manifests, validation output and human playtest evidence.
- Preserve failure knowledge before cherry-picking a fix.
- Prefer small cherry-picks or recreated coordination documents over merging large divergent histories.
- Do not touch active Opus implementation or legacy specialist/runtime branches from the workflow lane. GPT-6/Astra is not used; Codex owns future runtime validation.
