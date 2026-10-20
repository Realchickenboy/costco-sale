#!/usr/bin/env python3
"""costco.co.kr 공개 검색 API(SAP Commerce OCC)로 SpecialPriceOffers 할인 품목 수집 → data.json + index.html"""
import subprocess, sys, json, urllib.request, urllib.parse, datetime, os, time
BASE="https://www.costco.co.kr"
API=BASE+"/rest/v2/korea/products/search"
CAT={"Appliances":"가전","Foods":"식품","FurnitureBeddingHome":"가구·침구·홈","HomeKitchen":"주방","ClothingBagsAccessories":"의류·잡화","BeautyHouseholdPersonal-Care":"뷰티·생활용품","BabyKidsToysPets":"유아·완구·반려동물","HealthSupplement":"건강·영양제","HardwareAutomotive":"공구·자동차","PatioLawnGarden":"아웃도어·정원","Gift-Set-Special":"선물세트","ElectronicsComputers":"전자·컴퓨터","SportsFitnessCamping":"스포츠·캠핑","StationeryOffice-Supplies":"문구·사무","JewelryWatchesAccessories":"주얼리·시계","GrillsAccessories":"그릴"}
KST=datetime.timezone(datetime.timedelta(hours=9))
def kst(s):
    if not s: return None
    return datetime.datetime.fromisoformat(s.replace("Z","+00:00")).astimezone(KST).strftime("%Y-%m-%d %H:%M")
def get(page):
    q=urllib.parse.urlencode({"query":":relevance:allCategories:SpecialPriceOffers","pageSize":100,"currentPage":page,"lang":"ko","curr":"KRW","fields":"FULL"})
    r=urllib.request.Request(API+"?"+q,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"})
    return json.load(urllib.request.urlopen(r,timeout=30))
items={};page=0
while True:
    d=get(page)
    for p in d.get("products",[]):
        price=(p.get("price") or {}).get("value"); base=(p.get("basePrice") or {}).get("value")
        disc=(p.get("discountPrice") or (p.get("couponDiscount") or {})) ; disc=disc.get("value", disc.get("discountValue"))
        if not price: continue
        if not base and disc: base=price+disc
        if base and not disc: disc=base-price
        seg=(p.get("url") or "/").strip("/").split("/")[0]
        img=next((i["url"] for i in p.get("images",[]) if i.get("format")=="product"),None) or next((i["url"] for i in p.get("images",[])),None)
        items[p["code"]]=dict(code=p["code"],name=p.get("name"),category=CAT.get(seg,"기타"),regular_price=base,discount=disc,sale_price=price,
            discount_rate=round(disc/base*100,1) if base and disc else None,
            start=kst(p.get("discountStartDate") or (p.get("couponDiscount") or {}).get("discountStartDate")),
            end=kst(p.get("discountEndDate") or (p.get("couponDiscount") or {}).get("discountEndDate")),
            url=BASE+p["url"] if p.get("url") else None, image=BASE+img if img and img.startswith("/") else img,
            stock=(p.get("stock") or {}).get("stockLevelStatus"))
    page+=1
    if page>=d["pagination"]["totalPages"]: break
    time.sleep(0.5)
out=dict(updated=datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M KST"),source=API,count=len(items),items=list(items.values()))
here=os.path.dirname(os.path.abspath(__file__))
json.dump(out,open(os.path.join(here,"data.json"),"w"),ensure_ascii=False,indent=1)
subprocess.run([sys.executable,os.path.join(here,"video_store.py")],check=True)
subprocess.run([sys.executable,os.path.join(here,"images.py")],check=True)
subprocess.run([sys.executable,os.path.join(here,"comments.py")])
if os.path.exists("/workspace/yt/popular_raw.json"): subprocess.run([sys.executable,os.path.join(here,"popular_build.py")])
wanted=json.load(open(os.path.join(here,"wanted.json"),encoding="utf-8"))
store=json.load(open(os.path.join(here,"store_data.json"),encoding="utf-8"))
tpl=open(os.path.join(here,"template.html"),encoding="utf-8").read()
open(os.path.join(here,"index.html"),"w",encoding="utf-8").write(tpl.replace("/*DATA*/null",json.dumps(out,ensure_ascii=False).replace("</","<\\/")).replace("/*STORE*/null",json.dumps(store,ensure_ascii=False).replace("</","<\\/")))
print("수집",len(items),"개")
