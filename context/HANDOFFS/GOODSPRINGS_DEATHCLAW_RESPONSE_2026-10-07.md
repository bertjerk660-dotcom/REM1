# Goodsprings Deathclaw Response encounter v2 — 2026-10-07

## Implemented

The Goodsprings encounter is staged as a separate support feature and does not overwrite the protected Astra runtime DLL.

### Combine Solider
- Raider-derived NPC named exactly **Combine Solider**.
- 100,000 HP.
- speed multiplier 200 (2x).
- Frenzied / Foolhardy AI.
- current torso-lowered Combine armor.
- Minigun.
- 10,000,000 standard 5mm rounds.
- attacks player/NPCs/actors through Frenzied behavior.

### DEATHCLAW RESPONSE UNIT
- 10 vanilla Deathclaw-derived creatures placed around the Goodsprings encounter.
- display name exactly **DEATHCLAW RESPONSE UNIT**.
- base AI is Unaggressive, with zero factions and zero packages.
- they therefore do not independently choose the player or Goodsprings NPCs as targets.
- the separate runtime support DLL explicitly forces their combat target to the Combine guard every 750 ms while he is alive.
- if any unit temporarily targets something else, combat is stopped and retargeted to the Combine guard.
- after the guard is defeated, response-unit combat is stopped on every poll so they remain peaceful.

### Captain Claw
- vanilla Deathclaw-derived creature named **Captain Claw**.
- placed in Goodsprings but initially disabled.
- base AI is Unaggressive and factionless.
- persistent vanilla Bethesda package: `RunToPlayerForever [PACK:000CAFC6]`.
- after the Combine guard becomes dead/dying/otherwise non-alive, Captain is enabled and `evp` is called.
- Captain therefore pathfinds/runs to the player naturally.
- **No MoveTo/teleport command exists in the executable Captain path.**
- once within 275 game units, one message-box dialogue prompt is shown.
- Microsoft David Desktop TTS simultaneously plays the thank-you line.
- player receives exactly 1 vanilla Deathclaw Egg `[MISC:000E6627]`.
- persistent short global `REMCaptainClawRewarded` prevents repeat rewards across save/load.

## Deployed artifacts
- `Data\REM_Goodsprings_CombineDeathclawEncounter.esp`
  - SHA256 `B37B2087B75701AFAAE64FEA62B580774B99965A8B4C37CED32E4161FECB590F`
- `Data\NVSE\Plugins\REMGoodspringsResponse.dll`
  - SHA256 `2FCEAC8BB4B3AD11B774F9B9B0D9F97A08E9D9372205C9A7E4E34F2BF4F0F13F`
  - Win32/x86
- `Data\Sound\fx\rem\goodsprings\captain_claw_thanks.wav`
  - SHA256 `F0C6A0DAE22B6122DAC741E14CC3A8F255F50BC13A1A7B860AA42C8B4B74F62C`
  - PCM mono, 16-bit, 22050 Hz, ~9.79 sec.

## Final load order
1. `FalloutNV.esm`
2. `REM_GModTHUG2.esp`
3. `REM_CombineArmor_Test_TorsoLowered.esp`
4. `REM_Goodsprings_CombineDeathclawEncounter.esp`

The older `REM_CombineSolider_GoodspringsRampage.esp` remains on disk only as historical evidence and is disabled, preventing duplicate guards.

## Reproducibility
- xEdit authoring source:
  `third_party\tools\xEdit-4.1.5f\Edit Scripts\REM_CreateGoodspringsCombineDeathclawEncounter.pas`
- separate NVSE source:
  `third_party\NVSE-6.4.9\fnv_goodsprings_response_plugin\main.cpp`
- deterministic fallback patcher:
  `research\patch_goodsprings_response_v2.py`
- recursive validator:
  `research\validate_goodsprings_response.py`
- machine-readable manifest:
  `build\goodsprings_response\manifest_v2.json`

## Validation status
Static/build validation passes. The DLL builds with 0 errors and is x86. ESP hierarchy, 10 response refs, Captain package/disabled flag, guard stats/loadout, reward global and TTS asset all validate. Runtime smoke boot also passes: xNVSE 6.4.9 explicitly logged `REMGoodspringsResponse` version 2 as loaded correctly alongside `FNVGModTHUG2`, and the fresh main-menu test was then closed without loading a save. The actual Goodsprings encounter/playability test remains pending and must not be claimed successful until observed in-game.
