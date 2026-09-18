# 콜레스타 최저가 모니터링 봇

네이버쇼핑 "콜레스타" 검색결과에서 힐러문이 최저가 지위를 잃으면 텔레그램으로 알림을 보내는 자동화 봇입니다.
설계 배경과 전체 계획은 대화 세션에서 확정된 기획서를 참고하세요.

## 데이터 수집 방식 변경 기록

원래는 네이버 오픈API(쇼핑검색)를 쓰려 했으나, 가입 과정에서 developers.naver.com에도
NAVER API HUB(ncloud.com)에도 실제로 상품 가격을 주는 API를 찾지 못했다(전자는 "검색"
카테고리 자체가 목록에 없었고, 후자는 "쇼핑인사이트"라는 트렌드 통계만 있고 개별 상품
가격은 없었음). 커머스API센터(apicenter.commerce.naver.com)도 검토했으나 API 호출을
고정 IP 최대 3개로 제한하는 방식이라, IP가 계속 바뀌는 GitHub Actions 호스팅 러너와
근본적으로 맞지 않아 제외했다. 그래서 **검색결과 페이지(search.shopping.naver.com)를
직접 조회하는 방식**으로 전환했다 — API 키/IP 등록이 전혀 필요 없다.

## 준비물 (Stage 0)

1. **텔레그램 봇** 생성 (@BotFather, `t.me/BotFather`) → `/newbot`으로 봇 토큰 발급,
   본인과 봇의 채팅방에서 메시지를 하나 보낸 뒤 `https://api.telegram.org/bot{토큰}/getUpdates`로
   `chat_id` 확인
2. 발급받은 값을 리포지토리 **Settings → Secrets and variables → Actions**에 등록:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

## Stage 1: PoC 실행

```bash
cd price-monitor
pip install -r requirements.txt
python3 poc/poc_inspect_response.py
```

API 키가 필요 없다. 단, `naver_search_client.py`의 파싱 로직(`__NEXT_DATA__` 임베디드
JSON 가정)은 네트워크가 막힌 환경에서 작성되어 실제 페이지로 검증되지 않았다.
`SearchPageError`가 나면 아래로 원본 HTML을 저장해 직접 구조를 확인하고
`naver_search_client.py`의 `_find_item_list()`/`_normalize()`를 실제 구조에 맞게 고칠 것.

```bash
python3 poc/poc_catalog_page.py "https://search.shopping.naver.com/search/all?query=콜레스타"
```

출력에서 확인할 것:
- 힐러문 리스팅이 결과에 보이는가 (`mallName == "힐러문"`)
- `link`에 `/catalog/`가 포함된 카탈로그(그룹상품)형인가, 개별 노출형인가

카탈로그형이면 해당 URL로 구조를 추가 확인합니다.

```bash
python3 poc/poc_catalog_page.py "https://search.shopping.naver.com/catalog/12345678"
```

저장된 HTML에 판매처명·가격이 텍스트로 보이면 `catalog_fetcher.py`를 정적 파싱으로,
JS 렌더링이 필요한 SPA면 `tools/render.py`와 같은 Playwright 방식으로 구현합니다.

**PoC 결과는 이 섹션 아래에 직접 기록해두세요** (카탈로그형/개별형 여부, 힐러문 productId 등).

## Stage 2: 식별 정보 확정

PoC 결과를 바탕으로 `config.py`의 `OWNER_PRODUCT_ID`, `OWNER_STORE_SLUG`,
`PRODUCT_VARIANTS`를 실제 값으로 채웁니다.

```bash
python3 run.py --dry-run
```

콘솔에 힐러문 리스팅이 정확히 1건 식별되고 오탐이 없는지 확인합니다.

## Stage 3: 텔레그램 배선 확인

```bash
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python3 run.py --test-alert
```

## Stage 5: GitHub Actions

Secrets 등록 후 Actions 탭에서 `price-monitor` 워크플로를 `workflow_dispatch`로
수동 1회 실행해 커밋·푸시까지 끝까지 성공하는지 확인한 뒤 스케줄(30분 간격)을 신뢰합니다.

## 알림 종류

- ⚠️ 최저가 이탈 (핵심)
- ✅ 최저가 회복
- ❗ 힐러문 상품이 검색결과에서 사라짐
- 🔧 식별 애매 / 카탈로그 파싱 실패 (점검 필요)

## PoC 결과 기록

_(Stage 1 실행 후 여기에 기록)_
