# Support Playtest Checklist

Use this checklist for staged support features and regression evidence. It does not authorize support-lane changes to Astra's v88 runtime candidate.

## Before any test
- Run `research/support_playtest_preflight.ps1` with a descriptive label.
- Confirm installed runtime and Astra candidate hashes match the intended test.
- Confirm only the sidecar required by the specific test is enabled.
- Prefer a disposable/non-critical save.

## Baseline Fallout
- Reach main menu and load an existing save.
- Move/aim/attack and open/close Pip-Boy normally.
- Create and reload a save.
- Check plugin log and Windows Application events for new failures.

## Inventory / weapon presentation
- Verify GMod names and GMod origin icons.
- Verify THUG2 Skateboard name and THUG2 origin icon.
- Drop/pick up tested weapons.
- Move them to/from containers and normal trade where allowed.
- Verify intended world model.
- Test the RPG presentation sidecar only in isolation.
- Keep the GMod Camera view-model discrepancy as a documented review item rather than silently replacing it.

## THUG2 Skateboard baseline
- Normal equip must not unexpectedly change Fallout state.
- Held and dropped board visuals must be checked.
- Skate activation/exit belongs to the assigned Astra build.
- Exiting skate mode must restore Fallout HUD/input.
- Do not use support checks as proof that THUG2 physics/animations are complete.

## Curated prop catalog
- Enable only `REM_GModProps_Catalog.esp` for the isolated catalog test.
- Spawn a small representative sample from every prepared category.
- Check model, texture, scale, collision and stability.
- Distinguish fixed skate obstacles from truly movable props.
- Later Physgun testing must not assume a fixed native FNV NIF is movable without the correct runtime behavior.
- Disable the sidecar again after testing.

## Combine Soldier armor
- Enable only `REM_CombineArmor_Test.esp`.
- Check idle/walk/run/crouch/jump and common weapon poses.
- Check helmet/head/hands for clipping.
- Check first and third person.
- Drop the armor and inspect the world model.
- Equip on an NPC.
- Save/load with armor equipped.
- Do not replace Enclave/Remnants equipment until these gates pass.

## Later Q-menu / Tool Gun / Physgun
- Final menu behavior must come from the real GMod Q-menu port.
- Tool selection must occur in that Q menu, not Fallout prompts.
- GMod notifications replace Fallout tool prompts.
- Tool Gun and Physgun mechanics remain Astra/native-runtime validation work.

## After any test
- Run `research/support_playtest_postflight.ps1 -SessionDir <session>`.
- Preserve the log/event evidence.
- Record human observations separately.
- Investigate unexpected pre/post hash changes.
- Update CURRENT_STATE only with observed facts.
