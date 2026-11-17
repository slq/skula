"""Skula: 24-second Polish motion ad. Pillow + NumPy + FFmpeg.
Run: python render.py --preview  OR  python render.py
All artwork comes from the adjacent Skula brand and UI mockups.
The instrumental soundtrack is synthesized by this script.
"""
from pathlib import Path
from functools import lru_cache
import argparse, math, shutil, subprocess, wave, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W, H, FPS, SECONDS = 1080, 1920, 30, 24
NAVY = "#17354A"
TEAL = "#138F88"
MINT = "#66DFCB"
CREAM = "#F4F7F8"
WHITE = "#FFFFFF"
MUTED = "#607C8D"
FONT_ROOT = Path("C:/Windows/Fonts")
FFMPEG = shutil.which("ffmpeg") or "C:/Dev/Tools/ffmpeg/bin/ffmpeg.exe"
OUTPUT = HERE / "skula-reklama-pl-1080x1920.mp4"

def clamp(v, a=0., b=1.): return max(a, min(b, v))
def ease(v): return 1 - (1 - clamp(v)) ** 4
def smooth(v):
    v = clamp(v)
    return v*v*(3-2*v)
def ent(t, delay=0., duration=.7): return ease((t-delay)/duration)
def rgba(hexcolor, alpha=255):
    return tuple(int(hexcolor[i:i+2],16) for i in (1,3,5)) + (int(alpha),)

@lru_cache(None)
def font(size, weight="regular"):
    name = {"regular":"segoeui.ttf", "bold":"segoeuib.ttf", "light":"segoeuil.ttf"}[weight]
    return ImageFont.truetype(str(FONT_ROOT/name), int(size))

@lru_cache(400)
def text_sprite(txt, size, color, weight="regular"):
    f = font(size, weight)
    box = f.getbbox(txt, anchor="lt")
    img = Image.new("RGBA", (max(1,box[2]+6), max(1,box[3]+10)))
    ImageDraw.Draw(img).text((0,0), txt, font=f, fill=color, anchor="lt", stroke_width=0)
    return img

def paste(im, art, x, y, opacity=1., scale=1., angle=0):
    if opacity <= 0: return
    if scale != 1:
        art = art.resize((max(1,round(art.width*scale)), max(1,round(art.height*scale))),Image.Resampling.LANCZOS)
    if angle:
        art = art.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    if opacity < .999:
        art = art.copy()
        art.putalpha(art.getchannel("A").point(lambda v: round(v*clamp(opacity))))
    im.alpha_composite(art, (round(x), round(y)))

def txt(im, s, x, y, size=40, color=NAVY, weight="regular", p=1., center=False):
    art = text_sprite(s, size, color, weight)
    if center: x -= art.width/2
    paste(im, art, x, y + 32*(1-p), p)

def line_title(im, lines, y, t, dark=False, x=84, size=104, gap=122, center=False):
    for i, line in enumerate(lines):
        col = (MINT if dark else TEAL) if i==len(lines)-1 and len(lines)>1 else (WHITE if dark else NAVY)
        txt(im,line,x,y+i*gap,size,col,"bold",ent(t,i*.09),center)

@lru_cache(None)
def bg(mode):
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    if mode=="dark":
        base=np.array([17,43,60],dtype=np.float32)
        glow=np.exp(-(((xx-910)/730)**2+((yy-1190)/920)**2))*1.
        rgb=base[None,None,:]+glow[:,:,None]*np.array([0,28,29])
    elif mode=="mint":
        base=np.array([218,249,240],dtype=np.float32)
        glow=np.exp(-(((xx-80)/1100)**2+((yy-50)/1300)**2))
        rgb=base[None,None,:]+glow[:,:,None]*np.array([23,5,6])
    else:
        base=np.array([244,247,248],dtype=np.float32)
        glow=np.exp(-(((xx-1080)/900)**2+((yy-1200)/1400)**2))
        rgb=base[None,None,:]+glow[:,:,None]*np.array([-24,-6,-9])
    rng=np.random.default_rng(22)
    rgb += rng.uniform(-.55,.55,(H,W,1))
    return Image.fromarray(np.uint8(np.clip(rgb,0,255))).convert("RGBA")

