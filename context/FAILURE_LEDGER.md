# Normalized Failure Ledger — 2026-10-07

This ledger normalizes canonical failure knowledge into owner/action/retest form. Historical build/version facts are preserved from main unless explicitly marked branch-only.

| ID | Symptom / trigger | Evidence | Current rule / likely boundary | Current owner | Required retest |
|---|---|---|---|---|---|
| F001 | startup/load crashes around runtime skateboard CloneForm/serialized forms | context/FAILURE_KNOWLEDGE.md | skateboard identity must remain ESP-owned/persistent | Opus preserves; Codex validates save/load | inventory identity + save/load + activation |
| F002 | skate activation crash from direct `PlayerCharacter::playerNode` path | FAILURE_KNOWLEDGE F002 | use host-safe 3D root access; never assume playerNode validity | Opus implementation | Codex repeated camera/skate transition test |
| F003 | unsafe retarget bone caching across 3D/camera root rebuilds | FAILURE_KNOWLEDGE F003 | RTTI/type validation, root ownership, cache invalidation, finite clips/quaternions | Opus animation integration | Codex animation/transition soak test |
| F004 | held skateboard invisible | F004; later human playtest | held container fixed with BSFadeNode + Prn=Weapon | currently positive; Opus must preserve | Codex equip/drop/world/save-load regression |
| F005 | v80/v81 LMB skate activation c0000005 | F005 | historical pre-ride/update path; later enter/exit became reachable | treat as regression risk, not current proven failure | Codex repeated activation/crash-log test on current Opus candidate |
| F006 | stale docs disagree with source/build state | F006 | source/hashes/runtime evidence override stale prose | GPT-5.5 coordination | every session reconciliation |
| F007 | concurrent agents alter workspace | F007 | re-check source/version/hash before modify/deploy/test | GPT-5.5 + Codex/Opus discipline | preflight before each pass |
| F008 | Fallout HUD/top-left alerts remain in skate mode | F008 | THUG2 owns skating HUD; Fallout HUD suppressed during mode | Codex C07 -> Opus O07 | Codex HUD ownership/runtime test |
| F009a | Physgun usable range extremely short | F009 | source acquisition/range semantics missing/wrong | Codex C03 -> Opus O04 | Codex R03 range test |
| F009b | wrong Physgun held-target loop audio | F009 | held-state audio event/loop mapping wrong | Codex C03 -> Opus O04 | Codex R03 audio start/hold/stop |
| F009c | Physgun actor effect applies to player instead of acquired actor | F009 | target identity/state application bug | Codex C03 -> Opus O04 | Codex R03 NPC/player identity test |
| F010 | G triggers grind anywhere | F010 | missing THUG2 geometry/contact/state eligibility | Codex C04 -> Opus O05 | Codex valid/invalid grind matrix |
| F011a | board does not transition hand -> feet | F011 | board attachment/state integration missing | Codex C06 -> Opus O06 | Codex attachment-state test |
| F011b | THUG2 skate animation set not functioning | F011 | selection/retarget/blend/state integration incomplete | Codex C06 -> Opus O06 | Codex animation-family matrix |
| F012 | current visually correct GMod prop menu is placeholder | F012 | final requirement is real/source-faithful Q menu | Codex C01/C02 -> Opus O02/O03 | Codex Q-menu behavior test |

## Failure handling rule

When Codex finds a runtime failure in an Opus candidate:
1. freeze and record exact branch/commit/hashes;
2. capture minimal reproduction and logs/crash evidence;
3. distinguish observed fact from hypothesis;
4. link to the relevant source-evidence package;
5. send the fix request to Opus;
6. after Opus fixes it, Codex reruns the failing test plus neighboring regressions;
7. GPT-5.5 updates this ledger only after evidence is recorded.
