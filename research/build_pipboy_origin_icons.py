from pathlib import Path
from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import hashlib, json, shutil

root=Path(r"C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2")
build=root/"build/pipboy_origin_icons"
src=build/"sources"
out=build/"output"
out.mkdir(parents=True,exist_ok=True)

gmod=Image.open(src/"gmod_logo_brave.png").convert("RGBA")
thug_files=list((src/"thug2_extract").rglob("*.png"))
if not thug_files:
    raise SystemExit("THUG2 logo extract missing")
thug=Image.open(thug_files[0]).convert("RGBA")

def trim_alpha(im):
    a=im.getchannel("A")
    box=a.getbbox()
    return im.crop(box) if box else im

def mask_from_source(im):
    im=trim_alpha(im)
    a=im.getchannel("A")
    # Preserve transparent holes and use the source artwork silhouette itself.
    # GMod/THUG2 colors are deliberately discarded because Pip-Boy UI applies its tint.
    return a

def fit_mask(mask, max_w=186, max_h=186):
    w,h=mask.size
    scale=min(max_w/w,max_h/h)
    size=(max(1,round(w*scale)),max(1,round(h*scale)))
    return mask.resize(size,Image.Resampling.LANCZOS)

def compose_large(source, name):
    mask=fit_mask(mask_from_source(source),186,186)
    canvas=Image.new("L",(256,256),0)
    x=(256-mask.width)//2
    y=(256-mask.height)//2
    canvas.paste(mask,(x,y))
    rgba=Image.new("RGBA",(256,256),(255,255,255,0))
    rgba.putalpha(canvas)
    png=out/(name+"_large.png")
    dds=out/(name+"_large.dds")
    rgba.save(png)
    rgba.save(dds,pixel_format="DXT5")
    return rgba,png,dds

def compose_small(source,name):
    mask=fit_mask(mask_from_source(source),174,174)
    base=Image.new("L",(256,256),0)
    x=(256-mask.width)//2
    y=(256-mask.height)//2
    base.paste(mask,(x,y))
    glow=base.filter(ImageFilter.GaussianBlur(radius=5))
    # Keep a soft halo like Fallout's Pip-Boy small/glow icons.
    alpha=ImageChops.lighter(base.point(lambda x:int(x*0.88)),glow.point(lambda x:int(x*0.66)))
    rgb=Image.new("RGB",(256,256),(150,150,150))
    rgba=rgb.convert("RGBA")
    rgba.putalpha(alpha)
    png=out/(name+"_small_glow.png")
    dds=out/(name+"_small_glow.dds")
    rgba.save(png)
    rgba.save(dds,pixel_format="DXT5")
    return rgba,png,dds

records={}
for name,im in (("rem_gmod_origin",gmod),("rem_thug2_origin",thug)):
    large,lp,ld=compose_large(im,name)
    small,sp,sd=compose_small(im,name)
    records[name]={
        "source_size":im.size,
        "large_dds":str(ld),
        "large_sha256":hashlib.sha256(ld.read_bytes()).hexdigest().upper(),
        "small_dds":str(sd),
        "small_sha256":hashlib.sha256(sd.read_bytes()).hexdigest().upper(),
        "large_bbox":large.getbbox(),
        "small_bbox":small.getbbox(),
    }

(build/"manifest.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
print(json.dumps(records,indent=2))