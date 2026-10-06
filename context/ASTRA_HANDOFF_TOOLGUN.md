# Astra Handoff — Real GMod Tool Gun

## Original installed source evidence
- gmod_tool/shared.lua SHA256: BDD3127030C651127A02F7E208EE0B953A7A374EBA10ACBCC8B6522EF47DA1C3
- gmod_tool/stool.lua SHA256: 6CCED8F5FD1109FDA23B6AE0D89325831C7D5F2D9469CF8DD447FA0677A30FB3
- The real SWEP uses models/weapons/c_toolgun.mdl and models/weapons/w_toolgun.mdl.
- Shoot sound event: Toolgun.Single.
- The real SWEP reads the selected mode from gmod_toolmode.
- PrimaryAttack/SecondaryAttack/Reload delegate to the selected tool object's LeftClick/RightClick/Reload.
- The original shot feedback invokes selection_indicator and ToolTracer.

## Prepared support inputs
- Q-menu/tool dependency inventory and hashes.
- 40 stool/tool files identified.
- Tool Gun model/material candidates and source sound-event resolution evidence.
- 290-entry content adapter for prop-facing tools.
- Input matrix documents Q-menu selection as the authoritative Tool Gun mode path.

## Astra runtime work
Port the real SWEP/tool-state behavior through the Fallout/xNVSE compatibility layer, including actual trace semantics, selected-tool lifecycle, Duplicator/Remover state and GMod feedback. Do not replace the real tool mode flow with Fallout prompts.

## Validation gate
Choose a tool in Q -> equip/fire Tool Gun -> selected tool executes -> switch tools in Q -> behavior changes immediately -> GMod-style feedback appears -> no Fallout selection prompt appears.
