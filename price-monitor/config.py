import os

KEYWORD = "콜레스타"

# 힐러문 식별 앵커. OWNER_PRODUCT_ID는 Stage 2(PoC 이후)에 실제 값으로 채울 것.
OWNER_MALL_NAME = "힐러문"
OWNER_PRODUCT_ID = None  # TODO: PoC 결과 확인 후 실제 productId로 채우기
OWNER_STORE_SLUG = None  # TODO: 스마트스토어 URL slug (예: "healermoon")

# 그룹상품으로 묶이지 않는(개별 노출) 판매처들을 같은 상품으로 취급하기 위한 수동 매칭 규칙.
# Stage 1 PoC로 실제 검색결과 제목을 보고 조정할 것.
PRODUCT_VARIANTS = [
    {
        "key": "cholesta_basic",
        "match_keywords": ["콜레스타"],
        "exclude_keywords": [],
    },
]

# NOTE: Stage 0에서 NAVER API HUB 요금제/엔드포인트 확인 후 필요시 URL 조정.
NAVER_API_URL = "https://openapi.naver.com/v1/search/shop.json"
NAVER_CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

DISPLAY = 100
SORT = "sim"

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
