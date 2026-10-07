# IDA Pro 6.8 native evidence and limits — 2026-10-07

The supplied GMOD binaries remain the native-system authority. This pass reuses valid prior **IDA Pro 6.8** evidence rather than relaunching analysis indiscriminately. It establishes build identity, directly checks the native `weapon_physgun` registration, and records which earlier conclusions still need caller/callee and input-path proof. No IDA 9 output, binary transplant, runtime patch, proprietary assembly dump or original binary is committed.

## Immutable native build identity

Root-agent verification on the source Windows machine found the installed `garrysmod/bin/client.dll` and `server.dll` SHA-256 hashes equal their corresponding `C:\IDA68WORK` analysis input copies. Installed IDA `idaq.exe` and `idaq64.exe` file version is **6.8.15.0423**. Existing text exports begin with `IDA_VERSION 6.8`; the client export starts `INPUT GMODCLIENT.dll`.

| Input | Size | SHA-256 |
| --- | ---: | --- |
| Installed `garrysmod/bin/client.dll` / `C:\IDA68WORK\GMODCLIENT.dll` | 8,007,496 | `A1B56FDCB6E70C00241698C45EB145EED77477D8F760320B0A53BFEC330E53E6` |
| Installed `garrysmod/bin/server.dll` / `C:\IDA68WORK\GMODSERVER.dll` | 11,816,784 | `06688DD4C3499170951926A69BE91B6FC77B1DD428E4477566CB2EC6A13BE943` |

| Existing local evidence | SHA-256 |
| --- | --- |
| `C:\IDA68WORK\GMOD_GMODCLIENT_dll_physgun_ida68.txt` | `2F09F0D3999A2F593BEDE9EACB5B27FEBD84B1F578EDF6328DE306437F0554D7` |
| `C:\IDA68WORK\GMOD_GMODSERVER_dll_physgun_ida68.txt` | `4CA27607660E3C1DE8A709E31B4E666B71D3855E2AA85D7DAA4C127B46F616BC` |
| `C:\IDA68WORK\GMOD_phys_controller_methods_ida68.txt` | `2EECC7CD089F43A548135ECBEE24A36BA74A8D42F6B1FF9A1173992C0E51E032` |
| `C:\IDA68WORK\GMOD_phys_controller_xrefs_ida68.txt` | `0BC5710DE6D0D64557829A105FC5D5000C9E2E6102A778672819EA3C88B35F5D` |

Hash matching identifies the analyzed build; it does not independently validate every old semantic interpretation. The large IDBs remain local. The existing THUG2 interactive IDA session is unrelated and must remain untouched.

## Directly inspected native functions

The first 100 lines of the original client export were read directly in this session. Its following facts do not depend on the older prose handoff.

| Client VA | Exported range / size | Observed evidence | Confidence |
| --- | --- | --- | --- |
| `0x10038E00` | `0x10038E00–0x10038E21`, `0x21` bytes | Calls `sub_101D61E0`, passes `weapon_physgun`, `CWeaponPhysGun`, allocation value `0x18C8` and callback `loc_100B7E00`, then calls through returned interface vtable slot `+4`. | High: actual weapon class registration; factory interface identity remains unlabeled. |
| `0x10039090` | `0x10039090–0x100390A5`, `0x15` bytes | Passes `weapon_physgun`, callback `loc_1026A020` and registry address `0x107227B4` into `sub_10269F90`. | High: named registration; precise registry contract not labeled. |
| `0x10065390` | `0x10065390–0x100653BA`, `0x2A` bytes | Registers `cl_defaultweapon` with value `weapon_physgun`, description `Default Spawn Weapon`, flags value `0x280`. | High: convar registration; this is not pickup logic. |
| `0x100B6980` | `0x100B6980–0x100B7219`, `0x899` bytes | Export has `weapon_physgun` string comparison at `0x100B6A4C`; inspected prefix checks a handle, resolves an entity via masked index/serial and performs RTTI/vtable calls. | Medium: physgun-related client consumer; rendering/input ownership unresolved from inspected prefix. |

The first three are registration routines, not gameplay implementations. The later actual IDA 6.8 pass below verifies base `0x10000000` and supplies file offsets/call metadata for matched functions. The machine manifest joins those verified values; unmatched file offsets and semantic interface/vtable ownership remain unresolved rather than invented.

