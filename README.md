# 코스트코 할인 사이트

- `python3 fetch.py` : 온라인(costco.co.kr 공개 검색 API) 수집 → data.json, 이어서 video_store.py 실행 → store_data.json, 그리고 index.html 생성(데이터 인라인, 파일 하나로 열림).
- 댓글: comments.py 가 videos.json 영상 댓글을 받아 wanted.json 에 누적(실행마다 runs 기록).
- 매장 탭은 **매장 가격표를 직접 촬영한 영상**에서 읽은 값만 사용합니다. 현재: CoReview qqv3wouHsTk (공세점, 10/19 업로드). 종료일이 지난 품목은 자동 제외.

## 새 영상 넣기 (최신 영상 하나만 유지)
1. 영상 받기: `yt-dlp -f "bv*[height<=720]+ba/b" -o /workspace/costco/video.mp4 <URL>`
2. 가격표 부분만 2초 간격으로 잘라 시트 만들기: `python3 video/make_sheets.py /workspace/costco/video.mp4`
   (가격표 위치가 다르면 make_sheets.py 의 CROP 값을 수정) → /workspace/costco/sheets/s_XX.jpg (각 칸 왼쪽 아래 노란 표시 = 영상 시각)
3. 시트를 보고 `video/<영상ID>.tsv` 작성. 열: code, name, regular, discount, sale, start(YYYY-MM-DD), end, t(분:초), flag
   - 숫자는 가격표에 보이는 값만. 흐리거나 가려진 값은 비우고 flag 에 이유를 적으면 '미확인'으로 표시됨.
4. `video/videos.json` 을 새 영상 하나로 교체(id, tsv, source 문구, url). 예전 tsv는 지워도 됨.
5. `python3 fetch.py` 실행 후 index.html 확인.

## 방문자 직접 확인 제보 (video/manual.tsv)
영상에 없는 품목을 매장 가격표를 직접 본 제보로 추가할 때 사용합니다. 탭 구분 열:
`code name regular discount sale start end seen source flag`
- 모르는 값은 비워 두고 `flag`에 미확인 내용을 적습니다(→ '미확인' 표시). 상품번호가 없으면 사진은 붙지 않습니다.
- '영상에서 보기' 버튼은 없고, 기간이 없으면 '기간 미확인'으로 표시됩니다.
- `end`가 지나면, `end`가 없으면 `seen`(확인일)+14일이 지나면 주간 재빌드에서 자동 제외됩니다.

## 전단지 포스터 (poster2.py)
- `fetch.py` 가 store_data.json/이미지 갱신 뒤 `poster2.py` 를 실행해 먹거리·생필품 4개 카테고리(정육·수산·신선, 가공·간편식, 생활·세제, 음료·커피)에서 할인액 큰 순 일부 품목으로 전단지를 다시 만듭니다.
- 사진은 store_data.json 의 공식 사진만 `poster_img/` 에 미리 받아 base64로 넣습니다(영상 캡처 사용 안 함, '참고 사진' 표시 유지).
- 결과: `poster.png`(원본, 저장소에 안 올림), `poster.webp`(웹용, 사이트 맨 위 미리보기·저장 링크), `poster_meta.json`(가로·세로). index.html 에서는 `poster.webp?v=빌드시각` 으로 캐시를 갱신합니다.
- 단독 실행: `python3 poster2.py` (headless Chrome 필요).
