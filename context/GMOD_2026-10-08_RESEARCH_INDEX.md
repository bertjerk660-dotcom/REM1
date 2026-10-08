# Research follow-on index — 2026-10-08

This branch is a **documentation-only research extension** of `prep/opus-ready-20261007`. It does not implement, build, deploy, or playtest original GMOD functionality.

**Specialist source-to-host adapter handoff**: [GMOD UI / Physgun specialist contract](HANDOFFS/GMOD_UI_PHYSGUN_SPECIALIST_CONTRACT_2026-10-08.md).

## Evidence classification

- **Directly observed on 2026-10-08:** original installed sandbox `shared.lua`, `init.lua`, `cl_init.lua` and `lua/includes/modules/spawnmenu.lua` implementation details (permissions/hints/notifications/halo/tool panels/spawnlist clear).
- **Corroborated previous investigation:** `GMOD_2026-10-07/QMENU_ARCHITECTURE.md`, `PHYSGUN_ARCHITECTURE.md`, `IDA68_NATIVE_REPORT.md`, `INTEGRATION_BOUNDARY.md` and `manifests/gmod_2026-10-07` (original IDs, source dependency graphs, partial native evidence).
- **Unproven:** Native C01/C02/C03 closure, source-complete hold controller, rendering/sound/input callsites, first-person model and Fallout runtime parity.

## Owner gates

- **Codex:** precise C01/C02/C03 outstanding IDA 6.8 investigation and live-game failure diagnosis. Follow `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md` and new specialist contract.
- **Opus:** the sole source-to-FNV integration/visual implementation owner; wait for evidence-backed adapter specifications and use isolated reversible commits/gates.
- **Normal GPT:** documentation, coordination, provenance and manifest indexing. No user-facing implementation-complete claims from documentation.

**Repository note:** original game scripts and proprietary assets remain local. The Windows workspace inspected by Remote Desktop Commander was not itself a Git checkout; this GitHub branch holds the authored artifact. No existing runtime branch was merged or promoted.
