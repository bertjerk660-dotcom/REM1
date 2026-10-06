from pathlib import Path
import json, math, re, time, hashlib
if not hasattr(time,"clock"): time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
from bethesda_structs.archive import get_archive

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
DATA=Path(r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\Data")
MAN=ROOT/"build/prepared/fnv_prop_catalog_curated/manifest.json"
OUT=ROOT/"build/prepared/fnv_prop_catalog_curated/static_audit.json"
SHORT=ROOT/"build/prepared/fnv_prop_catalog_curated/static_shortlist.json"

manifest=json.loads(MAN.read_text(encoding="utf-8"))

# Index loose + archive texture paths without extracting proprietary payloads.
texture_paths=set()
loose=DATA/"textures"
if loose.exists():
    for p in loose.rglob("*.dds"):
        try:
            texture_paths.add(("textures/"+p.relative_to(loose).as_posix()).lower())
        except Exception:
            pass

archive_names=[]
for bsa in sorted(DATA.glob("*.bsa")):
    if "texture" not in bsa.name.lower():
        continue
    try:
        a=get_archive(str(bsa))
        idx=0
        count=0
        for db in a.container.directory_blocks:
            folder=db.name[:-1].replace("\\","/")
            for _fr in db.file_records:
                name=a.container.file_names[idx]; idx+=1
                full=(folder+"/"+name).replace("//","/").lower()
                if not full.startswith("textures/"):
                    full="textures/"+full
                if full.endswith(".dds"):
                    texture_paths.add(full)
                    count+=1
        archive_names.append({"name":bsa.name,"dds_indexed":count})
    except Exception as exc:
        archive_names.append({"name":bsa.name,"error":repr(exc)})

def sha(p:Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

def decode_name(v):
    if isinstance(v,bytes): return v.decode("latin1","ignore")
    return str(v)

def matrix_point(m,v):
    # PyFFI Matrix44 uses row-vector convention.
    x,y,z=v
    return (
        x*m.m_11+y*m.m_21+z*m.m_31+m.m_41,
        x*m.m_12+y*m.m_22+z*m.m_32+m.m_42,
        x*m.m_13+y*m.m_23+z*m.m_33+m.m_43,
    )

def texture_refs(raw:bytes):
    out=[]
    # NIF stores ASCII texture paths with null terminators.
    for m in re.finditer(rb"(?i)(textures[\\/][ -~]{1,240}?\.dds)",raw):
        s=m.group(1).decode("latin1","ignore").replace("\\","/").lower()
        if s not in out: out.append(s)
    return out

def audit_nif(p:Path):
    raw=p.read_bytes()
    d=NifFormat.Data()
    with p.open("rb") as f: d.read(f)
    roots=d.roots
    root=roots[0] if roots else None
    geom=[]
    allpts=[]
    collision_types={}
    havok_blocks=0
    for b in d.get_global_iterator():
        tn=type(b).__name__
        if tn.startswith("bhk"):
            havok_blocks+=1
            collision_types[tn]=collision_types.get(tn,0)+1
        dat=getattr(b,"data",None)
        if dat is not None and hasattr(dat,"vertices") and getattr(dat,"has_vertices",False):
            pts=[]
            try:
                if hasattr(b,"get_transform") and root is not None:
                    mat=b.get_transform(relative_to=root)
                else:
                    mat=None
            except Exception:
                mat=None
            for v in dat.vertices:
                q=(float(v.x),float(v.y),float(v.z))
                if mat is not None:
                    try:q=matrix_point(mat,q)
                    except Exception:pass
                pts.append(q)
                allpts.append(q)
            geom.append({
                "type":tn,
                "name":decode_name(getattr(b,"name","")),
                "vertices":len(pts),
                "triangles":int(getattr(dat,"num_triangles",0)),
            })
    bbox=None
    dims=None
    if allpts:
        mins=[min(p[k] for p in allpts) for k in range(3)]
        maxs=[max(p[k] for p in allpts) for k in range(3)]
        bbox=[mins,maxs]
        dims=[maxs[k]-mins[k] for k in range(3)]
    tex=texture_refs(raw)
    missing=[t for t in tex if t not in texture_paths]
    return {
        "sha256":sha(p),"bytes":p.stat().st_size,
        "root_types":[type(r).__name__ for r in roots],
        "geometry_shapes":len(geom),
        "vertices":sum(x["vertices"] for x in geom),
        "triangles":sum(x["triangles"] for x in geom),
        "havok_blocks":havok_blocks,
        "collision_types":collision_types,
        "has_collision":havok_blocks>0,
        "bbox":bbox,"dimensions":dims,
        "max_dimension":max(dims) if dims else None,
        "min_nonzero_dimension":min((x for x in dims if x>1e-5),default=None) if dims else None,
        "textures":tex,"missing_textures":missing,
        "geometry":geom[:20],
    }

records=[]
for i,r in enumerate(manifest["records"],1):
    staged=Path(r.get("curated_staged_path") or "")
    if not staged.is_absolute():
        staged=ROOT/staged
    item={
        "path":r["path"],
        "spawn_category":r["spawn_category"],
        "staged_path":str(staged),
        "exists":staged.exists()
    }
    if staged.exists():
        try:
            item.update(audit_nif(staged))
            item["parse_ok"]=True
        except Exception as exc:
            item["parse_ok"]=False
            item["parse_error"]=repr(exc)
    else:
        item["parse_ok"]=False
        item["parse_error"]="missing staged file"

    reasons=[]
    if not item["parse_ok"]: reasons.append("parse_fail")
    if item.get("geometry_shapes",0)==0: reasons.append("no_geometry")
    if not item.get("has_collision",False): reasons.append("no_havok_collision")
    if item.get("missing_textures"): reasons.append("missing_texture_refs")
    md=item.get("max_dimension")
    if md is not None and md>3000: reasons.append("very_large")
    if md is not None and md<3: reasons.append("very_small")
    item["static_flags"]=reasons
    item["static_candidate_ok"]=item["parse_ok"] and item.get("geometry_shapes",0)>0 and item.get("has_collision",False) and not item.get("missing_textures") and "very_large" not in reasons and "very_small" not in reasons
    records.append(item)
    if i%25==0: print(f"{i}/{len(manifest['records'])}",flush=True)

def count(key):
    return sum(1 for r in records if r.get(key))
flags={}
cats={}
for r in records:
    cat=r["spawn_category"]
    c=cats.setdefault(cat,{"total":0,"static_ok":0,"no_collision":0,"parse_fail":0,"missing_texture_refs":0,"very_large":0})
    c["total"]+=1
    if r["static_candidate_ok"]: c["static_ok"]+=1
    if "no_havok_collision" in r["static_flags"]: c["no_collision"]+=1
    if "parse_fail" in r["static_flags"]: c["parse_fail"]+=1
    if "missing_texture_refs" in r["static_flags"]: c["missing_texture_refs"]+=1
    if "very_large" in r["static_flags"]: c["very_large"]+=1
    for f in r["static_flags"]: flags[f]=flags.get(f,0)+1

static_ok=[r for r in records if r["static_candidate_ok"]]
result={
    "purpose":"Static audit of the curated FNV spawn-prop library before runtime/menu integration.",
    "source_manifest_sha256":sha(MAN),
    "archives_indexed":archive_names,
    "selected_count":len(records),
    "parse_ok":count("parse_ok"),
    "static_candidate_ok":len(static_ok),
    "flag_counts":dict(sorted(flags.items(),key=lambda x:(-x[1],x[0]))),
    "category_summary":cats,
    "status":"pass_with_review" if len(static_ok)>0 else "fail",
    "notes":[
        "Static_candidate_ok means parseable geometry + embedded Havok collision + resolved DDS references + non-extreme static bounds.",
        "This does not prove the prop is fun, correctly scaled in gameplay, movable, stable under Physgun, or skateable. Those require runtime checks.",
        "No asset was removed from the 300-item curated archive by this audit."
    ],
    "records":records
}
OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
SHORT.write_text(json.dumps({
    "purpose":"Static-clean shortlist derived from the 300 curated FNV candidates; runtime validation still required.",
    "count":len(static_ok),
    "records":[{
        "path":r["path"],"spawn_category":r["spawn_category"],
        "dimensions":r.get("dimensions"),"triangles":r.get("triangles"),
        "collision_types":r.get("collision_types",{})
    } for r in static_ok]
},indent=2),encoding="utf-8")
print(json.dumps({
    "selected_count":result["selected_count"],
    "parse_ok":result["parse_ok"],
    "static_candidate_ok":result["static_candidate_ok"],
    "flag_counts":result["flag_counts"],
    "category_summary":result["category_summary"]
},indent=2))