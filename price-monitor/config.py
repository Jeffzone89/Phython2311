import os

KEYWORD = "콜레스타"

# 힐러문 식별 앵커.
# https://smartstore.naver.com/healermoon/products/13739948467 에서 확보.
OWNER_MALL_NAME = "힐러문"
OWNER_STORE_SLUG = "healermoon"
# 스마트스토어 자체 상품번호. 네이버쇼핑 검색결과의 productId(nvMid)와 값 체계가
# 다를 수 있어(그룹상품이면 특히), 어느 쪽이든 매칭에 쓰도록 matcher.py에서
# productId 완전일치 또는 link에 OWNER_STORE_SLUG 포함 여부로 이중 확인한다.
# 실제 스크래핑 결과로 productId가 다르게 나오면 이 값은 무시되고 슬러그 매칭만 쓰인다.
OWNER_PRODUCT_ID = "13739948467"

# 그룹상품으로 묶이지 않는(개별 노출) 판매처들을 같은 상품으로 취급하기 위한 수동 매칭 규칙.
# Stage 1 PoC로 실제 검색결과 제목을 보고 조정할 것.
PRODUCT_VARIANTS = [
    {
        "key": "cholesta_basic",
        "match_keywords": ["콜레스타"],
        "exclude_keywords": [],
    },
]

# 가격 조정 가이드용 원가 정보. 최저가 이탈 알림에 "최소 판매 가능가"를 같이 보여준다.
OWNER_PRODUCT_COST = 27000  # 상품 원가
OWNER_SHIPPING_COST = 2500  # 배송비(무료배송 정책이라 판매가에서 부담)
MIN_MARGIN_WON = 100  # 최소 마진
MIN_VIABLE_PRICE = OWNER_PRODUCT_COST + OWNER_SHIPPING_COST + MIN_MARGIN_WON

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

STATE_FILE = os.path.join(os.path.dirname(__file__), "state.json")
