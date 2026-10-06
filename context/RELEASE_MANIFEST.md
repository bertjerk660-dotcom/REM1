# Release / Install Manifest

Generated from the current local workspace. This is a staging manifest, not a claim that the mashup is release-ready.

- Required-file gaps: 0.
- Curated prop catalog: 290 entries ({'Fallout New Vegas': 170, "Garry's Mod / mounted Source content": 120}).
- GMod/HL weapon classes indexed: 49.
- Isolated support sidecars disabled: True.
- Installed runtime is still v85; Astra v88 remains isolated/not installed.

## Promotion gates
- Run support static validator with zero errors.
- Human boot/load/save/load regression.
- Inventory/drop/pickup/container/trade checks.
- Representative prop collision/scale tests.
- Combine armor isolated equip/NPC/save-load tests before any Enclave replacement.
- Astra-owned THUG2/Q-menu/Tool Gun/Physgun runtime validation before release.

Machine-readable details: build/prepared/release_install_manifest.json