## Critical correction to the earlier closure claim

`PHYSGUN_IDA68_EVIDENCE_CLOSURE.md` said **“EVIDENCE COMPLETE FOR HANDOFF”**, but its strings and prose do not close the full behavioral trace. The older reports remain historical records. For implementation decisions, this report narrows their status to **build-identified, partial native evidence with unresolved behavior ownership**.

The direct client registration connects `weapon_physgun` to `CWeaponPhysGun`. This helps separate that class from `weapon_physcannon`, but it does **not** connect every `OnPhysGunPunt`, `physgun_minrange`, `physgun_interactions` or hold-controller string in a GMOD binary to the GMOD Physics Gun. Source binaries also contain the Half-Life gravity-gun and shared entity/physics paths. An entity output named `OnPhysGunPunt` is not evidence that the GMOD Physics Gun's secondary input launches an entity.

The previous reports list `m_hGrabbedEntity`, `m_vHitPosLocal`, `m_hPhysBeam`, `DT_WeaponPhysGun`, `CPhysBeam` and `DT_PhysBeam`, and a server range `0x10104A50–0x10105038` consuming rotation/wheel configuration. These are useful **candidates**. Until their actual class registration, vtable, callers and data accesses connect them to the input→acquire→controller→beam path, they are not a complete controller algorithm or verified exact input mapping.

Range registrar defaults (`physgun_maxrange=4096`, `physgun_minrange=40`) are now directly verified in the full export review below; their acquisition-path units and eligibility role still need proof. The controller tuning registrar defaults are now directly verified below; that does not prove their units, clamp order, applicability to all targets, update cadence, teleport behavior or full attack ownership. `physgun_timeToArriveRagdoll` does not prove the whole live-NPC conversion lifecycle. Shared `OnPhysGunPickup`/`Drop`/`Punt` events do not prove freeze or launch callflow.

## Required narrow native completion

| Boundary | Evidence still required | FNV relevance |
| --- | --- | --- |
| Native input | Weapon vtable attacks/think, player user-command flags, release, secondary/freeze, reload, use/rotation, wheel, prediction paths; connect the actual registered class. | Adapt current project LMB grab/RMB launch-release deliberately without changing recovered original semantics. |
| Acquisition | Trace origin/mask/filter, eligible target checks, physical object/bone, entity/serial lifetime, grabbed local point and range units. | Avoid short-range fallback ref; preserve acquired identity and reject player-self targeting. |
| Hold controller | Controller class factory, attach/detach, simulate/target updates, damping/arrival/teleport branches, physical body/bone and ragdoll differences. | Source physical-controller contract → validated Havok adapter, not per-frame hard teleport. |
| Beam | Client networked state receive path, actual renderer, attachments/local hit endpoint, draw hook, material/color/proxy calls. | Original beam resources and view/world transforms → overlay renderer. |
| Freeze/reload | Actual input routine and motion enable/disable lifecycle, frozen state, callback ordering. | Physical-object freeze map separate from project launch adaptation. |
| Sound/animation | Emit/start/stop/loop call sites, source sound event resolution, view/world model/animation selection and attachments. | Correct continuous audio and first/third-person presentation rather than guessing from event names. |
| Q command dispatch | Source key command registration and native→Lua hook dispatch for the original menu open/close commands. | FNV keyboard/mouse owner gate; original menu owns lifecycle. |
| `SpawnIcon`/`ModelImage` | Class factory, render queue/icon cache/file generation, renderer/model/mat-system calls. | Native model preview and icon services are not supplied by copying Lua alone. |
| VGUI focus/render | Native popup, keyboard/mouse capture, panel hierarchy and `surface`/`render`/`cam` bindings/interfaces. | Overlay backend preserves original panel semantics and restores Fallout input. |

Source interface versions/import ownership are unresolved until narrow PE/IDA metadata proves them. Common Source interfaces are investigation targets, not automatically verified imports for this build. Lua-only hook strings may not appear in native modules; missing a string does not mean missing functionality.

## Reproducible extension tooling

