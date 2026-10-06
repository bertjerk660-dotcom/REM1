# Per-Script Dependency Enumeration

Generated as integration preparation from the local research tree. This document defines the dependency-enumeration contract; machine-readable expansion should be regenerated from the current local workspace immediately before integration.

## High-value scripts

| Script | Runtime/tool dependencies | Inputs | Outputs / role |
|---|---|---|---|
| research/thug2_ida/export_skate_xrefs.py | IDA Pro 6.8, IDAPython: idaapi/idautils/idc | analyzed SLES_526.21 IDB | skate symbol string/xref evidence + saved IDB |
| research/disasm_thug2_skate.py | Python, capstone | SLES_526.21 SHA256 91C3…63D1 | thug2_skate_disasm.txt |
| research/thug2_mips_xrefs.py | Python, capstone | SLES_526.21 | independent MIPS xref evidence |
| research/thug2_table_scan.py | Python stdlib | SLES_526.21 | registration-table pointer context |
| research/extract_fallout_skeleton.py | Python stdlib | Fallout - Meshes.bsa | local fnv_skeleton.nif |
| research/list_fnv_skeleton_bones.py | Python, pyffi | fnv_skeleton.nif | canonical Bip01 node-name list |
| research/inspect_full_fnv_skeleton.py | Python, pyffi | fnv_skeleton.nif | target transform/scale evidence |
| research/thug2_glb_to_fnv_kf.py | Python + modules declared by script; conversion environment | THUG2 animation/skeleton evidence + validated FNV map | generated FNV KF animation |
| research/inventory_gmod_qmenu_sources.py | Python stdlib + installed GMod/VPK inputs | installed GMod Lua/VPK/appmanifest | Q-menu/Derma dependency manifest |
| research/inventory_tool_physgun_assets.py | Python, vpk | installed GMod + VPK index | Tool/Physgun asset dependency handoff |
| research/build_qmenu_content_adapter.py | Python stdlib | final prop catalog manifest | Q-menu data adapter |
| research/build_input_control_matrix.py | Python stdlib | decompiled THUG2 QB evidence | input/control evidence matrix |
| research/validate_support_lane_state.py | Python and support manifests | canonical support artifacts | static support validation |

## Enumeration rule
For every reusable Python script, integration preparation must record: script SHA256, interpreter/tool requirement, imported modules split into stdlib/external/local, hard-coded input paths, declared/generated output paths, source-game payload dependencies, and whether the output is authoritative evidence or regenerated handoff.

IDA scripts additionally require IDA version, processor/loader, target executable hash and expected database/evidence output. Scripts that auto-install packages are not considered hermetic until dependencies are pinned externally.

## Integration gate
GPT-6/Astra or Claude Opus should regenerate a machine-readable dependency inventory from the current workspace before modifying runtime code. Missing external modules, missing source payloads, changed source hashes, or unknown generated-output provenance are blockers, not warnings.
