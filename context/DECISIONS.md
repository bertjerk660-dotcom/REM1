# Decisions

## D-001 GitHub is canonical
Accepted: 2026-10-05.
GitHub is the durable source of truth for project source, documentation, pipeline configuration, manifests and project knowledge. Local tooling is used for build/extraction/decompilation/testing but must not become the sole holder of durable engineering knowledge.

## D-002 IDA version
Accepted: 2026-10-05.
Use IDA Pro 6.8 for project reverse-engineering work that requires IDA, rather than IDA 9.

## D-003 Preserve Fallout default gameplay
Normal Fallout: New Vegas mechanics remain active until the player explicitly activates the skateboard gameplay mode. Exiting skate mode restores normal Fallout-style gameplay.

## D-004 Reverse engineer rather than merely imitate
Where the project explicitly requires THUG2/GMod behavior to be merged, implementation should be grounded in analysis of the source game's behavior/code/assets where legally and technically appropriate, rather than claiming a 1:1 merge based only on a hand-authored approximation.
