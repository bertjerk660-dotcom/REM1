# Runtime Candidate Quarantine Registry — 2026-10-07

Purpose: retain later runtime/build evidence without allowing an unvalidated candidate to become canonical merely because its version number or branch is newer.

## Rules

A quarantined candidate may be inspected by Codex and used as historical/debug evidence. It may not update `CURRENT_STATE.md`, milestone completion, or "validated" claims until:
1. exact branch and commit are identified;
2. active source hash is recorded;
3. DLL and ESP hashes are recorded and matched to the tested files;
4. asset-manifest/load-order identity is recorded;
5. Codex runs the applicable deterministic runtime pack;
6. failures are resolved by Opus and regressed by Codex;
7. workflow review deliberately promotes the result.

## Registry

| Candidate / evidence | Branch/source | Recorded identity | Quarantine reason | Required resolution |
|---|---|---|---|---|
| v85 installed snapshot | prep/prop-content-phase4 and prep/support-workflow release ledgers | DLL BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41; ESP 0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7 | branch-only install claim conflicts with older canonical verified state; no current Codex runtime report | Codex local identity check + R01 and relevant subsystem packs |
| v88 isolated candidate | same release ledgers / historical specialist work | recorded SHA256 6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439 | explicitly not installed in release ledger; static/support state only | identify exact artifact/branch/commit before any test |
| v92/input candidate | runtime/astra-phase1-input92 | exact current candidate identity not reconciled in coordination docs | legacy specialist branch and higher version label are not validation | Codex inventory branch/commit/build/hashes; compare behavior/evidence before selecting for test |
| THUG2 native UI candidate | feature/thug2-native-ui-g6 | branch exists; exact frozen runtime identity not reconciled | implementation evidence may be useful, but current implementation ownership is Opus and runtime validation is Codex | mine technical evidence selectively; no wholesale promotion |
| v85 retarget quarantine history | diag/v85-retarget-quarantine | historical diagnostic branch | primarily failure/retarget evidence; not a release candidate | retain under FAILURE_KNOWLEDGE/FAILURE_LEDGER; use for regression design |
| disabled Combine armor support plugin | branch release ledger | static validation pass only | human/runtime armor checks pending | keep disabled; separate support lane |
| disabled GMod props catalog plugin | branch release ledger | 120 records; static pass | representative spawn/material/scale/collision runtime checks pending | keep disabled until selected support validation |
| disabled weapon presentation fixes plugin | branch release ledger | RPG presentation only; static pass | human presentation validation pending | keep disabled until selected support validation |

## Selection rule

Codex should not test every historical candidate merely because it exists. Before runtime work, workflow should choose the smallest candidate that:
- contains the implementation under test;
- has reproducible identity;
- preserves the strongest known-good baseline;
- does not unnecessarily bundle unrelated risky changes.

If no historical candidate satisfies those conditions, Opus should create a fresh isolated implementation candidate from the chosen baseline instead.

## Promotion record

When a candidate finally passes, record:
- old quarantine row;
- promoted branch/commit/build/hashes;
- Codex report path;
- acceptance rows passed;
- regressions passed;
- human-visible/playability evidence;
- CURRENT_STATE change commit.

Until then, quarantine is intentional project truth, not a blocker to preserving its evidence.
