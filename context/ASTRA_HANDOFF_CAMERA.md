# Astra Handoff — THUG2 Camera

## Failure evidence
A prior direct Fallout Camera3rd transform path used a raw global/object reinterpretation and direct transform writes. v83 visibly panned upward immediately before a repeatable access violation. v84 quarantined those raw writes. This failure is recorded in FAILURE_KNOWLEDGE as F008.

## Current rule
Do not restore guessed direct NiAVObject/dat0034 camera writes.

## Astra task
Using IDA Pro 6.8, verify Fallout's actual third-person camera object/lifecycle and legitimate engine mutation path. Independently recover THUG2 free-roam camera movement/rotation/coupling from THUG2 source/native behavior, then bridge them without fighting Fallout's scene graph updates.

## Validation gate
Repeated enter/exit, turn/carve/air/landing camera transitions, sensitivity/rotation checks against THUG2 evidence, no upward-pan corruption, no delayed crash, Fallout camera fully restored on exit.
