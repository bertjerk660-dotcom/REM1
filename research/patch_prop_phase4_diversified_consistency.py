from pathlib import Path
root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")

p=root/"research/build_prop_phase4_review_packet.py"
s=p.read_text(encoding="utf-8")
s=s.replace('LEAF=json.loads((BASE/"thug2_leaf_review.json").read_text())','LEAF=json.loads((BASE/"thug2_diversified_leaf_review.json").read_text())')
p.write_text(s,encoding="utf-8")

p=root/"research/build_prop_phase4_menu_taxonomy.py"
s=p.read_text(encoding="utf-8")
s=s.replace('P3=json.loads((ROOT/"build/prepared/prop_support_phase3/thug2_promotion_queue.json").read_text())','WAVE=json.loads((ROOT/"build/prepared/prop_support_phase4/thug2_diversified_first_wave.json").read_text())')
s=s.replace('for i,r in enumerate(P3["top20"],1):','for i,r in enumerate(WAVE["records"],1):')
p.write_text(s,encoding="utf-8")
print("patched diversified consistency")