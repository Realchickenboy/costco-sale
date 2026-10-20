import json,html,math,os,subprocess,base64,mimetypes
d=json.load(open('store_data.json'));cats=[('정육·수산·신선','#d7000f',8),('가공·간편식','#f07800',10),('생활·세제','#0057b8',7),('음료·커피','#14903a',7)]
f=lambda n:f"{n:,}"
pts=[];
for k in range(32):
  r=50 if k%2==0 else 40;a=math.pi*2*k/32;pts.append(f"{50+r*math.cos(a):.1f}% {50+r*math.sin(a):.1f}%")
star="polygon("+",".join(pts)+")"
REP=[];secs="";inc=0;tot=0
for c,col,n in cats:
  its=[i for i in d['items'] if i['category']==c];tot+=len(its)
  its=sorted(its,key=lambda i:-(i['discount'] or 0))[:n];inc+=len(its)
  cells=""
  for i in its:
    reg=f"<s>정상가 {f(i['regular_price'])}원</s>" if i['regular_price'] else "<s class=e>&nbsp;</s>"
    un='<span class=un>미확인</span>' if i['status']=='미확인' else ''
    sp=f"{f(i['sale_price'])}<small>원</small>" if i['sale_price'] else '<small>가격 미확인</small>'
    img=i.get('image');ph="<div class='ph none'></div>"
    if img and 'video' not in (i.get('image_src') or '') and img.startswith('http'):
      fn='poster_img/'+i['code']+os.path.splitext(img.split('?')[0])[1]
      if not os.path.exists(fn) or os.path.getsize(fn)<500: subprocess.run(['curl','-sL','--max-time','20','-o',fn,img])
      if os.path.exists(fn) and os.path.getsize(fn)>500:
        b=base64.b64encode(open(fn,'rb').read()).decode();mt=mimetypes.guess_type(fn)[0] or 'image/jpeg'
        ref="<span class=ref>참고 사진</span>" if '참고' in (i.get('image_src') or '') else ''
        ph=f"<div class=ph><img src='data:{mt};base64,{b}'>{ref}</div>";REP.append((i['name'],bool(ref)))
      else: REP.append((i['name'],None))
    else: REP.append((i['name'],None))
    cells+=f"<div class=cell>{ph}<div class=st><span>{f(i['discount'])}원<br>할인</span></div><div class=nm>{html.escape(i['name'])}{un}</div>{reg}<div class=pr>{sp}</div></div>"
  secs+=f"<section><h2 style='background:{col}'>{c}</h2><div class=grid>{cells}</div></section>"
import collections,datetime
_e=collections.Counter(i['end'] for i in d['items'] if i.get('end'))
END=''
if _e:
  _m=_e.most_common(1)[0][0];_mo,_dd=map(int,_m.split('.'));END=_m+'('+'월화수목금토일'[datetime.date(datetime.date.today().year,_mo,_dd).weekday()]+')'
open('poster2.html','w').write(f"""<html><head><meta charset=utf-8><style>
*{{box-sizing:border-box;margin:0}}body{{width:1080px;background:#fff;font-family:'Pretendard','Noto Sans CJK KR',sans-serif;color:#000;padding:0 0 30px}}
.ban{{background:#e31837;color:#fff;text-align:center;padding:30px 20px 26px;border-bottom:10px solid #ffd400}}
.ban .t{{font-size:34px;font-weight:900;background:#ffd400;color:#e31837;display:inline-block;padding:4px 22px;border-radius:8px;transform:rotate(-2deg)}}
.ban h1{{font-size:82px;font-weight:900;letter-spacing:-3px;margin:12px 0 6px;text-shadow:4px 4px 0 #8a000c}}
.ban .p{{font-size:36px;font-weight:900}}.ban .p b{{background:#fff;color:#e31837;padding:2px 14px;border-radius:6px}}.ban .n{{font-size:22px;margin-top:10px;font-weight:700}}
section{{margin:22px 18px 0}}h2{{color:#fff;font-size:40px;font-weight:900;padding:8px 24px;border-radius:10px 10px 0 0;letter-spacing:-1px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);border:4px solid #000;border-top:none}}
.cell{{position:relative;border-right:3px solid #000;border-bottom:3px solid #000;padding:18px 16px 14px;min-height:250px;display:flex;flex-direction:column}}
.cell:nth-child(3n){{border-right:none}}
.nm{{font-size:25px;font-weight:900;line-height:1.25;min-height:94px;margin-top:12px}}
.ph{{position:relative;width:190px;height:190px;background:#fff;border:2px solid #ddd;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.ph img{{max-width:174px;max-height:174px;object-fit:contain}}.ph.none{{border:2px dashed #ddd}}.ph.none::after{{content:'사진 없음';color:#bbb;font-size:18px;font-weight:700}}
.ref{{position:absolute;left:4px;bottom:4px;background:rgba(0,0,0,.65);color:#fff;font-size:14px;padding:1px 6px;border-radius:4px}}
.un{{display:inline-block;margin-left:6px;font-size:17px;background:#000;color:#ffd400;padding:1px 7px;border-radius:4px;vertical-align:middle}}
s{{font-size:19px;color:#555;margin-top:auto}}.pr{{color:#e31837;font-size:60px;font-weight:900;letter-spacing:-3px;line-height:1}}.pr small{{font-size:28px;letter-spacing:0}}
.st{{position:absolute;top:8px;right:8px;width:126px;height:126px;background:#e31837;clip-path:{star};display:flex;align-items:center;justify-content:center}}
.st::before{{content:'';position:absolute;inset:6px;background:#ffd400;clip-path:{star}}}
.st span{{position:relative;color:#e31837;font-weight:900;font-size:20px;text-align:center;line-height:1.1}}
footer{{margin:26px 18px 0;text-align:center;font-size:22px;font-weight:700;line-height:1.7;border-top:4px solid #000;padding-top:16px}}footer .u{{font-size:30px;font-weight:900;color:#e31837}}
</style></head><body><div class=ban><div class=t>먹거리 · 생필품 특가!</div><h1>코스트코 이번 주 매장 할인</h1>
<div class=p>대부분 <b>~{END}</b> 까지</div><div class=n>일부 품목 · 전체는 사이트에서 · 매장·시기에 따라 다를 수 있어요</div></div>{secs}
<footer>출처: CoReview 유튜브 매장 영상 · 방문자 제보<br><span class=u>realchickenboy.github.io/costco-sale</span><br>제작: X 리얼치킨보이</footer></body></html>""")
print(inc,tot);print(sum(1 for r in REP if r[1] is not None),sum(1 for r in REP if r[1]));print([r[0] for r in REP if r[1] is None])

# render → poster.png (full) + poster.webp (web copy)
import shutil
from PIL import Image
import numpy as np
here=os.path.dirname(os.path.abspath(__file__))
chrome=next((shutil.which(b) for b in ['google-chrome','google-chrome-stable','chromium','chromium-browser'] if shutil.which(b)),None)
full=os.path.join(here,'poster_full.png')
subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--window-size=1080,8000','--screenshot='+full,'file://'+os.path.join(here,'poster2.html')],timeout=120,stderr=subprocess.DEVNULL)
im=Image.open(full).convert('RGB');a=np.array(im);r=int(np.where((a!=255).any(2).any(1))[0][-1])+30
im=im.crop((0,0,1080,r));im.save(os.path.join(here,'poster.png'));im.save(os.path.join(here,'poster.webp'),'WEBP',quality=82,method=6)
json.dump({'w':1080,'h':r},open(os.path.join(here,'poster_meta.json'),'w'))
print('poster',1080,r)
