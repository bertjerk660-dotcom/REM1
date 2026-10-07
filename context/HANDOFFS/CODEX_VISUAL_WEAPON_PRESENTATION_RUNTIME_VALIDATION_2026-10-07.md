# Codex Visual Weapon Presentation Runtime Validation — 2026-10-07

Use for frozen Opus candidates:
- O01 Toolgun presentation;
- O08a Crowbar presentation;
- O08b Pistol presentation;
- O08c SMG1 presentation.

Run only after O00 has passed and Claude Opus has frozen the exact package candidate.

Codex validates; Codex does not implement or patch the candidate during this task.

## Candidate identity

Record:
- package ID;
- Opus branch;
- Opus commit;
- parent commit;
- candidate-manifest path/SHA256;
- ESP/DLL hashes if changed;
- first-person mesh path/SHA256;
- third-person/world mesh path/SHA256;
- all generated texture/material hashes;
- enabled plugin/load order;
- test save/location;
- current baseline main DLL/ESP hashes.

Stop with CANDIDATE_IDENTITY_FAIL if the candidate does not match its manifest.

## V01 — baseline boot/load

- fresh FalloutNV process;
- load declared save;
- verify normal player movement/HUD/Pip-Boy;
- equip a normal Fallout weapon first.

PASS: baseline works before imported presentation is exercised.

## V02 — inventory/equip identity

Equip the tested imported weapon/item through its intended inventory path.

Verify:
- correct inventory identity/name;
- no duplicate/runtime-clone regression;
- correct item selected;
- no grenade/type regression;
- no unrelated auto-equip behavior.

## V03 — first-person presentation

Inspect:
- model visible;
- correct orientation;
- correct scale;
- correct hand/weapon relationship;
- no missing geometry;
- no severe clipping;
- no inverted normals;
- no unexpected Fallout placeholder model;
- expected original material regions appear.

Capture screenshots/video.

## V04 — third-person presentation

Switch to third person and inspect:
- model visible;
- correct hand/weapon attachment;
- correct scale/orientation;
- no detached/floating model;
- no extreme bone/transform deformation;
- package-specific animation family remains as declared by the Opus packet.

Do not interpret presentation success as gameplay-parity proof.

## V05 — world/drop presentation

Where supported by the current item:
- drop item;
- inspect world model;
- verify orientation/scale/material;
- pick item back up;
- re-equip.

PASS: stable world presentation and inventory round trip.

If the package intentionally lacks drop behavior, record NOT_APPLICABLE with evidence.

## V06 — material/reference resolution

Verify:
- no missing textures;
- no absolute development paths;
- no black/purple placeholders;
- normal/specular/mask behavior visually plausible for the documented FNV shader translation;
- known package-specific dependencies are present.

For O08c explicitly verify the source-required `w_smg2specularmask` dependency is represented in the translated material path/intent.

## V07 — repeated transitions

Repeat:
- equip;
- holster/switch;
- first ↔ third person;
- Pip-Boy open/close;
- re-equip.

Minimum 5 cycles.

PASS:
- no crash;
- no accumulating transform error;
- no disappearing model;
- no stuck camera/input;
- no duplicate inventory item.

## V08 — save/load

With the package present:
1. save disposable slot;
2. return to menu;
3. reload;
4. re-equip and inspect first/third person.

PASS: no crash or persistence corruption.

## V09 — neighboring regressions

Verify the tested visual package did not change behavior outside its authorized scope.

At minimum:
- Toolgun behavior/Q menu not newly changed by O01 visual work;
- Physgun behavior unaffected;
- skateboard identity/held presentation/entry-exit path unaffected;
- baseline Fallout weapon switching still works.

## Verdict

Use:
- PASS
- FAIL
- BLOCKED_BY_CANDIDATE_IDENTITY
- BLOCKED_BY_ENVIRONMENT

On FAIL provide:
- first failing test;
- exact candidate identity;
- expected vs observed;
- evidence;
- minimal reproduction;
- passing gates to protect;
- suspected boundary clearly labeled evidence-backed or speculative.

Do not patch the candidate. Return failure evidence for normal GPT → Opus fix-packet conversion.
