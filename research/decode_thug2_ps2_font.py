"""Decode THUG2 PS2 FNT using IDA 6.8 loader 0x1A7468.
No game deployment. Version 1/2 only. See font_loader88.json."""
from pathlib import Path
import argparse,struct,json,hashlib
from PIL import Image

def decode(data):
    if len(data)<20: raise ValueError("truncated header")
    declared,version,count,height,baseline=struct.unpack_from("<5I",data)
    if version not in (1,2) or not 1<=count<=256: raise ValueError("unsupported font header")
    pos=20
    def take(n):
        nonlocal pos
        if pos+n>len(data): raise ValueError("truncated section")
        x=data[pos:pos+n]; pos+=n
        return x
    records=list(struct.iter_unpack("<Hhh",take(count*6)))
    texheader=take(16)
    width,texheight=struct.unpack_from("<HH",texheader,4)
    if not 1<=width<=4096 or not 1<=texheight<=4096: raise ValueError("invalid texture size")
    pixels=take((width*texheight+3)&~3)[:width*texheight]
    palette=list(struct.iter_unpack("<4B",take(1024)))
    # 0x1A7CA0..0x1A7DC8: exchange entries 8..15 and 16..23 in every block of 32.
    for block in range(0,256,32):
        for i in range(8):
            a,b=block+8+i,block+16+i
            palette[a],palette[b]=palette[b],palette[a]
    rect_count,=struct.unpack("<I",take(4))
    if rect_count!=count: raise ValueError("glyph rectangle count mismatch")
    rects=list(struct.iter_unpack("<4H",take(count*8)))
    if pos!=len(data): raise ValueError("unparsed trailing data")
    glyphs=[]
    for i,((metric,c1,c2),(x,y,w,h)) in enumerate(zip(records,rects)):
        if x+w>width or y+h>texheight: raise ValueError("glyph rectangle outside atlas")
        if version==1:
            codes=[c1] if c1>=0 else []
            special=~c1 if c1<0 else None
        else:
            codes=[]
            for c in (c1&255,(c1>>8)&255,c2&255,(c2>>8)&255):
                if c==255: break
                codes.append(c)
            special=None
        glyphs.append(dict(index=i,codes=codes,special=special,vertical_metric=metric,x=x,y=y,width=w,height=h))
    rgba=bytes(v for idx in pixels for v in (*palette[idx][:3],min(255,palette[idx][3]*2)))
    image=Image.frombytes("RGBA",(width,texheight),rgba)
    return image,dict(version=version,declared_size=declared,glyph_count=count,height=height,baseline=baseline,width=width,texture_height=texheight,glyphs=glyphs)

def main():
    p=argparse.ArgumentParser(); p.add_argument("source",type=Path);p.add_argument("output",type=Path);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    files=sorted(a.source.glob("*.fnt.ps2")) if a.source.is_dir() else [a.source]
    report=[]
    for src in files:
        try:
            data=src.read_bytes(); img,meta=decode(data)
            name=src.name.replace(".fnt.ps2",""); img.save(a.output/(name+".png"))
            meta["source_sha256"]=hashlib.sha256(data).hexdigest()
            (a.output/(name+".json")).write_text(json.dumps(meta,indent=2))
            report.append(dict(font=name,status="pass",glyphs=meta["glyph_count"],size=img.size,source_sha256=meta["source_sha256"]))
        except Exception as e:report.append(dict(font=src.name,status="fail",error=str(e)))
    (a.output/"manifest.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report),flush=True)
if __name__=="__main__":main()