Project-authored [ida68_gmod_boundary_inventory.py](../../research/ida68_gmod_boundary_inventory.py) checks the running IDA version starts with `6.8`, records input SHA-256/image base, and collects only a fixed list of UI/Physgun string xrefs plus function sizes, direct callers/callees, indirect call sites and file offsets. It refuses to overwrite an output file. Run it only on **a new copy** of the existing GMOD IDB with `GMOD_IDA68_OUTPUT` set to an unused local JSON path. It changes no labels/bytes and exports no proprietary binary or assembly payload. Semantic names still require analysis beyond metadata.

The script was subsequently executed successfully with IDA kernel 6.8 on copied client/server databases. Actual output and its bounded missing-string results are recorded below, separate from unresolved semantic analysis.

## Direct controller export review recovered this session

The original IDA 6.8 controller-method and convar-xref exports were recovered into an ignored local evidence cache and reviewed. They supply substantially stronger evidence than the old string summary, while still leaving original attack/input/vtable attribution incomplete. All following names are **analysis descriptions**, not recovered source symbols.

| Server VA / exported size | Authored functional description | Key calls / state evidence | Confidence and limit |
| --- | --- | --- | --- |
| `0x10103B60`, `0x318` | Controller attachment/initialization candidate | Errors if controller field `+0x48` already exists; stores physical object pointer at `+4`, target and owner handles at `+0x2C`/`+0x44`; gets local point via object vtable `+0xE0`, creates controller through global environment vtable `+0x74`, attaches object through controller `+8`, changes object flags and caches pose/settings. | High for point-controller attach; factory interface and actual weapon caller require database proof. |
| `0x10103E80`, `0x171` | Controller detachment/reset | Optionally restores saved object properties and clears held flag, destroys nonnull controller through environment `+0x78`, resets handles, pointer and target vectors. | High for teardown/reset; optional argument meaning and full call ordering need labels. |
| `0x10104000`, `0xF8` | Target-position update preserving local attachment offset | Validates cached object and target handle; computes transformed stored local point minus object's pose origin, subtracts that offset from desired target vector, stores resulting target at `+0x14..+0x1C`. | High for target-offset math; exact interface method names must be resolved. |
| `0x10104100`, `0x21` | Target-orientation setter | Copies three float components to `+0x20..+0x28` if physical-object pointer exists. | High for state copy; units/angle convention remain unresolved. |
| `0x10104130`, `0x2D4` | Motion-controller simulation candidate | Reads target position/orientation and six configuration-object families, passes assembled parameter block, arrival value and timestep to physical-object vtable `+0x120`, clears output acceleration vectors and returns `1`. Special branch for cached jeep flag changes angular limit using vector dot product. | High for parameterized physics update; underlying `+0x120` algorithm and return enum are unlabeled. This is not a direct transform teleport loop. |
| `0x10104410`, `0x103` | Weapon-sized construction/factory candidate | Allocates `0x1720`, sets object vtable `0x10785AFC`, initializes handle/vector fields and embedded controller at `+0x16D0`. | Medium; server class registration/RTTI must establish exact identity. |
| `0x10104710`, `0x16F` | Weapon held-state cleanup candidate | Calls controller detach with true argument on `this+0x16D0`, handles entity callbacks, clears handle at `+0x1698` and hit vector at `+0x16A0`. Neighbor teardown routines call this path. | High for cleanup effects; exact drop-event mapping requires call/class labels. |
| `0x10104990`, `0x2B` | Handle resolver getter | Index/serial checks for member `+0x1698`. | High for handle resolution, role tied to network table still pending. |
| `0x101049D0`, `0x2B` | Second handle resolver getter | Index/serial checks for member `+0x169C`. | High for handle resolution; likely beam/other member role needs registration proof. |
| `0x101049C0`, `0x6` | Name getter | Returns literal `physgun`. | High for string return; neighboring methods are not automatically all weapon methods. |

The controller configuration registrar exports directly verify defaults `maxAngular=5000`, `maxAngularDamping=10000`, `maxSpeed=5000`, `maxSpeedDamping=10000`, `DampingFactor=0.8`, `timeToArrive=0.05`, `timeToArriveRagdoll=0.1`, and `phys_spinspeed=200`. The teleport-distance default is exported as an unnamed data string and is **not invented**. Their xref export lists constructor/destructor refs to configuration objects; this is not itself a complete getter-use inventory. Simulation references the corresponding object families through global pointers, with native interface calls still unlabeled.

