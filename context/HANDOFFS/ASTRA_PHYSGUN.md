# Astra handoff — real GMod Physics Gun

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Installed Source weapon_physgun.txt and GMod physgun hooks are inventoried and hashed.
- Physgun/Toolgun visual/audio asset inventory: 27 / 28 direct refs resolve.
- Source script declares models/weapons/v_Physics.mdl, but that legacy view path is not mounted in this install; this discrepancy is recorded rather than silently recreated.
- Project currently stages c_superphyscannon as the visual view candidate and w_physics as world candidate. Treat this as a candidate requiring source/runtime verification, not proof of exact final GMod presentation.
- Original physbeam/physgun glow materials and Weapon_Physgun.On/Off/Special1 event definitions are indexed.
- Native target acquisition, held-object transform, rotation, freeze/unfreeze, drop/release and launch behavior remain Astra/IDA Pro 6.8 work.
- The recovered 2026-10-06 handoff recorded RMB pickup/hold and LMB launch. This historical mapping is superseded by the explicit 2026-10-07 user requirement below.


## 2026-10-07 reconciliation

Recovered from canonical branch `prep/support-workflow`, commit `492c3dc7c23bbcac9eb8c2a52b5e61e32fda775b`, original Git blob `322d23186c4299a02b898404b737658b70ca3c2d`. This preparation handoff was absent from `main`; it was not lost from GitHub. Its historical inventory counts are not proof of a running source-faithful integration. Read the new [original-system investigation](../GMOD_2026-10-07/README.md) for current source traces, provenance/staging, native-evidence limits and compatibility status.

The current session's explicit user requirement supersedes the older button override above: **left-click interacts/grabs; right-click performs the requested launch/release behavior**. Preserve the original GMOD behavior record separately from this host mapping. No runtime controls were changed by this documentation reconciliation.
