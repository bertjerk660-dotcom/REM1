# Astra handoff — real GMod Tool Gun

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Concrete weapon asset staging includes 48 view candidates and 48 world candidates.
- Weapon sound handoff unresolved count: 0.
- Tool/physgun source asset inventory resolves 27 / 28 requested visual/audio refs.
- Real Tool Gun source is local GMod gmod_tool shared.lua/stool.lua plus 40 stool files.
- Preserve DoToolTrace/LeftClick/RightClick/Reload/tool lifecycle and selection state semantics from GMod.
- Keep Tool Gun effects/ToolTracer/selection indicator and original Toolgun.Single event source-faithful.
- Do not use Fallout top-left menu prompts to choose tools.
- Runtime implementation, tool-object compatibility and Duplicator constraints are Astra-owned.


## 2026-10-07 reconciliation

Recovered from canonical branch `prep/support-workflow`, commit `492c3dc7c23bbcac9eb8c2a52b5e61e32fda775b`, original Git blob `c067f67c1ea3796a8a4e6ee22df5b079ebfef7b8`. This preparation handoff was absent from `main`; it was not lost from GitHub. Its historical inventory counts are not proof of a running source-faithful integration. Read the new [original-system investigation](../GMOD_2026-10-07/README.md) for current source traces, provenance/staging, native-evidence limits and compatibility status.
