# Astra handoff — GMod/Half-Life weapon models

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Concrete weapon model staging covers 49 concrete weapon classes.
- Static presentation audit records 48 prepared view candidates and 48 prepared world candidates; only camera/fists special cases lack ordinary pair geometry.
- Source sound dependency handoff has 0 unresolved refs.
- Preserve Source QC/SMD sequences for animation work; converted NIFs are geometry/material candidates only.
- First-person animation readiness, hand attachment, third-person animation and per-weapon mechanics remain Astra-owned.
- Inventory/drop/pickup presentation should be validated separately from firing mechanics.


## 2026-10-07 reconciliation

Recovered from canonical branch `prep/support-workflow`, commit `492c3dc7c23bbcac9eb8c2a52b5e61e32fda775b`, original Git blob `d9328187d4773f125af20c6f5803ce4a71498925`. This preparation handoff was absent from `main`; it was not lost from GitHub. Its historical inventory counts are not proof of a running source-faithful integration. Read the new [original-system investigation](../GMOD_2026-10-07/README.md) for current source traces, provenance/staging, native-evidence limits and compatibility status.
