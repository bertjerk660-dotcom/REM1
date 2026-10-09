# Astra handoff — complete THUG2 free-roam skate runtime

> Current ownership/order (2026-10-06): preparation only until Opus begins Thursday 2026-10-08. Opus owns models/materials/rigging/conversion/animations/retargeting/visual attachment. Astra owns native/runtime mechanics after corresponding visual gates pass; current Astra mode is inspection/planning only. Existing candidates are preserved, not promoted. See context/HANDOFFS/PRE_OPUS_READINESS_2026-10-06.md.

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Parsed THUG2 board animation assets: 20 moto-skateboard SKA files, with source key/bone-track counts recorded.
- Decompiled controller/trick/physics source handoff: 17 Q source files; trigger usage captured from 7 files.
- walking_control.q exposes explicit SwitchToWalkingPhysics / SwitchToSkatingPhysics transitions.
- physics.q preserves original ground/air gravity, acceleration, speed, turning, friction, snap and jump constants.
- manualtricks/grinds/tricks source preserves trigger timing and animation/state names.
- Goal is full THUG2 free-roam behavior in Fallout world: riding, pushing, ollies, manuals, grinds, lips, wallrides/wallplants, reverts, grabs, flips, specials, combos, bail/recovery, scoring, balance, camera and animation transitions.
- Do not import THUG2 maps, missions, NPCs, story or dialogue.
- Do not approximate source-known timing/physics values by feel.
- Runtime movement/collision/state machine/animation integration remains Astra-owned.
