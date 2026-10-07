# Selective Branch Reconciliation Plan — 2026-10-07

Current ownership: Codex investigates and runtime-validates; Claude Opus alone implements; normal GPT coordinates. Legacy GPT-6/Astra labels are historical only.

## Classification rules

- CHERRY-PICK CANDIDATE — durable evidence/manifests that remain useful after current hash/path checks and ownership normalization.
- KEEP BRANCH-ONLY — useful but tied to a historical branch/workspace snapshot.
- NEEDS REVIEW — useful but contains claims, paths, ownership or runtime assumptions requiring reconciliation.
- RUNTIME CANDIDATE ONLY — implementation/build state requiring Codex runtime validation before canonical promotion.
- HISTORICAL FAILURE EVIDENCE — preserve for debugging, never as current implementation truth.
- SUPERSEDED — current coordination documents already replace its workflow/ownership purpose.

## prep/code-preservation-20

| Artifact | Classification | Reason / action |
|---|---|---|
| context/SUPPORT_20_POINT_TRACKER.md | NEEDS REVIEW | Strong support inventory, but obsolete Astra/Opus ownership and branch-snapshot completion claims. Mine facts into current indexes; do not promote unchanged. |
| context/REGRESSION_PACKS.md | SUPERSEDED for ownership; historical test source | Current CODEX_RUNTIME_TEST_PACKS replaces Astra ownership and broadens testing. Preserve old preflight procedures as source material. |
| context/RUNTIME_OWNERSHIP_CONTRACT.md | CHERRY-PICK CANDIDATE after wording check | State ownership remains useful; current INPUT_OWNERSHIP_MATRIX is more explicit. Promote invariants selectively. |
| context/THUG2_INTEGRATION_PROVENANCE.json | CHERRY-PICK CANDIDATE after local hash re-check | High-value executable/skeleton/IDA 6.8 provenance and bone-name map. |
| context/GMOD_INTERFACE_PRESERVATION.md | CHERRY-PICK CANDIDATE after ownership normalization | High-value installed-GMod provenance and interface contracts. Feed C01-C03. |
| context/RELEASE_MANIFEST.md | RUNTIME CANDIDATE ONLY — INDEXED/QUARANTINED | v85/v88 identities are preserved in PROVENANCE_INDEX/EVIDENCE_INDEX and RUNTIME_CANDIDATE_QUARANTINE; they do not change canonical runtime state. |
| GMod/HL weapon staging audit | INDEXED PROVENANCE / SOURCE MANIFEST REMAINS BRANCH-ONLY | Identical Git blob corroborated across inspected later prep branches; 71/71 concrete refs staged. Current local hash check still required before implementation; runtime presentation unverified. |
| Q-menu source inventory | INDEXED PROVENANCE / SOURCE MANIFEST REMAINS BRANCH-ONLY | Identical Git blob corroborated across inspected later prep branches; 105 Lua / 46 VGUI / 29 refs. Current installed-GMod hash check still required; not runtime proof. |
| support validators/preflight/postflight scripts | CHERRY-PICK CANDIDATE | Reusable project tooling if current paths/hashes remain valid. |
| disabled sidecar plugins/manifests | KEEP BRANCH-ONLY / RUNTIME CANDIDATE ONLY | Static pass is not runtime proof. |
| THUG2 embedded-prop mapping | NEEDS REVIEW | 85 geometry candidates are evidence-backed; visual verification/conversion/collision remain Opus + Codex gates. |

## prep/opus-feed-bundle-20261006

| Artifact | Classification | Reason / action |
|---|---|---|
| feed_bundle/FEED_MANIFEST.json | NEEDS REVIEW | Useful Opus feed snapshot; legacy gpt6_opus path and old Astra fields must not define ownership. Verify source hash before dispatch. |
| feed_bundle/OPUS_START_PROMPT.md | SUPERSEDED as orchestration prompt | Current ownership/work-package system supersedes it. Reuse technical references only. |
| feed_bundle/ASSET_REFERENCE_INDEX.json | CHERRY-PICK CANDIDATE after current hash re-check | High-value asset hashes/provenance. |
| pre_opus_20261006/physgun_provenance_gap.json | CHERRY-PICK CANDIDATE / ACTIVE BLOCKER | Unresolved v_physics triplet and do-not-substitute policy remain active until C03 resolves them. |
| per-weapon source packets | KEEP BRANCH-ONLY until package selection | Useful Opus inputs; no need to promote all large artifacts before selected implementation work. |
| human playtest checklists | SUPERSEDED / source material | Current Codex runtime packs own future testing. |

