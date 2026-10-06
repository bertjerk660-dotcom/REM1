"""Read-only validation of preparation inputs. Writes only its own QA report."""
from pathlib import Path
import argparse,json,hashlib,struct,tempfile
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest().upper()
def file_ok(row):
 p=Path(row['path'])
 return p.is_file() and sha(p)==row['sha256']
def disabled(text,names):
 active={x.strip().lstrip('*').lower() for x in text.splitlines() if x.strip() and not x.lstrip().startswith('#')}
 return not active.intersection(n.lower() for n in names)
def glb_ok(p):
 try:
  with p.open('rb') as f:
   magic,version,total=struct.unpack('<4sII',f.read(12))
   if magic!=b'glTF' or version!=2 or total!=p.stat().st_size:return False
   n,kind=struct.unpack('<I4s',f.read(8))
   if kind!=b'JSON' or n%4 or n+20>total:return False
   j=json.loads(f.read(n)); binary_size=0; offset=n+20
   while offset<total:
    n,kind=struct.unpack('<I4s',f.read(8))
    if n%4 or offset+8+n>total:return False
    if kind==b'BIN\0':binary_size=n
    f.seek(n,1);offset+=8+n
   if offset!=total:return False
   buffers=j.get('buffers',[])
   for b in buffers:
    if 'uri' not in b and b['byteLength']>binary_size:return False
   for v in j.get('bufferViews',[]):
    if v['buffer']>=len(buffers):return False
    if v.get('byteOffset',0)+v['byteLength']>buffers[v['buffer']]['byteLength']:return False
   for node in j.get('nodes',[]):
    if 'mesh' in node and not 0<=node['mesh']<len(j.get('meshes',[])):return False
    if any(not 0<=c<len(j['nodes']) for c in node.get('children',[])):return False
   return True
 except (ValueError,KeyError,IndexError,struct.error,OSError):return False
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args()
 R=a.root;O=R/'build/prepared/pre_opus_20261006';checks=[]
 def ck(name,ok,details=None):checks.append({'name':name,'pass':bool(ok),'details':details})
 protected=load(O/'protected_before.json')
 for row in protected:ck('protected:'+row['path'],file_ok(row))
 expected=['BC24E9B15BCA28B33569BC9FF7FD59DB66E962150FD00A9350CE3367DCF06F41','0A81B42990EEA170E302393E514627E6735F1C05D28BB62EF460D6FFA7D1DEB7','6E977CC672317AF160B823F0B6159D8D893B56717FB3EDFF0F645A7AA110A439','3FB4FB4CFB83D161B6FEE4FCACCD07FFF451E9358C16A3546996F6F4C68CD6BD']
 actual={x['sha256'] for x in protected}
 ck('v85/ESP/v88/v92 expected hashes present',set(expected)<=actual)
 for f in O.glob('*_source_packet.json'):
  j=load(f);ck(f.stem+':no missing dependencies',not j['missing_dependencies'],j['missing_dependencies'])
  for row in j['files']:ck('staged:'+row['path'],file_ok(row))
  for row in j['model_components']+j['materials']:
   if not row['resolved']:continue
   p=Path(row['local_source']);ck('source:'+row['relative'],p.exists() and sha(p)==row['sha256'])
   data=p.read_bytes()
   if p.suffix=='.mdl':ck('MDL magic:'+j['id'],data[:4]==b'IDST')
   if p.suffix=='.vvd':ck('VVD magic:'+j['id'],data[:4]==b'IDSV')
   if p.suffix=='.vtf':ck('VTF magic:'+row['relative'],data[:4]==b'VTF\0')
   if row.get('staged_match') is not None:ck('archive/staged identity:'+row['relative'],row['staged_match'])
  for row in j['files']:
   if row['previous_hash_matches'] is not None:ck('previous source manifest:'+row['path'],row['previous_hash_matches'])
 for row in load(O/'thug2_evidence_index.json')['checks']:ck('THUG2:'+row['path'],file_ok(row) and row['match'])
 q=load(O/'thug2_prop_evidence_index.json')
 identities=lambda rows:{(x['level'],x['identifier']) for x in rows}
 ck('85 unique identities',len(q['targets'])==len(identities(q['targets']))==85)
 canonical=load(R/'build/handoffs/gpt6_opus/thug2_props/conversion_queue.json')
 ck('conversion/orchestration identity agreement',identities(canonical['targets'])==identities(q['targets']))
 first=load(R/'build/prepared/prop_support_phase4/thug2_diversified_first_wave.json')
 review=load(R/'build/prepared/prop_support_phase4/thug2_diversified_leaf_review.json')
 ledger=load(R/'build/prepared/prop_support_phase4/thug2_promotion_validation_ledger.json')
 ck('20 review identities agree',identities(first['records'])==identities(review['records'])==identities(ledger['records']))
 ck('review wave belongs to queue',identities(first['records'])<=identities(q['targets']))
 for row in q['source_files']:
  ck('THUG2 level source:'+row['path'],file_ok(row));ck('GLB container:'+row['path'],glb_ok(Path(row['path'])))
 for row in review['records']:
  ck('review GLB hash:'+row['identifier'],sha(R/row['source_glb'])==row['source_glb_sha256'])
 side=load(O/'sidecar_state.json')
 text=Path(side['plugins_file']['path']).read_text(errors='replace')
 ck('sidecars remain disabled',disabled(text,[r['name'] for r in side['sidecars']]))
 for row in side['sidecars']:ck('sidecar hash:'+row['name'],file_ok(row))
 # Metadata drift is an explicit finding, not hidden by refreshing old evidence.
 release=load(O/'release_install_overlay.json')
 for row in release['files']:ck('current release inventory:'+row['path'],file_ok(row))
 ck('never release ready',release['release_ready'] is False and not release['install_actions'])
 # Test the rejection paths without changing any real input.
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'asset';p.write_bytes(b'original');row={'path':str(p),'sha256':sha(p)}
  ck('selftest valid hash',file_ok(row));p.write_bytes(b'altered')
  ck('selftest rejects stale hash',not file_ok(row));p.unlink()
  ck('selftest rejects missing file',not file_ok(row))
  p.write_bytes(b'invalid GLB');ck('selftest rejects malformed GLB',not glb_ok(p))
  ck('selftest rejects enabled sidecar',not disabled('*REM_CombineArmor_Test.esp\n',['REM_CombineArmor_Test.esp']))
 errors=[x for x in checks if not x['pass']]
 result={'scope':'Static preparation only; no game validation','checks':len(checks),'errors':errors,'status':'PASS' if not errors else 'FAIL','results':checks,
 'known_blockers':['Exact Physgun first-person provenance unresolved','Bench wood/collision material mapping requires Opus review','All visual and gameplay acceptance pending'],
 'legacy_manifest_drift':[x for x in release['files'] if not x['previous_hash_matches']]}
 (O/'static_validation.json').write_text(json.dumps(result,indent=2))
 print(json.dumps({k:result[k] for k in ['checks','status','errors']},indent=2))
 if errors:raise SystemExit(1)
if __name__=='__main__':main()