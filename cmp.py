import json,urllib.request,urllib.parse
Q=[("앵커 무염버터","앵커 버터"),("신라면 블랙","신라면 블랙"),("햇반 쌀눈","햇반 쌀눈"),("퍼실 딥클린","퍼실 딥클린"),("다우니 실내건조","다우니 실내건조"),("리퀴드 IV","리퀴드 아이브이"),("챠오츄르","츄르"),("시저 소고기","시저"),("럭스나인 토퍼","럭스나인"),("보이러 전기요","보이러"),("쿡에버 찜기","쿡에버 찜기"),("아디다스 양말","아디다스 양말"),("프랑코페라로 베스트","프랑코페라로"),("니베아 바디로션","니베아 로션"),("웨이더 단백질","웨이더"),("커클랜드 마카다미아","마카다미아"),("이디야 모카블렌드","이디야"),("불닭볶음면 큰컵","불닭 큰컵"),("하림 닭가슴살","하림 닭가슴살"),("리스토란테 피자","리스토란테")]
for lab,q in Q:
  u="https://www.costco.co.kr/rest/v2/korea/products/search?"+urllib.parse.urlencode({"query":q,"pageSize":6,"lang":"ko","curr":"KRW","fields":"FULL"})
  try:d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
  except Exception as e: print(lab,"ERR",e);continue
  print("##",lab,d["pagination"]["totalResults"])
  for p in d.get("products",[])[:6]:
    print("  ",p["code"],p["name"],(p.get("price")or{}).get("value"),"base",(p.get("basePrice")or{}).get("value"),"disc",(p.get("discountPrice")or{}).get("value"),p.get("discountEndDate"),p.get("stock",{}).get("stockLevelStatus"))