## Specialist/runtime branches

| Branch/artifact family | Classification | Rule |
|---|---|---|
| runtime/astra-phase1-input92 | RUNTIME CANDIDATE ONLY — QUARANTINED | Registered in RUNTIME_CANDIDATE_QUARANTINE. Codex must reconcile exact branch/commit/build/hashes before deciding whether it is worth testing. |
| feature/thug2-native-ui-g6 | RUNTIME CANDIDATE ONLY — QUARANTINED | Registered in RUNTIME_CANDIDATE_QUARANTINE. Mine technical evidence selectively; no canonical completion claim. |
| diag/v85-retarget-quarantine | HISTORICAL FAILURE EVIDENCE — QUARANTINED | Registered in RUNTIME_CANDIDATE_QUARANTINE; preserve crash/retarget history for regression design, not release state. |
| prep/pre-opus-thursday | NEEDS REVIEW | Large later history; extract manifests selectively, never wholesale merge. |
| prep/prop-content-phase3/phase4 | NEEDS REVIEW | Extract provenance/catalog/validation artifacts selectively. |
| prep/support-workflow | NEEDS REVIEW | Useful support docs but overlaps other lanes and contains obsolete ownership wording. |
| support/combine-armor-autogive-20261006 | KEEP BRANCH-ONLY | Separate feature lane. |
| support/goodsprings-deathclaw-response-20261007 | KEEP BRANCH-ONLY | Separate encounter lane. |

## Canonicalization order

1. Codex/local preflight re-checks installed GMod, THUG2 executable, FNV skeleton and active runtime hashes.
2. Promote small evidence/provenance manifests that still match.
3. Normalize ownership wording during promotion.
4. Do not promote v84-v92 runtime claims until Codex identifies an exact candidate and validates it.
5. Never merge entire support/specialist branches merely to obtain a handful of manifests.
6. Update EVIDENCE_INDEX, PROVENANCE_INDEX, FAILURE_LEDGER and CURRENT_STATE only when evidence changes verified truth.

## Immediate downstream effect

This reconciliation does not bypass C01-C08. It reduces rediscovery by telling Codex which branch artifacts are trusted inputs, historical sources or runtime candidates.


## Reconciliation update — Opus readiness finalization

The remaining high-value prop-content branch evidence has now been selectively mined into `PROVENANCE_INDEX.md`.

### prep/prop-content-phase4
- final 290-entry catalog: **INDEXED PROVENANCE**; source manifest remains branch-only;
- 120-entry GMod curated pool: **INDEXED PROVENANCE**; no runtime claim promoted;
- cross-game prop-menu handoff: **INDEXED POLICY/EVIDENCE**;
- 20-item THUG2 diversified wave: **KEEP BRANCH-ONLY / REVIEW CANDIDATES**;
- phase-4 validator results: **STATIC EVIDENCE ONLY**;
- disabled GMod prop sidecar: **KEEP BRANCH-ONLY / RUNTIME CANDIDATE ONLY**.

No THUG2 candidate was promoted. The documented 0-ready/20-blocked sidecar state is preserved as the correct outcome.

### prep/pre-opus-thursday
Useful bench/source-packet and pre-Opus validator evidence remains a valid Opus input source after current-local hash re-check. Historical Astra ownership text is superseded. Do not wholesale merge this branch.

### Remaining reconciliation work
The workflow lane has now reconciled the highest-value provenance needed for Opus planning. Remaining branch work is intentionally deferred until package selection:
- per-weapon source packets;
- large converter/support tooling families;
- candidate-specific sidecars;
- runtime branches requiring Codex validation.

This changes S11 from broad branch archaeology to **package-triggered reconciliation**: reconcile only the assets/manifests needed by the next selected Opus package, with a fresh local hash check.
