# Next Codex kickoff — focused GMOD C01–C03 closure (2026-10-09)

**Status: queued instruction, not an executed Codex investigation.** Preparation remains **81/100** pending evidence review; do not claim +9 until all three original C01/C02/C03 stop conditions pass. Authoritative owner: Codex for investigation/IDA 6.8 and runtime debugging/validation; Opus alone implements and visually integrates into FNV.

## Bootstrap and evidence reuse
1. Start with `AGENTS.md`, `context/BOOTSTRAP.md`, `context/GOAL.md`, `context/ARCHITECTURE.md`, `context/CURRENT_STATE.md`, `context/OPEN_WORK.md`, `context/DECISIONS.md`, `context/FAILURE_KNOWLEDGE.md`, `context/AGENT_OWNERSHIP.md` and `context/OPUS_READINESS_81_TO_100_PLAN_2026-10-07.md`.
2. Canonical base GMod authenticated evidence: `main` commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`, notably `context/GMOD_2026-10-07/` and `manifests/gmod_2026-10-07/`.
3. Follow the **narrow gap packet** `context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`, plus the **newly integrated** `context/HANDOFFS/GMOD_UI_PHYSGUN_SPECIALIST_CONTRACT_2026-10-08.md`, `context/GMOD_2026-10-08_RESEARCH_INDEX.md`, `manifests/gmod_2026-10-08_research_status.json`.
4. The October 8 specialist handoff is directly observed Lua and previous evidence *synthesis*. It ran **no new IDA job or game test**; its C01/C02/C03 status is PARTIAL, not a gate closure. Don't count it as fresh native reverse-engineering proof.
5. Use the user's actual original installed Garry's Mod sources and **IDA Pro 6.8 exclusively** for any native binary investigation. Keep copyrighted game payloads local; store hashes, source paths, function offsets, graphs, and reproducible tooling on GitHub instead.

## Primary evidence closure (C01–C03)

**C01 — real Q menu + player-model changer** (+3 only on original native closure):
- Resolve engine `+menu/-menu/+menu_context/-menu_context` command registration through original Lua/Derma lifecycle, focus, text-entry HangOpen, pointer/cursor and input ownership.
- Trace exact native SpawnIcon/ModelImage preview, cache, rendering, mounted-content service, native spawnlist precedence, search.GetResults and icon-editor/property bridges.
- Supplement C01 research with the **actual GMod player-model changer**: original player-model browser, thumbnail/preview, bodygroups/skin, selection/persistence, server authority, `Player:SetModel`/related native calls and local content dependencies. Separate this extended requested feature from required C01 scoring if original gate did not include it.
- Record original UI events, data/state, source assets and FNV/xNVSE host adapter interface without rebuilding the Q menu as a Fallout lookalike.

**C02 — Toolgun, stool system, functional spawning, feedback** (+3 only on original closure):
- Continue `gmod_tool`, original registry, Q-click string-mode dispatch, LeftClick/RightClick/Reload, SWEP prediction, native trace range/mask/filter, ToolTracer, RenderScreen/RT and `Toolgun.Single` audio.
- Resolve Remover + Duplicator object/constraint copy/reference/undo representation; inventory additional useful original stool options by source dependency and implementation priority without blindly claiming all community stools supported.
- Trace `gm_spawn` request → model permission → entity creation → collision/physics/ownership → cleanup/undo; define how the curated project prop set substitutes for GMod mounted catalog data.
- Trace original GMod **notification/pop-up** implementation (`cl_notice.lua`, undo/cleanup/unfreeze notifications, hints/worldtips), original fonts/icons/materials/sounds, timing/stacking and event triggers. Explicitly separate actual GMOD events from Fallout HUD popup equivalents.

**C03 — native Physics Gun parity** (+3 only on original closure):
- Identify actual `CWeaponPhysGun` input/vtable/attack/acquire/hold-controller/rotation/freeze/unfreeze/drop/launch and release/cleanup call paths, distinguishing `weapon_physcannon`/Gravity Gun.
- Recover acquisition trace range/masks/filter and held grab point, beam client renderer, halo/color, start/loop/stop audio, model/first-person provenance and actor-target identity/lifetime rules.
- Compare source-backed behaviors against the existing FNV source `main.cpp` and `gmod_overlay.inc`, accounting for known short-range grab, incorrect loop audio and unconscious-player instead of acquired-target defects. Produce exact Opus fix evidence, not a speculative code patch.
- Record original GMOD input semantics separately from requested FNV LMB acquisition / RMB release-or-launch mapping.

## Evidence packet and decision contract

For each C01/C02/C03 provide:
- **COMPLETE or PARTIAL** against the fixed original stop condition, not visual impressions;
- exact source build/signature/path/hash, native function/class/address, caller/callee, state transitions, actions, permissions, effects/audio/UI and host boundary;
- original vs inferred vs FNV adaptation distinguished;
- unresolved gaps and how to test them;
- machine-readable function/dependency/state/host-contract files per `build/prepared/codex_c01_c08_output_contract_20261007.json`;
- Opus O02/O03/O04 preassembly delta, test acceptance pack and GitHub branch/commit SHA.

If any gate remains partial, **do not award points** or unblock corresponding Opus package. If all 3 pass **and coordination review accepts them**, readiness can move from 81/100 to **90/100**, not 100/100.

## Then progress toward 100/100

The next independent Codex investigation is C04 THUG2 state + movement/physics. Use `context/HANDOFFS/NEXT_CODEX_REQUEST_THUG2_C04_2026-10-07.md`. After C04, C05 camera, C06 animations/board, C07 HUD/UI/scoring and C08 unified source input remain evidence-gated. Do not redirect implementation to Codex or start blocked Opus packages.

No GMod game code, models, DLLs, ESPs or proprietary game assets are to be modified/pushed by this investigation. Opus O00 Golden Bench may start independently, with exact source hashes and unrelated test ESPs isolated/declared in candidate manifest.
