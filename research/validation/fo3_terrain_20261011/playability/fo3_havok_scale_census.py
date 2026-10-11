# Compare Fallout 3 NIF Havok geometry scale with visual geometry, research only.
import time,pathlib,json,math,statistics
time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
w=pathlib.Path(r"D:\REM_Dream_validation_20261011")
data=json.loads((w/"fo3_bsa_model_extract.json").read_text())["extracted"]
result=[]
for e in data:
 d=NifFormat.Data()
 with pathlib.Path(e["local_file"]).open("rb") as f:d.read(f)
 vis=[(v.x,v.y,v.z) for g in d.blocks if type(g).__name__=="NiTriStrips" for v in g.data.vertices]
 hk=[(v.x,v.y,v.z) for g in d.blocks if type(g).__name__=="hkPackedNiTriStripsData" for v in g.vertices]
 if not hk:continue
 amin=[min(v[k] for v in vis) for k in range(3)];amax=[max(v[k] for v in vis) for k in range(3)]
 bmin=[min(v[k] for v in hk)*7 for k in range(3)];bmax=[max(v[k] for v in hk)*7 for k in range(3)]
 vs=[amax[i]-amin[i] for i in range(3)];hs=[bmax[i]-bmin[i] for i in range(3)]
 ratio=[hs[i]/vs[i] if vs[i]>0.1 else 0 for i in range(3)]
 result.append({"source":e["path"],"visual_diameters":vs,"havok7_diameters":hs,"diameter_ratio":ratio,"vert_count":len(hk)})
summary=dict(models_with_havok=len(result),ratio_medians=[statistics.median(r["diameter_ratio"][i] for r in result) for i in range(3)],
ratio_min=[min(r["diameter_ratio"][i] for r in result) for i in range(3)],
ratio_max=[max(r["diameter_ratio"][i] for r in result) for i in range(3)],
outliers=[r["source"] for r in result if max(r["diameter_ratio"])>1.8 or min(r["diameter_ratio"])<0.15])
(w/"fo3_havok_scale_census.json").write_text(json.dumps(dict(summary=summary,per_model=result),indent=2))
print(json.dumps(summary,indent=2))
print('first5',json.dumps(result[:5],indent=2))
