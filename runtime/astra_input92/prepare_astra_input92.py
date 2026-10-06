from pathlib import Path
import hashlib, shutil, json, re, difflib
ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
SDK=ROOT/'third_party/NVSE-6.4.9'
parent=SDK/'fnv_gmod_thug2_plugin'
dest=SDK/'fnv_gmod_thug2_input92_candidate'
evidence=ROOT/'build/runtime/astra_input92'
game=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
protected={
 str(parent/'main.cpp'):'CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5',
 str(game/'Data/NVSE/Plugins/FNVGModTHUG2.dll'):'BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41',
 str(game/'Data/REM_GModTHUG2.esp'):'0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7'}
for p,h in protected.items(): assert sha(Path(p))==h,(p,'baseline drift')
assert not dest.exists(), 'candidate exists: do not overwrite'
dest.mkdir()
evidence.mkdir(parents=True,exist_ok=False)
for p in parent.iterdir():
 if p.is_file(): shutil.copy2(p,dest/p.name)
rollback=evidence/'rollback_v85'; rollback.mkdir()
for p in protected:
 shutil.copy2(p,rollback/Path(p).name)
original=(parent/'main.cpp').read_text()
s=original
def replace(a,b,count=1):
 global s
 assert s.count(a)==count,(a,s.count(a),count)
 s=s.replace(a,b)
replace('static bool g_skateboardAttackWasDown = false;',
 '#include "skate_activation_gate92.h"\nstatic SkateActivationGate92 g_skateActivation;')
replace('    g_skateboardAttackWasDown = attackDown;\n','')
replace('        g_skateboardAttackWasDown = false;','        g_skateActivation.WorldAvailable();',2)
replace('    if (!g_gameplayReady)\n        return;\n\n    PlayerCharacter* player = PlayerCharacter::GetSingleton();\n    if (!player || !player->parentCell)\n        return;',
'''    if (!g_gameplayReady)
    {
        g_skateActivation.Suspend();
        return;
    }

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
    {
        g_skateActivation.Suspend();
        return;
    }''')
replace('    if (!GameHasFocus()) return;',
'''    if (!GameHasFocus())
    {
        g_skateActivation.Suspend();
        return;
    }''')
replace('    if (g_buildMenu.open)\n    {\n        UpdateBuildMenuControls();',
'    if (g_buildMenu.open)\n    {\n        g_skateActivation.Suspend();\n        UpdateBuildMenuControls();')
replace('    if (g_vehicle.active)\n    {\n        UpdatePendingSpawn();',
'    if (g_vehicle.active)\n    {\n        g_skateActivation.Suspend();\n        UpdatePendingSpawn();')
replace('    if (!g_skate.active && skateboardEquipped && attackDown && !g_skateboardAttackWasDown)\n        EnterSkateMode();',
'''    const bool activationRequested = g_skateActivation.Sample(
        runtimeFormContextReady && !g_skate.active && skateboardEquipped,
        attackDown);
    if (activationRequested)
    {
        _MESSAGE("[THUG2] activation accepted after eligible release (input92)");
        EnterSkateMode();
    }''')
replace('    switch (msg->type)\n    {\n    case NVSEMessagingInterface::kMessage_PostLoad:',
'''    // Input-only invalidation: no script, scene, animation or teardown calls here.
    // Full active-mode cleanup remains a separate Phase 1 candidate.
    switch (msg->type)
    {
    case NVSEMessagingInterface::kMessage_PreLoadGame:
    case NVSEMessagingInterface::kMessage_ExitToMainMenu:
    case NVSEMessagingInterface::kMessage_ExitGame:
    case NVSEMessagingInterface::kMessage_ExitGame_Console:
        g_skateActivation.WorldUnavailable();
        break;
    default:
        break;
    }

    switch (msg->type)
    {
    case NVSEMessagingInterface::kMessage_PostLoad:
        g_skateActivation.WorldUnavailable();''')
replace('info->version = 85;','info->version = 92;')
replace('bridge loaded, version 85','bridge loaded, version 92 (astra-input92; parent v85)')
(dest/'main.cpp').write_text(s)
project=(dest/'FNVGModTHUG2.vcxproj').read_text(encoding='utf-8-sig')
project,n=re.subn(r'<PostBuildEvent>.*?</PostBuildEvent>','<PostBuildEvent><Command></Command></PostBuildEvent>',project,flags=re.S)
assert n==6,n
(dest/'FNVGModTHUG2.vcxproj').write_text(project,encoding='utf-8')
(evidence/'main.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='v85/main.cpp',tofile='input92/main.cpp')))
(evidence/'baseline.json').write_text(json.dumps({'parent':'v85','protected':protected,'candidate':str(dest),'rollback':str(rollback)},indent=2))
print(json.dumps({'candidate':str(dest),'parent_checks':'PASS','postbuild_deployment_events_removed':n}))
