class ParserDriftError(Exception):
    """카탈로그 페이지 구조가 예상과 달라 판매처 목록을 파싱할 수 없을 때"""


def fetch_sellers(catalog_id):
    """카탈로그 상품의 판매처별 [{mallName, price, productId, link}, ...] 목록을 반환한다.

    Stage 1 PoC(poc/poc_catalog_page.py)로 실제 카탈로그 페이지 구조(정적 HTML에
    임베디드 JSON이 있는지, SPA라 JS 렌더링이 필요한지)를 확인하기 전까지는 미구현이다.
    확인 후 정적 requests 파싱 또는 tools/render.py와 동일한 Playwright 패턴으로 구현할 것.
    """
    raise NotImplementedError(
        "catalog_fetcher.fetch_sellers()는 Stage 1 PoC 결과 확인 후 구현이 필요합니다. "
        "poc/poc_catalog_page.py로 카탈로그 페이지 구조를 먼저 확인하세요. "
        f"(catalog_id={catalog_id})"
    )
