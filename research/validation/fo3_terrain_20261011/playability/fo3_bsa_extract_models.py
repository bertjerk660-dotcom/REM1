# Index the owner's Fallout - Meshes.bsa and extract models referenced by
# two Wasteland cells. No redistributed assets.
import pathlib,struct,json,zlib,collections,hashlib
work=pathlib.Path(r"D:\REM_Dream_validation_20261011")
source=pathlib.Path(r"D:\SteamLibrary\steamapps\common\Fallout 3 goty\Data\Fallout - Meshes.bsa")
models=json.loads((work/"fo3_two_cell_base_models.json").read_text())["base_records"]
names={("meshes\\"+e["model"]).replace("/","\\").lower():[] for e in models.values() if e["model"] and e["model"].lower().endswith(".nif")}
record_by_name={("meshes\\"+e["model"]).replace("/","\\").lower():code for code,e in models.items() if e["model"] and e["model"].lower().endswith(".nif")}
found={}; extracted=[];errs=[]
with source.open("rb") as f:
 header=f.read(36)
 assert header[:4]==b"BSA\0"
 vers,folder_offset,archive_flags,folder_count,file_count,foldname_len,filename_len,file_flags=struct.unpack_from("<8I",header,4)
 assert vers==104
 records=[struct.unpack("<QII",f.read(16)) for _ in range(folder_count)]
 entries=[]
 for (hashval,count,off) in records:
   namelen=f.read(1)[0]
   name=f.read(namelen).rstrip(b"\0").decode("latin1").lower()
   for _ in range(count):
     h,size,offset=struct.unpack("<QII",f.read(16))
     entries.append((name,h,size,offset))
 assert len(entries)==file_count
 fn_block=f.read(filename_len)
 fnames=fn_block.split(b"\0")
 assert len(fnames)>=file_count
 for i,(folder,h,size,offset) in enumerate(entries):
   path=(folder+"\\"+fnames[i].decode("latin1")).lower()
   if path in names:found[path]=dict(index=i,size=size,offset=offset)
 for path,e in found.items():
   size=e["size"];off=e["offset"]
   compressed=bool(archive_flags & 4) ^ bool(size & (1<<30))
   length=size&0x3fffffff
   f.seek(off); raw=f.read(length)
   if compressed:
     expected=struct.unpack_from("<I",raw)[0]
     raw=zlib.decompress(raw[4:])
     if len(raw)!=expected:errs.append(f"uncompressed length mismatch {path}")
   if not raw.startswith(b"Gamebryo File Format") and not raw.startswith(b"NetImmerse File Format"):
     errs.append(f"unexpected NIF header: {path}:{raw[:40]!r}");continue
   rel=path.replace("\\","/")
   out=work/"fo3_original_models"/rel
   out.parent.mkdir(parents=True,exist_ok=True)
   out.write_bytes(raw)
   extracted.append(dict(path=path,local_file=str(out),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),base=record_by_name[path]))
manifest=dict(bsa_archive_sha256=None,archive_version=vers,archive_flags=archive_flags,folder_count=folder_count,file_count=file_count,target_nifs=len(names),found_nifs=len(found),extracted_nifs=len(extracted),issues=errs,missing=sorted(set(names)-set(found)),extracted=extracted)
(work/"fo3_bsa_model_extract.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k!="extracted"},indent=2))
print("EXAMPLES",json.dumps(extracted[:6],indent=2))
