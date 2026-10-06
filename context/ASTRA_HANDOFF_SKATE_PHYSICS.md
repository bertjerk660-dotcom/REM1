# Astra Handoff — THUG2 Skate Physics and Complete Free-Roam Runtime

## Prepared source evidence
- Real THUG2 QB files for physics, tricks, manuals, grinds, lips, ground/air tricks, wall tricks, walking/skating switching and control behavior have been extracted/decompiled locally.
- physics.q decompilation exposes 277 globals/constants plus the surrounding source gameplay definitions.
- Direct source evidence exists for walking <-> skating events and SwitchToWalkingPhysics / SwitchToSkatingPhysics.
- Input/control matrix is prepared from source evidence.
- 20 moto-skateboard SKA files are parsed and hashed; these are only one animation subset, not the entire skater animation library.

## Astra runtime scope
Implement the complete free-roam subsystem, not a THUG2-looking movement approximation: state machine, acceleration/momentum/friction, turning/carving, ollie/air/landing, manuals, grinds, lips, wallrides/wallplants, reverts, grabs/flips/specials, balance, scoring/combo/special state, bails/recovery, walking/skating transitions, collision/ground interaction and the correct coupling to camera/animation/board.

## Out of scope
No THUG2 maps, missions/goals, story NPC populations, dialogue or campaign progression.

## Reverse-engineering rule
Use the user's original THUG2 scripts/assets/executable and IDA Pro 6.8 for native behavior. Do not replace a discoverable THUG2 subsystem with a hand-authored approximation for convenience.

## Validation loop
Enter skate mode -> push/ride -> carve -> ollie -> air trick -> land -> grind/manual/lip -> combo/special -> bail/recover where applicable -> walk/skate transition -> continue -> exit to Fallout.
