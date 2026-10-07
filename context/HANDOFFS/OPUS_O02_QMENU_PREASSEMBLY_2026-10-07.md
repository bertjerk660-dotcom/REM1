# O02 Preassembled Opus Packet — Real GMod Q-menu renderer/compatibility

**Status: WAITING FOR CODEX GAP CLOSURE**

Evidence already available:
- main commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`;
- `context/GMOD_2026-10-07/QMENU_ARCHITECTURE.md`;
- `INTEGRATION_BOUNDARY.md`;
- `COMPATIBILITY_MATRIX.md`;
- qmenu/dependency/native manifests.

Already established for Opus:
- persistent original menu lifecycle;
- panel hierarchy and layout;
- content/search/tool browser structure;
- SpawnIcon click path;
- original input/focus/HangOpen rules;
- original tool-click selection semantics;
- explicit FNV bridge responsibilities;
- current placeholder behaviors that must be replaced.

Still blocking final packet:
- native opener dispatch;
- ModelImage/icon native service;
- spawnlist/search/editor closure;
- exact remaining native interface contract.

When those close, convert this shell to READY FOR OPUS and attach the final C01 commit.
