# Pipeline

## Required lifecycle
BOOTSTRAP -> INSPECT -> PLAN -> MODIFY -> BUILD -> VALIDATE -> PLAYABILITY CHECK -> RECORD RESULTS -> UPDATE PROJECT KNOWLEDGE.

## Reverse engineering
Use IDA Pro 6.8 where IDA is required.
Record useful reverse-engineering discoveries in repository documentation/tooling: signatures, offsets where stable, structures, call relationships, behavior notes, asset mappings and reproducible extraction/conversion steps.
Do not allow critical knowledge to exist only in an IDA database.

## Asset/content workflow
Prefer reproducible extraction and conversion from the user's legally obtained game installations.
Where proprietary source-game content should not be redistributed through GitHub, track:
- source game/version;
- source path or archive identity;
- hashes where practical;
- extraction command/tool/version;
- conversion/transformation steps;
- destination mapping;
- validation expectations.

## Automation rule
Repeated manual intervention is pipeline debt. If substantially the same manual repair happens twice, prefer a scripted transformation, compatibility rule or validation check.

## Build records
Every significant build should have an immutable manifest under builds/ containing build/iteration ID, parent, goal, source inputs, pipeline/tool versions, changes, validation results, known issues and playtest outcome.

## Validation
Use context/VALIDATION.md as the minimum gate set and add feature-specific regression checks as systems become operational.
