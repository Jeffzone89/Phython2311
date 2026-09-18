"""일회성 테스트: sellerradar.co.kr이 실제로 폐쇄됐는지 확인."""
from playwright.sync_api import sync_playwright

URL = "https://sellerradar.co.kr/"


def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(locale="ko-KR")
        try:
            resp = page.goto(URL, timeout=15000, wait_until="networkidle")
            print(f"status: {resp.status if resp else None}")
            text = page.inner_text("body")
            print(f"본문 길이: {len(text)}자\n")
            print(text[:2000])
        except Exception as exc:
            print(f"실패: {exc}")
        browser.close()


if __name__ == "__main__":
    main()