def background(mode,t):
    im=bg(mode).copy()
    d=ImageDraw.Draw(im)
    dark=mode=="dark"
    c="#214558" if dark else "#DCEAE8"
    ox=85*math.sin(t*.27)
    oy=50*math.cos(t*.32)
    for r in [380,510,640]:
        d.ellipse((720-r+ox,1130-r+oy,720+r+ox,1130+r+oy),outline=c,width=2)
    for j in range(4):
        x=90+j*24
        d.ellipse((x,1745,x+5,1750), fill=MINT if dark else TEAL)
    return im

@lru_cache(None)
def logo(dark, width):
    a=Image.open(ROOT/"brand"/("logo-light.png" if dark else "logo.png")).convert("RGBA")
    a=a.crop(a.getbbox())
    return a.resize((width,round(a.height*width/a.width)),Image.Resampling.LANCZOS)

def header(im,section,dark=False):
    paste(im,logo(dark,184),84,145)
    txt(im,section,996,158,23,"#9FBAC6" if dark else MUTED,center=False) if False else None
    s=text_sprite(section,23,"#9FBAC6" if dark else MUTED)
    paste(im,s,996-s.width,158)

def footer(im,dark=False,ui=False):
    if ui:
        txt(im,"Wizualizacja interfejsu",540,1718,22,"#ABC6D0" if dark else MUTED,center=True)

@lru_cache(64)
def panel(w,h,fill=WHITE,radius=34):
    pad=42
    sh=Image.new("RGBA",(w+2*pad,h+2*pad))
    d=ImageDraw.Draw(sh)
    d.rounded_rectangle((pad, pad+13,pad+w,pad+h+13),radius,fill=(13,43,58,24))
    sh=sh.filter(ImageFilter.GaussianBlur(19))
    d=ImageDraw.Draw(sh)
    d.rounded_rectangle((pad,pad,pad+w,pad+h),radius,fill=fill)
    return sh

def card(im,x,y,w,h,fill=WHITE,p=1,dy=65):
    paste(im,panel(w,h,fill),x-42,y-42+dy*(1-p),p)

def pill(im,s,x,y,w,fill=TEAL,color=WHITE,sz=28,p=1):
    h=64
    a=Image.new("RGBA",(w,h))
    d=ImageDraw.Draw(a)
    d.rounded_rectangle((0,0,w-1,h-1),32,fill=fill)
    atext=text_sprite(s,sz,color,"bold")
    paste(a,atext,(w-atext.width)/2,(h-atext.height)/2+2)
    paste(im,a,x,y+24*(1-p),p)

def icon(im,kind,x,y,size=54,color=TEAL,p=1):
    a=Image.new("RGBA",(size+8,size+8))
    d=ImageDraw.Draw(a)
    def q(v): return round(v*size/64)
    col=rgba(color)
    if kind=="calendar":
        d.rounded_rectangle((q(8),q(12),q(57),q(57)),q(7),outline=col,width=3)
        d.line((q(8),q(26),q(57),q(26)),fill=col,width=3)
        for dx in [21,44]:d.line((q(dx),q(5),q(dx),q(19)),fill=col,width=3)
        for dx in [21,33,45]:
            for dy in [37,47]:d.ellipse((q(dx-2),q(dy-2),q(dx+2),q(dy+2)),fill=col)
    elif kind=="mail":
        d.rounded_rectangle((q(6),q(14),q(58),q(53)),q(7),outline=col,width=3)
        d.line([(q(8),q(17)),(q(32),q(36)),(q(56),q(17))],fill=col,width=3)
    elif kind=="check":
        d.rounded_rectangle((q(9),q(9),q(55),q(55)),q(10),outline=col,width=3)
        d.line([(q(20),q(33)),(q(29),q(42)),(q(46),q(23))],fill=col,width=4)
    elif kind=="grade":
        d.line((q(13),q(53),q(13),q(30)),fill=col,width=5)
        d.line((q(32),q(53),q(32),q(12)),fill=col,width=5)
        d.line((q(51),q(53),q(51),q(22)),fill=col,width=5)
    paste(im,a,x,y,p)

