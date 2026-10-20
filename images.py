#!/usr/bin/env python3
"""매장 품목 이미지: 1) costco.co.kr 공개 검색 API에서 상품번호가 정확히 같은 상품의 공식 이미지 URL
2) 없으면 영상 해당 시각 프레임의 상품 부분(가격표 제외 왼쪽 영역)을 잘라 img/<code>.jpg (폭 300) → base64 인라인. 결과 img_map.json"""
import json, os, subprocess, urllib.request, urllib.parse, base64, time
H=os.path.dirname(os.path.abspath(__file__)); B="https://www.costco.co.kr"
VID={"qqv3wouHsTk":"/workspace/costco/video.mp4"}
M=json.load(open(os.path.join(H,"img_map.json"))) if os.path.exists(os.path.join(H,"img_map.json")) else {}
os.makedirs(os.path.join(H,"img"),exist_ok=True)
def official(code):
    u=B+"/rest/v2/korea/products/search?"+urllib.parse.urlencode({"query":code,"pageSize":10,"lang":"ko","curr":"KRW","fields":"FULL"})
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30))
    for p in d.get("products",[]):
        if p.get("code")==code:
            im=next((i["url"] for i in p.get("images",[]) if i.get("format")=="product"),None) or next((i["url"] for i in p.get("images",[])),None)
            if im: return (B+im if im.startswith("/") else im), B+p["url"]
    return None,None
# 공식 사진 없는 품목 → 코스트코 공식몰의 같은 상품(묶음·용량만 다름) 사진. 사람이 확인한 매핑, 모두 '참고 사진'
ALT={"685123":"687535","504159":"677499","664038":"688860","605698":"602500","691378":"680309","693154":"695898","688971":"688972",
"656361":"677493","663486":"666930","530790":"679686","672971":"681424","665976":"675893","659722":"660491","614105":"714105",
"664919":"663968","610017":"508166","610652":"508176","668937":"674729","742482":"742146","649324":"649349"}
# 브랜드(상품 권리자) 공식몰 사진. (이미지URL, 상품페이지, 참고여부, 메모) — 사람이 확인
BRAND={"580714":("https://www.lottefoodmall.com/data/goods/thumb/thumb_G61B6BE07EEDC1.jpg","https://www.lottefoodmall.com/?GS=3360&act=shop.goods_view",True,"롯데웰푸드몰 의성마늘햄 440g"),
"671490":("https://direct.maeil.com/UploadedFiles/direct/product/eb725a30-6e0a-410a-aa2c-f0225c7398f3.jpg","https://direct.maeil.com/product/productView.do?productCode=P18181",True,"매일유업 공식몰 엔요 300 280ml x 24"),
"607585":("https://www.otokimall.com/data/product/origin/20221125/28310002_1.jpg","https://www.otokimall.com/front/product/1068",True,"오뚜기몰 유기농콩으로만든 생낫또 150g"),
"587687":("http://img.dongwonmall.com/dwmall/static_root/model_img/main/724/72473_1_a.jpg","https://m.dongwonmall.com/product/detail.do?productId=003774922",True,"동원몰 소와나무 생크림 요거트 85g x 8")}
st=json.load(open(os.path.join(H,"store_data.json"),encoding="utf-8"))
for i in st["items"]:
    c=i["code"]
    if c in M and M[c]["kind"]=="official": continue
    try: url,purl=official(c)
    except Exception as e: url=purl=None
    time.sleep(0.3)
    if url: M[c]=dict(kind="official",src=url,product_url=purl,source="코스트코 공식",ref=False); continue
    if c in BRAND:
        u,p,ref,memo=BRAND[c]; M[c]=dict(kind="official",src=u,product_url=p,source="브랜드 공식",ref=ref,note=memo); continue
    if c in ALT:
        try: url,purl=official(ALT[c])
        except Exception: url=None
        if url: M[c]=dict(kind="official",src=url,product_url=purl,source="코스트코 공식",ref=True,alt_code=ALT[c]); continue
    M[c]=dict(kind="none"); continue  # 영상 캡처 비활성화
    vid=i["url"].split("v=")[1].split("&")[0]; t=int(i["url"].split("t=")[1].rstrip("s"))
    out=os.path.join(H,"img",c+".jpg")
    # 1280x720 기준 가격표(오른쪽 위)를 피해 왼쪽~가운데 상품 영역
    r=subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",VID.get(vid,""),"-frames:v","1","-vf","scale=1280:720,crop=720:560:20:100,scale=300:-1","-q:v","6",out])
    M[c]=dict(kind="video",src=out) if r.returncode==0 and os.path.exists(out) else dict(kind="none")
json.dump(M,open(os.path.join(H,"img_map.json"),"w"),ensure_ascii=False,indent=1)
for i in st["items"]:
    m=M.get(i["code"],{"kind":"none"})
    if m["kind"]=="official": i["image"]=m["src"]; i["image_src"]=m.get("source","코스트코 공식")+(" · 참고 사진" if m.get("ref") else ""); i["image_url_src"]=m["product_url"]
    elif False and m["kind"]=="video": i["image"]="data:image/jpeg;base64,"+base64.b64encode(open(m["src"],"rb").read()).decode(); i["image_src"]="영상 캡처"
    else: i["image"]=None; i["image_src"]=None
json.dump(st,open(os.path.join(H,"store_data.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
from collections import Counter; print("이미지",Counter(M.get(i["code"],{"kind":"none"})["kind"] for i in st["items"]))
