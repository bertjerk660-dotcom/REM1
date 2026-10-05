# IDA 6.8 / Python 2.7. Source animation discovery; no equivalence claims.
import idaapi,idautils,idc,json,os
idaapi.autoWait()
rows=[]
terms=("playanim","animloop","flip","grab","grind","manual","ollie","bone_board","skeletal","skeleton",".ska")
for s in idautils.Strings():
 try: name=str(s)
 except: continue
 if len(name)>180 or not any(t in name.lower() for t in terms): continue
 refs=[]
 for x in idautils.XrefsTo(s.ea,0):
  start=idc.GetFunctionAttr(x.frm,idc.FUNCATTR_START)
  candidate=idc.Dword(x.frm+4)
  refs.append({"xref":hex(x.frm),"function":hex(start),"neighbor_candidate":hex(candidate)})
 rows.append({"name":name,"address":hex(s.ea),"refs":refs})
with open(os.environ["REM_AUDIT_OUTPUT"],"w") as f: json.dump({"ida_version":idaapi.get_kernel_version(),"input":idc.GetInputFilePath(),"status":"discovery_only","records":rows},f,indent=2)
idc.Exit(0)