@lru_cache(None)
def phone_art(which,width):
    if which=="home":
        screen=Image.open(ROOT/"skula-04-start-360.png").convert("RGBA")
    else:
        sheet=Image.open(ROOT/"skula-02-ekrany.png").convert("RGBA")
        screen=sheet.crop((490,209,880,1053)) if which=="calendar" else sheet.crop((925,209,1315,1053))
    h=round(width*screen.height/screen.width)
    screen=screen.resize((width,h),Image.Resampling.LANCZOS)
    mask=Image.new("L",(width,h))
    ImageDraw.Draw(mask).rounded_rectangle((0,0,width-1,h-1),radius=round(width*.1),fill=255)
    screen.putalpha(mask)
    a=Image.new("RGBA",(width+100,h+100))
    sh=Image.new("RGBA",a.size)
    ImageDraw.Draw(sh).rounded_rectangle((40,50,width+60,h+70),radius=round(width*.12),fill=(3,22,34,80))
    a.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    d=ImageDraw.Draw(a)
    d.rounded_rectangle((40,30,width+60,h+50),radius=round(width*.12),fill="#102D3E",outline="#406474",width=3)
    paste(a,screen,50,40)
    return a

def phone(im,which,x,y,width,p=1,angle=0):
    a=phone_art(which,width)
    paste(im,a,x-50,y-40+90*(1-p),p,angle=angle)

def floating_card(title,body,kind,w=760):
    a=Image.new("RGBA",(w+84,255))
    paste(a,panel(w,166),0,0)
    icon(a,kind,70,83,54)
    txt(a,title,151,70,24,TEAL,"bold")
    txt(a,body,151,112,39,NAVY,"bold")
    return a

@lru_cache(None)
def intro_cards():
    return [
        floating_card("PLAN LEKCJI","08:00  Matematyka","calendar",720),
        floating_card("ZADANIA DOMOWE","Co jest na jutro?","check",720),
        floating_card("WIADOMOŚCI","Zebranie rodziców","mail",720),
        floating_card("OCENY","Nowy wpis w dzienniku","grade",720)
    ]

def shot0(t):
    im=background("light",t); header(im,"SZKOLNY RYTM")
    line_title(im,["Szkolny dzień.","Tyle spraw."],330,t,size=105,gap=124)
    txt(im,"Plan. Zadania. Oceny. Wiadomości.",84,621,39,MUTED,p=ent(t,.3))
    for j,a in enumerate(intro_cards()):
        p=ent(t,.2+j*.12,.8)
        settle=smooth((t-2.25)/1.2)
        angle=[-5,4,-3,3][j]*(1-settle)
        x=108+([30,-20,40,0][j])*(1-settle)
        y=775+j*194+12*math.sin(t*1.7+j)*(1-settle)
        paste(im,a,x-42+140*(1-p),y-42,p,angle=angle)
    txt(im,"Czas to poukładać.",84,1600,48,TEAL,"bold",ent(t,2.4))
    return im

def shot1(t):
    im=background("dark",t+4); header(im,"APLIKACJA NA ANDROIDA",True)
    line_title(im,["Poznaj Skulę."],323,t,True,size=109)
    txt(im,"Szkolne sprawy w jednym miejscu.",84,475,42,"#C0D6DD",p=ent(t,.22))
    p=ent(t,.12,.95)
    phone(im,"home",308,610+8*math.sin(t*1.2),464,p)
    pill(im,"Plan lekcji",98,857,225,MINT,NAVY,p=ent(t,.85))
    pill(im,"Oceny",769,1102,175,WHITE,NAVY,p=ent(t,1.1))
    pill(im,"Zadania",110,1370,195,MINT,NAVY,p=ent(t,1.35))
    footer(im,True,True)
    return im

def shot2(t):
    im=background("light",t+8);header(im,"01 / PLAN DNIA")
    line_title(im,["Plan dnia.","Pod kontrolą."],320,t,size=101,gap=121)
    txt(im,"Lekcje, terminy i przypomnienia.",84,607,41,MUTED,p=ent(t,.25))
    phone(im,"calendar",522,731,440,ent(t,.25),angle=-1.5+math.sin(t*.8)*.4)
    p=ent(t,.55)
    y=890+50*(1-p)
    card(im,84,y,555,305,p=p,dy=0)
    icon(im,"calendar",120,y+35,52,p=p)
    txt(im,"NAJBLIŻSZA LEKCJA",194,y+48,24,TEAL,"bold",p)
    txt(im,"08:00",120,y+112,89,NAVY,"bold",p)
    txt(im,"Matematyka",120,y+223,40,NAVY,"bold",p)
    p2=ent(t,1.25)
    card(im,111,1280,470,170,TEAL,p2)
    txt(im,"Wszystko ma swój czas.",146,1325,32,WHITE,"bold",p2)
    txt(im,"Ty masz spokojniejszy dzień.",146,1378,27,"#D8F9EF",p=p2)
    footer(im,False,True)
    return im

