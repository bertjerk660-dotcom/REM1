# Astra handoff — THUG2 HUD and input

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- THUG2 HUD/controller source asset handoff indexes 49 files; missing: [].
- Image previews: 22 / 22 successful.
- Original Xbox/PS2/NGC button font descriptors and image atlases are preserved.
- Original timer/trick fonts, balance/score/SPECIAL sprites, menu/controller scripts and HUD/menu sounds are preserved.
- Controller mapping handoff records PS2-to-Xbox face/trigger equivalents from menubuttonremap.q.
- HUD renderer and input switching must activate with skate mode and restore Fallout HUD/input cleanly on exit.
- Runtime renderer, score/special/balance state and mode-specific input interception remain Astra-owned.