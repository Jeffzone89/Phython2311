"""일회성 테스트 스크립트 (용도는 그때그때 바뀜).

현재: 모바일 버전(m.shopping.naver.com)이 데스크톱 검색결과 페이지와
차단 수준이 다른지 확인한다.
"""
from playwright.sync_api import sync_playwright

CANDIDATES = {
    "mobile_search": "https://msearch.shopping.naver.com/search/all?query=%EC%BD%9C%EB%A0%88%EC%8A%A4%ED%83%80",
    "mobile_shopping_m": "https://m.shopping.naver.com/search/all?query=%EC%BD%9C%EB%A0%88%EC%8A%A4%ED%83%80",
}


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for name, url in CANDIDATES.items():
            print(f"=== {name} ({url}) ===")
            page = browser.new_page(
                user_agent=(
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
                ),
                locale="ko-KR",
            )
            try:
                resp = page.goto(url, timeout=15000, wait_until="networkidle")
                print(f"status: {resp.status if resp else None}")
                text = page.inner_text("body")
                print(f"본문 길이: {len(text)}자")
                print(f"'콜레스타' 포함: {'콜레스타' in text}")
                print(text[:1500])
            except Exception as exc:
                print(f"실패: {exc}")
            finally:
                page.close()
            print()
        browser.close()


if __name__ == "__main__":
    main()
