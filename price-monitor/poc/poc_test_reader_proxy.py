"""일회성 테스트 스크립트 (용도는 그때그때 바뀜).

현재: apicenter.commerce.naver.com의 API 문서 페이지를 Playwright로 렌더링해
"카탈로그 조회" 등 커머스API가 판매처별 가격 정보를 주는지 확인한다.
Docusaurus 기반 OpenAPI 문서라 실제 파라미터/응답 스키마 표가 JS로 그려져서
plain requests로는 안 보였다 (내용이 거의 비어있고 한글도 깨졌음).
"""
from playwright.sync_api import sync_playwright

DOCS_URL = "https://apicenter.commerce.naver.com/docs/commerce-api/current/get-model-list-product"


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(locale="ko-KR")
        resp = page.goto(DOCS_URL, timeout=20000, wait_until="networkidle")
        print(f"status: {resp.status if resp else None}")
        text = page.inner_text("body")
        print(f"본문 텍스트 길이: {len(text)}자\n")
        print(text)
        browser.close()


if __name__ == "__main__":
    main()
