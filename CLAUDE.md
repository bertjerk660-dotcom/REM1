# Claude Repository Bootstrap

This GitHub repository is the canonical durable source of truth for the FALLOUT NV - GARRYS MOD + THUG2 merge project.

## Required startup sequence

Before substantial analysis, implementation, debugging, reverse engineering, asset integration, or planning:

1. Read `AGENTS.md`.
2. Read `context/BOOTSTRAP.md`.
3. Read `context/GOAL.md`.
4. Read `context/CURRENT_STATE.md`.
5. Read `context/OPEN_WORK.md` if present.
6. Read `context/ARCHITECTURE.md`.
7. Read `context/DECISIONS.md`.
8. Read `context/FAILURE_KNOWLEDGE.md`.
9. Read `context/SUPPORT_20_POINT_TRACKER.md` if present.
10. Review relevant files under `context/HANDOFFS/`, manifests, validation reports, source, tooling, and build metadata.
11. Inspect the actual current branch, recent commits, open issues, and relevant implementation state before changing anything.

## Operating rules

- Repository state overrides historical chat claims.
- Do not assume work is complete because it was discussed in chat.
- Verify actual files, commits, build outputs, manifests, hashes, and runtime evidence.
- Other agents may modify the repository between sessions; re-check state before continuing.
- Use branches and commits for significant work and verify that changes are actually pushed.
- Preserve reproducibility: record mappings, manifests, hashes, extraction/import steps, validation results, and failure knowledge.
- Do not commit proprietary game binaries or copyrighted game assets merely for archival. Prefer reproducible tooling, metadata, manifests, mappings, and instructions where redistribution is inappropriate.
- Reverse-engineering work that requires IDA must use IDA Pro 6.8 as required by the project owner.
- Never claim runtime success without validation evidence.

## Project scope

The project uses Fallout: New Vegas as the host game and integrates selected Garry's Mod systems and THUG2 skateboarding systems. The repository documentation defines the exact implementation state, ownership boundaries, staged work, known failures, and next actions.

When instructions conflict, follow this precedence:

1. Explicit current user instruction.
2. `AGENTS.md`.
3. `context/BOOTSTRAP.md`.
4. Current verified repository implementation and validation evidence.
5. Other context documents.
6. Historical chat context.

Start every new substantial session by reconciling the repository before proposing or performing work.