A server memory-offset map can therefore be captured as **build-specific provisional controller layout**: `+4` physical object, `+8..+0x10` local attachment point, `+0x14..+0x1C` target translation, `+0x20..+0x28` target orientation, `+0x2C` target handle, `+0x34/+0x3C` saved object scalars, `+0x38` arrival value, `+0x40` special vehicle flag, `+0x44` owner handle, `+0x48` motion controller. It is evidence about Source, never a license to reinterpret FNV/Havok memory with these offsets.

This confirms a clean interoperability boundary: controller attach, target update, orientation update, simulate and detach can be expressed as contracts around host physical objects. It still does not prove `OnPhysGunPunt` originates from this class or that secondary attack launches, nor does it settle native beam/sound/model paths. The machine inventory records observed call edges and incomplete caller coverage explicitly.

## Registered network state, input consumer and beam resources

The full prior client/server exports were subsequently reviewed for the following exact paths. The local read cache normalizes CRLF to LF; original Windows export hashes above retain immutable byte identity.

- Server `0x100063A0–0x100064B6` (`0x116` bytes) constructs the network state associated with `DT_WeaponPhysGun`: `m_hGrabbedEntity` at **`+0x1698`**, `m_hPhysBeam` at **`+0x169C`**, and `m_vHitPosLocal` at **`+0x16A0`**. Client `0x10038E70–0x10038F60` (`0xF0` bytes) explicitly builds `DT_WeaponPhysGun` receive entries at **`+0x18A8`**, **`+0x18AC`**, **`+0x18B0`** respectively. This directly names the two formerly provisional resolver getters and the cleanup vector. Native networking is explicit; no beam-implied held state is required.
- Server registry routines `0x10006580–0x10006595` and `0x100065A0–0x100065B6` register `weapon_physgun`, a template callback and factory metadata at `0x10987458`. Class metadata contains `CWeaponPhysGun` at `0x1098745C` and `DT_WeaponPhysGun` at `0x10987470`; the getter `0x10104A10` returns the former class metadata pointer. Exact factory/vtable pointer slots still need the narrow database output, but field identity matches the reviewed constructor/cleanup/controller family.
- `0x10104A50–0x10105038` (`0x5E8` bytes) is now directly reviewed. It checks a player-like owner and virtual eligibility methods; input masks `0x2000` and `0x800` from owner field `+0x22A0` dispatch weapon virtual slots `+0x520` and `+0x530`. The held path requires `(field +0x229C & 0x801) == 1`, dispatches slot `+0x52C`, checks the held-entity getter, and otherwise calls `0x10104710` cleanup. Slot identities must be labeled before calling them reload/freeze/acquire functions.
- In its held path, bit `0x20` selects manipulation mode. Forward/back-like bits `0x8/0x10` affect distance; `0x200/0x400` affect rotation with the `phys_spinspeed` configuration family. It obtains `physgun_rotation_sensitivity` via a player-indexed native interface, consumes signed command shorts `+0x34/+0x36`, clamps sensitivity between binary constants, performs matrix-based orientation transformations, and stores orientation at weapon `+0x16C4`. A wheel-like owner virtual method `+0x854` adjusts distance `+0x16AC` using player `physgun_wheelspeed`, then clamps against min/max configuration families. The exact user-command field types, constant numeric values, axis conventions and vtable method names remain unresolved.
- Finally the input consumer computes a view-direction/origin/distance-derived target position at weapon `+0x16B8..+0x16C0` and calls `0x10105F90` and `0x10105B20`, which the prior export does not include. These two routines are the next narrow controller/beam update targets, not arbitrary binary regions.
- Server range constructors are directly verified: `0x100064F0` registers `physgun_maxrange` default **4096**; `0x10006540` registers `physgun_minrange` default **40**. Those values now have direct registrar evidence. Their exact role in acquisition still needs attack/caller proof and Source→Fallout unit conversion.
- Server `0x101037B0–0x1010389A` (`0xEA` bytes) creates named `physgun_beam`, validates via RTTI, configures ownership/flags/bounds and returns the resulting entity. Server `0x101032D0–0x101037B0` contains an owner-derived aim trace with mask **`0x600400B`** through global interface virtual slot `+0x10`, stores result endpoint at entity `+0x13D0..+0x13D8`, and looks up `physgun_maxrange`. It is a beam/aim-trace candidate; this does **not** establish that weapon acquisition uses exactly that trace/mask.
- Client `0x100B7990–0x100B7A07` (`0x77` bytes) initializes original effect resources: `sprites/physg_glow1`, `sprites/physg_glow2`, **`sprites/physbeam.vmt`**, **`sprites/physbeama.vmt`**. It resolves beam materials through a global native interface virtual slot `+0x34` and stores returned pointers at object `+0x13A0/+0x13A4`. `sprites/physbeam.vmt` also has a separate consumer at `0x1033B250`; ownership must be maintained rather than conflating all consumers. This supplies exact beam/glow dependencies stronger than generic physcannon asset candidates.

