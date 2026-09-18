# 콜레스타 최저가 모니터링 봇

네이버쇼핑 "콜레스타" 검색결과에서 힐러문이 최저가 지위를 잃으면 텔레그램으로 알림을 보내는 자동화 봇입니다.
설계 배경과 전체 계획은 대화 세션에서 확정된 기획서를 참고하세요.

## 준비물 (Stage 0)

1. **developers.naver.com** (ncloud.com "NAVER API HUB"가 아님 — 거긴 쇼핑 상품검색을 제공하지 않음)에서
   Application 등록 → 사용 API에서 "검색" 선택 → 쇼핑 검색 Client ID/Secret 발급
   - 공식 문서: 검색 API > 쇼핑 검색 개요 (`openapi.naver.com/v1/search/shop.json`)
   - 무료 한도 하루 25,000회 (이 프로그램은 하루 50~150회 수준만 사용, 여유 충분)
2. **텔레그램 봇** 생성 (@BotFather) → 봇 토큰 발급, 본인과의 채팅으로 `chat_id` 확인
3. 발급받은 4개 값을 리포지토리 **Settings → Secrets and variables → Actions**에 등록:
   - `NAVER_CLIENT_ID`
   - `NAVER_CLIENT_SECRET`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

## Stage 1: PoC 실행

```bash
cd price-monitor
pip install -r requirements.txt
export NAVER_CLIENT_ID=...
export NAVER_CLIENT_SECRET=...
python3 poc/poc_inspect_response.py
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
