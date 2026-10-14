"""Regenerate icons with Pillow (development only; no runtime dependency)."""
from pathlib import Path
from PIL import Image, ImageDraw

DEST = Path(__file__).resolve().parents[1] / "skula_app" / "assets"
DEST.mkdir(exist_ok=True)


def draw_icon(name, color, size=24):
    scale = 4
    im = Image.new("RGBA", (size * scale, size * scale))
    d = ImageDraw.Draw(im)
    def line(points, fill=color, width=1.65):
        pts = [(round(x*size/24*scale), round(y*size/24*scale)) for x, y in points]
        d.line(pts, fill=fill, width=round(width*size/24*scale), joint="curve")
    def box(rect, radius=2, fill=None):
        d.rounded_rectangle([round(v*size/24*scale) for v in rect], radius=radius*size/24*scale,
                            outline=None if fill else color, fill=fill, width=round(1.65*size/24*scale))
    def circle(rect):
        d.ellipse([round(v*size/24*scale) for v in rect], outline=color, width=round(1.65*size/24*scale))
    if name == "overview":
        line([(3,11),(12,3),(21,11)]); line([(6,10),(6,21),(10,21),(10,15),(14,15),(14,21),(18,21),(18,10)])
    elif name == "schedule":
        box((3,5,21,21)); line([(3,10),(21,10)]); line([(8,2),(8,7)]); line([(16,2),(16,7)])
        for x,y in [(8,14),(13,14),(8,18),(13,18)]: box((x,y,x+1,y+1),0,fill=color)
    elif name == "messages":
        box((3,5,21,19)); line([(4,6),(12,12),(20,6)])
    elif name == "announcements":
        line([(4,10),(10,10),(20,5),(20,19),(10,14),(4,14),(4,10)])
        line([(8,14),(9,20),(13,20),(11,15)])
    elif name == "grades":
        box((4,13,8,21),1); box((10,8,14,21),1); box((16,3,20,21),1)
    elif name == "attendance":
        box((5,4,20,21)); line([(8,2),(8,6)]); line([(16,2),(16,6)]); line([(8,13),(11,16),(17,10)])
    elif name == "timetable":
        box((3,4,21,21)); line([(3,10),(21,10)]); line([(3,15),(21,15)]); line([(10,4),(10,21)])
    elif name == "reminders":
        line([(4,18),(6,15),(6,9),(8,5),(12,3),(16,5),(18,9),(18,15),(20,18),(4,18)])
        line([(9,21),(15,21)])
    elif name == "settings":
        for y,x in [(6,9),(12,16),(18,7)]:
            line([(3,y),(21,y)]); box((x-2,y-2,x+2,y+2),1,fill=color)
    elif name == "refresh":
        d.arc((3*scale,3*scale,21*scale,21*scale),40,315,fill=color,width=7)
        line([(21,3),(21,9),(15,9)])
    elif name == "account":
        circle((8,3,16,11)); line([(4,21),(4,18),(7,14),(17,14),(20,18),(20,21)])
    elif name == "brand":
        line([(4.5,10),(12,3.8),(19.5,10)], fill="#17354a", width=1.9)
        for points in [[(5.3,11.5),(8,11.1),(11.2,12.6),(11.2,19.5),(8,18),(5.3,18.2)],
                       [(12.8,12.6),(16,11.1),(18.8,11.5),(18.8,18.2),(16,18),(12.8,19.5)]]:
            d.polygon([(round(x*size/24*scale),round(y*size/24*scale)) for x,y in points],fill="#138f88")
    return im.resize((size,size), Image.Resampling.LANCZOS)


for name in ("overview","schedule","announcements","messages","grades","attendance",
             "timetable","reminders","settings","refresh","account"):
    for tone, color in (("muted","#687b84"),("teal","#087c75")):
        draw_icon(name,color).save(DEST/f"{name}-{tone}.png")
draw_icon("brand","#17354a",48).save(DEST/"brand.png")
print("Generated 23 bundled PNG icons")
