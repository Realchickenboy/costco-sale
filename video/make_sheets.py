#!/usr/bin/env python3
"""영상에서 2초마다 가격표 영역을 잘라 중복 제거 후 3x4 시트로 묶음. 사용: make_sheets.py video.mp4 [outdir]"""
import sys, os, glob, subprocess
from PIL import Image, ImageDraw
CROP="520:290:760:0"   # 1280x720 기준 오른쪽 위 가격표 오버레이
vid=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else os.path.join(os.path.dirname(vid),"sheets")
cd=os.path.join(out,"crops"); os.makedirs(cd,exist_ok=True)
for f in glob.glob(cd+"/*")+glob.glob(out+"/s_*.jpg"): os.remove(f)
subprocess.run(["ffmpeg","-v","error","-i",vid,"-vf",f"fps=1/2,scale=1280:720,crop={CROP}","-q:v","3",cd+"/c_%04d.jpg"],check=True)
def h(p):
    im=Image.open(p).convert("L").resize((64,36)); px=list(im.getdata()); m=sum(px)/len(px); return [x>m for x in px]
keep=[];prev=None
for p in sorted(glob.glob(cd+"/c_*.jpg")):
    v=h(p)
    if prev is None or sum(a!=b for a,b in zip(v,prev))>80: keep.append(p)
    prev=v
for s in range(0,len(keep),12):
    sh=Image.new("RGB",(1560,1200),"white"); d=ImageDraw.Draw(sh)
    for k,p in enumerate(keep[s:s+12]):
        x,y=(k%3)*520,(k//3)*300; sh.paste(Image.open(p),(x,y)); t=(int(p[-8:-4])-1)*2
        d.rectangle([x,y+272,x+60,y+292],fill="yellow"); d.text((x+3,y+276),f"{t//60}:{t%60:02d}",fill="black")
    sh.save(f"{out}/s_{s//12:02d}.jpg",quality=88)
print(len(keep),"장면 →",out)
