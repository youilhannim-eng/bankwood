# 은행나무요양원 인사이트 작성 규칙 (매일 1편 자동 게시용)

## 파일과 명령
- 글은 `content/insight/<YYYY-MM-DD>-<영문-slug>.json` 한 파일. 오늘 날짜는 `TZ=Asia/Seoul date +%F`.
- 쓴 뒤 `python3 tools/build.py` 실행 → 검증 통과 시 `insight/`, `guide/`, `sitemap.xml`, `rss.xml`, `llms.txt`, `llms-full.txt`, 홈의 최신 글 블록이 갱신된다. 실패하면 메시지대로 고쳐 다시 실행. 끝내 통과하지 못하면 커밋·푸시하지 말고 이유만 보고한다.
- 위 빌드 산출물과 새 JSON 외의 파일은 고치지 않는다.

## JSON 형식 (기존 파일 참고)
slug(영문 소문자·숫자·하이픈), guide(이 글을 붙일 안내 페이지 slug: choose cost grade admission vs-hospital dementia silvertown home-care ltc-insurance grade-compare near-seoul namyangju-areas namyangju cognitive-support-grade care-worker open-nursing-home 중 하나), title, description(60~160자), date, category, keywords[], summary[3줄], body(HTML), faq[{q,a}] 3~5개, sources[{title,url}].
- body 허용 태그: h2 h3 p ul ol li strong em a br table thead tbody tr th td blockquote. 본문 공백 제외 1,500자 이상(권장 2,000자). h1·스크립트 금지. 사진은 <figure class="post-photo"><img src="/assets/img/실제파일" alt="…" width height loading="lazy"><figcaption>…</figcaption></figure> 형식으로 실제 사진만(AI 사진 금지).
- 소제목(h2)은 질문형·상황형. '정리'·번호 나열형 남발 금지. 글 끝 상담 문구는 템플릿이 붙이므로 쓰지 않는다.
- 표는 모바일에서 넘치지 않게 3열 이하·짧은 문구.
- 내부 링크는 /guide/cost/, /guide/grade/, /guide/choose/, /guide/admission/, /guide/vs-hospital/, /guide/namyangju/, /#calculator, 이전 인사이트(/insight/<slug>/)를 자연스럽게 1~3개.

## 키워드 대기열 (2026-11-22부터, 가장 먼저 적용)
- 글을 쓰기 전에 `python3 tools/insight_queue.py` 를 실행하고 tools/INSIGHT_QUEUE.md '대기' 맨 위 키워드로 쓴다. 하루 최대 2편.
- JSON 에 "keyword": "<대기열의 키워드 그대로>" 와 "guide": "<표의 안내 페이지>" 를 넣고, 제목에 그 키워드를 띄어쓰기만 자연스럽게 바꿔 넣는다.
- 그 키워드로 검색한 보호자가 궁금해할 질문 하나를 깊게 다룬다. 안내 페이지 본문을 되풀이하지 않는다. 공식 출처로 확인되지 않으면 그 키워드는 건너뛰고 다음 키워드로 간다.
- 남양주 동네 이름 키워드(진접·별내·다산 등)는 그 동네에만 해당하는 사실(가까운 역·도로·보건소 치매안심센터 등 확인된 것)이 있을 때만 쓰고, 없으면 건너뛴다. 같은 글에 지역명만 바꿔 쓰지 않는다.
- '보류' 목록(다른 지역, 과장 표현, 금액·규정 확정 전)은 쓰지 않는다.

## 안내 페이지별 순환
- 글이 가장 적은 안내 페이지(guide)부터 채운다. 같은 페이지에 이틀 연속 쓰지 않는다. 글은 해당 안내 페이지 아래 '이 주제의 인사이트'에 자동으로 붙는다.

## 장르(category) — 돌아가며, 글이 적은 장르 우선
1. 요양원 선택 2. 비용·제도 3. 등급·입소 절차 4. 치매·돌봄 5. 지역·생활(남양주·화도·은행나무 이야기) 6. 요양원 개원·운영(예비 사업자용)

## 사실 규칙 (가장 중요)
- 법·제도·수가·금액·절차는 정부·공공기관(보건복지부, 국민건강보험공단, 노인장기요양보험 longtermcare.or.kr, 법제처, 지자체) 공식 페이지를 직접 열어 확인한 것만 쓴다. 확인 못 한 수치는 쓰지 않는다. 제도 글은 sources에 https 공식 링크와 본문에 "○○년 ○월 기준"을 넣는다.
- 은행나무요양원의 확정되지 않은 사항은 쓰지 않는다: 생활실 구성(1·2인실), 층별 안내, 인력 배치, 비급여 금액, 면회 규정, 개원일 확정, 직원 수, 후기·수상·평가등급. "개원 전 확정해 공개"라고만 쓴다.
- 확정된 사실: 경기도 남양주시 화도읍 가곡로 97-22(가곡리 256-9), 정원 49명, 2027년 1월 준공 예정, 사전 입소상담 접수 중, 원장 박민경 010-2109-7717, 개원·건축·가맹 010-2225-6775, 가곡리 약 600년 은행나무(남양주시 보호수 제21호).
- 지어낸 사례·후기·통계·인용 금지. 의료 조언·진단 금지(일반 정보로 쓰고 전문가 상담 권유). 타 시설 비방, 과장·보장 표현("최고", "100%") 금지.
- 이미 쓴 글(content/insight/*.json)의 제목·주제·FAQ 질문·첫 문단·마지막 문단과 겹치지 않게 한다. 최근 3편과 같은 시작·마무리 방식 금지.

## 문체
존댓말, 보호자(자녀)에게 말하듯 차분하고 구체적으로. 어르신을 '환자'가 아니라 '어르신'으로. 쉬운 말, 한 문단 3~4문장.

## 게시
git add -A → commit(메시지: "insight: <제목>") → `git push origin HEAD:main`. Cloudflare Pages가 자동 배포한다.
