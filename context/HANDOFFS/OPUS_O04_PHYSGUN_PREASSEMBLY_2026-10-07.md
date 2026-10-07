# O04 Preassembled Opus Packet — Physics Gun parity

**Status: WAITING FOR CODEX GAP CLOSURE**

Evidence already available:
- main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`;
- `context/GMOD_2026-10-07/PHYSGUN_ARCHITECTURE.md`;
- `IDA68_NATIVE_REPORT.md`;
- `INTEGRATION_BOUNDARY.md`;
- existing historical IDA 6.8 Physgun evidence;
- human failures: short range, wrong hold-loop audio, player receives actor effect.

Already established for Opus:
- FNV host responsibilities;
- target identity must never collapse to PlayerCharacter;
- beam/halo/audio/model/input are distinct state surfaces;
- existing runtime defects are not source parity.

Still blocking final packet:
- exact first-person model provenance;
- acquisition range/filter;
- hold-controller tuning/branches;
- release/freeze/reload/punt semantics;
- beam/halo renderer closure;
- held-loop audio semantics;
- actor/ragdoll source behavior and cleanup contract.

Do not implement final parity until C03 is reviewed COMPLETE.
