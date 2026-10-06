# IDA Pro 6.8 Preservation Handoff

## Rule
IDA Pro 6.8 is the required reverse-engineering version. Preserve scripts, addresses, xrefs, signatures, target binary hashes and interpretation notes independently of IDB files.

## Preserved THUG2 skate discovery
Project-authored IDA automation: `research/thug2_ida/export_skate_xrefs.py`.

The script searches the analyzed THUG2 image for these symbolic strings and records xrefs:
`SkaterPhysicsControl_SwitchSkatingToWalking`, `SkaterPhysicsControl_SwitchWalkingToSkating`, `GetSkaterVelocity`, `SetSkaterVelocity`, `AutoRail`, `DoBalanceTrick`, `StartBalanceTrick`, `StopBalanceTrick`, `BoardRotate`, `GetSpin`, `ResetSpin`, `DoNextManualTrick`, `SetManualTricks`, `UseGrindEvents`.

Recorded string/xref evidence includes:
- GetSkaterVelocity string 0x00422C78 -> xref 0x003FB398.
- SetSkaterVelocity string 0x00422C90 -> xref 0x003FB3A0.
- AutoRail string 0x00422D50 -> xref 0x003FB3E0.
- DoBalanceTrick string 0x00423E28 -> xref 0x003FB84C.
- StartBalanceTrick string 0x00423E60 -> xref 0x003FB858.
- StopBalanceTrick string 0x00423E48 -> xref 0x003FB854.
- BoardRotate string 0x00423FC8 -> xref 0x003FB8A8.
- GetSpin string 0x00424628 -> xref 0x003FBA0C.
- ResetSpin string 0x00424640 -> xref 0x003FBA14.
- DoNextManualTrick string 0x004244E0 -> xref 0x003FB9C0.
- SetManualTricks string 0x004244F8 -> xref 0x003FB9C4.
- UseGrindEvents string 0x004244A8 -> xref 0x003FB9B4.
- SwitchSkatingToWalking string 0x00424748 -> xref 0x003FBA50.
- SwitchWalkingToSkating string 0x00424778 -> xref 0x003FBA54.

A separate disassembly artifact identifies `GetSkaterVelocity` at 0x0027DC08 and `SetSkaterVelocity` at 0x0027E040. These addresses are evidence for the analyzed build only; Astra must verify the target binary hash/build before reusing addresses.

## Required reproducibility improvement
Before these addresses become implementation inputs, record:
1. exact THUG2 executable/container hash;
2. platform/region/build identity;
3. IDA loader/processor settings;
4. byte signatures around each native function;
5. calling-convention/argument hypotheses with confidence;
6. cross-check between registration-table xrefs and native function bodies.

Do not treat a string registration xref as proof of a function implementation address without that cross-check.
