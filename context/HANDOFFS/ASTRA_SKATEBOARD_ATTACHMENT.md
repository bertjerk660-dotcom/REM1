# Astra handoff — skateboard visibility, scale and attachment

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Board source files indexed: 4; converted source GLB count: 1.
- Current held board uses a Fallout BSFadeNode + Prn=Weapon container with authentic THUG2 board geometry.
- Current board visual/world NIF dimensions/hashes and a source-vs-live scale analysis are recorded.
- Canonical board identity requirement: the final assembled board used by THUG2 skating/animation is also the exact visible board when the Pip-Boy Skateboard weapon is equipped and the exact visual board used when dropped. Hand/riding/world states may use different Fallout attachment containers or transforms, but not different board geometry/materials.
- Equipping from the Pip-Boy must immediately show that canonical board in the player's hand before skate mode is activated.
- Do not deform/recreate board geometry to solve attachment.
- Resolve held-hand and riding-under-feet transforms against the correct Fallout/THUG2 bones and animation states.
- Validate transitions: equipped/held -> enter skate -> riding/tricks -> exit skate -> held/normal Fallout.
- Exact attachment transforms/retargeting remain Astra-owned.