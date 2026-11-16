#!/usr/bin/env python3
"""매장 품목 국산 여부: 가격표 상품명의 '국내산/국산' 표기 또는 costco.co.kr 상품상세 API의 원산지·제조국 항목만 근거로 사용. store_data.json 에 origin/origin_ev 추가."""
import json, os, re, urllib.request, time
H=os.path.dirname(os.path.abspath(__file__))
def api(code):
    for t in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(f"https://www.costco.co.kr/rest/v2/korea/products/{code}?fields=FULL&lang=ko",headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
        except Exception: time.sleep(2)
    return {}
CP=os.path.join(H,"origin_cache.json"); C=json.load(open(CP)) if os.path.exists(CP) else {}
def origin(code):
    if code in C: return tuple(C[code])
    d=api(code)
    F={f.get("name"):" ".join(v.get("value","") for v in f.get("featureValues",[])) for c in d.get("classifications",[]) for f in c.get("features",[])}
    for k,v in F.items():
        if re.search(r"원산지|제조국",k or ""):
            if re.search(r"국내|대한민국|한국|국산",v) and not re.search(r"수입|미국|중국|호주|칠레|베트남|태국|독일|프랑스|이탈리아|일본|덴마크|스페인",v): return "국산·국내생산",f"코스트코 공식몰 {k}: {v[:60]}"
            if re.search(r"미국|중국|호주|칠레|베트남|태국|독일|프랑스|이탈리아|일본|덴마크|스페인|캐나다|뉴질랜드|인도네시아|말레이시아|폴란드|영국|벨기에|네덜란드|대만|멕시코",v): return "수입",f"{k}: {v[:60]}"
    return None,None
def origin_c(code):
    r=origin(code); C[code]=list(r); return r
P=os.path.join(H,"store_data.json"); S=json.load(open(P,encoding="utf-8")); n=0
for i in S["items"]:
    o=ev=None
    if re.search(r"원산지\s*:\s*국내산|\(국내산\)",i["name"]): o,ev="국산·국내생산","매장 가격표 표기: 원산지 국내산"
    elif re.search(r"(?<![가-힣])국산(?!차)",i["name"]): o,ev="국산·국내생산","매장 가격표 상품명에 '국산' 표기"
    elif i["code"]: o,ev=origin_c(i["code"])
    i["origin"]=o; i["origin_ev"]=ev; n+=o=="국산·국내생산"
json.dump(S,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
json.dump(C,open(CP,"w"),ensure_ascii=False,indent=0)
print("국산",n,"개")
