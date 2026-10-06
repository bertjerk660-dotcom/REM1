from pathlib import Path
import json,re,hashlib,collections,vpk

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/gmod_weapon_runtime_candidates"
IDX=BASE/"sound_vpk_index.txt"
MAN=json.loads((BASE/"manifest.json").read_text())
OUT=BASE/"resolved_sound_events"
OUT.mkdir(parents=True,exist_ok=True)

def sha_bytes(b): return hashlib.sha256(b).hexdigest().upper()

# path -> archive(s)
pa=collections.defaultdict(list); arc=None
for line in IDX.read_text(encoding="utf-8-sig",errors="ignore").splitlines():
    s=line.strip()
    if s.startswith("### "): arc=Path(s[4:].strip()); continue
    if arc and s: pa[s.replace("\\","/").lower()].append(arc)

unresolved=sorted({s["ref"] for w in MAN["weapons"] for s in w["sound_refs"] if not s["resolved_any"]})
script_paths=sorted(p for p in pa if p.startswith("scripts/") and p.endswith(".txt") and ("game_sounds" in p or "/sounds/" in p or "npc_sounds" in p))
archives={}

def get_bytes(rel,archive):
    key=str(archive)
    if key not in archives: archives[key]=vpk.open(key)
    try:return archives[key][rel].read()
    except Exception:return None

def tokens(text):
    text=re.sub(r"//.*?$","",text,flags=re.M)
    return [m.group(1) if m.group(1) is not None else m.group(2) if m.group(2) else m.group(3)
            for m in re.finditer(r'"((?:\\.|[^"])*)"|([{}])|([A-Za-z0-9_./\\*#@<>^$!:-]+)',text)]

def blocks(text):
    t=tokens(text); out=[]; i=0
    while i<len(t)-1:
        name=t[i]
        if t[i+1]!="{": i+=1; continue
        i+=2; dep=1; body=[]
        while i<len(t) and dep:
            x=t[i]
            if x=="{": dep+=1
            elif x=="}": dep-=1
            if dep: body.append(x)
            i+=1
        out.append((name,body))
    return out

def waves(body):
    out=[]
    for i,x in enumerate(body[:-1]):
        if x.lower()=="wave":
            w=body[i+1].lstrip("*#@<>^)}$!").replace("\\","/")
            if w.lower().endswith((".wav",".mp3")): out.append(w)
    return list(dict.fromkeys(out))

defs={}
script_meta=[]
for rel in script_paths:
    for a in pa[rel]:
        b=get_bytes(rel,a)
        if b is None: continue
        text=b.decode("cp1252","ignore")
        added=0
        for name,body in blocks(text):
            ws=waves(body)
            if ws:
                defs.setdefault(name.lower(),[]).append({"name":name,"waves":ws,"script_path":rel,"archive":str(a),"script_sha256":sha_bytes(b)})
                added+=1
        script_meta.append({"path":rel,"archive":str(a),"sha256":sha_bytes(b),"definitions":added})
        if added: break

sound_paths=set(p for p in pa if p.startswith("sound/") and p.endswith((".wav",".mp3")))
rows=[]
for event in unresolved:
    ms=defs.get(event.lower(),[])
    wr=[]
    seen=set()
    for m in ms:
        for w in m["waves"]:
            key=("sound/"+w.lstrip("/")).lower()
            if key in seen: continue
            seen.add(key)
            wr.append({"wave":w,"payload_found":key in sound_paths,"archives":[str(x) for x in pa.get(key,[])]})
    rows.append({"event":event,"definitions":ms,"waves":wr,"resolved_definition":bool(ms),"all_payloads_found":bool(wr) and all(x["payload_found"] for x in wr)})

res={
 "purpose":"Resolve Source/GMod named weapon sound events from original installed VPK sound-script definitions.",
 "input_events":len(unresolved),
 "resolved_definitions":sum(r["resolved_definition"] for r in rows),
 "fully_payload_resolved":sum(r["all_payloads_found"] for r in rows),
 "unresolved_after":[r["event"] for r in rows if not r["resolved_definition"]],
 "scripts_scanned":len(script_meta),
 "records":rows,
 "script_meta":script_meta,
 "rule":"No Fallout sound substitutions; unresolved events remain explicit."
}
(OUT/"manifest.json").write_text(json.dumps(res,indent=2))
(OUT/"summary.json").write_text(json.dumps({k:res[k] for k in ("input_events","resolved_definitions","fully_payload_resolved","unresolved_after","scripts_scanned")},indent=2))
print((OUT/"summary.json").read_text())