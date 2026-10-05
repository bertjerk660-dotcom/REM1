# IDA Pro 6.8 / Python 2.7; isolated database only.
import idaapi,idautils,idc,json,os
idaapi.autoWait()
out={"ida_version":idaapi.get_kernel_version(),"input":idc.GetInputFilePath(),"vtables":[]}
for name,td in [("NiNode",0x118602c),("NiAVObject",0x1186044)]:
 for xr in idautils.XrefsTo(td,0):
  col=xr.frm-12
  if idc.Dword(col)!=0 or idc.Dword(col+12)!=td: continue
  for ref in idautils.XrefsTo(col,0):
   vt=ref.frm+4
   slots=[]
   for i in range(64):
    ea=idc.Dword(vt+4*i)
    if not idaapi.getseg(ea): break
    row={"slot":i,"address":hex(ea),"name":idc.GetFunctionName(ea)}
    if i in [2,3,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2c,0x2d]:
     end=idc.GetFunctionAttr(ea,idc.FUNCATTR_END)
     row["instructions"]=[hex(h)+" "+idc.GetDisasm(h) for h in list(idautils.Heads(ea,min(end,ea+700)))[:120]] if end!=idc.BADADDR else []
    slots.append(row)
   out["vtables"].append({"class":name,"vtable":hex(vt),"slots":slots})
with open(os.environ["REM_AUDIT_OUTPUT"],"w") as f: json.dump(out,f,indent=2)
idc.Exit(0)