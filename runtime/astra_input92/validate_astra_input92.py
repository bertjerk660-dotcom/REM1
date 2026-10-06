from pathlib import Path
import hashlib,json,re,struct,xml.etree.ElementTree as ET
R=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
C=R/'third_party/NVSE-6.4.9/fnv_gmod_thug2_input92_candidate'
E=R/'build/runtime/astra_input92'
B=json.loads((E/'baseline.json').read_text())
P=R/'third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
checks=[]
def check(name,ok):
 checks.append({'name':name,'pass':bool(ok)})
 if not ok: raise AssertionError(name)
for p,h in B['protected'].items():
 check('protected unchanged: '+p,sha(Path(p))==h)
 check('rollback exact: '+Path(p).name,sha(E/'rollback_v85'/Path(p).name)==h)
old=(P/'main.cpp').read_text(); new=(C/'main.cpp').read_text()
check('native hexadecimal constants unchanged',re.findall(r'0x[0-9a-fA-F]+',old)==re.findall(r'0x[0-9a-fA-F]+',new))
check('retarget quarantine remains', 'kTHUG2RetargetDiagnosticEnabled = false;' in new)
# Compare every source line outside the four approved function/global change regions.
import difflib
allowed=[(685,687),(6262,6360),(6760,6948),(6953,6992)]
for tag,i,j,k,l in difflib.SequenceMatcher(None,old.splitlines(),new.splitlines()).get_opcodes():
 if tag!='equal': check('diff scope at parent line '+str(i+1),any(i>=a and j<=b for a,b in allowed))
for p in P.iterdir():
 if p.is_file() and p.name not in ('main.cpp','FNVGModTHUG2.vcxproj'):
  check('inherited file unchanged: '+p.name,sha(p)==sha(C/p.name))
ns={'m':'http://schemas.microsoft.com/developer/msbuild/2003'}
tree=ET.parse(C/'FNVGModTHUG2.vcxproj')
check('all deployment commands removed',all(not (n.text or '').strip() for n in tree.findall('.//m:PostBuildEvent/m:Command',ns)))
dll=C/'bin/FNVGModTHUG2.dll'; data=dll.read_bytes()
pe=struct.unpack_from('<I',data,0x3c)[0]
check('PE signature',data[pe:pe+4]==b'PE\0\0')
check('x86 machine',struct.unpack_from('<H',data,pe+4)[0]==0x14c)
check('DLL flag',bool(struct.unpack_from('<H',data,pe+22)[0]&0x2000))
check('plugin exports present',b'NVSEPlugin_Query\0' in data and b'NVSEPlugin_Load\0' in data)
check('loaded identity marker',b'bridge loaded, version 92 (astra-input92; parent v85)' in data)
test=(E/'test.log').read_text(encoding='utf-16')
check('C++ state machine tests', 'PASS: 979826 checks; 279936 exhaustive lifecycle/input traces' in test)
report={'candidate':'astra-input92','version':92,'parent_build':'v85','branch':'runtime/astra-phase1-input92',
'changed_functions':['PollControls','MessageHandler','NVSEPlugin_Query','NVSEPlugin_Load','SkateActivationGate92::WorldUnavailable/WorldAvailable/Suspend/Sample'],
'scope':'Phase 1 subsection: release-to-rearm activation ownership only; not full lifecycle cleanup',
'native_addresses_changed':[],'new_native_signatures':[],'ida_required':False,
'dll':str(dll),'dll_sha256':sha(dll),'esp_changed':False,
'esp_sha256':B['protected'][next(p for p in B['protected'] if p.endswith('.esp'))],
'parent':B,'checks':checks,'automated_tests':{'checks':979826,'exhaustive_traces':279936,'observed':'PASS'},
'build':'PASS; initial quoting and dependency-path failures resolved; warnings retained in logs',
'common_lib_sha256':sha(C/'bin/common_vc9.lib'),
'targeted_gameplay_test':{'status':'NOT RUN','expected':'held LMB across load/focus/Q-menu/vehicle/equip cannot activate; release then fresh press activates once','observed':None},
'plugin_log_evidence':None,'windows_crash_event_evidence':None,'deployment':'NOT PERFORMED',
'known_issues':['Full v85 active-mode cleanup on load/title is still unresolved; v89 not merged.',
'Fallout native menu/Pip-Boy gating and console skatemode bypass are unchanged.',
'Failed-load gameplay readiness remains a separate lifecycle review.',
'Xbox routing, complete mechanics, camera and visual/animation integration remain incomplete.',
'Host tests exercise the actual pure gate, not Fallout engine callbacks.'],
'opus_dependency':'None for this input-only subsection; validated held/mount/ride/exit animation and attachment interface needed before later integration.',
'next_runtime_step':'Phase 1 active-mode teardown and safe restoration, including failed load; keep separate candidate.',
'rollback':str(E/'rollback_v85')}
(E/'validation92.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'static_checks':len(checks),'all_pass':all(x['pass'] for x in checks),'dll_sha256':report['dll_sha256']}))
