# Local Workspace Inventory — 2026-10-05

Root: C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2

## Authored/runtime source
Primary plugin source is under third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/ and includes main.cpp plus generated/maintained GMod NPC, overlay, prop, tool, weapon and THUG2 animation definition/include files.

## Research and pipeline
research/ contains conversion, extraction, validation, patch and reverse-engineering tooling. Verified examples include GMod prop/weapon converters and manifests, THUG2 board extraction/validation, THUG2 animation conversion/retarget tooling, xEdit generation scripts, skateboard stability patches v75-v81, and IDA 6.8 Havok/motion analysis scripts.

## Build evidence
build/manifests contains v80.json, v81.json and v82.json. Build tree also contains GMod batch conversion output, GMod spawn-menu source extraction, THUG2 board conversion stages, THUG2 exact animation/KF output and runtime screenshots/log evidence.

## Backups
backups/ preserves source snapshots across v54-v81-era changes, including v65 stable source/ESP, v67-v80 source checkpoints and pre-v82 held-board asset.

## Third-party/proprietary boundary
third_party/ contains xNVSE source/runtime and downloaded tools. research/ida68_live includes a live Fallout executable/IDA database. build/ and research/ contain extracted/converted game assets. These are inventoried but should not be blindly copied into GitHub; repository preservation should focus on project-authored source/tooling plus manifests/provenance unless redistribution rights are established.
