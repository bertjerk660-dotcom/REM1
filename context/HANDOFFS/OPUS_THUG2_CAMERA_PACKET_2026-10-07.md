# Opus packet — THUG2 skate camera

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX C05.**

Implement the source-grounded THUG2 camera through the host-safe adapter defined by C05. Do not imitate it with arbitrary Fallout offsets and do not revive direct unsafe playerNode/camera transform assumptions.

Acceptance: source-faithful follow/yaw/pitch/distance/smoothing/speed/air/landing/state coupling; no clipping regression beyond defined source/host behavior; repeated entry/exit restores Fallout camera; zoom/transition stable. Codex runs R04/R05 plus camera regressions.
