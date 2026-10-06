# GPT-6 / Claude Opus Preservation Integration Packet

Use this packet before touching the active runtime.

## Pinned inputs
- THUG2 PS2 executable: SLES_526.21, 4,518,260 bytes, SHA256 `91C3D11BF0F1546F8EA20A22E7C1708EA91697F3C1393F36D9D7F2D4449963D1`.
- Extracted FNV male skeleton: 191,216 bytes, SHA256 `C6667DD94FD10392F851F748438B7C69C0D2CB407448BECAE6431D5ED1994C4C`.
- Required reverse-engineering environment: IDA Pro 6.8.
- Validated clean retarget target names are in `context/THUG2_INTEGRATION_PROVENANCE.json`.
- Legacy malformed bone-map targets are forbidden.

## Native entry evidence
Current build-bound native body evidence: GetSkaterVelocity 0x0027DC08, SetSkaterVelocity 0x0027E040, AutoRail 0x002752A8. Existing registration/xref evidence for the wider skate API remains in `IDA68_PRESERVATION_HANDOFF.md`.

Before using an address in runtime work, verify the executable hash and capture a byte signature/call-context in IDA 6.8. Do not transplant offsets to another build.

## Required read order
1. AGENTS.md and BOOTSTRAP/GOAL/CURRENT_STATE.
2. FAILURE_KNOWLEDGE.md.
3. CODE_PRESERVATION_SEMANTICS.md.
4. IDA68_PRESERVATION_HANDOFF.md.
5. THUG2_CODE_PRESERVATION.md and THUG2_INTEGRATION_PROVENANCE.json.
6. GMOD_INTERFACE_PRESERVATION.md.
7. RUNTIME_OWNERSHIP_CONTRACT.md.
8. PER_SCRIPT_DEPENDENCIES.md.
9. Run `python tools/validate_code_preservation.py`.

## Integration rules
- Preserve the active-runtime isolation boundary until validation says a candidate is ready.
- Do not revive runtime CloneForm skateboard identity, raw Camera3rd writes, stale bone caches, or malformed retarget targets.
- Keep Q-menu selection authoritative for Tool Gun modes.
- Keep Physgun native behavior behind the documented adapter boundary.
- Every imported mode must restore Fallout input/camera/HUD/animation ownership on exit.
- Static preservation validation is not gameplay validation.

## Remaining high-value evidence enrichment
The next integration agent should generate exact byte signatures and call-context hashes for all promoted THUG2 native functions using IDA 6.8, then extend the provenance JSON. This packet deliberately does not pretend those signatures were verified when only addresses/disassembly were available.
