# Opus packet — cross-system state transitions and fixes

**Implementer: Claude Opus only.**
**Readiness: NOT READY until subsystem candidates exist and Codex has runtime evidence.**

This packet is for integration fixes after Q/Toolgun/Physgun/THUG2 subsystem candidates exist. It must consume Codex failure reports rather than guessing.

Required transition sequence: Fallout baseline -> Q -> Toolgun -> Physgun -> Fallout -> skateboard -> THUG2 -> Fallout -> save/load -> repeat.

Success requires no HUD/camera/input/audio/animation ownership leakage, no inventory identity corruption, no crash, and all applicable acceptance/save-load/regression gates. Codex runs R09 and targeted failing tests after every Opus fix.
