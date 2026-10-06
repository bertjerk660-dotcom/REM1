from pathlib import Path
import json,re

ROOT=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
BASE=ROOT/"build/prepared/gmod_weapon_runtime_candidates"
m=json.loads((BASE/"manifest.json").read_text(encoding="utf-8"))
lines=[]
for line in (BASE/"sound_vpk_index.txt").read_text(encoding="utf-8-sig",errors="ignore").splitlines():
    s=line.strip().replace("\\","/").lower()
    if s.startswith("sound/") and s.endswith((".wav",".mp3")):
        lines.append(s)

ALIASES={
    "weapon_fiveseven":"fiveseven","weapon_mac10":"mac10","weapon_m249":"m249",
    "weapon_xm1014":"xm1014","weapon_ump45":"ump45","weapon_glock":"glock",
    "weapon_m4a1":"m4a1","weapon_usp":"usp","weapon_deagle":"deagle",
    "weapon_scout":"scout","weapon_slam":"slam",
    "default_zoom":"zoom","c4_disarmfinish":"c4",
    "npc_hunter_flechetteshoot":"flechette","toolgun_single":"toolgun",
}

def key_for(event):
    k=re.sub(r"[^a-z0-9]+","_",event.lower()).strip("_")
    if k in ALIASES:return ALIASES[k]
    if event.lower().startswith("weapon_"):
        return event.split(".",1)[0][len("Weapon_"):].lower()
    return event.split(".",1)[0].lower().replace("npc_","")

unresolved={}
for w in m["weapons"]:
    for s in w["sound_refs"]:
        if s["resolved_any"]:continue
        unresolved.setdefault(s["ref"],set()).add(w["class"])

rows=[]
for event,classes in sorted(unresolved.items()):
    key=key_for(event)
    candidates=[]
    # Strongest: dedicated weapon directory.
    pref=f"sound/weapons/{key}/"
    candidates=[x for x in lines if x.startswith(pref)]
    # Common single-file fallbacks such as sound/weapons/zoom.wav.
    if not candidates:
        candidates=[x for x in lines if f"/{key}" in x and len(candidates)<80]
    # Flechette NPC paths are outside sound/weapons.
    if not candidates and key=="flechette":
        candidates=[x for x in lines if "flechette" in x]
    rows.append({
        "event":event,"classes":sorted(classes),"search_key":key,
        "candidate_waves":candidates[:80],
        "candidate_count":len(candidates),
        "status":"source_event_definition_unresolved_candidates_only"
    })

result={
    "purpose":"Evidence-only candidate wave index for unresolved Source/GMod named sound events. This does not claim event-to-wave equivalence.",
    "unresolved_event_count":len(rows),
    "events_with_candidates":sum(bool(x["candidate_waves"]) for x in rows),
    "records":rows,
    "rule":"Astra/runtime work must resolve named Source sound events from original engine/sound-script behavior. Candidate waves are only local source evidence; do not silently substitute them."
}
(BASE/"sound_event_candidates.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
print(json.dumps({k:result[k] for k in ("unresolved_event_count","events_with_candidates")},indent=2))
for r in rows:
    print(r["event"],"->",r["search_key"],len(r["candidate_waves"]),r["candidate_waves"][:5])