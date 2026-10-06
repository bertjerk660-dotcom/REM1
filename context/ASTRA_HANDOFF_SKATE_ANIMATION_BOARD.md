# Astra Handoff — THUG2 Animation and Skateboard Attachment

## Board evidence
- Source pickup-board GLB dimensions: 38.875 x 75.6875 x 10.125.
- Live visual/world NIF dimensions: 10.5 x 36.375 x 6.6875.
- Held BSFadeNode candidate dimensions: about 16.165 x 56.0 x 10.296.
- Held candidate root is BSFadeNode THUG2_Skateboard_Weapon with NiStringExtraData Prn=Weapon.
- Current held NIF SHA256: 4F12178D6D4004B29B46BCF61365A6B48D2EF007B862B292B4CDA80DF7BBD08A.
- Current visual NIF SHA256: C13CC1ABB997D85E0C5A4860410A7EF14E8DFDCA5EA14D29983EBDAAA7843E4C.
- Scale analysis shows the current source->NIF relationship is non-uniform; do not assume one scalar fixes attachment.

## Animation evidence
20 real THUG2 moto-skateboard animations are parsed/hashes recorded, including accel, air idle, brake, bump, flip, getup, grab, land, manual, moving/stationary idle, ollie, revert, turning and wallplant. Each parsed file contains 50 bone tracks.

## Astra runtime work
Recover the complete skater animation set/state selection, retarget source motion to the Fallout player rig without changing intended timing/motion, and attach the authentic board correctly to hand/feet across carry, walking, mount, riding, trick, bail and exit states.

## Rule
Do not deform/recreate the source board to hide an attachment problem. Correct the host container/bone/state mapping after source-faithful rig analysis.
