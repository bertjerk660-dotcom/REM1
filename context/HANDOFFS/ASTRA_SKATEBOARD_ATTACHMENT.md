# Astra handoff — skateboard visibility, scale and attachment

Generated support-lane handoff. Proprietary source assets remain local; GitHub should store paths/hashes/provenance/tooling, not game binaries.

- Board source files indexed: 4; converted source GLB count: 1.
- Current held board uses a Fallout BSFadeNode + Prn=Weapon container with authentic THUG2 board geometry.
- Current board visual/world NIF dimensions/hashes and a source-vs-live scale analysis are recorded.
- Do not deform/recreate board geometry to solve attachment.
- Resolve held-hand and riding-under-feet transforms against the correct Fallout/THUG2 bones and animation states.
- Validate transitions: equipped/held -> enter skate -> riding/tricks -> exit skate -> held/normal Fallout.
- Exact attachment transforms/retargeting remain Astra-owned.