def draw_check(im,x,y,p):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y,x+65,y+65),16,fill=TEAL if p>0 else "#FFFFFF",outline=TEAL if p>0 else "#BBD1D7",width=3)
    if p>0:
        pts=[(x+16,y+34),(x+29,y+46),(x+51,y+21)]
        p=clamp(p)
        if p<.4:
            end=(pts[0][0]+(pts[1][0]-pts[0][0])*p/.4,pts[0][1]+(pts[1][1]-pts[0][1])*p/.4)
            d.line([pts[0],end],fill=WHITE,width=6)
        else:
            d.line(pts[:2],fill=WHITE,width=6)
            f=(p-.4)/.6
            end=(pts[1][0]+(pts[2][0]-pts[1][0])*f,pts[1][1]+(pts[2][1]-pts[1][1])*f)
            d.line([pts[1],end],fill=WHITE,width=6)

def shot3(t):
    im=background("light",t+12);header(im,"02 / ZADANIA")
    line_title(im,["Zadania?","Odhaczone."],320,t,size=108,gap=124)
    txt(im,"Małe kroki. Spokojniejszy dzień.",84,613,42,MUTED,p=ent(t,.25))
    p=ent(t,.25)
    y=755+70*(1-p)
    card(im,84,y,912,664,p=p,dy=0)
    txt(im,"ZADANIA DOMOWE",126,y+49,27,TEAL,"bold",p)
    pill(im,"Na jutro",768,y+33,181,"#F9F0DF","#87632F",27,p)
    q1=smooth((t-1.)/.35);q2=smooth((t-2.)/.35)
    if p>.97:
        draw_check(im,130,round(y+164),q1)
        draw_check(im,130,round(y+346),q2)
    txt(im,"Ćwiczenia z ułamków",227,y+160,41,NAVY,"bold",p)
    txt(im,"Matematyka · str. 42, zad. 1–3",227,y+220,30,MUTED,p=p)
    ImageDraw.Draw(im).line((126,y+300,952,y+300),fill="#E3ECEE",width=2)
    txt(im,"Słówka: my neighbourhood",227,y+344,36,NAVY,"bold",p)
    txt(im,"Język angielski · rozdział 3",227,y+405,30,MUTED,p=p)
    bar_y=y+518
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((128,bar_y,950,bar_y+16),8,fill="#E8F2EF")
    amount=(q1+q2)/2
    if amount>0:d.rounded_rectangle((128,bar_y,128+822*amount,bar_y+16),8,fill=TEAL)
    txt(im,f"{int(q1>.99)+int(q2>.99)} z 2 zadań oznaczonych jako zrobione",128,y+570,29,MUTED,p=p)
    pill(im,"Gotowe. Możesz odetchnąć.",249,1500,582,TEAL,WHITE,33,ent(t,2.45))
    footer(im,False,True)
    return im

def shot4(t):
    im=background("dark",t+16); header(im,"03 / NA BIEŻĄCO",True)
    line_title(im,["Wiesz,","co nowego."],320,t,True,size=107,gap=122)
    txt(im,"Oceny i wiadomości pod ręką.",84,611,43,"#C0D6DD",p=ent(t,.25))
    phone(im,"messages",548,745,412,ent(t,.18),angle=1.8)
    p=ent(t,.6)
    y=907+60*(1-p)
    card(im,84,y,530,248,p=p,dy=0)
    d=ImageDraw.Draw(im)
    if p>.95:d.rounded_rectangle((120,y+49,238,y+171),27,fill="#E4F4EE")
    txt(im,"5",179,y+66,80,TEAL,"bold",p,True)
    txt(im,"Matematyka",267,y+63,35,NAVY,"bold",p)
    txt(im,"Nowa ocena",267,y+119,29,MUTED,p=p)
    txt(im,"Praca klasowa",122,y+193,26,MUTED,p=p)
    p2=ent(t,1.3)
    card(im,112,1285,838,231,p=p2)
    icon(im,"mail",151,1332,58,p=p2)
    txt(im,"NOWA WIADOMOŚĆ",238,1323,26,TEAL,"bold",p2)
    txt(im,"Zebranie rodziców",238,1376,45,NAVY,"bold",p2)
    txt(im,"Ważne informacje w jednym miejscu.",151,1455,29,MUTED,p=p2)
    footer(im,True,True)
    return im

