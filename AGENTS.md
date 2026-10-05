# Engineering Agent Instructions

This repository is the durable source of truth for the FALLOUT NV - GARRYS MOD mashup project.

## Bootstrap
At the start of every substantial task:
1. Read AGENTS.md.
2. Read context/BOOTSTRAP.md.
3. Read context/GOAL.md.
4. Read context/CURRENT_STATE.md.
5. Read relevant architecture, pipeline, decisions, validation, and failure-knowledge documents.
6. Inspect actual source/build state before assuming documentation is correct.

## Priorities
Optimize for playability, stability, coherent game design, correct integration, reproducibility, automation, reduced manual intervention, and learning from failures.

## Lifecycle
BOOTSTRAP -> INSPECT -> PLAN -> MODIFY -> BUILD -> VALIDATE -> PLAYABILITY CHECK -> RECORD RESULTS -> UPDATE PROJECT KNOWLEDGE.

Never claim success without validation. Never record assumptions as confirmed facts.

## Source of truth
Actual repository source/files are authoritative for implementation. context/GOAL.md defines product intent. context/ARCHITECTURE.md defines intended design. context/CURRENT_STATE.md records verified state. context/DECISIONS.md records accepted decisions. context/FAILURE_KNOWLEDGE.md records proven failure knowledge.

Use GitHub branches/commits for significant automated changes. Verify commits/pushes rather than assuming them.

## Local tooling
Desktop Commander may be used for local build, extraction, decompilation, emulation and testing. IDA Pro 6.8 is the required IDA version for reverse-engineering work requested by the project owner.

Do not commit proprietary game binaries/assets merely to archive them. Store reproducible tooling, manifests, hashes, mappings and extraction/import instructions where direct redistribution is inappropriate.
