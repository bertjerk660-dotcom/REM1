# GMOD / bridge / Fallout boundary — 2026-10-07

The payloads staged in this pass are original source dependencies. They do not execute in Fallout merely because the files have been copied. The Source interfaces used by those files must be hosted or adapted with preserved semantics. The current FNV menu renderer does not become Derma by loading original icons.

## Three responsibilities

**GMOD side:** original gamemode/spawnmenu/Derma/tool scripts, content and tool registries, selected-mode identity, tool callbacks, UI layout and events, notification timing, original materials/fonts/sound-event definitions, original Source model/animation packages, and native Physgun behavior supported by build-specific evidence.

**Bridge side:** a compatible Lua dialect/runtime and original API contracts; panel tree, layout, skins, cursor/focus and event delivery; material/font/rendering and sound-event services; entity/trace/physics wrappers; selected-tool/command dispatch; persistent identity mapping and safe lifecycle cleanup. This is where Gamebryo/NVSE/Havok adaptation belongs. No current adapter is declared complete by this report.

**Fallout side:** actual host references/base forms, cells, inventory, actor state, Havok simulation, graphics device/render pass, normal input/menu ownership, saves and world state. Normal Fallout remains the default. GMOD temporarily owns only its invoked menu/actions/transient feedback.

## The executable compatibility gap

Original installed Lua uses GMOD dialect constructs and GMOD globals/metatables. Stock Lua is not sufficient. Preserve original files unchanged in staging. A verified interpreter or a reproducible, semantics-preserving syntax adaptation may be evaluated by the integration owner; ad hoc rewrites of each menu/tool are not the intended boundary.

The required runtime API surface must be measured from the dependency graph: `hook`, `concommand`, `cvars`, `spawnmenu`, `vgui`, `derma`, `surface`, `render`, `cam`, `input`, `file`, `language`, `list`, `net`, `timer`, entity/player/weapon/physics metatables and GMOD Vector/Angle/Color values. Some are original Lua modules; others cross into native Source services. A name in a script proves an interface requirement, not a recovered native implementation.

Do not link a handful of Source DLLs into the FNV process and assume their ABI, global engine state, factory interfaces, filesystem and rendering ownership will operate. The PE/build hashes and IDA evidence describe the analysed GMOD runtime, not relocatable code for FNV. This pass prepares interoperability contracts, not binary transplants.

## Smallest measured adapter surfaces

| Source expectation | FNV/bridge translation | Required invariant |
| --- | --- | --- |
| Source entity and entity handle | stable FNV reference wrapper; base-form/catalog mapping | explicit target identity, invalidation on cell/load/delete; never confuse player with acquired actor |
| Source aim trace result | host world ray/hull trace with mask/filter/bone/hit data translation | trace range, hit point/normal/entity/physics bone preserved where supported |
| Physics object/local hit point | Havok body/ragdoll-bone wrapper and local-space transform | local grab offset remains attached through translation/rotation |
| Native Physgun hold controller | evidence-backed damped target-follow controller | source controller tuning and state transitions; no unexplained per-frame teleport substitute |
| Source bind press/release and command identity | FNV input hook with one contextual owner | Q command pairs, focus and release honored; E/Pip-Boy/combat inputs do not leak into menu actions |
| VGUI/Derma panels | panel lifecycle/layout/event contract over host overlay backend | original hierarchy, skin paint, tabs, scroll/search, hit tests, focus and hover remain script-driven |
| Source surface/render/cam | host graphics pass, text metrics, render targets, clipping and state restoration | original draw order/material semantics; FNV graphics state restored after overlay |
| Source `SpawnIcon`/`ModelImage` model service | model identity mapped to an original-source model preview or explicit host renderer wrapper | skin/bodygroup/camera identity and asynchronous icon cache semantics; static fallback is not parity |
| VMT/VTF and material proxies | original-definition-aware texture/material compatibility | transparency, blend/tint, depth, filtering, texture transforms and beam/skin behavior retained; no lookalike assets |
| Source studio MDL/VVD/VTX/PHY/QC sequences | provenance-preserving model/rig/animation conversion queue | correct first/third/world identity, attachment/scale, timing, collision and all required sequence bindings |
| Source sound event | original event resolver to original payload playback | wave sets, pitch/volume/channel, loop start/stop and transition ownership; no Fallout audio substitutes |
| Source spawn console command | bridge dispatcher into validated FNV ref creation | catalog identity, model/skin/bodygroups, permitted placement, undo/cleanup ownership |
| Tool selection/mode and callback | exact original tool identifier and tool object lifecycle | Q selection immediately affects Tool Gun; no Fallout function-selection dialog |
| Source undo/cleanup/duplicator constraint data | versioned host ref/body/constraint representation | original action ordering/ownership and paste cleanup; unsupported entity types explicitly rejected |
| Source timers/clock/frame time | host monotonic/paused game/frame clocks matching API semantics | distinguish SysTime, CurTime and RealFrameTime; original UI expiry/animation behavior preserved |
| Source net/prediction | host dispatcher preserving client/server realm and first-predicted-action guards | one world mutation per action; original client-only visual feedback remains client-side |
| Source game/filesystem mount paths | explicit virtual path resolver over local exact staged sources | internal paths, precedence and source provenance preserved; mounts and add-ons not silently assumed |

The component-by-component matrix and actual status are in `COMPATIBILITY_MATRIX.md` and its machine-readable counterpart. Native routines supported by IDA evidence are separately recorded in `IDA68_NATIVE_REPORT.md`; unresolved mappings do not gain confidence from this table.

## Integration proof order

1. Validate original source closure and virtual paths without invoking world operations. Identify unimplemented native Lua globals/panel primitives explicitly.
2. Host the original spawnmenu creation/open/close and one original prop content entry through the original panel hierarchy. Prove cursor/focus behavior and graphic-state restoration against original menu semantics.
3. Prove original `SpawnIcon`/preview behavior and a single validated external prop spawn, including material/scale/collision. The curated 290-entry adapter supplies content metadata; generated support thumbnails are audit aids.
4. Wire original tool selection to original Tool Gun mode/callbacks. Prove Remover first, then Duplicator with an explicitly supported entity/constraint subset, preserving registry/lifecycle/prediction and undo/cleanup boundaries.
5. Prove original notification and tool screen/effect/sound paths. Exercise repeated open/close, text focus, tool switching, weapon switch, Pip-Boy, device reset and save/load cleanup.
6. Implement native-evidence-backed Physgun acquisition/hold/rotation/distance/freeze/drop and original visual/audio path. Resolve declared-versus-actual first-person model evidence before choosing converted output. Treat the project's requested right-click launch as a documented compatibility behavior where it differs from original input semantics.
7. Validate actor/ragdoll and target identity independently before allowing actor manipulation. Follow existing reference invalidation and weapon-form safety rules. Preserve the current THUG2 stack and held-board work.

Each proof is a future isolated integration/playtest gate. No runtime promotion, game launch, source rewrite, shader conversion or binary transplant is performed by this evidence pass.