The full export's `OnPhysGunPunt` literal xrefs are data-registration routines `0x10344160` and `0x10374350`, not the reviewed `0x10104A50` weapon input consumer. This confirms the original caveat: these are event metadata, not evidence of a secondary-attack launch algorithm. Likewise a `Weapon_Physgun.Off` reference at `0x105E5CC0` needs actual class/caller and sound-state context before being interpreted as this gun's hold-loop stop.


## Actual fresh IDA 6.8 execution completed

Root executed the corrected authored collector against new copies of the original client/server databases using the installed IDA 6.8 binary. Both outputs report kernel **6.8**, image base **`0x10000000`**, and the exact matching source-module SHA-256 identities above. Original IDBs and unrelated interactive THUG2 analysis were preserved. The first attempted collector run failed because IDA 6.8 expects a string-type bitmask; the corrected `STR_C | STR_UNICODE` run succeeded. Preparation or Python syntax validation was not substituted for this actual execution.

- [native_boundary_client.json](../../manifests/gmod_2026-10-07/native_boundary_client.json): **20 selected strings, 14 function metadata records**; includes actual file offsets, RVA, chunks, direct caller sites, direct callees and indirect call sites.
- [native_boundary_server.json](../../manifests/gmod_2026-10-07/native_boundary_server.json): **16 selected strings, 22 function metadata records**, plus three identified virtual-slot pointer probes.
- [native_functions.json](../../manifests/gmod_2026-10-07/native_functions.json) now joins the fresh metadata with the authored controller/network/input descriptions. RVAs use the verified base; file offsets remain null for older reviewed functions absent from the narrow fresh capture. Actual raw metadata and authored semantic confidence remain separate.

The candidate weapon vtable **`0x10785AFC`** resolves slot `+0x520` to **`0x101058B0`**, `+0x530` to **`0x10105990`**, and `+0x52C` to **`0x10105130`**. These are concrete targets for the previously observed input dispatch. Source input masks identify reload/secondary/primary-like branches, but target bodies were not decompiled by this metadata pass; freeze/unfreeze/acquisition semantics must still be confirmed from these particular routines. No punt/launch behavior is inferred from the slot names or shared entity outputs.

Actual native import modules in both builds include `KERNEL32`, `USER32`, `WS2_32`, `steam_api`, `tier0`, `RPCRT4`, `vstdlib`, `ADVAPI32`, `CRYPT32`; client additionally imports `Kinect10`. Exact imported symbol/IAT metadata is preserved in the fresh files. This proves these imports, not arbitrary Source interface version numbers. VGUI/render/Lua/physics services may be dynamically acquired or statically linked; their precise contracts still need call/interface proof.

The exact-string scan did **not** find `+menu`, `-menu`, context command counterparts or the selected menu hook names in either analyzed database. `DrawPhysgunBeam` was also absent in this exact scan. This is a bounded result about selected literals and database string recognition, **not** evidence those commands/hooks do not exist or the original Lua flow is wrong. Engine command registration, another module, enum-based dispatch, alternate names or stripped/string-recognition issues remain plausible boundaries. Native `ModelImage`/rebuild-related client literals have metadata candidates; generic `SetModel` consumers are not automatically icon services. The original-source menu bind and Lua trace remain authoritative for visible behavior.

The completed pass closes native build/base identity and supplies reproducible narrow addresses/calls/imports. It does not close the entire original Physgun input/physics/render/audio/view-model or Q/VGUI implementation. Those limits remain explicit and support the thinnest future FNV adapter rather than a look-alike substitute.
