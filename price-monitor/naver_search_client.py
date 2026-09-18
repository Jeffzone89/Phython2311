"""네이버쇼핑 검색결과 페이지를 직접 조회해 상품 목록을 만든다.

공식 오픈API(shop.json)가 막혀 있어(price-monitor/README.md의 Stage 0 기록 참고)
검색결과 페이지(search.shopping.naver.com/search/all)를 직접 파싱하는 방식으로 전환했다.

순수 requests로는 헤더를 브라우저와 동일하게 맞춰도 HTTP 418(차단)이 떨어졌다
(2026-09-18, GitHub Actions 실제 실행에서 확인). requests/urllib3의 TLS 핸드셰이크
지문이 실제 브라우저와 달라 차단되는 것으로 보여, tools/render.py와 같은 Playwright
(실제 Chromium 엔진)로 전환했다.

이 파일은 네트워크가 막힌 개발 환경에서 작성돼 __NEXT_DATA__ 파싱 로직 자체는
실제 페이지 구조로 검증하지 못했다. SearchPageError가 나면 poc_inspect_response.py가
저장하는 raw_page_dump.html을 GitHub Actions 아티팩트로 내려받아 실제 구조를 확인하고
_find_item_list()/_normalize()를 고칠 것.
"""
import json
import os
import re

from playwright.sync_api import sync_playwright

from config import KEYWORD

SEARCH_URL = "https://search.shopping.naver.com/search/all"

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

_NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__" type="application/json"[^>]*>(.*?)</script>', re.DOTALL
)

# 공식 문서(developers.naver.com > 검색 > 쇼핑) productType 표 기준.
# 상품종류 = ((productType - 1) % 3) + 1  (1=가격비교 상품, 2=비매칭, 3=매칭)
# 스크래핑한 데이터엔 이 필드가 없을 수 있어 None을 허용한다.

# poc_inspect_response.py가 파싱 실패 시 원본 HTML을 저장해두는 경로.
RAW_DUMP_PATH = os.path.join(os.path.dirname(__file__), "poc", "raw_page_dump.html")


class SearchPageError(Exception):
    pass


def fetch_html(query=KEYWORD, timeout_ms=20000):
    """Playwright(실제 Chromium)로 검색결과 페이지를 렌더링해 최종 HTML을 반환한다."""
    url = f"{SEARCH_URL}?query={query}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            page = browser.new_page(user_agent=_USER_AGENT, locale="ko-KR")
            resp = page.goto(url, timeout=timeout_ms, wait_until="networkidle")
            if resp is None or resp.status != 200:
                status = resp.status if resp else None
                raise SearchPageError(f"검색결과 페이지 요청 실패: status={status}")
            return page.content()
        finally:
            browser.close()


def search_shopping(query=KEYWORD):
    html = fetch_html(query=query)
    return parse_html(html)


def parse_html(html):
    match = _NEXT_DATA_RE.search(html)
    if not match:
        raise SearchPageError(
            "__NEXT_DATA__ 임베디드 JSON을 찾지 못함 - 페이지가 이 가정과 다른 구조일 수 있음. "
            "poc/poc_catalog_page.py를 검색결과 URL로 실행해 실제 HTML을 저장한 뒤 "
            "직접 구조를 확인하고 이 파일의 파싱 로직을 다시 구현할 것."
        )

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise SearchPageError(f"__NEXT_DATA__ JSON 파싱 실패: {exc}") from exc

    items = _find_item_list(data)
    if items is None:
        raise SearchPageError(
            "__NEXT_DATA__ 안에서 상품 목록으로 보이는 배열을 찾지 못함. "
            "page.json으로 저장해 직접 구조를 확인 후 _find_item_list()의 휴리스틱을 조정할 것. "
            f"최상위 키: {list(data.keys()) if isinstance(data, dict) else type(data)}"
        )
    return [_normalize(item) for item in items]


# 각 그룹에서 하나라도 키가 있으면 "히트"로 치는 휴리스틱.
# 실제 키 이름은 Stage 1 PoC 전까지 미확정이라 흔한 후보를 나열해둔다.
_PRODUCT_KEY_HINTS = (
    ("price", "lprice", "salePrice", "minPrice", "productPrice"),
    ("mallName", "mall", "sellerName", "storeName", "mallInfo"),
    ("productId", "id", "nvMid", "itemId"),
    ("link", "url", "productUrl", "linkUrl"),
)


def _looks_like_product(d):
    if not isinstance(d, dict):
        return False
    return sum(any(k in d for k in group) for group in _PRODUCT_KEY_HINTS) >= 2


def _find_item_list(node, _seen=None):
    """JSON 트리에서 상품 리스트로 보이는 배열을 재귀적으로 찾는다.

    실제 키 경로를 모르기 때문에, 원소들이 상품처럼 보이는 필드 조합을
    가졌는지로 판별한다 (정확한 경로 하드코딩 대신 쓰는 임시 방편).
    """
    if _seen is None:
        _seen = set()
    node_id = id(node)
    if node_id in _seen:
        return None
    _seen.add(node_id)

    if isinstance(node, list) and node:
        sample = node[:5]
        if sample and sum(_looks_like_product(x) for x in sample) >= min(3, len(sample)):
            return node
        for value in node:
            found = _find_item_list(value, _seen)
            if found:
                return found
    elif isinstance(node, dict):
        for value in node.values():
            found = _find_item_list(value, _seen)
            if found:
                return found
    return None


def _normalize(item):
    mall = item.get("mallName")
    if mall is None and isinstance(item.get("mall"), dict):
        mall = item["mall"].get("name")
    if mall is None:
        mall = item.get("sellerName") or item.get("storeName")

    raw_id = item.get("productId") or item.get("id") or item.get("nvMid") or item.get("itemId")
    return {
        "productId": str(raw_id) if raw_id is not None else None,
        "productType": item.get("productType"),
        "mallName": mall,
        "lprice": _to_int(item.get("lprice") or item.get("price") or item.get("salePrice") or item.get("minPrice")),
        "link": item.get("link") or item.get("url") or item.get("productUrl") or item.get("linkUrl"),
        "title": item.get("title") or item.get("productTitle") or "",
    }


def _to_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def product_kind(product_type):
    if product_type is None:
        return None
    try:
        return ((int(product_type) - 1) % 3) + 1
    except (TypeError, ValueError):
        return None
