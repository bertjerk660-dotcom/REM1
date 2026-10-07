# GMod Codex Evidence Intake Review — 2026-10-07

Preferred preparation branch: `prep/opus-ready-20261007`.

Canonical authenticated evidence source:
- `main` commit `19a8046b3d4950545c2d8e3dc03d47ffc5aaafe0`;
- `context/GMOD_2026-10-07/*`;
- `manifests/gmod_2026-10-07/*`.

The canonical GMod bundle metadata validation reports:
- pass = true;
- 36,078 checks;
- 0 errors;
- 58 dependency-graph nodes;
- 89 graph edges;
- 14 required roots.

This proves evidence-bundle consistency only, not final Fallout runtime parity.

## Gate review

### C01 Q-menu
**SUBSTANTIAL PARTIAL**

Strongly traced:
- Q/`+menu` source bind and spawnmenu Lua lifecycle;
- persistent panel/open/close/focus/HangOpen behavior;
- CreationMenu/ToolMenu/content hierarchy;
- tabs/categories/content/search;
- SpawnIcon click/spawn flow;
- tool-selection path;
- required host compatibility surface.

Still required:
- native opener registration/dispatch closure;
- native ModelImage/icon cache/render service;
- spawnlist/search/editor native closure;
- final remaining host-interface identifiers/contracts.

O02 remains blocked pending C01 completion.

### C02 Toolgun
**SUBSTANTIAL PARTIAL**

Strongly traced:
- stable string-mode registry/selection;
- Q-selection → Toolgun state;
- LeftClick/RightClick/Reload architecture;
- Remover semantics;
- Duplicator graph-copy/paste model;
- undo/cleanup and entity/trace/constraint boundaries.

Still required:
- ToolTracer;
- RenderScreen;
- exact Toolgun sound-event closure;
- native trace range/filter;
- prediction/realm semantics;
- explicitly supported Duplicator host constraint representation.

O03 remains blocked pending C01+C02 completion.

### C03 Physgun
**PARTIAL**

Strongly traced:
- build/native identity;
- adapter responsibilities;
- target identity must remain distinct from PlayerCharacter;
- current FNV defect categories.

Still required:
- exact first-person model provenance;
- acquisition range/filter;
- hold-controller branches/tuning;
- rotation/distance/freeze/reacquire;
- release/drop/punt semantics;
- held-loop audio;
- beam/halo renderer closure;
- actor/ragdoll semantics and cleanup.

O04 remains blocked pending C03 completion.

## Next action

Use:
`context/HANDOFFS/CODEX_GMOD_GAP_CLOSURE_2026-10-07.md`

Do not repeat the broad authenticated investigation. Close only the enumerated gaps.

Machine status:
`build/prepared/gmod_codex_evidence_intake_20261007.json`.