def shot5(t):
    im=background("mint",t+20)
    header(im,"TWÓJ SZKOLNY RYTM")
    p=ent(t,.12,.85)
    a=logo(False,590)
    paste(im,a,(W-a.width)/2,455+38*(1-p),p)
    line_title(im,["Mniej chaosu.","Więcej spokoju."],810,t-.12,x=540,size=94,gap=119,center=True)
    txt(im,"Szkolne sprawy zawsze pod ręką.",540,1110,39,MUTED,p=ent(t,.65),center=True)
    pill(im,"APLIKACJA NA ANDROIDA",285,1224,510,WHITE,NAVY,27,ent(t,.8))
    # A readable final call to action without an unverified store link.
    pp=ent(t,1.05)
    a=Image.new("RGBA",(660,122))
    d=ImageDraw.Draw(a)
    d.rounded_rectangle((0,0,659,121),61,fill=NAVY)
    txt(a,"Poznaj Skulę",290,34,46,WHITE,"bold",center=True)
    d.line((530,61,581,61),fill=MINT,width=5)
    d.line([(563,43),(583,61),(563,79)],fill=MINT,width=5)
    paste(im,a,210,1395+30*(1-pp),pp)
    # Gentle settling particles; final CTA stays still long enough to read.
    for j in range(8):
        angle=j*math.tau/8+t*.1
        cx=540+math.cos(angle)*390
        cy=591+math.sin(angle)*250
        r=4+j%3
        ImageDraw.Draw(im).ellipse((cx-r,cy-r,cx+r,cy+r),fill=TEAL if j%2 else MINT)
    return im

SHOTS=[shot0,shot1,shot2,shot3,shot4,shot5]

