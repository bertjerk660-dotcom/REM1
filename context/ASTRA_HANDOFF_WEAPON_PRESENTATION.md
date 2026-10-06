# Astra Handoff — GMod/HL Weapon Presentation and Animation

## Prepared support state
- Concrete weapon-model staging coverage: 71/71 source model references.
- 48 converted view-model candidates and 48 converted world-model candidates are staged.
- No missing material paths in the prepared concrete candidates.
- 49 GMod weapon records audited in REM_GModTHUG2.esp; 47 are presentation-clean under the current static audit.
- A single clear RPG world-model/icon defect has a separate disabled fix sidecar: REM_WeaponPresentation_Fixes.esp.
- GMod/THUG2 Pip-Boy origin icons are installed and hash-validated.
- All 15 previously unresolved named Source weapon sound events have now been found in original installed Source/GMod sound-script definitions; 14 have every referenced payload confirmed in the mounted VPK index.

## Astra/runtime boundary
The converted view NIFs are geometry/material candidates only. They are not claimed to be source-faithful FNV first-person animation integrations. Use the preserved QC/SMD/source behavior to implement correct animation, hands, attachment, timing and weapon semantics.

## Validation gate
For each promoted weapon: Pip-Boy name/icon -> equip -> correct first person -> correct third person -> fire/reload/idle source behavior -> drop/world model -> pickup -> container/trade -> save/load -> no crash.
