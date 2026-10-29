#!/usr/bin/env python3
"""/workspace/yt/popular_raw.json(유튜브 집계) + 수동 활용법/매장매칭 → wanted.json 의 popular 섹션. 원산지는 costco.co.kr 상품상세 API 근거만."""
import json, os, re, urllib.request, datetime
H=os.path.dirname(os.path.abspath(__file__)); KST=datetime.timezone(datetime.timedelta(hours=9))
raw=json.load(open("/workspace/yt/popular_raw.json",encoding="utf-8"))
store={i["code"]:i for i in json.load(open(os.path.join(H,"store_data.json"),encoding="utf-8"))["items"]}
# 활용법: 수집한 영상 설명·댓글 문장을 요약 (근거 문장 없으면 None)
TIP={"치즈":"벽돌 모짜렐라는 샌드위치용 슬라이스·간식용 큐브로 잘라 냉동 소분 (영상 설명 타임라인)",
"계란":"뾰족한 쪽이 아래로 가게 보관하라는 댓글이 여러 개, 판째 넣는 계란 정리함 추천 (댓글)",
"새우":"냉동 새우는 파스타 토핑·새우장에 활용. 단 생으로 양념장 담그면 위험하다는 댓글도 있음 (댓글)",
"피자":"도우를 냉장 숙성 후 에어프라이어로 굽는 법 소개 (영상 설명)",
"버터":"버터 소분틀로 잘라 빵·치즈와 함께 소분 보관 (영상 설명·댓글)",
"냄비/프라이팬":None,"아보카도":None,
"김치":"남은 고기와 함께 냉동 김치찜 밀키트로 만들어 두기 (영상 설명)",
"딸기":None,"세제":None,
"샐러드":"남은 채소는 샐러드로, 샐러드 토퍼는 소분 보관 (영상 설명·댓글)",
"그릭요거트":"꿀·바질·토마토 조합, 요거트 바크 레시피로 활용 (댓글·영상 설명)",
"부채살":"손질해 스테이크용으로 소분해 두면 먹기 편함 (영상 설명·댓글)",
"소불고기":"덮밥·파스타로 활용, 소분해 보관 (댓글)",
"연어":"대용량은 받자마자 소분 (영상 설명)",
"블루베리":None,
"올리브오일":"치즈·바질 샌드위치에 곁들여 냉동 보관 (영상 설명)",
"꿀":"그릭요거트에 곁들임 (댓글)",
"키친타월":"낱개 포장이라 보관이 편하다는 댓글 (댓글)",
"떡볶이·떡":None,
"로티세리 치킨":"다리·날개를 분리해 나눠 보관한다는 댓글 (댓글)",
"라면":None,"핫도그":"번·소시지 소분 이야기 (댓글)","밀폐용기":None,
"초콜릿":"초콜릿 케이크는 데워 먹으면 퐁당오쇼콜라 같다는 댓글 (댓글)"}
# 현재 매장 할인 중인 같은 종류 상품 (영상 가격표 상품번호)
MATCH={"냄비/프라이팬":["670208","678567"],"세제":["680688","695501","607206"],"김치":["563542","682484"],"피자":["663486"],"냉동 만두":["665140","625256"],"와인":["683369"],"라면":["620834","616212","612003"],"쌀":["610038","686497"]}
def origin(code):
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://www.costco.co.kr/rest/v2/korea/products/{code}?fields=FULL&lang=ko",headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
    except Exception: return "미확인",None
    F={f.get("name"):" ".join(v.get("value","") for v in f.get("featureValues",[])) for c in d.get("classifications",[]) for f in c.get("features",[])}
    for k,v in F.items():
        if re.search(r"원산지|제조국",k or ""):
            if re.search(r"국내|대한민국|한국|국산",v): return "국산·국내생산",f"{k}: {v[:60]}"
            if v.strip(): return "수입",f"{k}: {v[:60]}"
    imp=next((v for k,v in F.items() if "수입신고" in (k or "")),None); prod=next((v for k,v in F.items() if "생산자" in (k or "") or "제조자" in (k or "")),"")
    if imp and "해당사항 없음" in imp and re.search(r"특별시|광역시|도 |경기|충청|전라|경상|강원|제주|서울",prod): return "국산·국내생산",f"생산자: {prod[:50]} / 수입신고: 해당사항 없음"
    if imp and "필함" in imp and "없음" not in imp: return "수입",f"수입신고: {imp[:40]}"
    return "미확인",None
P=os.path.join(H,"wanted.json"); W=json.load(open(P,encoding="utf-8"))
now=datetime.datetime.now(KST)
pop=[]
for x in raw["items"][:25]:
    codes=[c for c in MATCH.get(x["item"],[]) if c in store]; orig=[]
    for c in codes:
        o,ev=origin(c)
        if o=="미확인":
            n=store[c]["name"]
            if "(국내산)" in n: o,ev="국산·국내생산","매장 가격표 원산지: 국내산"
            else:
                m=re.search(r"\((페루|칠레|미국|호주|뉴질랜드|중국)\)",n)
                if m: o,ev="수입","매장 가격표 원산지: "+m.group(1)
        orig.append(dict(code=c,name=store[c]["name"],origin=o,evidence=ev))
    pop.append(dict(item=x["item"],video_mentions=x["video_mentions"],comment_mentions=x["comment_mentions"],comment_likes=x["comment_likes"],
      evidence=x["evidence"][:2],usage=TIP.get(x["item"]) or "영상·댓글에서 활용법 미확인",
      on_sale_now=bool(codes),sale_items=[dict(code=c,name=store[c]["name"],sale_price=store[c]["sale_price"],discount=store[c]["discount"],end=store[c]["end"]) for c in codes],
      origin_items=orig,domestic=any(o["origin"]=="국산·국내생산" for o in orig),
      last_mentioned=max([e["date"] for e in x["evidence"]] or [None])))
W["popular"]=dict(updated=now.strftime("%Y-%m-%d %H:%M KST"),videos=len(raw["videos"]),recent_videos=raw["n_recent"],comments=raw["comments"],
  video_list=raw["videos"],items=pop)
W.setdefault("popular_history",[]).append(dict(at=now.strftime("%Y-%m-%d"),top=[(p["item"],p["video_mentions"],p["comment_mentions"]) for p in pop]))
json.dump(W,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
for p in pop: print(p["item"],p["video_mentions"],p["comment_mentions"],p["on_sale_now"],[(o["name"][:20],o["origin"],o["evidence"]) for o in p["origin_items"]])
