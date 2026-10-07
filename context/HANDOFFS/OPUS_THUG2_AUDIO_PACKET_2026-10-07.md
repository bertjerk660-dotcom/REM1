# Opus packet — THUG2 audio integration

**Implementer: Claude Opus only.**
**Readiness: WAITING FOR CODEX SOURCE/EVENT EVIDENCE.**

## Objective
Integrate original THUG2 free-roam/skating audio so sound ownership follows the same gameplay states as movement, tricks, board, HUD and camera, with clean restoration to Fallout audio ownership on exit.

## Required Codex evidence before implementation
At minimum, the relevant C04/C06/C07 findings must identify the gameplay/animation/UI events that drive audio. If those packets do not establish the original sound-event names, source files, loop rules and stop/transition semantics, Codex must produce a narrow audio evidence addendum before this packet becomes READY.

Required evidence must cover:
- push/coast/board movement events where source behavior uses them;
- ollie/air/landing;
- flip/grab/manual/grind/lip/wall/special events;
- bail/fall/recovery;
- board pickup/mount/dismount/break/recovery;
- combo/SPECIAL/UI feedback where audio is part of the original system;
- looping versus one-shot behavior;
- start/stop/fade/interrupt rules;
- source asset/event provenance.

## Existing evidence
Current human observation that THUG2 audio “appears promising” is **not** sufficient implementation evidence or validation. Treat it only as a positive historical observation.

## Fallout integration boundary
- THUG2 audio owns only the events/states proven by source evidence while THUG2 mode is active.
- Normal Fallout audio must remain intact outside THUG2 ownership.
- Mode exit, weapon switch, cell/load transition and failure recovery must stop imported loops cleanly.
- Do not replace missing original THUG2 events with invented Fallout substitutes.

## Dependencies
- C04 gameplay state machine.
- C06 animation/board state bindings.
- C07 HUD/scoring event bindings where UI audio applies.
- C08 input only where an input action directly triggers a source event.
- Provenance index entries for original audio assets/events.

## Known failures / preservation
- Preserve any currently correct source audio only after its identity is verified.
- Physgun audio belongs to the separate GMod Physgun package and must not be mixed into this packet.
- Avoid persistent loops after THUG2 mode exit.

## Acceptance criteria
Codex must validate representative audio for idle/movement, jump/landing, trick families, grind/manual/lip/wall states, bail/recovery, board transitions and UI/combo feedback where applicable.

PASS requires:
- correct original event for the tested state;
- correct timing and one-shot/loop semantics;
- no duplicated events;
- no stuck loop after state transition or exit;
- no Fallout/THUG2 ownership leakage;
- repeated enter/exit and save/load cleanup pass.

Use R04-R06 and R09, with an audio-specific evidence matrix attached to the runtime report.

## Readiness rule
Do not mark READY FOR IMPLEMENTATION until the required source event map/provenance exists and GPT workflow review confirms the dependencies above.

## Haiku audit addendum (2026-10-07)

- Failure protections: this packet must honor every P-F entry in context/HANDOFFS/OPUS_FAILURE_PROTECTIONS_HAIKU_2026-10-07.md that applies to this package. These rules are not optional.
- Evidence boundary: this packet does not authorize rediscovering original behavior that the Codex gate has not closed. Where the owner directive in context/AGENT_OWNERSHIP.md (2026-10-07) lets Opus investigate, the findings must be recorded as evidence with branch, commit and hashes, and reviewed before any readiness point is awarded.
- Candidate handoff: before any build goes to Codex, pass the intake checklist section F and the candidate freeze validator (research/validate_opus_candidate_manifest.py --mode freeze).
- Quarantined candidates must not be promoted by version number alone.