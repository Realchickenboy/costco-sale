import json,html,collections
d=json.load(open('store_data.json'));cats=['정육·수산·신선','가공·간편식','생활·세제','음료·커피']
N={'정육·수산·신선':8,'가공·간편식':10,'생활·세제':7,'음료·커피':7}
f=lambda n:f"{n:,}"
secs="";inc=0;tot=0;ends=collections.Counter();rep=[]
for c in cats:
  its=[i for i in d['items'] if i['category']==c];tot+=len(its)
  its=sorted(its,key=lambda i:-(i['discount'] or 0))[:N[c]];inc+=len(its)
  rows=""
  for i in its:
    ends[i['end']]+=1;rep.append(f"{c} | {i['name']} | {i['sale_price']} | -{i['discount']} | {i['status']}")
    reg=f"<s>{f(i['regular_price'])}원</s>" if i['regular_price'] else ""
    un='<span class=un>미확인</span>' if i['status']=='미확인' else ''
    sp=f"{f(i['sale_price'])}<small>원</small>" if i['sale_price'] else '<small>가격 미확인</small>'
    rows+=f"<div class=row><div class=nm>{html.escape(i['name'])}{un}</div><div class=pr>{reg}<b>{sp}</b><span class=pill>-{f(i['discount'])}</span></div></div>"
  secs+=f"<section><h2>{c}</h2>{rows}</section>"
end=max((e for e in ends if e),key=lambda e:ends[e])
open('poster.html','w').write(f"""<html><head><meta charset=utf-8><style>
*{{box-sizing:border-box;margin:0}}body{{width:1080px;background:#f5f5f7;font-family:'Pretendard','Noto Sans CJK KR',sans-serif;color:#1d1d1f;padding:64px 56px}}
.top{{font-size:24px;color:#e31837;font-weight:700;letter-spacing:1px}}h1{{font-size:68px;font-weight:800;letter-spacing:-2px;margin:10px 0 8px}}
.sub{{font-size:28px;color:#6e6e73}}.note{{display:inline-block;margin-top:18px;font-size:22px;background:#fff;border-radius:99px;padding:8px 20px;color:#6e6e73}}
section{{background:#fff;border-radius:32px;padding:30px 40px 14px;margin-top:32px}}h2{{font-size:32px;font-weight:800;margin-bottom:8px}}
.row{{display:flex;justify-content:space-between;align-items:center;gap:20px;padding:16px 0;border-top:1px solid #ececf0}}
.nm{{font-size:25px;font-weight:500;flex:1;line-height:1.3}}.pr{{display:flex;align-items:center;gap:12px;white-space:nowrap}}
s{{color:#a1a1a6;font-size:20px}}b{{font-size:32px;font-weight:800}}small{{font-size:20px}}
.pill{{background:#e31837;color:#fff;font-weight:700;font-size:21px;border-radius:99px;padding:5px 14px}}
.un{{margin-left:10px;font-size:18px;color:#e31837;border:1.5px solid #e31837;border-radius:8px;padding:1px 8px;vertical-align:middle}}
footer{{margin-top:40px;text-align:center;color:#6e6e73;font-size:21px;line-height:1.7}}footer .u{{color:#1d1d1f;font-size:26px;font-weight:700}}
</style></head><body><div class=top>COSTCO KOREA · 먹거리 & 생필품</div><h1>코스트코 이번 주 매장 할인</h1>
<div class=sub>대부분 ~{end} 까지 · 할인액 큰 순</div><div class=note>일부 품목 · 전체는 사이트에서</div>{secs}
<footer>출처: CoReview 유튜브 매장 영상 · 방문자 제보<br>매장·시기에 따라 다를 수 있어요<br><span class=u>realchickenboy.github.io/costco-sale</span><br>제작: X 리얼치킨보이</footer></body></html>""")
print(inc,tot,ends);print("\n".join(rep))
