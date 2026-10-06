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