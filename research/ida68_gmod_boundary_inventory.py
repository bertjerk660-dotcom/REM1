# Project-authored metadata-only evidence collector, IDA Pro 6.8 / Python 2.
# Run only on a new copy of the existing GMODCLIENT/GMODSERVER IDB.
# Does not rename, patch, decompile or dump binary/assembly payloads.
import hashlib
import json
import os
import idaapi
import idautils
import idc

TARGETS = set([
    'OpenSpawnMenu', 'CloseSpawnMenu', 'RenderSpawnIcons', 'SpawnIcon',
    'ModelImage', 'MakePopup', 'PhysgunBeam', 'DrawPhysgunBeam',
    'weapon_physgun', 'CWeaponPhysGun', 'DT_WeaponPhysGun', 'physgun_beam',
    'CPhysBeam', 'DT_PhysBeam', 'CPhysGunControllerPoint',
    'm_hGrabbedEntity', 'm_vHitPosLocal', 'm_hPhysBeam',
    'OnPhysGunPunt', 'physgun_rotation_sensitivity', 'physgun_wheelspeed',
    'Weapon_Physgun.On', 'Weapon_Physgun.Off', 'Weapon_Physgun.Special1',
    '+menu', '-menu', '+menu_context', '-menu_context',
    'OnSpawnMenuOpen', 'OnSpawnMenuClose', 'OnContextMenuOpen', 'OnContextMenuClose',
    'RebuildSpawnIcon', 'RebuildSpawnIconEx', 'SetSpawnIcon', 'SetModel', 'physgun_maxrange',
    'CPhysGunControllerPoint already has controller?',
    'sprites/physbeam.vmt', 'sprites/physbeama.vmt'
])

def address(ea):
    return None if ea == idc.BADADDR else '0x%X' % ea

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest().upper()

version = str(idaapi.get_kernel_version())
if not version.startswith('6.8'):
    raise RuntimeError('This project permits only IDA Pro 6.8, got ' + version)
idaapi.autoWait()
source_path = idc.GetInputFilePath()
base = idaapi.get_imagebase()
functions = {}

def function_record(ea):
    f = idaapi.get_func(ea)
    if f is None:
        return None
    start, end = f.startEA, f.endEA
    key = address(start)
    if key in functions:
        return key
    direct, indirect = set(), []
    for instruction in idautils.FuncItems(start):
        if idc.GetMnem(instruction).lower() != 'call':
            continue
        refs = list(idautils.CodeRefsFrom(instruction, False))
        if refs:
            direct.update(refs)
        else:
            indirect.append(address(instruction))
    chunks = list(idautils.Chunks(start))
    try:
        offset = idaapi.get_fileregion_offset(start)
        if offset == -1:
            offset = None
    except Exception:
        offset = None
    functions[key] = {
        'ida_name': idc.GetFunctionName(start), 'va': key,
        'rva': address(start - base),
        'file_offset': None if offset is None else address(offset),
        'range_end_va': address(end), 'range_size': end - start,
        'chunk_size': sum(b - a for a, b in chunks),
        'chunks': [{'start_va': address(a), 'end_va': address(b)} for a, b in chunks],
        'direct_callers': [address(x) for x in idautils.CodeRefsTo(start, False)],
        'direct_callees': [address(x) for x in sorted(direct)],
        'indirect_call_sites': indirect,
        'confidence': 'string_xref_candidate_unlabelled_semantics',
        'pseudocode': None,
        'vtable_class': None,
        'interfaces': [],
        'scope_note': 'IDA metadata; an xref or name does not prove full subsystem ownership.'
    }
    return key

records = []
found = set()
strings = idautils.Strings()
strings.setup(strtypes=idautils.Strings.STR_C | idautils.Strings.STR_UNICODE)
for item in strings:
    value = str(item)
    if value not in TARGETS:
        continue
    found.add(value)
    refs = []
    for xref in idautils.XrefsTo(item.ea, 0):
        refs.append({'xref_va': address(xref.frm),
                     'xref_rva': address(xref.frm - base),
                     'xref_type': xref.type,
                     'function': function_record(xref.frm)})
    records.append({'value': value, 'string_va': address(item.ea),
                    'string_rva': address(item.ea - base), 'xrefs': refs})
result = {
    'schema': 'rem.gmod.ida68.boundary_metadata.v1',
    'ida_version': version, 'input_path': source_path,
    'module_sha256': sha256(source_path), 'image_base_va': address(base),
    'analysis_kind': 'existing_database_narrow_string_xref_metadata',
    'strings': records, 'functions': functions,
    'requested_strings_not_found': sorted(TARGETS - found),
    'missing_strings_note': 'Absence may reflect spelling, realm/module, Lua-only hook, stripped binding or string recognition. Not absence of feature.'
}
probes = []
if os.path.basename(source_path).lower() in ('gmodserver.dll', 'server.dll'):
    for slot in (0x520, 0x530, 0x52C):
        cell = 0x10785AFC + slot
        target = idc.Dword(cell)
        probes.append({'candidate_vtable_va': '0x10785AFC',
                       'slot_offset': address(slot), 'cell_va': address(cell),
                       'target_va': address(target), 'function': function_record(target),
                       'confidence': 'observed_candidate_vtable_slot_only_semantic_label_pending'})
result['vtable_probes'] = probes

imports = []
for index in range(idaapi.get_import_module_qty()):
    module_name = idaapi.get_import_module_name(index)
    symbols = []
    def collect_import(ea, name, ordinal):
        symbols.append({'iat_va': address(ea), 'name': name, 'ordinal': ordinal})
        return True
    idaapi.enum_import_names(index, collect_import)
    imports.append({'module': module_name, 'symbols': symbols})
result['imports'] = imports

output = os.environ.get('GMOD_IDA68_OUTPUT')
if not output:
    raise RuntimeError('Set GMOD_IDA68_OUTPUT to an unused local evidence JSON path')
if os.path.exists(output):
    raise RuntimeError('Refusing to overwrite prior evidence output: ' + output)
with open(output, 'wb') as stream:
    stream.write(json.dumps(result, indent=2, sort_keys=True))
idc.Exit(0)
