#!/usr/bin/env python3
"""videos.json 의 영상 댓글을 yt-dlp로 받아 매장 품목 언급을 누적(wanted.json). 실제 댓글에 품목 키워드가 있을 때만 집계."""
import json, os, subprocess, time, datetime, re
H=os.path.dirname(os.path.abspath(__file__)); KST=datetime.timezone(datetime.timedelta(hours=9))
now=datetime.datetime.now(KST); P=os.path.join(H,"wanted.json")
W=json.load(open(P,encoding="utf-8")) if os.path.exists(P) else {"schema":"items[name]: mentions, likes, summary_comments, last_mentioned, on_sale_now, matched_code","runs":[],"items":{}}
store={i["code"]:i for i in json.load(open(os.path.join(H,"store_data.json"),encoding="utf-8"))["items"]}
def keys(n):  # 품목명에서 검색어(한글 2자 이상 단어) 뽑기
    return [w for w in re.findall(r"[가-힣]{2,}",n) if w not in ("국내산","원산지","할인","사이즈")]
for v in json.load(open(os.path.join(H,"video","videos.json"),encoding="utf-8")):
    base=os.path.join("/tmp","cm_"+v["id"]); err=None
    for a in range(3):
        r=subprocess.run(["yt-dlp","--skip-download","--write-comments","--no-warnings","-o",base,v["url"]],capture_output=True,text=True)
        if "429" in r.stderr+r.stdout: err="429"; time.sleep(30*(a+1)); continue
        err=None if r.returncode==0 else r.stderr[-300:]; break
    cm=[]; cc=None
    if os.path.exists(base+".info.json"):
        d=json.load(open(base+".info.json")); cm=d.get("comments") or []; cc=d.get("comment_count")
    W["runs"].append(dict(at=now.strftime("%Y-%m-%d %H:%M KST"),video=v["id"],comment_count=cc,fetched=len(cm),error=err))
    for c in cm:
        t=c.get("text",""); day=datetime.datetime.fromtimestamp(c.get("timestamp") or now.timestamp(),KST).strftime("%Y-%m-%d")
        for code,i in store.items():
            ks=keys(i["name"])
            if ks and sum(k in t for k in ks)>=min(2,len(ks)):
                e=W["items"].setdefault(i["name"],dict(mentions=0,likes=0,summary_comments=[],last_mentioned=None,matched_code=code,seen_ids=[]))
                if c.get("id") in e["seen_ids"]: continue
                e["seen_ids"].append(c.get("id")); e["mentions"]+=1; e["likes"]+=c.get("like_count") or 0
                e["last_mentioned"]=max(filter(None,[e["last_mentioned"],day])); e["summary_comments"]=(e["summary_comments"]+[t[:80]])[:3]
for n,e in W["items"].items(): e["on_sale_now"]=e.get("matched_code") in store
json.dump(W,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("댓글",W["runs"][-1],"인기품목",len(W["items"]))
