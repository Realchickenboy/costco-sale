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
