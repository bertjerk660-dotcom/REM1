# 03 — Failure-to-evidence map

Each failure in `context/FAILURE_KNOWLEDGE.md` mapped to the evidence Opus should read first. "In repo" means it is in the canonical GitHub snapshot. "Local" means it exists only in the local workspace.

| ID | Failure | Status | Primary evidence | Location | Opus first action |
|---|---|---|---|---|---|
| F001 | Runtime WEAP cloning / serialized forms | Durable rule | `FAILURE_KNOWLEDGE.md`; `builds/v80.json` (persistent STAT used, no CloneForm) | In repo | Keep ESP-owned persistent WEAP. Do not reintroduce CloneForm. |
| F002 | Direct `PlayerCharacter::playerNode` deref (v76 crash) | Durable rule | `FAILURE_KNOWLEDGE.md`; v76 log not in repo | Rule in repo; log lost | Use `GetNiNode()`; defer binding. |
| F003 | Unsafe retarget bone caching | Suspected cause of activation crash, **not proven** | `builds/v81.json`; local `build/manifests/v85.json` (retarget quarantined) | v81 in repo; v85 local | Re-enable retargeting in isolated steps with heartbeat logs. |
| F004 | Held board invisible | **Fixed** | `builds/v82.json`; `CURRENT_STATE.md` 2026-10-06 playtest (held board visible, correct placement) | In repo | Preserve as regression R01. |
| F005 | v80/v81 activation crash | **Not reproduced** in latest test. Cause unattributed (see F003). v84 still crashed with camera writes quarantined. | `v80.json`, `v81.json`, `v84.json` (local), 2026-10-09 playtest | Mixed | Do not attribute to NIF or camera alone. Confirm which DLL was tested first (see `01_BASELINE_FREEZE.md`). |
| F006 | Stale documentation | Ongoing | This folder; repo vs local mismatch in `02_THUG2_EVIDENCE_INVENTORY.md` | In repo + local | Treat CURRENT_STATE as authority only after reconciling it against deployed hashes. |
| F007 | Concurrent state changes | Ongoing | Hash-recorded baseline in `01_BASELINE_FREEZE.md` | Local | Re-hash before every deploy. |
| F008 | Fallout HUD and top-left alerts stay on in skate mode | **Open** (2026-10-06 and 2026-10-09 playtests) | `CURRENT_STATE.md`; `context/HANDOFFS/THUG2_OVERLAY_EVIDENCE_2026-10-06.md` (HUD contract); `ASTRA_THUG2_HUD_INPUT.md`; `thug2_ui_asset_handoff` (24 files) | Repo + local | Suppress Fallout HUD on enter, restore on exit, host THUG2 HUD. Gated: O07 waits on C07/C04. |
| F009 | Physics Gun range, held-target audio, wrong actor target | **Open** (2026-10-06 playtest) | `CURRENT_STATE.md`; `context/GMOD_2026-10-07/PHYSGUN_ARCHITECTURE.md`; `context/HANDOFFS/PHYSGUN_IDA68_EVIDENCE_CLOSURE.md` | Repo | Package O04 after C03 closes. Requires regression tests for range, loop, release, target identity. |
| F010 | G triggers grind anywhere | **Open** | `CURRENT_STATE.md`; `thug2_controller_map` (18 files, local); `ASTRA_THUG2_SKATE_RUNTIME.md` | Repo + local | Implement grind eligibility from recovered THUG2 logic. Gated: O05 waits on C04/C08. |
| F011 | Board does not move to feet; THUG2 animations not functioning; duplicate board | **Open** (2026-10-06 and 2026-10-09 playtests) | `thug2_skateboard_asset_handoff` (4 files, local); `ASTRA_SKATEBOARD_ATTACHMENT.md` (local); 20 SKA animation files (local) | Local | Hide/unequip held board on mount, restore on exit. Gated: O06 waits on C06. |
| F012 | Current GMod prop menu is a placeholder | **Open** | `context/GMOD_2026-10-07/QMENU_ARCHITECTURE.md`; `ASTRA_GMOD_QMENU.md`; `CURRENT_STATE.md` | Repo | Build real Q-menu port (O02). Gated: waits on C01 gap closure. |

## Missing evidence to note

- The F002 crash log (v76) and the F004/F005 playtest logs are not stored anywhere in the repo. Opus should be given the log for each new test.
- F003 has no proven root cause. Its fix must come with a validation run, not just the v85 quarantine.
