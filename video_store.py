#!/usr/bin/env python3
"""매장 가격표 영상에서 사람이 읽어 적은 TSV(video/*.tsv)를 store_data.json으로 변환. 종료일이 지난 품목은 제외."""
import csv, json, os, re, datetime
H=os.path.dirname(os.path.abspath(__file__)); KST=datetime.timezone(datetime.timedelta(hours=9))
today=datetime.datetime.now(KST).date()
CATS=[("정육·수산·신선",r"사과|아보카도|레몬|고구마|마늘|루꼴라|카이피라|건가지|명란|장조림|닭 가슴살|버팔로|어묵|크래미|골뱅이|꽁치|번데기|다시마|햄|돈까스"),
("가공·간편식",r"치킨|순살|피자|우동|쫄면|칼국수|막국수|라면|볶음면|추어탕|설농탕|석박지|청국장|스프|햇반|약밥|흑미밥|쌀|찹|현미|체질|낫또|맥스봉|고구마|육수|치킨스톡|쯔유|올리브|마시멜로|그래놀라|빼빼로|보름달|떡|호두과자|마카다미아|크림치즈|요거트|엔요"),
("음료·커피",r"주스|두유|수염차|소다|스프라이트|라떼|모카|쌍화차|홍삼|전해질|코코컵"),
("생활·세제",r"유연제|세탁|세정제|수세미|티슈|타월|호일|필터|버블|로션"),
("반려동물",r"츄르|쥬레|애견|비스트로"),("의류·잡화",r"양말|브라|티셔츠|베스트|슬립온|가방"),
("가전·침구",r"보이러|토퍼|찜기")]
def cat(n):
    for c,p in [CATS[3],CATS[4],CATS[5],CATS[6],CATS[2],CATS[0],CATS[1]]:
        if re.search(p,n): return c
    return "기타"
n=lambda s:int(s) if s and s.strip() else None
items=[];dropped=0
for v in json.load(open(os.path.join(H,"video","videos.json"),encoding="utf-8")):
    for r in csv.DictReader(open(os.path.join(H,"video",v["tsv"]),encoding="utf-8"),delimiter="\t"):
        end=r["end"] or None
        if end and datetime.date.fromisoformat(end)<today: dropped+=1; continue
        m,s=map(int,r["t"].split(":")); reg,d,sale=n(r["regular"]),n(r["discount"]),n(r["sale"])
        items.append(dict(code=r["code"],name=r["name"],category=cat(r["name"]),regular_price=reg,discount=d,sale_price=sale,
          discount_rate=round(d/reg*100,1) if reg and d else None,start=end and r["start"][5:].replace("-","."),end=end and end[5:].replace("-","."),
          source=v["source"],url=f'https://www.youtube.com/watch?v={v["id"]}&t={m*60+s}s',video_time=r["t"],image=None,
          status="미확인" if r["flag"].strip() else "확인",note=r["flag"].strip() or None))
ends=[i["end"] for i in items if i["end"]]
out=dict(updated=datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),count=len(items),dropped_expired=dropped,
  period=[min(i["start"] for i in items if i["start"]),max(ends)] if ends else None,
  sources=json.load(open(os.path.join(H,"video","videos.json"),encoding="utf-8")),items=items)
json.dump(out,open(os.path.join(H,"store_data.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("매장",len(items),"개 (만료 제외",dropped,")")