def frame(t):
    shot=min(5,int(t//4))
    local=t-shot*4
    im=SHOTS[shot](local)
    # Smooth short dissolves between full compositions, no black frames.
    if shot>0 and local<.3:
        old=SHOTS[shot-1](4+local)
        im=Image.blend(old,im,smooth(local/.3))
    return im.convert("RGB")

def soundtrack():
    sr=48000;n=SECONDS*sr
    out=np.zeros((n,2),dtype=np.float64)
    rng=np.random.default_rng(42)
    def add(sig,start,pan=0,level=1):
        pos=round(start*sr)
        if pos<0:return
        count=min(len(sig),n-pos)
        if count<=0:return
        left=math.sqrt((1-pan)/2);right=math.sqrt((1+pan)/2)
        out[pos:pos+count,0]+=sig[:count]*left*level
        out[pos:pos+count,1]+=sig[:count]*right*level
    def note(midi,dur,kind="pluck"):
        tt=np.arange(round(dur*sr))/sr
        f=440*2**((midi-69)/12)
        if kind=="pad":
            env=np.minimum(tt/.45,1)*np.minimum((dur-tt)/.75,1)
            sig=(np.sin(math.tau*f*tt)+.28*np.sin(math.tau*f*2.002*tt)+.16*np.sin(math.tau*f*.998*tt))*env
        elif kind=="bass":
            env=np.minimum(tt/.015,1)*np.exp(-tt*5)*np.minimum((dur-tt)/.07,1)
            sig=(np.sin(math.tau*f*tt)+.13*np.sin(math.tau*f*2*tt))*env
        else:
            env=np.minimum(tt/.006,1)*np.exp(-tt*4.6)*np.minimum((dur-tt)/.08,1)
            sig=(np.sin(math.tau*f*tt)+.28*np.sin(math.tau*f*2*tt)+.07*np.sin(math.tau*f*3*tt))*env
        return sig
    chords=[[50,57,61,66,69],[47,54,57,62,66],[43,50,54,59,62],[45,52,57,59,64],[50,57,61,66,69],[50,57,62,66,69]]
    roots=[38,35,31,33,38,38]
    for bar,chord in enumerate(chords):
        start=bar*4.
        for j,midi in enumerate(chord):
            add(note(midi,4.7,"pad"),start,pan=(j-2)*.23,level=.030)
        melody=[chord[2]+12,chord[4]+12,chord[3]+12,chord[1]+12,chord[2]+12,chord[3]+12,chord[4]+12,chord[3]+12]
        for j,midi in enumerate(melody):
            at=start+j*.5
            a=note(midi,.9)
            add(a,at,pan=math.sin(j*1.7)*.4,level=.085 if j%2==0 else .055)
            add(a,at+.25,pan=-math.sin(j*1.7)*.4,level=.022)
        for beat in range(8):
            at=start+beat*.5
            if at>22.5:continue
            add(note(roots[bar]+(12 if beat%4==3 else 0),.38,"bass"),at,level=.15)
            tt=np.arange(int(.25*sr))/sr
            phase=math.tau*(48*tt+100*.035*(1-np.exp(-tt/.035)))
            kick=np.sin(phase)*np.exp(-tt*20)*np.minimum(tt/.004,1)
            add(kick,at,level=.18)
            if beat%2==1:
                tt=np.arange(int(.16*sr))/sr
                noise=rng.standard_normal(len(tt))
                noise=np.concatenate([[0],np.diff(noise)])*.35
                clap=noise*np.exp(-tt*35)*np.minimum(tt/.003,1)
                add(clap,at,pan=.08,level=.065)
            for off in [0,.25]:
                tt=np.arange(int(.065*sr))/sr
                noise=rng.standard_normal(len(tt))
                noise=np.concatenate([[0],np.diff(noise)])*.3
                hat=noise*np.exp(-tt*65)*np.minimum(tt/.002,1)
                add(hat,at+off,pan=-.3 if off==0 else .3,level=.035 if off==0 else .022)
    # Subtle melodic confirmation accents, aligned to animated checks.
    for at,midi in [(13.05,81),(14.05,86),(21.1,86)]:
        add(note(midi,.7),at,pan=.2,level=.045)
    # Short soft transition risers.
    for at in [3.72,7.72,11.72,15.72,19.72]:
        tt=np.arange(int(.4*sr))/sr
        noise=rng.standard_normal(len(tt))
        noise=np.convolve(noise,np.ones(18)/18,mode="same")
        env=np.sin(math.pi*tt/.4)**2
        add(noise*env,at,pan=0,level=.06)
    tt=np.arange(n)/sr
    env=np.minimum(tt/.18,1)*np.minimum((SECONDS-tt)/1.1,1)
    out*=env[:,None]
    peak=float(np.max(np.abs(out)))
    out*=.79/max(peak,.79)
    with wave.open(str(HERE/"skula-muzyka-original.wav"),"wb") as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr)
        f.writeframes((np.clip(out,-1,1)*32767).astype("<i2").tobytes())
    print(f"Audio: 48 kHz stereo, peak {np.max(np.abs(out)):.3f}",flush=True)

def preview():
    times=[2.8,6.6,10.6,14.8,18.8,22.8]
    sheet=Image.new("RGB",(1080,1280),"#D9E5E6")
    for i,t in enumerate(times):
        im=frame(t)
        im.save(HERE/f"scena-{i+1:02d}.jpg",quality=94)
        thumb=im.resize((360,640),Image.Resampling.LANCZOS)
        sheet.paste(thumb,((i%3)*360,(i//3)*640))
    sheet.save(HERE/"storyboard.jpg",quality=94)
    frame(22.8).save(HERE/"skula-okladka.jpg",quality=95)
    print("Storyboard and six preview frames saved.",flush=True)

def render():
    soundtrack();preview()
    args=[FFMPEG,"-hide_banner","-y","-f","rawvideo","-vcodec","rawvideo","-pix_fmt","rgb24",
          "-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-i",str(HERE/"skula-muzyka-original.wav"),
          "-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","fast","-crf","18",
          "-pix_fmt","yuv420p","-profile:v","high","-level","4.1",
          "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
          "-c:a","aac","-b:a","192k","-ar","48000","-af","loudnorm=I=-16:TP=-1.5:LRA=9",
          "-t",str(SECONDS),"-movflags","+faststart","-metadata","title=Skula — Mniej chaosu. Więcej spokoju.",
          "-metadata","comment=Polska reklama, wizualizacje interfejsu, autorski podkład instrumentalny.",
          str(OUTPUT)]
    with open(HERE/"render.log","w",encoding="utf-8") as log:
        proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=log,stderr=log)
        try:
            for i in range(SECONDS*FPS):
                proc.stdin.write(frame(i/FPS).tobytes())
                if i%60==0: print(f"Rendering {i}/{SECONDS*FPS} frames ({i/FPS:.0f}s)",flush=True)
        except BaseException:
            proc.kill();proc.wait();raise
        finally:
            proc.stdin.close()
        rc=proc.wait()
    if rc:raise RuntimeError(f"FFmpeg failed ({rc}); see render.log")
    print(f"Finished: {OUTPUT}",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--preview",action="store_true");args=p.parse_args()
    if args.preview:preview()
    else:render()

